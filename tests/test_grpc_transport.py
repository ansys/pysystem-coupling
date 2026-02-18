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

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from ansys.systemcoupling.core.client.grpc_transport import (
    ConnectionType,
    StartupAndConnectionInfo,
    StartupArgumentCategory,
    _ConnectionOptions,
    _find_port,
    _grpc_argument_category,
    _TransportMode,
)


class TestEnumsAndDataClasses:
    """Test the enum classes and data classes."""

    def test_connection_type_enum_values(self):
        """Test ConnectionType enum has expected values."""
        assert ConnectionType.SECURE_LOCAL.value == 1
        assert ConnectionType.UNIX_DOMAIN_SOCKETS.value == 2
        assert ConnectionType.WINDOWS_NAMED_USER_AUTHENTICATION.value == 3
        assert ConnectionType.MTLS_LOCAL.value == 4
        assert ConnectionType.MTLS_REMOTE.value == 5
        assert ConnectionType.INSECURE_LOCAL.value == 6
        assert ConnectionType.INSECURE_REMOTE.value == 7

    def test_transport_mode_enum_values(self):
        """Test _TransportMode enum has expected string values."""
        assert _TransportMode.INSECURE == "insecure"
        assert _TransportMode.UDS == "uds"
        assert _TransportMode.MTLS == "mtls"
        assert _TransportMode.WNUA == "wnua"

    def test_startup_argument_category_enum(self):
        """Test StartupArgumentCategory enum values."""
        assert StartupArgumentCategory.OLD_ARGUMENTS.value == 0
        assert StartupArgumentCategory.NEW_OR_OLD_ARGUMENTS.value == 1
        assert StartupArgumentCategory.NEW_ARGUMENTS.value == 2

    def test_connection_options_defaults(self):
        """Test _ConnectionOptions dataclass default values."""
        options = _ConnectionOptions()
        assert options.transport_mode == _TransportMode.INSECURE
        assert options.allow_remote_host is False
        assert options.port is None
        assert options.host == "127.0.0.1"
        assert options.certs_folder is None
        assert options.uds_service == "systemcoupling"
        assert options.uds_dir is None
        assert options.uds_id is None

    def test_connection_options_custom_values(self):
        """Test _ConnectionOptions with custom values."""
        options = _ConnectionOptions(
            transport_mode=_TransportMode.MTLS,
            allow_remote_host=True,
            port=8080,
            host="192.168.1.1",
            certs_folder="/path/to/certs",
            uds_service="custom_service",
            uds_dir="/tmp",
            uds_id="test_id",
        )
        assert options.transport_mode == _TransportMode.MTLS
        assert options.allow_remote_host is True
        assert options.port == 8080
        assert options.host == "192.168.1.1"
        assert options.certs_folder == "/path/to/certs"
        assert options.uds_service == "custom_service"
        assert options.uds_dir == "/tmp"
        assert options.uds_id == "test_id"


class TestUtilityFunctions:
    """Test standalone utility functions."""

    def test_grpc_argument_category_old_version(self):
        """Test categorization of old versions."""
        assert _grpc_argument_category((24, 1)) == StartupArgumentCategory.OLD_ARGUMENTS
        assert _grpc_argument_category((23, 2)) == StartupArgumentCategory.OLD_ARGUMENTS

    def test_grpc_argument_category_transitional_versions(self):
        """Test categorization of transitional versions."""
        assert (
            _grpc_argument_category((24, 2))
            == StartupArgumentCategory.NEW_OR_OLD_ARGUMENTS
        )
        assert (
            _grpc_argument_category((25, 1))
            == StartupArgumentCategory.NEW_OR_OLD_ARGUMENTS
        )
        assert (
            _grpc_argument_category((25, 2))
            == StartupArgumentCategory.NEW_OR_OLD_ARGUMENTS
        )

    def test_grpc_argument_category_new_versions(self):
        """Test categorization of new versions."""
        assert _grpc_argument_category((26, 1)) == StartupArgumentCategory.NEW_ARGUMENTS
        assert _grpc_argument_category((25, 3)) == StartupArgumentCategory.NEW_ARGUMENTS

    @patch("socket.socket")
    def test_find_port(self, mock_socket_class):
        """Test _find_port function with mocked socket."""
        mock_socket = Mock()
        mock_socket.getsockname.return_value = ("127.0.0.1", 8080)
        mock_socket_class.return_value.__enter__ = Mock(return_value=mock_socket)
        mock_socket_class.return_value.__exit__ = Mock(return_value=None)

        port = _find_port()

        assert port == 8080
        mock_socket.bind.assert_called_once_with(("", 0))
        mock_socket.getsockname.assert_called_once()


