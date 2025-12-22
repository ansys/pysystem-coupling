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

import threading

import pytest  # noqa: F401

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    SeriesData,
    TimestepData,
)
from ansys.systemcoupling.core.charts.message_dispatcher import (
    Message,
    MessageDispatcher,
    MsgType,
    PlotterProtocol,
)


class Plotter(PlotterProtocol):
    def __init__(self):
        self._record = []

    def set_metadata(self, metadata: InterfaceInfo):
        self._record.append(f"metadata: {metadata.name}")

    def set_timestep_data(self, timestep_data: TimestepData):
        self._record.append(f"timestep data: {len(timestep_data.timestep)}")

    def update_line_series(self, series_data: SeriesData):
        self._record.append(f"series data: {len(series_data.data)}")

    def close(self):
        self._record.append("close")


def test_message_dispatcher():

    dispatcher = MessageDispatcher()
    plotter = Plotter()
    dispatcher.set_plotter(plotter)

    thread = threading.Thread(target=dispatcher.dispatch_messages)
    thread.start()

    dispatcher.put_msg(Message(MsgType.METADATA, InterfaceInfo("interface-1")))
    dispatcher.put_msg(
        Message(
            MsgType.TIMESTEP_DATA,
            TimestepData(
                timestep=[1, 1, 1, 2, 2, 2], time=[0.1, 0.1, 0.1, 0.2, 0.2, 0.2]
            ),
        )
    )
    dispatcher.put_msg(
        Message(MsgType.SERIES_DATA, SeriesData("interface-1", 0, data=[0.1, 0.5]))
    )
    dispatcher.put_msg(
        Message(MsgType.SERIES_DATA, SeriesData("interface-1", 0, data=[0.1, 0.5, 0.8]))
    )
    dispatcher.put_msg(
        Message(MsgType.SERIES_DATA, SeriesData("interface-1", 0, data=[0.1]))
    )
    dispatcher.put_msg(Message(MsgType.CLOSE_PLOT))

    thread.join()

    assert plotter._record[0] == "metadata: interface-1"
    assert plotter._record[1] == "timestep data: 6"
    assert plotter._record[2] == "series data: 2"
    assert plotter._record[3] == "series data: 3"
    assert plotter._record[4] == "series data: 1"
    assert plotter._record[5] == "close"
