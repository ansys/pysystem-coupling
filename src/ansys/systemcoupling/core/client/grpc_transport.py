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

from dataclasses import dataclass, fields
from enum import Enum
import os
import pathlib
import re
import socket
from uuid import uuid4

from ansys.tools.common.cyberchannel import (
    LOOPBACK_HOSTS,
    create_channel,
    determine_uds_folder,
)
import grpc

from ansys.systemcoupling.core.client.syc_launch_script import path_to_system_coupling
from ansys.systemcoupling.core.syc_version import (
    SYC_VERSION_CONCAT,
    normalize_version,
)
from ansys.systemcoupling.core.util.logging import LOG

_IS_WINDOWS = os.name == "nt"

_version_re = re.compile(r"\bv[0-9][0-9][0-9]\b")


class ConnectionType(Enum):
    """Enum containing the various gRPC connection options that
    are supported.

    Note that not all options are supported in all contexts. For
    example, in the case of calling ``launch()`` to launch a process
    and connect to it, only local host connections are currently supported.
    """

    SECURE_LOCAL = 1
    """The usual default. This selects a supported secure local
    connection type appropriate for the platform and server version.
    In practice, this is ``UNIX_DOMAIN_SOCKETS`` or
    ``WINDOWS_NAMED_USER_AUTHENTICATION``."""
    UNIX_DOMAIN_SOCKETS = 2
    """Use a standard Unix domain socket to connect. This is the
    default on Linux and may be supported on Windows in some cases."""
    WINDOWS_NAMED_USER_AUTHENTICATION = 3
    """A local connection with additional authentication that ensures
    the client and server are running as the same Windows user. This
    is only available on Windows and is the default secure local
    connection type if UDS is not available."""
    MTLS_LOCAL = 4
    """A local connection authenticated using mutual TLS."""
    MTLS_REMOTE = 5
    """A remote connection authenticated using mutual TLS."""
    INSECURE_LOCAL = 6
    """A local connection with no authentication mechanism. Should not
    normally be used, but might be necessary for certain older server
    versions."""
    INSECURE_REMOTE = 7
    """A remote connection with no authentication mechanism. Should not
    normally be used, but might be necessary for certain older server
    versions."""


class _TransportMode(str, Enum):
    """Enum containing the different modes of connection."""

    INSECURE, UDS, MTLS, WNUA = ("insecure", "uds", "mtls", "wnua")


class StartupArgumentCategory(Enum):
    """Enum containing the form of the startup arguments relating to the
    gRPC transport.

    The category is associated with a given server version. Depending on
    the version and any installed service pack, the arguments might take the
    new or old form.
    """

    OLD_ARGUMENTS = 0
    NEW_OR_OLD_ARGUMENTS = 1
    NEW_ARGUMENTS = 2


@dataclass
class _ConnectionOptions:
    transport_mode: _TransportMode = _TransportMode.INSECURE
    allow_remote_host: bool = False
    port: int | None = None
    host: str = "127.0.0.1"
    certs_folder: str | None = None
    uds_service: str = "systemcoupling"
    uds_dir: str | None = None
    uds_id: str | None = None


