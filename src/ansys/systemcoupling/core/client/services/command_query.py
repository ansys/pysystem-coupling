# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

import ansys.api.systemcoupling.v0.command_pb2_grpc as command_pb2_grpc
import ansys.api.systemcoupling.v0.error_pb2 as syc_error_pb2
import grpc
from grpc_status.rpc_status import from_call


class CommandQueryService:
    def __init__(self, channel):
        self.__stub = command_pb2_grpc.CommandStub(channel)

    def execute_command(self, request):
        try:
            response, call = self.__stub.InvokeCommand.with_call(request)
            return response, call.trailing_metadata()
        except grpc.RpcError as rpc_error:
            status = from_call(rpc_error)
            msg = f"Command execution failed: {status.message} (code={status.code})"
            for detail in status.details:
                if detail.Is(syc_error_pb2.ErrorDetails.DESCRIPTOR):
                    info = syc_error_pb2.ErrorDetails()
                    detail.Unpack(info)
                    msg += (
                        f"\n\nServer exception details:\n"
                        f"{info.exception_classname}\n{info.stack_trace}"
                    )
            raise RuntimeError(msg) from None
