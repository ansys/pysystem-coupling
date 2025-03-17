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

# from dataclasses import dataclass, field
import csv
from typing import TextIO, Union

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    InterfaceSeriesData,
    SeriesData,
    SeriesType,
    TimestepData,
    TransferSeriesInfo,
)

HeaderList = list[str]
ChartData = list[list[float]]


class CsvReader:
    def __init__(self, file_or_filename: Union[str, TextIO]):
        self._file_or_filename = file_or_filename
        self._headers: HeaderList = []
        self._data: ChartData = []
        self._started = False

    def read_data(self) -> bool:
        try:
            if not self._started:
                self._read_data_initial()
                self._started = True
            else:
                self._read_data_incr()
                # print("incremental data read")
            return True  # File exists - haven't necessarily read anything yet
        except FileNotFoundError:
            # It is expected that the file is not necessarily immediately available
            print(f"Failed to open {self._file_or_filename}")
            return False
        except Exception as e:
            # Temporary - see if anything else goes wrong
            print(e)
            return False

    @property
    def headers(self) -> HeaderList:
        return self._headers

    @property
    def data(self) -> ChartData:
        return self._data

    def _read_data_initial(self):
        f = None
        try:
            f = self._get_file()
            reader = csv.reader(f)
            header = None
            for row in reader:
                if header is None:
                    header = row
                else:
                    self._append_row(row)
        finally:
            self._close_file(f)

        self._headers = header

    def _read_data_incr(self):
        f = None
        try:
            f = self._get_file()
            reader = csv.reader(f)
            nlines = len(self._data) + 1
            # TODO: try using seek/tell
            for i, row in enumerate(reader):
                if i < nlines:
                    continue
                self._append_row(row)
        finally:
            self._close_file(f)

    def _append_row(self, row_data: list[str]) -> None:
        self._data.append([float(f) for f in row_data])

    def _get_file(self) -> TextIO:
        if isinstance(self._file_or_filename, str):
            return open(self._file_or_filename, newline="")
        else:
            return self._file_or_filename

    def _close_file(self, f: TextIO):
        # Only close if we opened it ourself
        if f and isinstance(self._file_or_filename, str):
            f.close()


class CsvChartDataReader:
    """Reader of chart data and metadata from a single CSV file, which
    contains data for a single coupling interface.

    The metadata is derived from the column headings in the file.
    """

    def __init__(self, interface_name: str, csvfile: Union[str, TextIO]) -> None:
        self._interface_name = interface_name
        self._csv_reader = CsvReader(csvfile)
        self._metadata: InterfaceInfo = None
        self._data: InterfaceSeriesData = None
        self._timestep_data = TimestepData()

    def read_metadata(self) -> bool:
        if not self._csv_reader.read_data():
            return False
        self._metadata = parse_csv_metadata(
            self._interface_name, self._csv_reader.headers
        )
        self._init_data()
        return True

    @property
    def metadata(self) -> InterfaceInfo:
        return self._metadata

    @property
    def data(self) -> InterfaceSeriesData:
        return self._data

    @property
    def timestep_data(self) -> TimestepData:
        return self._timestep_data

    def read_new_data(self):
        self._csv_reader.read_data()
        self._process_curr_data()

    def _init_data(self):
        series_data_list: list[SeriesData] = []
        for i, trans_info in enumerate(self._metadata.transfer_info):
            if not trans_info.line_suffixes:
                series_data_list.append(SeriesData(transfer_index=i))
            else:
                for j in range(len(trans_info.line_suffixes)):
                    series_data_list.append(
                        SeriesData(transfer_index=i, component_index=j)
                    )
        self._data = InterfaceSeriesData(self._metadata, series=series_data_list)

    def _process_curr_data(self):
        raw_data = self._csv_reader.data
        last_data_len = len(self._data.series[0].data)

        has_time = self._metadata.is_transient
        for i in range(last_data_len, len(raw_data)):
            row = raw_data[i]
            self._timestep_data.timestep.append(round(row[1]))
            start_index = 2
            if has_time:
                self._timestep_data.time.append(row[2])
                start_index += 1
            for j in range(start_index, len(row)):
                self._data.series[j - start_index].data.append(row[j])


def _extract_transfer_value_type(header: str) -> str:
    for value_type in ("Sum", "Weighted Average"):
        if f" ({value_type}):" in header:
            return value_type
    return None


