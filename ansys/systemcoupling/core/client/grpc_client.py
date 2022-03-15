#
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#

import os
import platform
from queue import Queue, Empty
import subprocess
import threading
import time

import grpc

import ansys.api.systemcoupling.v0.sycapi_pb2 as sycapi_pb2
from ansys.systemcoupling.core.client.services.command_query import CommandQueryService
from ansys.systemcoupling.core.client.services.output_stream import OutputStreamService
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

def _start_system_coupling(host, port, working_dir, log_level=1):
    from copy import deepcopy
    env = deepcopy(os.environ)
    env['PYTHONUNBUFFERED'] = '1'
    env['SYC_GUI_SILENT_SERVER'] = '1'
    args = [_path_to_system_coupling(), '-m', 'cosimtest', f'--grpcport={host}:{port}']
    if log_level:
        args += ['-l', str(log_level)]
    print("Starting System Coupling: ", args[0])
    return subprocess.Popen(args,
                            env=env,
                            cwd=working_dir,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT
                            )


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

    def __init__(self):
        self._reset()

    def _reset(self):
        self.__process = None
        self.__channel = None
        self.__output_thread = None

    def start_and_connect(self, host, port, working_dir):
        """Start system coupling in server mode and establish a connection.

        The standard streams are redirected via a single pipe in current impl.
        The output is gathered asynchronously but is currently only accessible
        via take_stdout().
        """
        self.__process = _start_system_coupling(host, port, working_dir)
        self._connect(host, port)

    def connect(self, host, port):
        """Connect to an already running system coupling server running on a known
        host and port.

        No standard stream output is available when connecting in this manner.
        """
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

        self.__command_service = CommandQueryService(self.__channel)
        self.__ostream_service = OutputStreamService(self.__channel)

    def exit(self):
        """Shut down the remote System Coupling server.

        Reset this object ready to start and connect to a new
        server if wished.
        """
        if self.__channel is not None:
            #self.__ostream_service.end_streaming()
            self.end_output()
            self.__command_service.quit()
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

    def start_output(self):
        """Start streaming of standard output streams from System Coupling
        and print on the console.
        """
        self.__outbuf = ''
        self.__output_thread = threading.Thread(target=self._read_stdstreams)
        self.__output_thread.daemon = True
        self.__output_thread.start()

    def end_output(self):
        self.__ostream_service.end_streaming()
        print(f'buffered output:\n{self.__outbuf}\n')
        self.__outbuf = ''
        if not self.__output_thread:
            return
        alive = self.__output_thread.is_alive()
        print("out thread alive ?", alive)
        if alive:
            print("checkagain...")
            time.sleep(1)
            print("out thread alive ?", self.__output_thread.is_alive())

    def _read_stdstreams(self):
        output_iter = self.__ostream_service.begin_streaming()
        text = ''
        while True:
            try:
                response = next(output_iter)
                text += response.text
                if text[-1] == '\n':
                    self.__outbuf += text
                    print(text[0:-1])
                    text = ''
            except StopIteration:
                print("output thread stopping")
                break

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
        response, meta = self.__command_service.execute_command(request)
        # Expect meta to comprise a 1-tuple containing a pair value,
        # ('nosync', 'True'|'False'). This tells us whether the command was
        # state changing. Not currently used, but potentially useful if
        # we ever implement incremental updating to optimise client side
        # state cacheing.
        # print(f"meta = {meta[0][0]}: {meta[0][1]}")
        return from_variant(response.result)

    def ping(self):
        return self.__command_service.ping()
