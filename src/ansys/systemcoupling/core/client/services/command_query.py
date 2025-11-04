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

import ansys.api.systemcoupling.v0.command_pb2_grpc as command_pb2_grpc
import grpc

from ansys.systemcoupling.core.client.services.handle_rpc_error import handle_rpc_error


class CommandQueryService:
    def __init__(self, channel):
        self.__stub = command_pb2_grpc.CommandStub(channel)

    def execute_command(self, request):
        try:
            print("about to call execute_command")
            response, call = self.__stub.InvokeCommand.with_call(request)
            return response, call.trailing_metadata()
        except grpc.RpcError as rpc_error:
            print("caught rpc error")
            msg = handle_rpc_error(rpc_error)
            if "License check" in msg:
                import glob
                import os

                # Print out a recursive directory listing, indicating which entries are directories

                msg += "\n\nCurrent directory listing:\n"
                for root, dirs, files in os.walk("."):
                    msg += f"\nContents of directory: {root}\n"
                    for name in files:
                        msg += f" - {os.path.join(root, name)}\n"
                    for name in dirs:
                        msg += f" - {os.path.join(root, name)}/\n"

                # Look in current directory for files named licdebug.* and ansyscl*
                licdebug_files = glob.glob("licdebug.*")
                ansyscl_files = glob.glob("ansyscl*")
                if licdebug_files or ansyscl_files:
                    msg += "\n\nLicense debug files found in current directory:\n"
                    for f in licdebug_files + ansyscl_files:
                        # Print file contents to the console
                        msg += f"\nContents of {f}:\n"
                        with open(f, "r") as file:
                            msg += file.read()
                else:
                    msg += "\n\nNo license debug files found in current directory."
            raise RuntimeError(msg) from None
