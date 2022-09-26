from typing import Callable, Optional

from ansys.systemcoupling.core.adaptor.impl.source import get_root
from ansys.systemcoupling.core.adaptor.impl.syc_proxy import SycProxy
from ansys.systemcoupling.core.native_api import NativeApi

try:
    # It's worth having these for type hinting and documentation links but
    # we need the import check and fallback because they are generated
    # classes and Session plays a "bootstrapping" role in generating them
    from ansys.systemcoupling.core.adaptor.api.case_root import case_root
    from ansys.systemcoupling.core.adaptor.api.setup_root import setup_root
    from ansys.systemcoupling.core.adaptor.api.solution_root import solution_root
except ImportError:
    # Fallback to generic type
    # (should not occur in normal use and in doc generation)
    from ansys.systemcoupling.core.adaptor.impl.types import Container

    case_root = setup_root = solution_root = Container


class _DefunctRpcImpl:
    def __getattr__(self, _):
        raise RuntimeError(
            "This session instance has exited. Launch or attach to a new instance."
        )


class Session:
    """Client interface to a System Coupling server instance, providing
    an API to set up and solve coupled analyses.

    The API that is provided is a fairly thin adaptation of the existing
    System Coupling data model access and command and query API.

    System Coupling runs as a server process, which is accessed via the
    provided ``rpc`` object. This services the command and query requests
    made here.
    """

    def __init__(self, rpc):
        """Initializes a ``Session`` instance.

        Parameters
        ----------
        rpc
            Provider of remote command and query services.
        """
        self.__case_root = None
        self.__setup_root = None
        self.__solution_root = None
        self.__rpc = rpc
        self.__native_api = None

    def exit(self) -> None:
        """Close the System Coupling server instance.

        Following this, the current instance of this class will not
        be usable. Create a new instance if required.
        """
        self.__rpc.exit()
        self.__rpc = _DefunctRpcImpl()
        if self.__native_api:
            # Pass in defunct RPC for better behaviour if
            # anyone has held on to a native API reference
            self.__native_api._exit(self.__rpc)
            self.__native_api = None
        # XXX TODO see about doing something similar for case, setup, solution
        self.__case_root = None
        self.__setup_root = None
        self.__solution_root = None

    def start_output(
        self, handle_output: Optional[Callable[[str], None]] = None
    ) -> None:
        """Start streaming the `standard output` written by the System Coupling server.

        The ``stdout`` and ``stderr`` streams of the server process are
        merged into a single stream.

        By default, the output text is written to the console, but a custom
        handler may be specified that deals with it in a different way (for
        example, the handler might write the output to a file or display it
        in a separate window). In the default case, printing is done from a
        separate thread and this may lead to unusual behaviour in some
        Python console environments. In such cases, a custom approach based
        on the handler might be preferred.

        Streaming can be cancelled by calling the ``end_output`` method.

        Parameters
        ----------
        handle_output : callable, optional
            Called with string argument that provides the latest text in the
            stream. The text may be assumed to comprise one or more complete
            lines of text, with no final newline character. The callback
            should therefore be consistent with a simple call to ``print(text)``.
        """
        self.__rpc.start_output(handle_output)

    def end_output(self) -> None:
        """Cancels output streaming previously started by ``start_output``."""
        self.__rpc.end_output()

    def ping(self) -> bool:
        """Simple test that the server is alive and responding."""
        return self.__rpc.ping()

    @property
    def case(self) -> case_root:
        """Provides access to the `Pythonic` client-side form of the System
        Coupling case persistence API.
        """
        if self.__case_root is None:
            self.__case_root = self._get_api_root(category="case")
        return self.__case_root

    @property
    def setup(self) -> setup_root:
        """Provides access to the `Pythonic` client-side form of the System
        Coupling setup API and data model.
        """
        if self.__setup_root is None:
            self.__setup_root = self._get_api_root(category="setup")
        return self.__setup_root

    @property
    def solution(self) -> solution_root:
        """Provides access to the `Pythonic` client-side form of the System
        Coupling solution API.
        """
        if self.__solution_root is None:
            self.__solution_root = self._get_api_root(category="solution")
        return self.__solution_root

    def _get_api_root(self, category):
        if isinstance(self.__rpc, _DefunctRpcImpl):
            self.__rpc.trigger_error
        sycproxy = SycProxy(self.__rpc)
        return get_root(sycproxy, category=category)

    @property
    def _native_api(self) -> NativeApi:
        """Provides access to the 'native' System Coupling API and data
        model.

        Use of this API is not particularly encouraged but there may be
        situations where it is useful to access functionality that has
        not directly been exposed in PySystemCoupling.

        Furthermore, existing users of the System Coupling CLI may initially
        find it comfortable to work with the familiar API while transitioning
        to using PySystemCoupling.

        This API is exposed dynamically on the client side and provides
        little runtime assistance and documentation.

        See the ``NativeApi`` class itself for more details.
        """
        if self.__native_api is None:
            self.__native_api = NativeApi(self.__rpc)
        return self.__native_api

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.exit()
