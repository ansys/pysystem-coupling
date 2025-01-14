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

from dataclasses import dataclass
from enum import IntEnum
import queue
from typing import Protocol, Union

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    SeriesData,
    TimestepData,
)


class PlotterProtocol(Protocol):
    def set_metadata(self, metadata: InterfaceInfo): ...
    def set_timestep_data(self, timestep_data: TimestepData): ...
    def update_line_series(self, series_data: SeriesData): ...
    def close(self): ...


class MsgType(IntEnum):
    NO_DATA_AVAILABLE = 1
    END_OF_DATA = 2
    CLOSE_PLOT = 3
    METADATA = 4
    TIMESTEP_DATA = 5
    SERIES_DATA = 6


@dataclass
class Message:
    type: MsgType
    data: Union[InterfaceInfo, TimestepData, SeriesData, None] = None


class MessageDispatcher:
    def __init__(self):
        self._q = queue.Queue()

    def set_plotter(self, plotter: PlotterProtocol):
        self._plotter = plotter

    def put_msg(self, msg: Message):
        self._q.put(msg)

    def dispatch_messages(self):
        while True:
            try:
                msg: Message = self._q.get(timeout=0.001)
                msg_t = msg.type
                print(f"dispatch message of type: {msg.type.name}")
                if msg_t == MsgType.METADATA:
                    self._plotter.set_metadata(msg.data)
                elif msg_t == MsgType.TIMESTEP_DATA:
                    self._plotter.set_timestep_data(msg.data)
                elif msg_t == MsgType.SERIES_DATA:
                    self._plotter.update_line_series(msg.data)
                elif msg_t in (MsgType.END_OF_DATA, MsgType.NO_DATA_AVAILABLE):
                    return
                elif msg_t == MsgType.CLOSE_PLOT:
                    self._plotter.close()
            except queue.Empty:
                return
