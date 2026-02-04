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

from typing import Callable, Generator, Protocol

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    SeriesData,
    TimestepBeginData,
    TimestepData,
    TimestepEndData,
)
from ansys.systemcoupling.core.charts.message_dispatcher import (
    Message,
    MsgType,
)
from ansys.systemcoupling.core.util.logging import LOG


# This should be consistent with the gRPC ChartService methods
# but we don't want a direct dependency here.
class GrpcDataSourceProtocol(Protocol):
    def stream_chart_data(
        self,
    ) -> Generator[
        InterfaceInfo | SeriesData | TimestepBeginData | TimestepEndData, None, None
    ]: ...
    def cancel_stream(self) -> None: ...
    def get_chart_metadata(self) -> list[InterfaceInfo]: ...
    def get_chart_series_data(self) -> list[SeriesData]: ...
    def get_chart_timestep_data(self) -> TimestepData: ...


class LiveGrpcDataSource:
    def __init__(
        self,
        live_interface_names: list[str],
        grpc_data_source: GrpcDataSourceProtocol,
        put_msg: Callable[[InterfaceInfo | SeriesData | TimestepData], None],
    ):
        self._live_interface_names = live_interface_names
        self._grpc_data_source = grpc_data_source
        self._put_msg = put_msg

    def cancel(self):
        self._grpc_data_source.cancel_stream()

    def read_data(self):
        timestep_data = TimestepData()
        for data_event in self._grpc_data_source.stream_chart_data():
            LOG.debug(
                "LiveGrpcDataSource read_data received event: %s", type(data_event)
            )
            match data_event:
                case InterfaceInfo():
                    data_event: InterfaceInfo
                    if data_event.name in self._live_interface_names:
                        msg = Message(type=MsgType.METADATA, data=data_event)
                        self._put_msg(msg)
                case TimestepBeginData():
                    data_event: TimestepBeginData
                    msg = Message(type=MsgType.TIMESTEP_BEGIN_DATA, data=data_event)
                    self._put_msg(msg)
                case TimestepEndData():
                    data_event: TimestepEndData
                    msg = Message(type=MsgType.TIMESTEP_END_DATA, data=data_event)
                    self._put_msg(msg)
                case SeriesData():
                    data_event: SeriesData
                    if data_event.interface_name in self._live_interface_names:
                        msg = Message(type=MsgType.SERIES_DATA, data=data_event)
                        self._put_msg(msg)
                case _:
                    LOG.warning(
                        "LiveGrpcDataSource read_data received unknown event type: %s",
                        type(data_event),
                    )
                    break
        self._put_msg(Message(type=MsgType.END_OF_DATA))
        LOG.debug("LiveGrpcDataSource read_data stream loop exited.")
