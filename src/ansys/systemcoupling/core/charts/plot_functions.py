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
from typing import Callable, Generator, Protocol

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    InterfaceSeriesData,
    SeriesData,
    TimestepBeginData,
    TimestepData,
    TimestepEndData,
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


# This should be consistent with the gRPC ChartService methods
# but we don't want a direct dependency here.
class GrpcDataSourceProtocol(Protocol):
    def stream_chart_data(
        self,
    ) -> Generator[
        InterfaceInfo | SeriesData | TimestepBeginData | TimestepEndData, None, None
    ]: ...
    def get_chart_metadata(self) -> list[InterfaceInfo]: ...
    def get_chart_series_data(self) -> list[SeriesData]: ...
    def get_chart_timestep_data(self) -> TimestepData: ...


def _create_and_show_impl(
    spec: PlotSpec, readers: list[ChartDataReader], is_csv_source: bool = False
) -> Plotter:
    manager = PlotDefinitionManager(spec, is_csv_source=is_csv_source)
    plotter = Plotter(manager)

    for reader in readers:
        reader.read_metadata()
        plotter.set_metadata(reader.metadata)

    for ireader, reader in enumerate(readers):
        reader.read_new_data()
        data = reader.data

        # Each reader has own timestep data but they should be consistent
        # so we only use the first one.
        # This is an artifact of using the CSV files as the data source.
        # (A streaming data source would only have one timestep data.)
        if ireader == 0 and reader.metadata.is_transient:
            plotter.set_timestep_data(reader.timestep_data)

        for line_series in data.series:
            plotter.update_line_series(line_series)

    plotter.show_plot(noblock=True)
    return plotter


def create_and_show_plot_csv(spec: PlotSpec, csv_list: list[str]) -> Plotter:
    """Create and show a plot based on System Coupling CSV chart data."""
    if len(spec.interfaces) != len(csv_list):
        raise ValueError(
            "'csv_list' should have length equal to the number of interfaces"
        )
    readers = [
        CsvChartDataReader(intf.name, csvfile)
        for intf, csvfile in zip(spec.interfaces, csv_list)
    ]
    return _create_and_show_impl(spec, readers, is_csv_source=True)


def create_and_show_plot_grpc(
    spec: PlotSpec, grpc_source: GrpcDataSourceProtocol
) -> Plotter:
    """Create and show a plot based on System Coupling gRPC chart data."""

    # We need to implement the ChartDataReader protocol for the gRPC source.
    # _create_and_show_impl expects a list of readers, one per interface,
    # whereas the gRPC source provides a single source for all interfaces.

    # Need to filter all data to the interfaces in the spec
    active_interfaces = set(intf.name for intf in spec.interfaces)
    if not (
        metadata := [
            m
            for m in grpc_source.get_chart_metadata()
            if m.interface_name in active_interfaces
        ]
    ):
        # This is OK; we just won't have any data to plot.
        return

    data = [
        d
        for d in grpc_source.get_chart_series_data()
        if d.interface_name in active_interfaces
    ]

    timestep_data = (
        grpc_source.get_chart_timestep_data()
        if metadata and metadata[0].is_transient
        else None
    )

    # Adapt to ChartDataReader protocol
    readers = []

    class GrpcChartDataReader:
        def __init__(
            self,
            metadata: InterfaceInfo,
            data: SeriesData,
            timestep_data: TimestepData | None,
        ):
            self._metadata = metadata
            self._data = data
            self._timestep_data = timestep_data

        def read_metadata(self) -> bool:
            return len(self._metadata) > 0

        def read_new_data(self) -> None:
            return

        @property
        def metadata(self) -> InterfaceInfo:
            return self._metadata

        @property
        def data(self) -> InterfaceSeriesData:
            return self._data

        @property
        def timestep_data(self) -> TimestepData:
            return self._timestep_data

    for meta in metadata:
        series = next(
            (d for d in data if d.interface_name == meta.interface_name), None
        )
        readers.append(GrpcChartDataReader(meta, series, timestep_data))
    return _create_and_show_impl(spec, readers, is_csv_source=False)


def _solve_with_live_plot_impl(
    spec,
    make_live_data_source: Callable[[str, Callable], LiveDataSource],
    solve_func: Callable[[], None],
    is_csv_source: bool = False,
):
    manager = PlotDefinitionManager(spec, is_csv_source=is_csv_source)
    dispatcher = MessageDispatcher()
    plotter = Plotter(manager, request_update=dispatcher.dispatch_messages)
    dispatcher.set_plotter(plotter)

    data_source = make_live_data_source(
        [intf.name for intf in spec.interfaces], dispatcher.put_msg
    )
    data_thread = threading.Thread(target=data_source.read_data)

    def solve():
        solve_func()
        data_source.cancel()

    solve_thread = threading.Thread(target=solve)

    data_thread.start()
    solve_thread.start()

    plotter.show_animated()
    solve_thread.join()
    data_source.cancel()
    data_thread.join()


def solve_with_live_plot_csv(
    spec: PlotSpec,
    csv_list: list[str],
    solve_func: Callable[[], None],
):
    if len(spec.interfaces) != len(csv_list):
        raise ValueError(
            "'csv_list' should have length equal to the number of interfaces"
        )

    _solve_with_live_plot_impl(
        spec,
        lambda interface_names, put_msg: LiveCsvDataSource(
            interface_names, csv_list, put_msg
        ),
        solve_func,
        is_csv_source=True,
    )

    # Show a non-blocking static plot
    return create_and_show_plot_csv(spec, csv_list)
