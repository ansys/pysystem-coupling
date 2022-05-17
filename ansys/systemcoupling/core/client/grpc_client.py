import atexit
import itertools
import threading

import grpc

import ansys.api.systemcoupling.v0.command_pb2 as command_pb2
from ansys.systemcoupling.core.client.services.command_query import CommandQueryService
from ansys.systemcoupling.core.client.services.output_stream import OutputStreamService
from ansys.systemcoupling.core.client.services.process import SycProcessService
from ansys.systemcoupling.core.client.services.solution import SolutionService
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

    - All calls synchronous at the moment. We might want to do something
    different with Solve(), for example.
    """

    _id_iter = itertools.count()
    _instances = {-1: None}

    def __init__(self):
        self._reset()
        self.__id = next(SycGrpc._id_iter)

    def _reset(self):
        self.__process = None
        self.__channel = None
        self.__output_thread = None

    @classmethod
    def _cleanup(cls):
        for instance in list(cls._instances.values()):
            instance.exit()

    def start_and_connect(self, host, port, working_dir):
        """Start system coupling in server mode and establish a connection.

        The standard streams are redirected via a single pipe in current impl.
        The output is gathered asynchronously but is currently only accessible
        via take_stdout().
        """
        # print("starting process...")
        self.__process = SycProcess(host, port, working_dir)
        # print("...started. Connecting...")
        self._connect(host, port)
        # print("...connected")

    def connect(self, host, port):
        """Connect to an already running system coupling server running on a known
        host and port.

        No standard stream output is available when connecting in this manner.
        """
        self._connect(host, port)

    def _register_for_cleanup(self):
        SycGrpc._instances[self.__id] = self
        if -1 in SycGrpc._instances:
            # First registration so register atexit handler
            atexit.register(SycGrpc._cleanup)
            # Discard the sentinel
            del SycGrpc._instances[-1]

    def _connect(self, host, port):
        self._register_for_cleanup()
        self.__channel = grpc.insecure_channel(f"{host}:{port}")

        # Wait for server to be ready
        timeout = _CHANNEL_READY_TIMEOUT_SEC
        try:
            grpc.channel_ready_future(self.__channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            raise RuntimeError(
                "Aborting attempt to connect to gRPC channel "
                f"after {timeout} seconds."
            )

        self.__command_service = CommandQueryService(self.__channel)
        self.__ostream_service = OutputStreamService(self.__channel)
        self.__process_service = SycProcessService(self.__channel)
        self.__solution_service = SolutionService(self.__channel)

    def exit(self):
        """Shut down the remote System Coupling server.

        Reset this object ready to start and connect to a new
        server if wished.
        """
        if self.__id in SycGrpc._instances:
            # Remove from atexit cleanup list
            del SycGrpc._instances[self.__id]

        if self.__channel is not None:
            self.__ostream_service.end_streaming()
            self.__process_service.quit()
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
            target=self._read_stdstreams, args=(handle_output,)
        )
        self.__output_thread.daemon = True
        self.__output_thread.start()

    def end_output(self):
        self.__ostream_service.end_streaming()

    def _read_stdstreams(self, handle_output):
        output_iter = self.__ostream_service.begin_streaming()
        text = ""
        while True:
            try:
                response = next(output_iter)
                text += response.text
                if text and text[-1] == "\n":
                    handle_output(text[0:-1])
                    text = ""
            except StopIteration:
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
            arg = command_pb2.CommandRequest.Argument()
            arg.name = name
            to_variant(val, arg.val)
            return arg

        request = command_pb2.CommandRequest(command=cmd_name)
        request.args.extend([make_arg(name, val) for name, val in kwargs.items()])
        response, meta = self.__command_service.execute_command(request)
        # Expect meta to comprise a 1-tuple containing a pair value,
        # ('nosync', 'True'|'False'). This tells us whether the command was
        # state changing. Not currently used, but potentially useful if
        # we ever implement incremental updating to optimise client side
        # state caching.
        # print(f"meta = {meta[0][0]}: {meta[0][1]}")
        return from_variant(response.result)

    def solve(self):
        self.__solution_service.solve()

    def interrupt(self, reason_msg=""):
        self.__solution_service.interrupt(reason=reason_msg)

    def abort(self, reason_msg=""):
        self.__solution_service.abort(reason=reason_msg)

    def ping(self):
        return self.__process_service.ping()
