# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
"""Tests that launched process shutdown reports whether termination completed."""

import subprocess
from unittest.mock import Mock, patch

from ansys.systemcoupling.core.client.syc_process import SycProcess


def make_process(process):
    syc_process = SycProcess.__new__(SycProcess)
    starter = Mock()
    starter.get_running_process.return_value = process
    syc_process._SycProcess__starter = starter
    return syc_process, starter


def test_end_reports_normal_process_exit():
    process = Mock()
    process.poll.return_value = None
    syc_process, _ = make_process(process)

    assert syc_process.end() is True
    process.wait.assert_called_once_with(5)


def test_end_waits_after_forcible_termination():
    process = Mock()
    process.poll.return_value = None
    process.wait.side_effect = [subprocess.TimeoutExpired("systemcoupling", 5), None]
    syc_process, _ = make_process(process)

    with patch(
        "ansys.systemcoupling.core.client.syc_process._kill_process_tree"
    ) as kill:
        assert syc_process.end() is True

    kill.assert_called_once_with(process.pid, timeout=0.5)
    assert process.wait.call_count == 2


def test_end_reports_process_that_survives_termination():
    process = Mock()
    process.poll.return_value = None
    process.wait.side_effect = subprocess.TimeoutExpired("systemcoupling", 5)
    syc_process, starter = make_process(process)

    with patch("ansys.systemcoupling.core.client.syc_process._kill_process_tree"):
        assert syc_process.end() is False

    assert syc_process._SycProcess__starter is starter
