#
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
import atexit
import itertools
import os
import platform
from queue import Queue, Empty
import subprocess
import threading
import time
from typing import Callable, List, Tuple, Optional

import grpc
from grpc_status.rpc_status import from_call

import ansys.api.systemcoupling.v0.sycapi_pb2 as sycapi_pb2
import ansys.api.systemcoupling.v0.sycapi_pb2_grpc as sycapi_pb2_grpc
from ansys.systemcoupling.core.client.variant import from_variant, to_variant

_isWindows = any(platform.win32_ver())

_INSTALL_ROOT = "AWP_ROOT222"
_SC_ROOT_ENV = "SYSC_ROOT"

_SCRIPT_EXT = '.bat' if _isWindows else ''
_SCRIPT_NAME = 'systemcoupling' + _SCRIPT_EXT

_CHANNEL_READY_TIMEOUT_SEC = 10

def _path_to_system_coupling():
    scroot = os.environ.get(_SC_ROOT_ENV, None)

    if not scroot:
        scroot = os.environ.get(_INSTALL_ROOT, None)
        if scroot:
            scroot = os.path.join(scroot, 'SystemCoupling')

    if scroot is None:
        raise RuntimeError("Failed to locate SystemCoupling from environment.")

    script_path = os.path.join(scroot, 'bin', _SCRIPT_NAME)

    if not os.path.isfile(script_path):
        raise RuntimeError(f"System coupling script does not exist at {script_path}")

    return script_path

def _start_system_coupling(host, port, working_dir, redirect_std=False):
    from copy import deepcopy
    env = deepcopy(os.environ)
    env['PYTHONUNBUFFERED'] = '1'
    if redirect_std:
        env['PYTHONIOENCODING'] = 'utf-8'
    args = [_path_to_system_coupling(), '-m', 'cosimtest', f'--grpcport={host}:{port}']
    print("Starting System Coupling: ", args[0])
    return subprocess.Popen(args,
                            env=env,
                            cwd=working_dir,
                            stdout=subprocess.PIPE if redirect_std else None,
                            # for now, merge stderr with stdout if redirectng
                            stderr=subprocess.STDOUT if redirect_std else None)

class _CleanupThread(threading.Thread):
    """ Ensures registered cleanup callbacks are called on
    exit.

    This approach is taken because atexit() cannot be relied
    upon if the main thread is lost.
    """
    def __init__(self):
        super().__init__(daemon=False)
        self.callbacks: List[Callable]=[]

    def run(self):
        t = threading.main_thread()
        t.join()
        print("len(callbacks)=", len(self.callbacks))
        for callback in self.callbacks:
            callback()

class CleanupManager:
    """ Ensures registered cleanup callbacks are called on exit.

    """
    def __init__(self):
        self.__callbacks: List[Tuple[int, Callable]]=[]
        atexit.register(self._cleanup)

    def add_callback(self, id, cb):
        self.__callbacks.append((id, cb))

    def remove_callback(self, id):
        idx = None
        for i, elem in enumerate(self.__callbacks):
            if elem[0] == id:
                idx = i
                break
        if idx is not None:
            # This will be called during cleanup while
            # iterating over the cb list, so we null the
            # entry rather than resizing it
            self.__callbacks[idx] = (None, None)

    def _cleanup(self):
        for _, cb in self.__callbacks:
            if cb is not None:
                cb()

class CommandQueryService:
    def __init__(self, channel):
        self.__stub = sycapi_pb2_grpc.SycApiStub(channel)

    def execute_command(self, request):
        try:
            response, call = self.__stub.InvokeCommand.with_call(request)
            return response, call.trailing_metadata()
        except grpc.RpcError as rpc_error:
            status = from_call(rpc_error)
            msg = f"Command execution failed: {status.message} (code={status.code})"
            for detail in status.details:
                if detail.Is(sycapi_pb2.ErrorDetails.DESCRIPTOR):
                    info = sycapi_pb2.ErrorDetails()
                    detail.Unpack(info)
                    msg += (f"\n\nServer exception details:\n"
                            f"{info.exception_classname}\n{info.stack_trace}")
            raise RuntimeError(msg) from None

    def ping(self):
        request = sycapi_pb2.PingRequest()
        response = self.__stub.Ping(request)
        return True

    def quit(self):
        request = sycapi_pb2.QuitRequest()
        response = self.__stub.Quit(request)
        return True


