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

import threading
from typing import Callable

from ansys.systemcoupling.core.charts.csv_chartdata import CsvChartDataReader
from ansys.systemcoupling.core.charts.datasource_csv import DataSource
from ansys.systemcoupling.core.charts.message_dispatcher import MessageDispatcher
from ansys.systemcoupling.core.charts.plotdefinition_manager import (
    DataTransferSpec,
    InterfaceSpec,
    PlotDefinitionManager,
    PlotSpec,
)
from ansys.systemcoupling.core.charts.plotter import Plotter


def make_plot_spec(
    is_transient: bool, interface_list: list[tuple[str, str, list[str]]]
) -> PlotSpec:
    # Expand the specification of what we want into in a more structured form
    spec = PlotSpec()
    for interface_name, interface_disp_name, transfers in interface_list:
        intf_spec = InterfaceSpec(interface_name, interface_disp_name)
        spec.interfaces.append(intf_spec)
        for transfer in transfers:
            intf_spec.transfers.append(DataTransferSpec(transfer))
    spec.plot_time = is_transient
    return spec


def make_plot_data_manager(
    is_transient: bool, interface_list: list[tuple[str, str, list[str]]]
) -> PlotDefinitionManager:
    spec = make_plot_spec(is_transient, interface_list)
    # pprint(spec)
    return PlotDefinitionManager(spec)


def create_and_show_plot(
    is_transient: bool,
    interface_list: list[tuple[str, str, list[str]]],
    csv_list: list[str],
):
    assert len(interface_list) == 1, "Plots currently only support one interface"
    assert len(interface_list) == len(csv_list)

    manager = make_plot_data_manager(is_transient, interface_list)
    reader = CsvChartDataReader(interface_list[0][0], csv_list[0])
    plotter = Plotter(manager)

    reader.read_metadata()
    plotter.set_metadata(reader.metadata)

    reader.read_new_data()
    data = reader.data
    if reader.metadata.is_transient:
        plotter.set_timestep_data(reader.timestep_data)

    for line_series in data.series:
        plotter.update_line_series(line_series)

    plotter.show_plot(noblock=True)
    return plotter


def solve_with_live_plot(
    is_transient: bool,
    interface_list: list[tuple[str, str, list[str]]],
    csv_list: list[str],
    solve_func: Callable[[], None],
):
    assert len(interface_list) == 1, "Plots currently only support one interface"
    assert len(interface_list) == len(csv_list)

    manager = make_plot_data_manager(is_transient, interface_list)
    dispatcher = MessageDispatcher()
    plotter = Plotter(manager, dispatcher.dispatch_messages)
    dispatcher.set_plotter(plotter)

    data_source = DataSource(interface_list[0][0], csv_list[0], dispatcher.put_msg)
    data_thread = threading.Thread(target=data_source.read_data)

    def solve():
        # print("solving...")
        solve_func()
        # print("sleeping after solve...")
        # time.sleep(30)
        # print("cancel live plot")
        data_source.cancel()

    solve_thread = threading.Thread(target=solve)

    data_thread.start()
    solve_thread.start()

    plotter.show_animated()
    data_source.cancel()
    data_thread.join()
    solve_thread.join()

    # Show a non-blocking static plot
    return create_and_show_plot(is_transient, interface_list, csv_list)


if __name__ == "__main__":

    # The very basic specification of what we want
    # interface_list = [("Interface-1", "Interface-1", ["input", "input2"])]
    # plotter = create_and_show_plot(False, interface_list, ["Interface-1.csv"])
    interface_list = [("Interface-1", "Interface-1", ["Force", "displacement"])]
    input("Create plot...")
    plotter = create_and_show_plot(True, interface_list, ["oscplt_csv/Interface-1.csv"])
    # plotter2 = create_and_show_plot(manager, reader)
    input("Quit?")
