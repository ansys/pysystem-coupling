from ansys.systemcoupling.core.native_api import NativeApi
from ansys.systemcoupling.core.settings.datamodel import get_root
from ansys.systemcoupling.core.syc_proxy_adapter import SycProxyAdapter


class _DefunctRpcImpl:
    def __getattr__(self, _):
        raise RuntimeError(
            "This analysis instance has exited. Launch or " "attach to a new instance."
        )


class SycAnalysis:
    """Encapsulates a System Coupling analysis, providing access to the
    System Coupling data model and its command and query API.

    System Coupling is presumed to be running remotely and is accessed
    via the provided "rpc impl" which services command and query
    requests made via ``SycAnalysis``.
    """

    def __init__(self, rpc_impl):
        self.__case_root = None
        self.__setup_root = None
        self.__solution_root = None
        self.__rpc_impl = rpc_impl
        self.__native_api = None

    def exit(self):
        """Close the remote System Coupling instance.

        Following this, the current instance of this class will not
        be usable. Create a new instance if required.
        """
        self.__rpc_impl.exit()
        self.__rpc_impl = _DefunctRpcImpl()
        if self.__native_api:
            # Pass in defunct RPC for better behaviour if
            # anyone has held on to a native API reference
            self.__native_api._exit(self.__rpc_impl)
            self.__native_api = None
        # XXX TODO see about doing something similar for setup
        self.__case_root = None
        self.__setup_root = None
        self.__solution_root = None

    def start_output(self, handle_output=None):
        """Start streaming the "standard output" written by System Coupling.

        The "stdout" and "stderr" streams are merged into a single stream.

        By default, the output text is written to the console, but a custom
        handler may be specified that deals with it in a different way (e.g.,
        write to a file or display in a separate window). Note that if the
        default is used, the printing is done from a separate thread. This
        may lead to unusual behaviour in some Python console environments.
        In such cases, a custom approach based on the handler could be
        adopted.

        Streaming can be cancelled via the `end_output` method.

        Parameters
        ----------
        handle_output : callable
            Called with str argument that provides the latest text in the
            stream. Might represent multiple lines of output (with embedded
            newlines).
        """
        self.__rpc_impl.start_output(handle_output)

    def end_output(self):
        """Cancels output streaming previously started by `start_output`."""
        self.__rpc_impl.end_output()

    def solve(self):
        """Solves the current case."""
        self.__rpc_impl.solve()

    def interrupt(self, reason_msg=""):
        """Interrupts a solve in progress.

        See also `abort`. The difference between an interrupted and
        aborted solve is that an interrupted solve may be resumed.

        Parameters
        ----------
        reason_msg : str
            Text to describe the reason for the interrupt. This might be
            used for such purposes as providing additional annotation in
            transcript output.
        """
        self.__rpc_impl.interrupt(reason=reason_msg)

    def abort(self, reason_msg=""):
        """Aborts a solve in progress.

        See also `interrupt`. In contrast to an interrupted solve,
        an aborted solve may not be resumed.

        Parameters
        ----------
        reason_msg : str
            Text to describe the reason for the abort. This might be
            used for such purposes as providing additional annotation in
            transcript output.
        """
        self.__rpc_impl.abort(reason=reason_msg)

    def ping(self):
        """Simple test that the server is alive and responding."""
        return self.__rpc_impl.ping()

    @property
    def case(self):
        """Provides access to the 'Pythonic' client-side form of the System
        Coupling case persistence API.
        """
        if self.__case_root is None:
            self.__case_root = self._get_api_root(category="case")
        return self.__case_root

    @property
    def setup(self):
        """Provides access to the 'Pythonic' client-side form of the System
        Coupling setup API and data model.
        """
        if self.__setup_root is None:
            self.__setup_root = self._get_api_root(category="setup")
        return self.__setup_root

    @property
    def solution(self):
        """Provides access to the 'Pythonic' client-side form of the System
        Coupling solution API.
        """
        if self.__solution_root is None:
            self.__solution_root = self._get_api_root(category="solution")
        return self.__solution_root

    def _get_api_root(self, category):
        if isinstance(self.__rpc_impl, _DefunctRpcImpl):
            self.__rpc_impl.trigger_error
        sycproxy = SycProxyAdapter(self.__rpc_impl)
        return get_root(sycproxy, category=category)

    @property
    def native_api(self):
        """Provides access to the 'native' System Coupling API and data
        model.

        This is aimed at existing users of the System Coupling CLI who are
        more comfortable with retaining familiar syntax while transitioning
        to use of pySystemCoupling.

        This API is exposed almost completely dynamically on the client side
        so provides little runtime assistance and documentation.

        See `NativeApi` itself for more details.
        """
        if self.__native_api is None:
            self.__native_api = NativeApi(self.__rpc_impl)
        return self.__native_api

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.exit()
