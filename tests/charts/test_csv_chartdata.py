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

from io import StringIO

import pytest

from ansys.systemcoupling.core.charts.chart_datatypes import SeriesType
from ansys.systemcoupling.core.charts.csv_chartdata import (
    CsvChartDataReader,
    parse_csv_metadata,
)


@pytest.fixture
def data1():
    return """Iteration,Step,Time,Data Transfer Convergence (RMS Change in Target Value): Interface-1 - Temperature,Temperature (Weighted Average): Thermal,Temperature (Weighted Average): ANSYS Electronics Desktop,Data Transfer Convergence (RMS Change in Target Value): Interface-1 - heatrate,heatrate (Sum): ANSYS Electronics Desktop,heatrate (Sum): Thermal
1,1,0.11,1.0,42.0,42.0,1.0,84.0,84.0
2,1,0.11,1e-14,42.0,42.0,1e-14,84.0,84.0
3,2,0.2,1.0,42.0,42.0,1.0,84.0,84.0
4,2,0.2,1e-14,42.0,42.0,1e-14,84.0,84.0
5,3,0.31,1.0,42.0,42.0,1.0,84.0,84.0
6,3,0.31,1e-14,42.0,42.0,1e-14,84.0,84.0
7,4,0.4,1.0,42.0,42.0,1.0,84.0,84.0
8,4,0.4,1e-14,42.0,42.0,1e-14,84.0,84.0
"""  # noqa: E501


@pytest.fixture
def data2():
    return """Iteration,Step,Data Transfer Convergence (RMS Change in Target Value): Interface-1 - Temperature,Temperature (Weighted Average): Thermal,Temperature (Weighted Average): ANSYS Electronics Desktop,Data Transfer Convergence (RMS Change in Target Value): Interface-1 - heatrate,heatrate (Sum): ANSYS Electronics Desktop,heatrate (Sum): Thermal
1,1,1.0,42.0,42.0,1.0,84.0,84.0
2,1,1e-14,42.0,42.0,1e-14,84.0,84.0
3,1,1.0,42.0,42.0,1.0,84.0,84.0
"""  # noqa: E501


@pytest.fixture
def data3():
    return """Iteration,Step,Time,Data Transfer Convergence (RMS Change in Target Value): I1 - T,T (Weighted Average): P1,T (Weighted Average): P2,Data Transfer Convergence (RMS Change in Target Value): I1 - X,X (Sum): P2 x real,X (Sum): P2 x imag,X (Sum): P2 y real,X (Sum): P2 y imag,X (Sum): P2 z real,X (Sum): P2 z imag,X (Sum): P1 real,X (Sum): P1 imag
1,1,0.11,1.0,42.0,42.0,1.0,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
2,1,0.11,1e-14,42.0,42.0,1e-14,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
3,2,0.2,1.0,42.0,42.0,1.0,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
4,2,0.2,1e-14,42.0,42.0,1e-14,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
"""  # noqa: E501


@pytest.fixture
def data3_pt2():
    return """5,3,0.31,1.0,42.0,42.0,1.0,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
6,3,0.31,1e-14,42.0,42.0,1e-14,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
7,4,0.4,1.0,42.0,42.0,1.0,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
8,4,0.4,1e-14,42.0,42.0,1e-14,84.0,85.0,86.0,87.0,88.0,89.0,84.0,84.5
"""


@pytest.fixture
def data4():
    return """Iteration,Step,Data Transfer Convergence (RMS Change in Target Value): Interface-1 - input,input (Weighted Average): rootFind,input (Weighted Average): rootFind 2,Data Transfer Convergence (RMS Change in Target Value): Interface-1 - input,input (Weighted Average): rootFind 2,input (Weighted Average): rootFind
1,0,1.0,0.75,0.75,1.0,0.5,0.5
2,0,0.2222222222222196,0.9375,0.9375,0.5454545454545375,0.875,0.875
3,0,0.048780487804877544,0.984375,0.984375,0.10169491525423618,0.96875,0.96875
"""  # noqa: E501


def test_parse_header():
    header = (
        "Iteration,"
        "Step,"
        "Time,"
        "Data Transfer Convergence (RMS Change in Target Value): Intf-1 - input,"
        "input (Weighted Average): rootFind,"
        "input (Weighted Average): rootFind 2,"
        "Data Transfer Convergence (RMS Change in Target Value): Intf-1 - input2,"
        "input2 (Weighted Average): rootFind 2,"
        "input2 (Weighted Average): rootFind"
    )

    info = parse_csv_metadata("Intf-1", header.split(","))

    assert info.display_name == "Intf-1"
    assert info.is_transient
    assert len(info.transfer_info) == 6

    info0 = info.transfer_info[0]
    assert info0.transfer_display_name == "input"
    assert info0.series_type == SeriesType.CONVERGENCE
    assert info0.participant_display_name is None
    assert info0.data_index == 0
    assert info0.line_suffixes == []

    info1 = info.transfer_info[1]
    assert info1.transfer_display_name == "input"
    assert info1.series_type == SeriesType.WEIGHTED_AVERAGE
    assert info1.participant_display_name == "rootFind"
    assert info1.data_index == 1
    assert info1.line_suffixes == []

    info2 = info.transfer_info[2]
    assert info2.transfer_display_name == "input"
    assert info2.series_type == SeriesType.WEIGHTED_AVERAGE
    assert info2.participant_display_name == "rootFind 2"
    assert info2.data_index == 2
    assert info2.line_suffixes == []

    info3 = info.transfer_info[3]
    assert info3.transfer_display_name == "input2"
    assert info3.series_type == SeriesType.CONVERGENCE
    assert info3.participant_display_name is None
    assert info3.data_index == 3
    assert info3.line_suffixes == []

    info4 = info.transfer_info[4]
    assert info4.transfer_display_name == "input2"
    assert info4.series_type == SeriesType.WEIGHTED_AVERAGE
    assert info4.participant_display_name == "rootFind 2"
    assert info4.data_index == 4
    assert info4.line_suffixes == []

    info5 = info.transfer_info[5]
    assert info5.transfer_display_name == "input2"
    assert info5.series_type == SeriesType.WEIGHTED_AVERAGE
    assert info5.participant_display_name == "rootFind"
    assert info5.data_index == 5
    assert info5.line_suffixes == []


