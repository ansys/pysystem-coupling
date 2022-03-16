#
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#

import threading

import grpc

import ansys.api.systemcoupling.v0.sycapi_pb2 as sycapi_pb2
from ansys.systemcoupling.core.client.services.command_query import CommandQueryService
from ansys.systemcoupling.core.client.services.output_stream import OutputStreamService
from ansys.systemcoupling.core.client.syc_process import SycProcess
from ansys.systemcoupling.core.client.variant import from_variant, to_variant

_CHANNEL_READY_TIMEOUT_SEC = 10


class SycGrpc(object):
    """Provides a remote proxy API to System Coupling's Command/Query
    external interface, built on a basic gRPC interface.

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
        self.__process = SycProcess(host, port, working_dir)
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
            self.__ostream_service.end_streaming()
            self.__command_service.quit()
            self.__channel = None
        if self.__process:
            self.__process.end()
            self.__process = None
        self._reset()

    def start_output(self, handle_output=None):
        """Start streaming of standard output streams from System Coupling
        and, by default, print to the console.
        """
        def default_handler(text):
            print(text)
        handle_output = handle_output or default_handler
        self.__output_thread = threading.Thread(
            target=self._read_stdstreams,
            args=(handle_output,))
        self.__output_thread.daemon = True
        self.__output_thread.start()

    def end_output(self):
        self.__ostream_service.end_streaming()
        # if not self.__output_thread:
        #     return
        # alive = self.__output_thread.is_alive()
        # print("out thread alive ?", alive)
        # if alive:
        #     print("checkagain...")
        #     time.sleep(1)
        #     print("out thread alive ?", self.__output_thread.is_alive())

    def _read_stdstreams(self, handle_output):
        output_iter = self.__ostream_service.begin_streaming()
        text = ''
        while True:
            try:
                response = next(output_iter)
                text += response.text
                if text[-1] == '\n':
                    handle_output(text[0:-1])
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
