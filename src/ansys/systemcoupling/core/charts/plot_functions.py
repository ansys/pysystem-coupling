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
from typing import Callable, Protocol

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    InterfaceSeriesData,
    TimestepData,
)
from ansys.systemcoupling.core.charts.csv_chartdata import CsvChartDataReader
from ansys.systemcoupling.core.charts.live_csv_datasource import LiveCsvDataSource
from ansys.systemcoupling.core.charts.message_dispatcher import MessageDispatcher
from ansys.systemcoupling.core.charts.plotdefinition_manager import (
    PlotDefinitionManager,
    PlotSpec,
)
from ansys.systemcoupling.core.charts.plotter import Plotter


class ChartDataReader(Protocol):
    def read_metadata(self) -> bool: ...
    def read_new_data(self) -> None: ...
    @property
    def metadata(self) -> InterfaceInfo: ...
    @property
    def data(self) -> InterfaceSeriesData: ...
    @property
    def timestep_data(self) -> TimestepData: ...


class LiveDataSource(Protocol):
    def cancel(self) -> None: ...
    def read_data(self) -> None: ...


def _make_csv_data_reader(interface_name: str) -> ChartDataReader:
    return CsvChartDataReader(interface_name)


def _create_and_show_impl(spec: PlotSpec, reader: ChartDataReader) -> Plotter:
    if len(spec.interfaces) != 1:
        raise ValueError("Plots currently only support one interface")

    manager = PlotDefinitionManager(spec)
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


def create_and_show_plot_csv(spec: PlotSpec, csv_list: list[str]) -> Plotter:
    """Create and show a plot based on System Coupling CSV chart data."""
    if len(spec.interfaces) != 1:
        raise ValueError("Plots currently only support one interface")
    if len(spec.interfaces) != len(csv_list):
        raise ValueError(
            "'csv_list' should have length equal to the number of interfaces"
        )
    reader = _make_csv_data_reader(spec.interfaces[0].name)
    return _create_and_show_impl(spec, reader)


def _solve_with_live_plot_impl(
    spec,
    make_live_data_source: Callable[[str, Callable], LiveDataSource],
    solve_func: Callable[[], None],
):
    if len(spec.interfaces) != 1:
        raise ValueError("Plots currently only support one interface")
    manager = PlotDefinitionManager(spec)
    dispatcher = MessageDispatcher()
    plotter = Plotter(manager, request_update=dispatcher.dispatch_messages)
    dispatcher.set_plotter(plotter)

    data_source = make_live_data_source(spec.interfaces[0].name, dispatcher.put_msg)
    data_thread = threading.Thread(target=data_source.read_data)

    def solve():
        solve_func()
        data_source.cancel()

    solve_thread = threading.Thread(target=solve)

    data_thread.start()
    solve_thread.start()

    plotter.show_animated()
    data_source.cancel()
    data_thread.join()
    solve_thread.join()


def solve_with_live_plot_csv(
    spec: PlotSpec,
    csv_list: list[str],
    solve_func: Callable[[], None],
):
    if len(spec.interfaces) != 1:
        raise ValueError("Plots currently only support one interface")
    if len(spec.interfaces) != len(csv_list):
        raise ValueError(
            "'csv_list' should have length equal to the number of interfaces"
        )

    _solve_with_live_plot_impl(
        spec,
        lambda interface_name, put_msg: LiveCsvDataSource(
            interface_name, csv_list[0], put_msg
        ),
        solve_func,
    )

    # Show a non-blocking static plot
    return create_and_show_plot_csv(spec, csv_list)