class StartupAndConnectionInfo:
    """Encapsulates most of the considerations relating to choice of
    connection type."""

    def __init__(self, launching: bool, connection_type: ConnectionType, **kwargs):

        version = kwargs.pop("version", "")

        self._exe_path = None
        if launching:
            self._exe_path = path_to_system_coupling(version)

            if version:
                version_str = version
            elif m := _version_re.search(self._exe_path):
                # Use .../vNNN/... from path
                version_str = m.group(0)[1:]
            else:
                # Fall back to the default version
                version_str = SYC_VERSION_CONCAT

        else:
            version_str = version if version else SYC_VERSION_CONCAT

        # Store normalised version info
        self._version = normalize_version(version_str)
        self._version_category = _grpc_argument_category(self._version)

        self._options = self._make_options(connection_type, **kwargs)

    def executable_path(self) -> str | None:
        """Return the path to the executable to be launched.

        If ``launching`` was not specified, this is ``None``.
        """
        return self._exe_path

    def command_line_arguments(self) -> list[str]:
        """Return the list of command line arguments based on the current transport
        options.

        This is valid to call only if the server is a version that
        definitely or possibly supports the new format.
        """
        opt = self._options
        args = ["--grpc", f"--transport-mode={opt.transport_mode.value}"]
        port = self._get_port()
        match opt.transport_mode:
            case _TransportMode.UDS:
                # Always send uds-dir as some older versions might be
                # inconsistent with us about the default location.
                args.append(f"--uds-dir={self._get_uds_folder()}")
                if opt.uds_id:
                    args.append(f"--uds-id={opt.uds_id}")
            case _TransportMode.WNUA:
                args.append(f"--port={port}")
            case _TransportMode.MTLS:
                args.append(f"--port={port}")
                if opt.allow_remote_host:
                    args.append("--allow-remote-host")
                    args.append(f"--host={opt.host}")
                if opt.certs_folder:
                    args.append(f"--certs-folder={opt.certs_folder}")
            case _TransportMode.INSECURE:
                args.append(f"--port={port}")
                if opt.allow_remote_host:
                    args.append("--allow-remote-host")
                    args.append(f"--host={opt.host}")
        return args

    @property
    def startup_argument_category(self) -> StartupArgumentCategory:
        """Returns the `StartupArgumentCategory` based on the assumed version.

        This informs the caller which form of command line arguments to use
        when System Coupling is launched.
        """
        return self._version_category

    @property
    def is_insecure_connection_requested(self) -> bool:
        """Returns whether an insecure connection type was specified."""
        return self._options.transport_mode == _TransportMode.INSECURE

    def old_command_line_arguments(self) -> list[str]:
        """Returns the command line argument in the `old` server format.

        This is valid to call only if the server is a version that
        definitely or possibly supports the old format.
        """
        opt = self._options
        if self._version_category == StartupArgumentCategory.NEW_ARGUMENTS:
            raise RuntimeError(
                f"The assumed version of the System Coupling server"
                f" {self._version[0]}.{self._version[1]} does not accept the old"
                " command line format."
            )
        if opt.transport_mode != _TransportMode.INSECURE:
            raise RuntimeError(
                "You must specify an insecure connection type to be able "
                "to use the requested version of System Coupling."
            )
        return [f"--grpcport={opt.host}:{self._get_port()}"]

    def get_server_channel(self) -> grpc.Channel:
        """Return the gRPC server channel object appropriate for the
        requested connection type.
        """
        opt = self._options
        if opt.transport_mode == _TransportMode.INSECURE:
            LOG.warning(
                "The System Coupling session will be connected in insecure gRPC mode. "
                "This mode is not recommended. Refer to the 'launch()' API "
                "documentation for secure connection options."
            )

        LOG.info(f"Creating gRPC channel with transport mode: {opt.transport_mode}")
        return create_channel(
            opt.transport_mode.value,
            host=opt.host,
            port=opt.port,
            uds_service=opt.uds_service,
            uds_dir=opt.uds_dir,
            uds_id=opt.uds_id,
            certs_dir=opt.certs_folder,
        )

    def _make_options(
        self, connection_type: ConnectionType, **kwargs
    ) -> _ConnectionOptions:
        relevant_args = {}
        for field in fields(_ConnectionOptions):
            if value := kwargs.get(field.name):
                if field.name == "port":
                    value = int(value)
                relevant_args[field.name] = value

        options = _ConnectionOptions(**relevant_args)

        match connection_type:
            case ConnectionType.SECURE_LOCAL:
                options.transport_mode = (
                    _TransportMode.UDS
                    if self._is_uds_supported()
                    else _TransportMode.WNUA
                )
                # If UDS, uds_id will be set later if not already set
            case ConnectionType.UNIX_DOMAIN_SOCKETS:
                if not self._is_uds_supported():
                    raise RuntimeError(
                        "Unix Domain Sockets are not supported for "
                        "the version of the server in use."
                    )
                if options.host not in LOOPBACK_HOSTS:
                    raise ValueError(
                        "UDS transport only supports localhost connections."
                    )
                options.transport_mode = _TransportMode.UDS
                # uds_id will be set later if not already set
            case ConnectionType.WINDOWS_NAMED_USER_AUTHENTICATION:
                if not _IS_WINDOWS:
                    raise ValueError(
                        "Windows Named User Authentication (WNUA) is only supported on Windows."
                    )
                if options.host not in LOOPBACK_HOSTS:
                    raise ValueError(
                        "Remote host connections are not supported with WNUA."
                    )
                options.transport_mode = _TransportMode.WNUA
            case ConnectionType.MTLS_LOCAL:
                if options.host not in LOOPBACK_HOSTS:
                    raise ValueError(
                        "Remote host connections are not supported with"
                        " selected connection type, 'MTLS_Local'."
                    )
                options.transport_mode = _TransportMode.MTLS
                options.certs_folder = self._get_certs_folder(options.certs_folder)
            case ConnectionType.MTLS_REMOTE:
                options.transport_mode = _TransportMode.MTLS
                options.allow_remote_host = True
                options.certs_folder = self._get_certs_folder(options.certs_folder)
            case ConnectionType.INSECURE_LOCAL:
                if options.host not in LOOPBACK_HOSTS:
                    raise ValueError(
                        "Remote host connections are not supported with"
                        " selected connection type, 'Insecure_Local'."
                    )
                options.transport_mode = _TransportMode.INSECURE
            case ConnectionType.INSECURE_REMOTE:
                options.transport_mode = _TransportMode.INSECURE
                options.allow_remote_host = True

        if options.transport_mode == _TransportMode.UDS:
            if not options.uds_id:
                options.uds_id = uuid4().hex

        return options

    def _is_uds_supported(self):
        # NEW_ARGUMENTS is a proxy for supporting UDS on Windows as it
        # indicates a version where the server side gRPC supports UDS.
        # UDS support on Windows also requires client side support, which
        # depends on the Python gPRC version. In practice, we should always
        # be beyond the version where gRPC started supporting UDS on Windows,
        # but we can assume it will be checked in the 'cyberchannel' module.
        return (
            not _IS_WINDOWS
            or self._version_category == StartupArgumentCategory.NEW_ARGUMENTS
        )

    def _get_uds_folder(self) -> pathlib.Path:
        return determine_uds_folder(self._options.uds_dir)

    def _get_certs_folder(self, specified_folder: str | None) -> str:
        # Explicit setting overrides other options
        if folder := (specified_folder or os.environ.get("ANSYS_GRPC_CERTIFICATES")):
            return folder
        else:
            # Fall back to default location
            return "certs"

    def _get_port(self) -> int:
        if self._options.port is None:
            self._options.port = _find_port()
        return self._options.port


def _grpc_argument_category(version: tuple[int, int]) -> StartupArgumentCategory:
    """Categorise version into `StartupArgumentCategory`."""
    if version < (24, 2):
        return StartupArgumentCategory.OLD_ARGUMENTS
    if version in ((24, 2), (25, 1), (25, 2)):
        return StartupArgumentCategory.NEW_OR_OLD_ARGUMENTS
    else:
        return StartupArgumentCategory.NEW_ARGUMENTS


def _find_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]
