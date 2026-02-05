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

from typing import Generator, Union

import ansys.api.systemcoupling.v0.chart_pb2 as chart_pb2
import ansys.api.systemcoupling.v0.chart_pb2_grpc as chart_pb2_grpc

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    SeriesData,
    SeriesType,
    TimestepBeginData,
    TimestepData,
    TimestepEndData,
    TransferSeriesInfo,
)


def _convert_series_type(proto_type: chart_pb2.TransferSeriesType) -> SeriesType:
    """Convert protobuf TransferSeriesType to native SeriesType enum."""
    return SeriesType(proto_type)


def _convert_transfer_series_info(
    proto_info: chart_pb2.TransferSeriesInfo,
) -> TransferSeriesInfo:
    """Convert protobuf TransferSeriesInfo to native TransferSeriesInfo dataclass."""
    return TransferSeriesInfo(
        series_type=_convert_series_type(proto_info.series_type),
        transfer_display_name=proto_info.transfer_name,
        transfer_id=proto_info.transfer_name,  # Using transfer_name as ID
        # TODO: the gRPC messages contain internal unique participant name and
        # not the display name. We can use this for now but we need to find a
        # way to get the display name later.
        participant_display_name=(
            proto_info.participant_name if proto_info.participant_name else None
        ),
        component_suffix=(
            proto_info.component_suffix if proto_info.component_suffix else None
        ),
    )


def _convert_interface_info(
    proto_metadata: chart_pb2.ChartMetadata,
) -> list[InterfaceInfo]:
    """Convert protobuf ChartMetadata to list of native InterfaceInfo dataclasses."""
    result = []
    for proto_interface in proto_metadata.interface_info:
        transfer_info = [
            _convert_transfer_series_info(transfer)
            for transfer in proto_interface.transfer_info
        ]
        interface_info = InterfaceInfo(
            name=proto_interface.interface_name,
            display_name=proto_interface.interface_name,  # Use name as display name
            is_transient=proto_metadata.is_transient,
            transfer_info=transfer_info,
        )
        result.append(interface_info)
    return result


def _convert_series_data(proto_series: chart_pb2.SeriesData) -> SeriesData:
    """Convert protobuf SeriesData to native SeriesData dataclass."""
    return SeriesData(
        interface_name=proto_series.interface_name,
        transfer_index=proto_series.transfer_series_index,
        start_index=proto_series.start_index,
        data=list(proto_series.data),
    )


def _convert_timestep_data(proto_timestep: chart_pb2.TimestepData) -> TimestepData:
    """Convert protobuf TimestepData to native TimestepData dataclass."""
    # Provided data has 1-based indexing; convert to 0-based.
    # TODO: Consider changing at the protobuf level instead.
    return TimestepData(
        last_iterations=[i - 1 for i in proto_timestep.timestep_to_iteration],
        times=list(proto_timestep.time_values),
    )


def _convert_timestep_begin_data(
    proto_timestep_begin: chart_pb2.TimestepStart,
) -> TimestepBeginData:
    """Convert protobuf TimestepBeginData to native TimestepBeginData dataclass."""
    return TimestepBeginData(
        timestep=proto_timestep_begin.timestep_count,
        time=proto_timestep_begin.time,
    )


def _convert_timestep_end_data(
    proto_timestep_end: chart_pb2.TimestepEnd,
) -> TimestepEndData:
    """Convert protobuf TimestepEndData to native TimestepEndData dataclass."""
    return TimestepEndData(
        timestep=proto_timestep_end.timestep_count,
        iteration=proto_timestep_end.iteration_count - 1,
    )


def _convert_all_series_data(
    proto_all_series: chart_pb2.AllSeriesData,
) -> list[SeriesData]:
    """Convert protobuf AllSeriesData to list of native SeriesData dataclasses."""
    result = []
    for proto_series in proto_all_series.series_data:
        series_data = _convert_series_data(proto_series)
        result.append(series_data)
    return result


class ChartService:
    """Client for interacting with System Coupling chart data via gRPC.

    For convenience and encapsulation, gRPC data types are converted to
    the native datatypes defined in
    `ansys.systemcoupling.core.charts.chart_datatypes`.
    """

    def __init__(self, channel):
        self.__stub = chart_pb2_grpc.ChartDataStub(channel)
        self.__chart_stream = None

    def _stream_chart_data(self) -> Generator[chart_pb2.ChartDataEvent, None, None]:
        """Streams chart data events from System Coupling."""
        request = chart_pb2.ChartDataRequest()
        self.__chart_stream = self.__stub.StreamChartData(request)
        for chart_event in self.__chart_stream:
            yield chart_event

    def stream_chart_data(
        self,
    ) -> Generator[
        Union[InterfaceInfo, SeriesData, TimestepBeginData, TimestepEndData], None, None
    ]:
        """Streams chart data events from System Coupling and converts them to
        appropriate datatypes.

        Note: Only metadata and series_data events are yielded as converted objects.
        Timestep start/end events are handled internally but not yielded.
        """
        if self.__chart_stream is not None:
            raise RuntimeError("Chart data stream is already active.")

        try:
            for chart_event in self._stream_chart_data():
                match chart_event.WhichOneof("event_data"):
                    case "metadata":
                        # Convert metadata and yield each interface info
                        interface_infos = _convert_interface_info(chart_event.metadata)
                        for interface_info in interface_infos:
                            yield interface_info
                    case "series_data":
                        yield _convert_series_data(chart_event.series_data)
                    case "timestep_start":
                        yield _convert_timestep_begin_data(chart_event.timestep_start)
                    case "timestep_end":
                        yield _convert_timestep_end_data(chart_event.timestep_end)
        finally:
            self.__chart_stream = None

    def cancel_stream(self) -> None:
        """Cancels the active chart data stream."""
        if self.__chart_stream is not None:
            self.__chart_stream.cancel()
            self.__chart_stream = None

    def get_chart_metadata(self) -> list[InterfaceInfo]:
        """Retrieves the chart metadata for all available series."""
        request = chart_pb2.ChartMetadataRequest()
        return _convert_interface_info(self.__stub.GetChartMetadata(request))

    def get_chart_series_data(self) -> list[SeriesData]:
        """Retrieves all chart series data."""
        request = chart_pb2.ChartSeriesDataRequest()
        return _convert_all_series_data(self.__stub.GetChartSeriesData(request))

    def get_chart_timestep_data(self) -> TimestepData:
        """Retrieves all chart timestep data."""
        request = chart_pb2.ChartTimestepDataRequest()
        return _convert_timestep_data(self.__stub.GetChartTimestepData(request))
