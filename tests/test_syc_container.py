# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

from unittest.mock import patch

from ansys.systemcoupling.core.client.syc_container import start_container


@patch("ansys.systemcoupling.core.client.syc_container.subprocess.run")
def test_start_container_gh_actions_261_uses_host_network(
    mock_subprocess_run,
):
    with patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}, clear=False):
        start_container(
            mounted_from=".",
            mounted_to="/working",
            network="",
            port=50051,
            version="v26.1.0",
        )

    run_args = mock_subprocess_run.call_args.args[0]

    assert "--network=host" in run_args
    assert "-p" not in run_args


@patch("ansys.systemcoupling.core.client.syc_container.LOG")
@patch("ansys.systemcoupling.core.client.syc_container.subprocess.run")
def test_start_container_ignores_custom_network_when_host_network_active(
    mock_subprocess_run,
    mock_log,
):
    with patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}, clear=False):
        start_container(
            mounted_from=".",
            mounted_to="/working",
            network="custom-net",
            port=50051,
            version="v26.1.0",
        )

    run_args = mock_subprocess_run.call_args.args[0]

    assert "--network=host" in run_args
    assert "--network" not in run_args
    mock_log.warning.assert_called_once_with(
        "Ignoring 'network' argument because --network=host is active."
    )


@patch("ansys.systemcoupling.core.client.syc_container.subprocess.run")
def test_start_container_applies_custom_network_when_port_mapping_active(
    mock_subprocess_run,
):
    with patch.dict("os.environ", {}, clear=True):
        start_container(
            mounted_from=".",
            mounted_to="/working",
            network="custom-net",
            port=50051,
            version="v24.1.0",
        )

    run_args = mock_subprocess_run.call_args.args[0]

    assert "-p" in run_args
    assert "50051:50051" in run_args
    assert "--network" in run_args
    network_idx = run_args.index("--network")
    assert run_args[network_idx + 1] == "custom-net"
