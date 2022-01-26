#
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#

import json
import os
import platform
from queue import Queue, Empty
import socket
import subprocess
import threading
import time
import xml.etree.ElementTree as XET

_isWindows = any(platform.win32_ver())

_INSTALL_ROOT = "AWP_ROOT222"
_SC_ROOT_ENV = "SYSC_ROOT"

_SCRIPT_EXT = '.bat' if _isWindows else ''
_SCRIPT_NAME = 'systemcoupling' + _SCRIPT_EXT

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
    args = [_path_to_system_coupling(), '-m', 'cosimtest', f'--port={host}:{port}']
    return subprocess.Popen(args,
                            env=env,
                            cwd=working_dir,
                            stdout=subprocess.PIPE if redirect_std else None,
                            # for now, merge stderr with stdout if redirectng
                            stderr=subprocess.STDOUT if redirect_std else None)

def _read_connection_info(sock):
    buf = ''
    bufsize = 1024
    done = False
    while not done:
        ret = sock.recv(bufsize)
        buf += ret.decode('ascii')
        done = buf.endswith('</connectAt>')

    xconnect = XET.fromstring(buf)
    host = port = None
    for child in xconnect:
        if child.tag == 'host':
            host = child.text
        elif child.tag == 'port':
            port = int(child.text)

    assert None not in (host, port)

    return (host, port)

class SycRpc(object):
    """Provides a remote proxy API to System Coupling's Command/Query
    external interface.

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
        self.__startTag = "<start>"
        self._reset()

    def _reset(self):
        self.__process = None
        self.__serversock = None
        self.__clientsock = None
        self.__sparesock = None

        self.__response_thread = threading.Thread(target=self._listen_to_server)
        self.__response_thread.daemon = True

        self.__keepreading = True
        self.__keepreading_lock = threading.Lock()

        self.__response = None
        self.__response_cv = threading.Condition()

    def start_and_connect(self, working_dir):
        """Start system coupling in server mode and establish a connection.

        The standard streams are redirected via a single pipe in current impl.
        The output is gathered asynchronously but is currently only accessible
        via take_stdout().
        """

        # Start server socket to which SyC will attach
        connect_server = self.__serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_server.bind((socket.gethostname(), 0))
        connect_server.listen(1)

        # Host and port on which SyC initially connects to connection server
        sockname = connect_server.getsockname()

        # SyC start
        self.__process = _start_system_coupling(*sockname, working_dir, redirect_std=True)

        self.__stdout_reader = _StreamReader(self.__process.stdout)

        # SyC establishes connection with us and tells us about *its* server socket
        sock = connect_server.accept()[0]
        srv_host, srv_port = _read_connection_info(sock)

        # Have kept this open in the past to implement solver interrupt
        self.__sparesock = sock

        self._connect(srv_host, srv_port)

    def connect(self, host, port):
        """Connect to an already running system coupling server running on a known
        host and port.

        No standard stream output is available when connecting in this manner.
        """
        self.__stdout_reader = _NullStreamReader()
        self._connect(host, port)

    def _connect(self, host, port):
        # Connect to SyC server - this is now our main communication socket
        self.__clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nattempt = 5
        for i in range(nattempt):
            # Sometimes server is not immediately ready to accept connection
            try:
                self.__clientsock.connect((host, port))
                print(f'{i+1} attempts to connect')
                break
            except:
                if i == nattempt-1:
                    raise
                time.sleep(0.1 * i)

        self.__response_thread.start()

    def exit(self):
        """Shut down the remote System Coupling server.

        Reset this object ready to start and connect to a new
        server if wished.
        """
        self._write(XET.tostring(XET.Element('exit')))
        self.__response_thread.join(timeout=5.0)
        self.__clientsock.close()
        self.__sparesock and self.__sparesock.close()
        # TODO check process for shutdown - forcibly close otherwise?
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

        rpc = XET.Element('jsonrpc')
        cmd = {'method': cmd_name,
               'params': [kwargs]} # NB : args wrapped in list for historical reasons
        rpc.text = json.dumps(cmd)

        # This defaults to ascii encoding, which is consistent with server
        serialized_cmd = XET.tostring(rpc)

        self._write(serialized_cmd)
        serialized_response = self._wait_for_response()
        return self._process_response(serialized_response)

    def _listen_to_server(self):

        # This is just to avoid having a 'public' read() on the main class
        class Wrapper(object): pass
        wrapper = Wrapper()
        wrapper.read = self._read

        try:
            items = XET.iterparse(wrapper)
            for event, node in items:
                if event != 'end':
                    # shouldn't actually see anything else
                    continue
                if node.tag == 'disconnect':
                    print("disconnect received")
                    break
                elif node.tag == 'methodResponse':
                    response = node.text
                    self._read_response(response)
                else:
                    # TODO? other node types ?
                    continue
        except Exception as e:
            print(f'exception in listener thread, probable disconnection: {str(e)}')
            pass

    def _read_response(self, response):
        with self.__response_cv:
            self.__response = response
            self.__response_cv.notify()

    def _wait_for_response(self):
        with self.__response_cv:
            self.__response_cv.wait_for(lambda : self.__response is not None)
            response = self.__response
            self.__response = None
            return response

    def _process_response(self, serialized_response):
        response = json.loads(serialized_response)
        if 'nosync' in response:
            return None
        elif 'result' in response:
            return response['result']
        elif 'faultCode' in response:
            raise RuntimeError(f"[Remote error] {response['faultString']}\n\n"
                               f"[Remote traceback]\n{response['detail']['stackTrace']}")
        else:
            raise RuntimeError("Remote method call error. Unrecognized response.")

    def _read(self, bufsize):
        if self.__startTag:
            startTag = self.__startTag
            self.__startTag = None
            return startTag

        ret = self.__clientsock.recv(bufsize)
        return ret.decode('ascii')

    def _write(self, buf):
        buflen, totsent = len(buf), 0
        while totsent < buflen:
            totsent += self.__clientsock.send(buf if totsent == 0 else buf[totsent:])


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
