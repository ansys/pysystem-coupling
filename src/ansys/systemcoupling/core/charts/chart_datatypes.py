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

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# Common intermediate metadata and data types for chart series information.
# All series are assumed to belong to an interface and a data transfer within the interface

# Idea is that data should be processed into this format from whatever raw source (CSV file,
# streamed data, etc.) and the actual charts will be built from this.


class SeriesType(Enum):
    CONVERGENCE = 1
    SUM = 2
    WEIGHTED_AVERAGE = 3


@dataclass
class TransferSeriesInfo:
    """Information about chart series data associated with a data transfer.

    The `data_index` fields are used by the data source processor to associate
    this information (likely obtained from heading or other metadata) with the
    correct data series. It indexes into the full list of series associated
    with a given interface.

    `line_suffixes` is either empty or contains the suffixes for
    component series of various types (real/imag and or x/y/z).
    It is assumed that such components can be found via the index
    information - i.e. that they will be contiguous from the
    specified index.
    """

    data_index: int
    series_type: SeriesType
    transfer_display_name: str
    disambiguation_index: int
    # Remainder for non-CONVERGENCE series only
    participant_display_name: Optional[str] = None
    line_suffixes: list[str] = field(default_factory=list)


@dataclass
class InterfaceInfo:
    name: str
    display_name: str = ""
    is_transient: bool = False
    transfer_info: list[TransferSeriesInfo] = field(default_factory=list)


@dataclass
class SeriesData:
    """Fundamentally, all series data is stored per iteration.

    Data during or at end of timestep is found by indexing into
    this data.
    """

    transfer_index: int  # Index into transfer_info of associated InterfaceInfo
    component_index: Optional[int] = None  # Component index if applicable

    start_index: int = 0  # Use when providing incremental data

    data: list[float] = field(default_factory=list)


@dataclass
class InterfaceSeriesData:
    """Container for all series data for given interface"""

    info: InterfaceInfo
    series: list[SeriesData] = field(default_factory=list)


@dataclass
class TimestepData:
    """Map iteration to timestep.

    Typically multiple iterations map to the same timestep index and time.

    """

    timestep: list[int] = field(default_factory=list)  # iter -> step index
    time: list[float] = field(default_factory=list)  # iter -> time