class SycGrpc(object):
    """Provides a remote proxy API to System Coupling's Command/Query
    external interface, built of a basic gRPC interface.

    An instance of this class controls starting System Coupling as
    a server in cosimulation mode and handles the underlying RPC to
    provide the Command/Query API. The 'start_and_connect' method
    should be used to start the remote SystemCoupling, and 'exit'
    to close the connection and shut down SystemCoupling. Alternatively,
    'connect' can be used to connect to an already running server
    instance.

    Other than the external interface API being accessed as member
    methods of this class, the calls should be of the same form as
    if invoked locally.

    Thus:

    ``s = GetState(ObjectPath='/SystemCoupling/Library')``

    becomes

    ``s = sycRpc.GetState(ObjectPath='/SystemCoupling/Library')``

    .. note::
       System Coupling runs in a server mode that expects a single
       client to connect after start up and which becomes the only
       means of controlling the server during its lifetime.

    TODO:

    - Stdout and stderr capture - accessible but nothing done with them
    at the moment. What do we want to do?
    - All calls synchronous at the moment. We might want to do something
    different with Solve(), for example.
    """

    #_cleanupThread = None
    _cleanupMgr = Optional[CleanupManager]
    _id_iter = itertools.count()

    def __init__(self):
        self._reset()
        self.__id= next(SycGrpc._id_iter)
        #if not SycGrpc._cleanupThread:
        #    SycGrpc._cleanupThread = _CleanupThread()
        #    SycGrpc._cleanupThread.start()
        if not SycGrpc._cleanupMgr:
            SycGrpc._cleanupMgr = CleanupManager()

    def _reset(self):
        self.__process = None
        self.__channel = None

    def start_and_connect(self, host, port, working_dir):
        """Start system coupling in server mode and establish a connection.

        The standard streams are redirected via a single pipe in current impl.
        The output is gathered asynchronously but is currently only accessible
        via take_stdout().
        """
        self.__process = _start_system_coupling(host, port, working_dir, redirect_std=True)
        # Since we started this process try to ensure it is shut down
        SycGrpc._cleanupMgr.add_callback(self.__id, self.exit)
        self.__stdout_reader = _StreamReader(self.__process.stdout)
        self._connect(host, port)

    def connect(self, host, port):
        """Connect to an already running system coupling server running on a known
        host and port.

        No standard stream output is available when connecting in this manner.
        """
        self.__stdout_reader = _NullStreamReader()
        self._connect(host, port)

    def _connect(self, host, port):
        self.__channel = grpc.insecure_channel(f'{host}:{port}')

        # Wait for server to be ready
        timeout = _CHANNEL_READY_TIMEOUT_SEC
        try:
            grpc.channel_ready_future(self.__channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            raise RuntimeError("Aborting attempt to connect to gRPC channel "
                               f"after {timeout} seconds.")

        self.__command_stub = CommandQueryService(self.__channel)

    def exit(self):
        """Shut down the remote System Coupling server.

        Reset this object ready to start and connect to a new
        server if wished.
        """

        SycGrpc._cleanupMgr.remove_callback(self.__id)

        if self.__channel is not None:
            self.__command_stub.quit()
            self.__channel.close()
            self.__channel = None
        if self.__process and self.__process.poll() is None:
            try:
                print("wait for process to exit...")
                self.__process.wait(5)
                print("...done")
            except subprocess.TimeoutExpired:
                print("process still alive - killing it...")
                self.__process.kill()
                time.sleep(0.5)
                ret_code = self.__process.poll()
                print("process exit code: ",
                      "Unknown - still alive?" if ret_code is None
                      else ret_code)
            self.__process = None
        self._reset()

    def take_stdout(self):
        """Returns any stdout(/err) output from the server that is currently buffered
        client side and removes it from the buffer.
        """
        out = b''
        while True:
            line = self.__stdout_reader.readline()
            if line is None:
                break
            out += line
        return out.decode('utf-8')

    def __getattr__(self, name):
        """Support command/query interface as method attributes as an
        alternative to ``execute_command``.

        Thus, rather than
           ``client.execute_command('CommandName', Arg1='value1', Arg2='value2')``
        the following is supported:
           ``client.CommandName(Arg1='value1', Arg2='value2')``
        """

        def f(**kwargs):
            return self.execute_command(name, **kwargs)
        return f

    def execute_command(self, cmd_name, **kwargs):
        """Run a System Coupling 'external interface' command or query,
        specified by its name and keyword arguments.

        All commands and queries are currently run synchronously.

        See also ``__getattr__``.
        """
        def make_arg(name, val):
            arg = sycapi_pb2.CommandRequest.Argument()
            arg.name = name
            to_variant(val, arg.val)
            return arg

        request = sycapi_pb2.CommandRequest(command=cmd_name)
        request.args.extend([make_arg(name, val) for name, val in kwargs.items()])
        response, meta = self.__command_stub.execute_command(request)
        # Expect meta to comprise a 1-tuple containing a pair value,
        # ('nosync', 'True'|'False'). This tells us whether the command was
        # state changing. Not currently used, but potentially useful if
        # we ever implement incremental updating to optimise client side
        # state cacheing.
        # print(f"meta = {meta[0][0]}: {meta[0][1]}")
        return from_variant(response.result)

    def ping(self):
        return self.__command_stub.ping()


class _StreamReader:
    def __init__(self, stream):
        self.__stream = stream
        self.__queue = Queue()

        def _enqueue(stream, queue):
            try:
                while True:
                    line = stream.readline()
                    if line:
                        queue.put(line)
                    else:
                        raise UnexpectedEndOfStream
            except:
                pass

        self.__readthrd = threading.Thread(target=_enqueue,
                                           args=(self.__stream, self.__queue))
        self.__readthrd.daemon = True
        self.__readthrd.start()

    def readline(self, timeout=None):
        try:
            return self.__queue.get(block=timeout is not None,
                                    timeout = timeout)
        except Empty:
            return None

class _NullStreamReader:
    def readline(self, timeout=None):
        return None

class UnexpectedEndOfStream(Exception):
    pass
