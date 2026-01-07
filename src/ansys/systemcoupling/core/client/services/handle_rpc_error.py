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

import ansys.api.systemcoupling.v0.error_pb2 as syc_error_pb2
import grpc
from grpc_status.rpc_status import from_call


def _error_details_msg(error_details: syc_error_pb2) -> str:
    return (
        f"Command or query execution failed with error: {error_details.exception_classname}"
        f"\n\nServer stacktrace:\n{error_details.stack_trace}"
    )


def _check_for_syc_exception(rpc_error):
    # grpc_status is not available in some server versions so
    # check for bespoke method of returning error details via
    # trailing metadata.
    meta = rpc_error.trailing_metadata()
    if meta is not None:
        for key, value in meta:
            if key == "syc-exception-bin":
                error_details = syc_error_pb2.ErrorDetails()
                error_details.ParseFromString(value)
                return _error_details_msg(error_details)
    return None


def handle_rpc_error(rpc_error: grpc.RpcError):
    msg = _check_for_syc_exception(rpc_error)
    if msg is not None:
        return msg

    status = from_call(rpc_error)
    if status is None:
        return "Command or query execution failed. No details available."

    msg = f"Command execution failed: {status.message} (code={status.code})"
    for detail in status.details:
        if detail.Is(syc_error_pb2.ErrorDetails.DESCRIPTOR):
            error_details = syc_error_pb2.ErrorDetails()
            detail.Unpack(error_details)
            msg += _error_details_msg(error_details)
    return msg
