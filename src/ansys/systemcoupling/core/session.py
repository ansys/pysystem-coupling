import importlib
import os
from typing import Callable, Optional

from ansys.systemcoupling.core.adaptor.impl.injected_commands import (
    get_injected_cmd_map,
)
from ansys.systemcoupling.core.adaptor.impl.root_source import get_root
from ansys.systemcoupling.core.adaptor.impl.syc_proxy import SycProxy
from ansys.systemcoupling.core.native_api import NativeApi

if os.environ.get("PYSYC_DOC_BUILD_VERSION"):
    # It is useful to import explicit types while building doc as it
    # gives us better Sphinx-generated links.
    api_path = (
        f"ansys.systemcoupling.core.adaptor.api_{os.environ['PYSYC_DOC_BUILD_VERSION']}"
    )
    case_root = importlib.import_module(f"{api_path}.case_root").case_root
    setup_root = importlib.import_module(f"{api_path}.setup_root").setup_root
    solution_root = importlib.import_module(f"{api_path}.solution_root").solution_root
else:
    # Fallback to generic type
    from ansys.systemcoupling.core.adaptor.impl.types import Container

    case_root = setup_root = solution_root = Container


class _DefunctRpcImpl:
    def __getattr__(self, _):
        """Any attempted attribute access will raise an exception
        with an explanatory message."""
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
        self.__syc_version = None

    def exit(self) -> None:
        """Close the System Coupling server instance.

        After the server instance is closed, the current instance of
        this class is not usable. Create a new instance if required.
        """
        self.__rpc.exit()
        self.__rpc = _DefunctRpcImpl()
        if self.__native_api:
            # Pass in defunct RPC for better behaviour if
            # anyone has held on to a native API reference
            self.__native_api._exit(self.__rpc)
            self.__native_api = None
        if self.__case_root:
            self.__case_proxy.reset_rpc(self.__rpc)
            self.__case_root = None
        if self.__setup_root:
            self.__setup_proxy.reset_rpc(self.__rpc)
            self.__setup_root = None
        if self.__solution_root:
            self.__solution_proxy.reset_rpc(self.__rpc)
            self.__solution_root = None

    def start_output(
        self, handle_output: Optional[Callable[[str], None]] = None
    ) -> None:
        """Start streaming the standard output written by the System Coupling server.

        The *stdout* and *stderr* streams of the server process are
        merged into a single stream.

        By default, the output text is written to the console, but a custom
        handler may be specified that deals with it in a different way. For
        example, the handler might write the output to a file or display it
        in a separate window. In the default case, printing is done from a
        separate thread. This may lead to unusual behavior in some
        Python console environments. In such cases, a custom approach based
        on the handler might be preferred.

        Streaming can be cancelled by calling the `end_output()` method.

        Parameters
        ----------
        handle_output : callable, optional
            Called with a string argument that provides the latest text in the
            stream. The text may be assumed to comprise one or more complete
            lines of text, with no final newline character. The callback
            should therefore be consistent with a simple call to the
            ``print(text) method``.
        """
        self.__rpc.start_output(handle_output)

    def end_output(self) -> None:
        """Cancels output streaming previously started by the ``start_output`` method."""
        self.__rpc.end_output()

    def ping(self) -> bool:
        """Simple test that the server is alive and responding."""
        return self.__rpc.ping()

    @property
    def case(self) -> case_root:
        """Pythonic client-side form of the System Coupling case persistence API."""
        if self.__case_root is None:
            self.__case_root, self.__case_proxy = self._get_api_root(category="case")
        return self.__case_root

    @property
    def setup(self) -> setup_root:
        """Pythonic client-side form of the System Coupling setup API and data model."""
        if self.__setup_root is None:
            self.__setup_root, self.__setup_proxy = self._get_api_root(category="setup")
        return self.__setup_root

    @property
    def solution(self) -> solution_root:
        """Pythonic client-side form of the System Coupling solution API."""
        if self.__solution_root is None:
            self.__solution_root, self.__solution_proxy = self._get_api_root(
                category="solution"
            )
        return self.__solution_root

    def _get_api_root(self, category):
        if isinstance(self.__rpc, _DefunctRpcImpl):
            self.__rpc.trigger_error
        sycproxy = SycProxy(self.__rpc)
        if self.__syc_version is None:
            version = sycproxy.get_version()
            self.__syc_version = version.replace(".", "_")
        root = get_root(sycproxy, category=category, version=self.__syc_version)
        sycproxy.set_injected_commands(get_injected_cmd_map(category, root, self.__rpc))
        return (root, sycproxy)

    @property
    def _native_api(self) -> NativeApi:
        """Access to the *native* System Coupling API and data model.

        Use of this API is not particularly encouraged, but there may be
        situations where it is useful to access functionality that, for
        some reason, not been fully exposed in PySystemCoupling.

        Furthermore, existing users of the System Coupling CLI may initially
        find it comfortable to work with the familiar API while transitioning
        to using PySystemCoupling.

        This API is exposed dynamically on the client side and provides
        little runtime assistance and documentation.

        For more information, see the `NativeApi` class itself.
        """
        if self.__native_api is None:
            self.__native_api = NativeApi(self.__rpc)
        return self.__native_api

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.exit()
