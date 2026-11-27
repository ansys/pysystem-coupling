# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
"""Tests for cleanup of private UDS directories owned by launched clients."""

from unittest.mock import Mock, patch

import pytest

from ansys.systemcoupling.core.client.grpc_client import SycGrpc
from ansys.systemcoupling.core.client.grpc_transport import (
    ConnectionType,
    StartupArgumentCategory,
)


def test_startup_failure_stops_process_before_private_directory_cleanup():
    events = []
    private_directory = Mock()
    private_directory.close.side_effect = lambda: events.append("directory")
    process = Mock()
    process.end.side_effect = lambda: events.append("process")
    connection_info = Mock()
    connection_info.prepare_private_uds_directory.return_value = private_directory
    connection_info.startup_argument_category = StartupArgumentCategory.NEW_ARGUMENTS
    connection_info.is_insecure_connection_requested = False
    connection_info.command_line_arguments.return_value = ["--grpc"]
    connection_info.executable_path.return_value = "systemcoupling"

    client = SycGrpc()
    with (
        patch(
            "ansys.systemcoupling.core.client.grpc_client.StartupAndConnectionInfo",
            return_value=connection_info,
        ),
        patch(
            "ansys.systemcoupling.core.client.grpc_client.SycProcess",
            return_value=process,
        ),
        patch.object(client, "_connect", side_effect=RuntimeError("connect failed")),
    ):
        with pytest.raises(RuntimeError, match="connect failed"):
            client.start_and_connect(connection_type=ConnectionType.SECURE_LOCAL)

    assert events == ["process", "directory"]
    private_directory.close.assert_called_once()


def test_failed_process_stop_preserves_private_directory_until_retry():
    private_directory = Mock()
    process = Mock()
    process.end.side_effect = [False, True]
    connection_info = Mock()
    connection_info.prepare_private_uds_directory.return_value = private_directory
    connection_info.startup_argument_category = StartupArgumentCategory.NEW_ARGUMENTS
    connection_info.is_insecure_connection_requested = False
    connection_info.command_line_arguments.return_value = ["--grpc"]
    connection_info.executable_path.return_value = "systemcoupling"

    client = SycGrpc()
    with (
        patch(
            "ansys.systemcoupling.core.client.grpc_client.StartupAndConnectionInfo",
            return_value=connection_info,
        ),
        patch(
            "ansys.systemcoupling.core.client.grpc_client.SycProcess",
            return_value=process,
        ),
        patch.object(client, "_connect"),
    ):
        client.start_and_connect(connection_type=ConnectionType.SECURE_LOCAL)

    with pytest.raises(RuntimeError, match="did not stop"):
        client.exit()
    private_directory.close.assert_not_called()

    client.exit()
    private_directory.close.assert_called_once()


def test_transport_override_is_rejected_before_server_launch():
    private_directory = Mock()
    connection_info = Mock()
    connection_info.prepare_private_uds_directory.return_value = private_directory
    connection_info.validate_extra_args.side_effect = ValueError(
        "extra_args cannot override transport"
    )

    client = SycGrpc()
    with (
        patch(
            "ansys.systemcoupling.core.client.grpc_client.StartupAndConnectionInfo",
            return_value=connection_info,
        ),
        patch("ansys.systemcoupling.core.client.grpc_client.SycProcess") as process,
    ):
        with pytest.raises(ValueError, match="cannot override"):
            client.start_and_connect(
                connection_type=ConnectionType.SECURE_LOCAL,
                extra_args=["--transport-mode=insecure"],
            )

    process.assert_not_called()
    private_directory.close.assert_called_once()


def test_output_start_failure_stops_process_before_private_directory_cleanup():
    events = []
    private_directory = Mock()
    private_directory.close.side_effect = lambda: events.append("directory")
    process = Mock()
    process.end.side_effect = lambda: events.append("process") or True
    connection_info = Mock()
    connection_info.prepare_private_uds_directory.return_value = private_directory
    connection_info.startup_argument_category = StartupArgumentCategory.NEW_ARGUMENTS
    connection_info.is_insecure_connection_requested = False
    connection_info.command_line_arguments.return_value = ["--grpc"]
    connection_info.executable_path.return_value = "systemcoupling"

    client = SycGrpc()
    with (
        patch(
            "ansys.systemcoupling.core.client.grpc_client.StartupAndConnectionInfo",
            return_value=connection_info,
        ),
        patch(
            "ansys.systemcoupling.core.client.grpc_client.SycProcess",
            return_value=process,
        ),
        patch.object(client, "_connect"),
        patch.object(client, "start_output", side_effect=RuntimeError("stream failed")),
    ):
        with pytest.raises(RuntimeError, match="stream failed"):
            client.start_and_connect(
                connection_type=ConnectionType.SECURE_LOCAL, start_output=True
            )

    assert events == ["process", "directory"]