class TestStartupAndConnectionInfo:
    """Test the main StartupAndConnectionInfo class."""

    def setup_method(self):
        """Setup common mocks for each test."""
        # Common patches for all tests
        self.path_to_system_coupling_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.path_to_system_coupling"
        )
        self.normalize_version_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.normalize_version"
        )
        self.syc_version_concat_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.SYC_VERSION_CONCAT", "25.2"
        )
        self.create_channel_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.create_channel"
        )
        self.is_uds_supported_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.is_uds_supported"
        )
        self.determine_uds_folder_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.determine_uds_folder"
        )
        self.loopback_hosts_patcher = patch(
            "ansys.systemcoupling.core.client.grpc_transport.LOOPBACK_HOSTS",
            ["127.0.0.1", "localhost"],
        )

        # Start all patches
        self.mock_path_to_system_coupling = self.path_to_system_coupling_patcher.start()
        self.mock_normalize_version = self.normalize_version_patcher.start()
        self.mock_syc_version_concat = self.syc_version_concat_patcher.start()
        self.mock_create_channel = self.create_channel_patcher.start()
        self.mock_is_uds_supported = self.is_uds_supported_patcher.start()
        self.mock_determine_uds_folder = self.determine_uds_folder_patcher.start()
        self.mock_loopback_hosts = self.loopback_hosts_patcher.start()

        # Set common return values
        self.mock_path_to_system_coupling.return_value = (
            "/opt/ansys/v252/SystemCoupling/bin/systemcoupling"
        )
        self.mock_normalize_version.return_value = (25, 2)
        self.mock_is_uds_supported.return_value = True
        self.mock_determine_uds_folder.return_value = Path("/tmp/uds")
        self.mock_create_channel.return_value = Mock()

    def teardown_method(self):
        """Stop all patches."""
        self.path_to_system_coupling_patcher.stop()
        self.normalize_version_patcher.stop()
        self.syc_version_concat_patcher.stop()
        self.create_channel_patcher.stop()
        self.is_uds_supported_patcher.stop()
        self.determine_uds_folder_patcher.stop()
        self.loopback_hosts_patcher.stop()

    def test_init_launching_with_version(self):
        """Test initialization when launching with specific version."""
        info = StartupAndConnectionInfo(
            launching=True, connection_type=ConnectionType.SECURE_LOCAL, version="25.2"
        )

        assert (
            info.executable_path()
            == "/opt/ansys/v252/SystemCoupling/bin/systemcoupling"
        )
        self.mock_path_to_system_coupling.assert_called_once_with("25.2")
        self.mock_normalize_version.assert_called_once_with("25.2")

    def test_init_launching_without_version_extracts_from_path(self):
        """Test initialization when launching without version extracts version from path."""
        self.mock_path_to_system_coupling.return_value = (
            "/opt/ansys/v251/SystemCoupling/bin/systemcoupling"
        )
        self.mock_normalize_version.side_effect = [(25, 1)]

        info = StartupAndConnectionInfo(
            launching=True, connection_type=ConnectionType.SECURE_LOCAL
        )

        assert (
            info.executable_path()
            == "/opt/ansys/v251/SystemCoupling/bin/systemcoupling"
        )
        self.mock_path_to_system_coupling.assert_called_once_with("")
        # Should extract v251 from path and normalize it
        self.mock_normalize_version.assert_called_once_with("251")

    def test_init_launching_without_version_fallback_to_default(self):
        """Test initialization falls back to default version when path doesn't contain version."""
        self.mock_path_to_system_coupling.return_value = "/some/path/systemcoupling"

        info = StartupAndConnectionInfo(
            launching=True, connection_type=ConnectionType.SECURE_LOCAL
        )

        # Should fall back to SYC_VERSION_CONCAT
        self.mock_normalize_version.assert_called_once_with("25.2")

    def test_init_not_launching(self):
        """Test initialization when not launching uses provided or default version."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.SECURE_LOCAL, version="24.2"
        )

        assert info.executable_path() is None
        self.mock_path_to_system_coupling.assert_not_called()
        self.mock_normalize_version.assert_called_once_with("24.2")

    def test_startup_argument_category_property(self):
        """Test startup_argument_category property returns correct value."""
        self.mock_normalize_version.return_value = (25, 2)

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.SECURE_LOCAL
        )

        assert (
            info.startup_argument_category
            == StartupArgumentCategory.NEW_OR_OLD_ARGUMENTS
        )

    def test_is_insecure_connection_requested_true(self):
        """Test is_insecure_connection_requested returns True for insecure connections."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.INSECURE_LOCAL
        )

        assert info.is_insecure_connection_requested is True

    def test_is_insecure_connection_requested_false(self):
        """Test is_insecure_connection_requested returns False for secure connections."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.SECURE_LOCAL
        )

        assert info.is_insecure_connection_requested is False

    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_command_line_arguments_uds(self, mock_find_port):
        """Test command line arguments generation for UDS transport."""
        mock_find_port.return_value = 8080

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.UNIX_DOMAIN_SOCKETS
        )

        args = info.command_line_arguments()

        expected_args = [
            "--grpc",
            "--transport-mode=uds",
        ]
        # Check that the basic args are there (uds_id will be random)
        assert args[:2] == expected_args
        assert args[2].startswith("--uds-dir=")
        assert args[3].startswith("--uds-id=")

    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_command_line_arguments_wnua(self, mock_find_port):
        """Test command line arguments generation for WNUA transport."""
        mock_find_port.return_value = 8080

        with patch("ansys.systemcoupling.core.client.grpc_transport._IS_WINDOWS", True):
            info = StartupAndConnectionInfo(
                launching=False,
                connection_type=ConnectionType.WINDOWS_NAMED_USER_AUTHENTICATION,
            )

            args = info.command_line_arguments()

            expected_args = ["--grpc", "--transport-mode=wnua", "--port=8080"]
            assert args == expected_args

    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_command_line_arguments_mtls_local(self, mock_find_port):
        """Test command line arguments generation for mTLS local transport."""
        mock_find_port.return_value = 8080

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.MTLS_LOCAL
        )

        args = info.command_line_arguments()

        expected_args = [
            "--grpc",
            "--transport-mode=mtls",
            "--port=8080",
            "--certs-folder=certs",
        ]
        assert args == expected_args

    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_command_line_arguments_mtls_remote(self, mock_find_port):
        """Test command line arguments generation for mTLS remote transport."""
        mock_find_port.return_value = 8080

        info = StartupAndConnectionInfo(
            launching=False,
            connection_type=ConnectionType.MTLS_REMOTE,
            host="192.168.1.100",
        )

        args = info.command_line_arguments()

        expected_args = [
            "--grpc",
            "--transport-mode=mtls",
            "--port=8080",
            "--allow-remote-host",
            "--host=192.168.1.100",
            "--certs-folder=certs",
        ]
        assert args == expected_args

    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_command_line_arguments_insecure(self, mock_find_port):
        """Test command line arguments generation for insecure transport."""
        mock_find_port.return_value = 8080

        info = StartupAndConnectionInfo(
            launching=False,
            connection_type=ConnectionType.INSECURE_REMOTE,
            host="192.168.1.100",
        )

        args = info.command_line_arguments()

        expected_args = [
            "--grpc",
            "--transport-mode=insecure",
            "--port=8080",
            "--allow-remote-host",
            "--host=192.168.1.100",
        ]
        assert args == expected_args

    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_old_command_line_arguments(self, mock_find_port):
        """Test old format command line arguments generation."""
        mock_find_port.return_value = 8080
        self.mock_normalize_version.return_value = (24, 1)  # Old version

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.INSECURE_LOCAL
        )

        args = info.old_command_line_arguments()

        expected_args = ["--grpcport=127.0.0.1:8080"]
        assert args == expected_args

    def test_old_command_line_arguments_new_version_raises_error(self):
        """Test old command line arguments raises error for new versions."""
        self.mock_normalize_version.return_value = (26, 1)  # New version

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.INSECURE_LOCAL
        )

        with pytest.raises(
            RuntimeError, match="does not accept the old command line format"
        ):
            info.old_command_line_arguments()

    def test_old_command_line_arguments_secure_connection_raises_error(self):
        """Test old command line arguments raises error for secure connections."""
        self.mock_normalize_version.return_value = (24, 1)  # Old version

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.SECURE_LOCAL
        )

        with pytest.raises(
            RuntimeError, match="You must specify an insecure connection type"
        ):
            info.old_command_line_arguments()

    @patch("ansys.systemcoupling.core.client.grpc_transport.LOG")
    def test_get_server_channel(self, mock_log):
        """Test get_server_channel creates channel and logs appropriately."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.SECURE_LOCAL
        )

        channel = info.get_server_channel()

        # Verify channel was created and logging occurred
        mock_log.info.assert_called_once()
        self.mock_create_channel.assert_called_once()
        # The channel should be what create_channel returns
        assert channel == self.mock_create_channel.return_value

    @patch("ansys.systemcoupling.core.client.grpc_transport.LOG")
    @patch("ansys.systemcoupling.core.client.grpc_transport._find_port")
    def test_get_server_channel_insecure_warning(self, mock_find_port, mock_log):
        """Test get_server_channel logs warning for insecure connections."""
        mock_find_port.return_value = 8080

        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.INSECURE_LOCAL
        )

        channel = info.get_server_channel()

        # Verify warnings and channel creation
        mock_log.warning.assert_called_once()
        mock_log.info.assert_called_once()
        self.mock_create_channel.assert_called_once()
        assert channel is not None

    def test_secure_local_with_uds_when_supported(self):
        """Test SECURE_LOCAL chooses UDS when supported."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.SECURE_LOCAL
        )

        # With default setup (UDS supported), should use UDS
        assert info._options.transport_mode == _TransportMode.UDS

    def test_secure_local_fallback_to_wnua_when_uds_not_supported(self):
        """Test SECURE_LOCAL falls back to WNUA when UDS is truly not supported."""
        # Override the setup method's mocks to simulate UDS not supported
        with patch("ansys.systemcoupling.core.client.grpc_transport._IS_WINDOWS", True):
            # Override the instance method to return False for UDS support
            with patch.object(
                StartupAndConnectionInfo, "_is_uds_supported", return_value=False
            ):
                info = StartupAndConnectionInfo(
                    launching=False, connection_type=ConnectionType.SECURE_LOCAL
                )

                # Should use WNUA transport mode when UDS not supported on Windows
                assert info._options.transport_mode == _TransportMode.WNUA

    def test_uds_connection_with_explicit_uds_selection(self):
        """Test UDS connection works when explicitly requested and supported."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.UNIX_DOMAIN_SOCKETS
        )

        # Should use UDS transport mode when explicitly requested
        assert info._options.transport_mode == _TransportMode.UDS
        assert info._options.uds_id is not None  # Should auto-generate ID

    def test_uds_connection_raises_error_for_non_localhost(self):
        """Test UDS connection raises error for non-localhost host."""
        with pytest.raises(
            ValueError, match="UDS transport only supports localhost connections"
        ):
            StartupAndConnectionInfo(
                launching=False,
                connection_type=ConnectionType.UNIX_DOMAIN_SOCKETS,
                host="192.168.1.100",
            )

    def test_wnua_connection_raises_error_on_non_windows(self):
        """Test WNUA connection raises error on non-Windows platforms."""
        with patch(
            "ansys.systemcoupling.core.client.grpc_transport._IS_WINDOWS", False
        ):
            with pytest.raises(
                ValueError,
                match="Windows Named User Authentication.*only supported on Windows",
            ):
                StartupAndConnectionInfo(
                    launching=False,
                    connection_type=ConnectionType.WINDOWS_NAMED_USER_AUTHENTICATION,
                )

    def test_wnua_connection_raises_error_for_remote_host(self):
        """Test WNUA connection raises error for remote host."""
        with patch("ansys.systemcoupling.core.client.grpc_transport._IS_WINDOWS", True):
            with pytest.raises(
                ValueError, match="Remote host connections are not supported with WNUA"
            ):
                StartupAndConnectionInfo(
                    launching=False,
                    connection_type=ConnectionType.WINDOWS_NAMED_USER_AUTHENTICATION,
                    host="192.168.1.100",
                )

    def test_mtls_local_raises_error_for_remote_host(self):
        """Test MTLS_LOCAL raises error for remote host."""
        with pytest.raises(
            ValueError, match="Remote host connections are not supported.*MTLS_Local"
        ):
            StartupAndConnectionInfo(
                launching=False,
                connection_type=ConnectionType.MTLS_LOCAL,
                host="192.168.1.100",
            )

    def test_insecure_local_raises_error_for_remote_host(self):
        """Test INSECURE_LOCAL raises error for remote host."""
        with pytest.raises(
            ValueError,
            match="Remote host connections are not supported.*Insecure_Local",
        ):
            StartupAndConnectionInfo(
                launching=False,
                connection_type=ConnectionType.INSECURE_LOCAL,
                host="192.168.1.100",
            )

    @patch.dict(os.environ, {"ANSYS_GRPC_CERTIFICATES": "/env/certs"}, clear=True)
    def test_get_certs_folder_from_environment(self):
        """Test certs folder is read from environment variable."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.MTLS_LOCAL
        )

        assert info._options.certs_folder == "/env/certs"

    def test_get_certs_folder_explicit_override(self):
        """Test explicit certs folder overrides environment."""
        with patch.dict(
            os.environ, {"ANSYS_GRPC_CERTIFICATES": "/env/certs"}, clear=True
        ):
            info = StartupAndConnectionInfo(
                launching=False,
                connection_type=ConnectionType.MTLS_LOCAL,
                certs_folder="/explicit/certs",
            )

            assert info._options.certs_folder == "/explicit/certs"

    def test_uds_id_auto_generated_when_not_provided(self):
        """Test UDS ID is auto-generated when not provided."""
        info = StartupAndConnectionInfo(
            launching=False, connection_type=ConnectionType.UNIX_DOMAIN_SOCKETS
        )

        # Should have generated a UDS ID
        assert info._options.uds_id is not None
        assert len(info._options.uds_id) == 32  # UUID hex length

    def test_uds_id_preserved_when_provided(self):
        """Test UDS ID is preserved when explicitly provided."""
        custom_id = "my_custom_id"
        info = StartupAndConnectionInfo(
            launching=False,
            connection_type=ConnectionType.UNIX_DOMAIN_SOCKETS,
            uds_id=custom_id,
        )

        assert info._options.uds_id == custom_id

    def test_port_conversion_to_int(self):
        """Test port parameter is converted to integer."""
        info = StartupAndConnectionInfo(
            launching=False,
            connection_type=ConnectionType.INSECURE_LOCAL,
            port="8080",  # String port
        )

        assert info._options.port == 8080
        assert isinstance(info._options.port, int)
