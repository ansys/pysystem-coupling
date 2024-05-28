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

from dataclasses import dataclass
from enum import IntEnum
import queue
import time
from typing import Optional, Protocol, Union

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

    def wait_for_metadata(self) -> Optional[InterfaceInfo]:
        # Alternative approach - supports waiting for metadata and
        # initialising figure before creating the animation
        while True:
            try:
                msg: Message = self._q.get(timeout=0.001)
                msg_t = msg.type
                if msg_t == MsgType.METADATA:
                    return msg.data
                elif msg_t == MsgType.END_OF_DATA:
                    return None
            except queue.Empty:
                pass
            time.sleep(0.2)

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


if __name__ == "__main__":
    from pprint import pprint
    import threading

    from ansys.systemcoupling.core.charts.datasource_csv import DataSource
    from ansys.systemcoupling.core.charts.plotdefinition_manager import (
        DataTransferSpec,
        InterfaceSpec,
        PlotDefinitionManager,
        PlotSpec,
    )
    from ansys.systemcoupling.core.charts.plotter import Plotter

    # The very basic specification of what we want
    interface_list = [("Interface-1", "Interface-1", ["input", "input2"])]

    # The specification of what we want expanded into in a more structured form
    spec = PlotSpec()
    for interface_name, interface_disp_name, transfers in interface_list:
        intf_spec = InterfaceSpec(interface_name, interface_disp_name)
        spec.interfaces.append(intf_spec)
        for transfer in transfers:
            intf_spec.transfers.append(DataTransferSpec(transfer))
    spec.plot_time = False

    pprint(spec)
    input("...")

    # Conversion of specification into a matplotlib-compatible
    # description of a figure and "subplots"
    manager = PlotDefinitionManager(spec=spec)

    dispatcher = MessageDispatcher()
    plotter = Plotter(
        manager, dispatcher.dispatch_messages  # ,dispatcher.wait_for_metadata
    )
    dispatcher.set_plotter(plotter)

    data_source = DataSource(interface_name, "Interface-1.csv", dispatcher.put_msg)
    data_thread = threading.Thread(target=data_source.read_data)

    data_thread.start()

    plotter.show_animated()
    data_source.cancel()
    data_thread.join()

    input("...")
