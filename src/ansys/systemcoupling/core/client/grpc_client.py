import atexit
import itertools
import json
import os
import socket
import threading

import ansys.api.systemcoupling.v0.command_pb2 as command_pb2
import grpc

from ansys.systemcoupling.core.client.services.command_query import CommandQueryService
from ansys.systemcoupling.core.client.services.output_stream import OutputStreamService
from ansys.systemcoupling.core.client.services.process import SycProcessService
from ansys.systemcoupling.core.client.services.solution import SolutionService
from ansys.systemcoupling.core.client.syc_container import start_container
from ansys.systemcoupling.core.client.syc_process import SycProcess
from ansys.systemcoupling.core.client.variant import from_variant, to_variant
from ansys.systemcoupling.core.util.logging import LOG

_CHANNEL_READY_TIMEOUT_SEC = 15
_LOCALHOST_IP = "127.0.0.1"


def _find_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class SycGrpc(object):
    """Provides a remote proxy API to System Coupling's command and
    query external interface, built on a basic gRPC interface.

    An instance of this class controls starting System Coupling as
    a server in cosimulation mode and handles the underlying RPC (remote
    procedure call) to provide the command and query API. The
    ``start_and_connect`` method should be used to start the remote
    SystemCoupling instance, and the ``exit`` method should be used
    to close the connection and shut down this instance. Alternatively,
    the ``connect`` method can be used to connect to an already running server
    instance.

    This class supports two approaches to making API calls on System
    Coupling:

    # Using the ``execute_command`` method, which takes the command name
      as a string and a dictionary of keyword arguments.
    # Using the ``__getattr__`` method, which allows commands to be called
      as if direct methods of this class.

    Both of these are useful in different contexts.

    .. note::
       System Coupling runs in a server mode that expects a single
       client to connect after start up and which becomes the only
       means of controlling the server during its lifetime.

    TODO:

    - All calls are synchronous at the moment. We might want to do something
    different with the Solve() command. For example, you might want to
    do something like this:
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

    def start_and_connect(self, **kwargs):
        """Start System Coupling in server mode and establish a connection."""

        # Support backdoor container launch via an environment variable.
        # For example, we might want to default to launching installation
        # locally but container on GitHub (for build tasks like code generation).
        # You could still switch to the container locally by setting the
        # environment variable.

        working_dir = kwargs.pop("working_dir", None)
        port = kwargs.pop("port", None)
        version = kwargs.pop("version", None)

        if os.environ.get("SYC_LAUNCH_CONTAINER") == "1":
            mounted_from = working_dir if working_dir else "./"
            mounted_to = "/working"
            self.start_container_and_connect(
                mounted_from, mounted_to, port=port, version=version
            )
        else:  # pragma: no cover
            if port is None:
                port = _find_port()
            if working_dir is None:
                working_dir = "."
            LOG.debug("Starting process...")
            self.__process = SycProcess(
                _LOCALHOST_IP, port, working_dir, version, **kwargs
            )
            LOG.debug("...started")
            self._connect(_LOCALHOST_IP, port)

    def start_container_and_connect(
        self,
        mounted_from: str,
        mounted_to: str,
        network: str = None,
        port: int = None,
        version: str = None,
    ):
        """Start the System Coupling container and establish a connection."""
        LOG.debug("Starting container...")
        port = port if port is not None else _find_port()
        start_container(mounted_from, mounted_to, network, port, version)
        LOG.debug("...started")
        self._connect(_LOCALHOST_IP, port)

    def connect(self, host, port):
        """Connect to an already running System Coupling server running on a known
        host and port.
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
        LOG.debug("Connecting...")
        self._register_for_cleanup()
        self.__channel = grpc.insecure_channel(f"{host}:{port}")

        # Wait for server to be ready
        timeout = _CHANNEL_READY_TIMEOUT_SEC
        try:
            grpc.channel_ready_future(self.__channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            raise RuntimeError(
                "Stopping attempt to connect to gRPC channel "
                f"after {timeout} seconds."
            )

        LOG.debug("...connected")

        self.__command_service = CommandQueryService(self.__channel)
        self.__ostream_service = OutputStreamService(self.__channel)
        self.__process_service = SycProcessService(self.__channel)
        self.__solution_service = SolutionService(self.__channel)

    def exit(self):
        """Shut down the remote System Coupling server.

        Reset this object so it is ready to start and connect to a new
        server if needed.
        """
        if self.__id in SycGrpc._instances:
            # Remove from atexit cleanup list
            del SycGrpc._instances[self.__id]

        if self.__channel is not None:
            try:
                self.__ostream_service.end_streaming()
            except Exception as e:
                LOG.debug("Exception on OutputStreamService.end_straming(): " + str(e))
            self.__process_service.quit()
            self.__channel = None
        if self.__process:
            self.__process.end()
            self.__process = None
        self._reset()

    def start_output(self, handle_output=None):
        """Start streaming of standard streams from System Coupling
        and print to the console be default.

        Standard output and error streams are combined in the output
        streamed to this client.
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
        """Stop streaming standard streams."""
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
                # Flush any trailing text
                if text:
                    handle_output(text)
                break

    def __getattr__(self, name):
        """Support command and query interfaces as method attributes to provide an
        alternative to the``execute_command`.

        Here is how you use the ``execute_command``:
           ``client.execute_command('CommandName', Arg1='value1', Arg2='value2')``
        Instead, you can use this:
           ``client.CommandName(Arg1='value1', Arg2='value2')``
        """

        def f(**kwargs):
            return self.execute_command(name, **kwargs)

        return f

    def execute_command(self, cmd_name, **kwargs):
        """Run a System Coupling *external interface* command or query,
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

        # The second element of the above tuple (which is actually gRPC
        # trailing metadata) is currently unused, but it comprises a 1-tuple
        # containing a pair value, ('nosync', 'True'|'False').
        #     is_nosync = bool(meta[0][1])
        # This tells us whether the command was state changing. This will
        # be useful if, as is likely, we implement incremental updating to
        # optimize client-side state caching.

        ret = from_variant(response.result)
        if "json_ret" in kwargs:
            # Expect the result to decode as a (JSON) string
            return json.loads(ret)
        return ret

    def solve(self):
        self.__solution_service.solve()

    def interrupt(self, reason_msg=""):
        self.__solution_service.interrupt(reason=reason_msg)

    def abort(self, reason_msg=""):
        self.__solution_service.abort(reason=reason_msg)

    def ping(self):
        return self.__process_service.ping()
