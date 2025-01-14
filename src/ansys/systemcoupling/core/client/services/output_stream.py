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

import ansys.api.systemcoupling.v0.output_stream_pb2 as output_stream_pb2
import ansys.api.systemcoupling.v0.output_stream_pb2_grpc as output_stream_pb2_grpc


class OutputStreamService:
    def __init__(self, channel):
        self.__stub = output_stream_pb2_grpc.OutputStreamStub(channel)
        self.__stream = None

    def begin_streaming(self):
        """Begins streaming combined standard output streams from
        System Coupling.

        Yields
        ------
        str
             A line of output.
        """
        request = output_stream_pb2.StdStreamRequest()
        self.__stream = self.__stub.BeginStdStreaming(request)

        while True:
            try:
                yield next(self.__stream)
            except:
                break

    def end_streaming(self):
        """Cancels streaming of System Coupling output streams."""
        if self.__stream and not self.__stream.cancelled():
            self.__stream.cancel()
            self.__stream = None
