# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

from unittest.mock import create_autospec

import ansys.platform.instancemanagement as pypim
import grpc

import ansys.systemcoupling.core as pysystemcoupling


def test_pim(monkeypatch, with_launching_container):
    # Launch the product "normally" - this will stand in for the container launched by PIM
    syc = pysystemcoupling.launch()

    # Create a mock PyPIM instance object representing the running product
    mock_instance = pypim.Instance(
        definition_name="definitions/fake-syc",
        name="instances/fake-syc",
        ready=True,
        status_message=None,
        services={"grpc": pypim.Service(uri=syc._grpc._channel_str, headers={})},
    )

    # Create a working gRPC channel to this product
    pim_channel = grpc.insecure_channel(syc._grpc._channel_str)

    # Mock the wait_for_ready method so that it immediately returns
    mock_instance.wait_for_ready = create_autospec(mock_instance.wait_for_ready)

    # Mock the `build_grpc_channel` to return the working channel
    mock_instance.build_grpc_channel = create_autospec(
        mock_instance.build_grpc_channel, return_value=pim_channel
    )

    # Mock the deletion method
    mock_instance.delete = create_autospec(mock_instance.delete)

    # Mock the PyPIM client so that on the "create_instance" call it returns the mock instance
    # Note: the host and port here will not be used.
    mock_client = pypim.Client(channel=grpc.insecure_channel("localhost:12345"))
    mock_client.create_instance = create_autospec(
        mock_client.create_instance, return_value=mock_instance
    )

    # Mock the general PyPIM connection and configuration check method to expose the mock client.
    mock_connect = create_autospec(pypim.connect, return_value=mock_client)
    mock_is_configured = create_autospec(pypim.is_configured, return_value=True)
    monkeypatch.setattr(pypim, "connect", mock_connect)
    monkeypatch.setattr(pypim, "is_configured", mock_is_configured)

    # This initial setup is faking all the necessary parts of PyPIM. From here,
    # calling the launch() method with no parameter is expected to
    # call only the mocks, which the test should now do:

    syc = pysystemcoupling.launch()
    # After this call, the test is ready to make all the assertions verifying
    # that the PyPIM workflow was applied:

    # Unlike Fluent and MAPDL, we only support "skip exit" as a backdoor for testing
    syc._grpc._skip_exit = True

    # The launch method checked if it was in a PyPIM environment
    assert mock_is_configured.called

    # It connected to PyPIM
    assert mock_connect.called

    # It created a remote instance through PyPIM
    mock_client.create_instance.assert_called_with(
        product_name="systemcoupling", product_version="latest"
    )

    # It waited for this instance to be ready
    assert mock_instance.wait_for_ready.called

    # It created an gRPC channel from this instance
    assert mock_instance.build_grpc_channel.called

    # It connected using the channel created by PyPIM
    assert syc._grpc._channel == pim_channel

    syc.exit()
    assert mock_instance.delete.called
