# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import importlib
import os
from typing import Callable, Optional

from ansys.systemcoupling.core.adaptor.impl.injected_commands import (
    get_injected_cmd_map,
)
from ansys.systemcoupling.core.adaptor.impl.root_source import get_root
from ansys.systemcoupling.core.adaptor.impl.syc_proxy import SycProxy
from ansys.systemcoupling.core.native_api import NativeApi
from ansys.systemcoupling.core.participant.manager import ParticipantManager

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
        self.__part_mgr = None

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
        """Cancel output streaming previously started by the ``start_output`` method."""
        self.__rpc.end_output()

    def ping(self) -> bool:
        """Simple test that the server is alive and responding."""
        return self.__rpc.ping()

    @property
    def version(self) -> str:
        """Return the server version as a string.

        The version string is in the form of dot-separated major and minor
        version numbers. For example, "24.2".
        """
        # Internal version string is in '_'-separated form as that is what is used elsewhere.
        return self._get_version().replace("_", ".")

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

    def _get_version(self):
        if self.__syc_version is None:
            proxy = SycProxy(self.__rpc)
            version = proxy.get_version()
            self.__syc_version = version.replace(".", "_")
        return self.__syc_version

    def _get_api_root(self, category):
        if isinstance(self.__rpc, _DefunctRpcImpl):
            self.__rpc.trigger_error
        sycproxy = SycProxy(self.__rpc)
        root = get_root(sycproxy, category=category, version=self._get_version())
        if self.__part_mgr is None:
            self.__part_mgr = ParticipantManager(self, self.__syc_version)
        sycproxy.set_injected_commands(
            get_injected_cmd_map(category, self, self.__part_mgr, self.__rpc)
        )
        return (root, sycproxy)

    @property
    def _native_api(self) -> NativeApi:
        """Access to the *native* System Coupling API and data model.

        Use of this API is not particularly encouraged, but there may be
        situations where it is useful to access functionality that, for
        some reason, has not been fully exposed in PySystemCoupling.

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

    @property
    def _grpc(self):
        """The gRPC connection object, exposed for testing purposes only."""
        return self.__rpc

    def upload_file(
        self,
        file_name: str,
        remote_file_name: Optional[str] = None,
        overwrite: bool = False,
    ):
        """For internal use only: upload a file to the PIM-managed instance.

        Reduces to a no-op if the System Coupling instance is not managed by PIM.

        The remote file may optionally be given a different name from the local one
        and, if not, any directory prefix is stripped in the PIM case.

        Unless ``overwrite`` is ``True``, a ``FileExistsError`` will be raised if
        the remote file already exists.

        Parameters
        ----------
        file_name : str
            local file name
        remote_file_name : str, optional
            remote file name - default is None
        overwrite: bool, optional
            whether to overwrite the remote file if it already exists - default is False

        Returns
        -------
        str
            The remote file name, excluding any directory prefix that might have been
            present in ``file_name``.
        """
        return self.__rpc.upload_file(file_name, remote_file_name, overwrite)

    def download_file(
        self, file_name: str, local_file_dir: str = ".", overwrite: bool = False
    ):
        """For internal use only: download a file from the PIM-managed instance.

        Unless ``overwrite`` is ``True``, a ``FileExistsError`` will be raised if
        the local file already exists.

        Parameters
        ----------
        file_name : str
            file name
        local_file_dir : str, optional
            local directory to write the file - default is current directory, "."
        overwrite : bool, optional
            whether to overwrite the remote file if it already exists - default is False
        """
        self.__rpc.download_file(file_name, local_file_dir, overwrite)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.exit()