def _parse_header(header: str) -> tuple[SeriesType, str, str]:
    if header.startswith("Data Transfer Convergence (RMS Change in Target Value):"):
        ipfx = header.find(":")
        isep = header.find(" - ", ipfx)
        intf_disp_name = header[ipfx + 1 : isep].strip()
        trans_disp_name = header[isep + 3 :].strip()
        return SeriesType.CONVERGENCE, intf_disp_name, trans_disp_name
    elif value_type := _extract_transfer_value_type(header):
        trans_disp_name = header[: header.find(f"({value_type})")].strip()
        part_disp_name = header[header.find(":") + 1 :].strip()
        part_disp_name = _remove_suffix(part_disp_name)
        return (
            SeriesType.SUM if value_type == "Sum" else SeriesType.WEIGHTED_AVERAGE,
            part_disp_name,
            trans_disp_name,
        )
    raise ValueError(f"Invalid column header in CSV file: {header}")


def _remove_suffix(label: str) -> str:
    def remove_partial_suffix(str_in: str, suffixes: tuple[str]) -> str:
        for suffix in suffixes:
            suffix = f" {suffix}"
            if str_in.endswith(suffix):
                return str_in[: len(str_in) - len(suffix)]
        return str_in

    # Suffix has format "[ <x|y|z>][ <real|imag>]" so remove real/imag first
    label = remove_partial_suffix(label, ("real", "imag"))
    label = remove_partial_suffix(label, ("x", "y", "z"))
    return label


def _parse_suffix(header: str, part_disp_name: str) -> str:
    idx = header.find(f": {part_disp_name} ")
    if idx == -1:
        return ""
    return header[idx + len(part_disp_name) + 3 :].strip()


def parse_csv_metadata(interface_name: str, headers: list[str]) -> InterfaceInfo:
    intf_info = InterfaceInfo(name=interface_name)
    assert headers[0] == "Iteration"
    assert headers[1] == "Step"
    intf_info.is_transient = headers[2] == "Time"

    start_index = 3 if intf_info.is_transient else 2
    prev_part_name = ""

    transfer_disambig: dict[str, int] = {}
    for i in range(start_index, len(headers)):
        header = headers[i]
        data_index = i - start_index
        series_type, intf_or_part_disp_name, trans_disp_name = _parse_header(header)
        if series_type == SeriesType.CONVERGENCE:
            prev_part_name = ""

            # If there are no convergence headings, transfer_disambig will
            # remain unpopulated. In this case, assume for now that there
            # is no ambiguity. Although not strictly correct, this is a
            # reasonable assumption for the majority of cases.
            # TODO: look for alternative method to determine a
            # disambiguation index in the case of no convergence headers.
            # If this is not possible, look for a way to detect that
            # data transfers are ambiguous and raise an exception or
            # warn and skip plotting.

            if trans_disp_name in transfer_disambig:
                transfer_disambig[trans_disp_name] += 1
            else:
                transfer_disambig[trans_disp_name] = 0

            intf_disp_name = intf_or_part_disp_name
            if data_index == 0:
                assert intf_info.display_name == ""
                intf_info.display_name = intf_disp_name
            series_info = TransferSeriesInfo(
                data_index,
                series_type,
                transfer_display_name=trans_disp_name,
                # get(..., 0) for case where transfer_disambig empty (see note above)
                disambiguation_index=transfer_disambig.get(trans_disp_name, 0),
            )
            intf_info.transfer_info.append(series_info)
        else:
            part_disp_name = intf_or_part_disp_name
            suffix = _parse_suffix(header, part_disp_name)
            if suffix:
                if prev_part_name != part_disp_name:
                    # Start a new series info for a group of components
                    # Thus if there are 3 components, say, they will
                    # implicitly have data indexes, data_index, data_index+1,
                    # data_index+2, and the next TransferSeriesInfo will
                    # have index data_index+3.
                    intf_info.transfer_info.append(
                        TransferSeriesInfo(
                            data_index,
                            series_type,
                            transfer_display_name=trans_disp_name,
                            disambiguation_index=transfer_disambig.get(
                                trans_disp_name, 0
                            ),
                            participant_display_name=part_disp_name,
                            line_suffixes=[suffix],
                        )
                    )
                    prev_part_name = part_disp_name
                else:
                    # Append component info to current series info
                    intf_info.transfer_info[-1].line_suffixes.append(suffix)
            else:
                prev_part_name = ""
                intf_info.transfer_info.append(
                    TransferSeriesInfo(
                        data_index,
                        series_type,
                        transfer_display_name=trans_disp_name,
                        disambiguation_index=transfer_disambig.get(trans_disp_name, 0),
                        participant_display_name=part_disp_name,
                    )
                )
    return intf_info
