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

import ansys.api.systemcoupling.v0.solution_pb2 as solution_pb2
import ansys.api.systemcoupling.v0.solution_pb2_grpc as solution_pb2_grpc
import grpc

from ansys.systemcoupling.core.client.services.handle_rpc_error import handle_rpc_error


class SolutionService:
    def __init__(self, channel):
        self.__stub = solution_pb2_grpc.SolutionStub(channel)

    def solve(self):
        request = solution_pb2.SolveRequest()
        try:
            print("about to call solve")
            self.__stub.Solve(request)
        except grpc.RpcError as rpc_error:
            print("caught rpc error")
            msg = handle_rpc_error(rpc_error)

            if "License check" in msg:
                import glob
                import os

                # Print out a directory listing
                msg += "\n\nCurrent directory listing:\n"
                for item in os.listdir("."):
                    msg += f" - {item}\n"

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

    def interrupt(self, reason):
        request = solution_pb2.InterruptRequest(reason=reason)
        self.__stub.Interrupt(request)

    def abort(self, reason):
        request = solution_pb2.AbortRequest(reason=reason)
        self.__stub.Abort(request)