def test_parse_header_components():
    header = (
        "Iteration,"
        "Step,"
        "Time,"
        "Data Transfer Convergence (RMS Change in Target Value): Intf-1 - input,"
        "input (Sum): part1 x,"
        "input (Sum): part1 y,"
        "input (Sum): part1 z,"
        "input (Sum): part2 x,"
        "input (Sum): part2 y,"
        "input (Sum): part2 z,"
        "Data Transfer Convergence (RMS Change in Target Value): Intf-1 - input2,"
        "input2 (Sum): part2,"
        "input2 (Sum): part1"
    )

    info = parse_csv_metadata("Intf-1", header.split(","))

    assert info.display_name == "Intf-1"
    assert info.is_transient
    assert len(info.transfer_info) == 6

    info0 = info.transfer_info[0]
    assert info0.transfer_display_name == "input"
    assert info0.series_type == SeriesType.CONVERGENCE
    assert info0.participant_display_name is None
    assert info0.data_index == 0
    assert info0.line_suffixes == []

    info1 = info.transfer_info[1]
    assert info1.transfer_display_name == "input"
    assert info1.series_type == SeriesType.SUM
    assert info1.participant_display_name == "part1"
    assert info1.data_index == 1
    assert info1.line_suffixes == ["x", "y", "z"]

    info2 = info.transfer_info[2]
    assert info2.transfer_display_name == "input"
    assert info2.series_type == SeriesType.SUM
    assert info2.participant_display_name == "part2"
    assert info2.data_index == 4
    assert info2.line_suffixes == ["x", "y", "z"]

    info3 = info.transfer_info[3]
    assert info3.transfer_display_name == "input2"
    assert info3.series_type == SeriesType.CONVERGENCE
    assert info3.participant_display_name is None
    assert info3.data_index == 7
    assert info3.line_suffixes == []

    info4 = info.transfer_info[4]
    assert info4.transfer_display_name == "input2"
    assert info4.series_type == SeriesType.SUM
    assert info4.participant_display_name == "part2"
    assert info4.data_index == 8
    assert info4.line_suffixes == []

    info5 = info.transfer_info[5]
    assert info5.transfer_display_name == "input2"
    assert info5.series_type == SeriesType.SUM
    assert info5.participant_display_name == "part1"
    assert info5.data_index == 9
    assert info5.line_suffixes == []


def test_timestep(data1):

    sio = StringIO(data1)
    reader = CsvChartDataReader("intf1", sio)

    reader.read_metadata()
    assert reader.metadata.is_transient
    # pprint(reader.metadata)

    reader.read_new_data()
    assert reader.timestep_data.timestep == [
        1,
        1,
        2,
        2,
        3,
        3,
        4,
        4,
    ], f"{reader.timestep_data.timestep}"

    assert all(
        abs(
            reader.timestep_data.time[i]
            - (0.11, 0.11, 0.2, 0.2, 0.31, 0.31, 0.4, 0.4)[i]
        )
        < 1e-7
        for i in range(8)
    )


def test_isnt_transient(data2):

    sio = StringIO(data2)
    reader = CsvChartDataReader("intf2", sio)

    reader.read_metadata()
    assert not reader.metadata.is_transient
    # pprint(reader.metadata)


def test_incremental_read(data3, data3_pt2):
    sio = StringIO(data3)

    reader = CsvChartDataReader("intf3", sio)

    reader.read_metadata()
    assert reader.metadata.is_transient
    # pprint(reader.metadata)
    reader.read_new_data()
    # pprint(reader.data)
    assert (
        len(reader.data.series) == 12
    ), f"Actual number of series = {len(reader.data.series)}"
    assert (
        len(reader.data.series[0].data) == 4
    ), f"Actual length of series data = {len(reader.data.series[0].data)}"
    # pprint(reader.data)

    sio.write(data3_pt2)
    sio.seek(0)
    reader.read_new_data()
    assert (
        len(reader.data.series[0].data) == 8
    ), f"Actual length of series data = {len(reader.data.series[0].data)}"


def test_non_unique_transfer_name(data4):
    sio = StringIO(data4)
    reader = CsvChartDataReader("intf4", sio)
    reader.read_metadata()
    assert reader.metadata.transfer_info[0].transfer_display_name == "input"
