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

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

"""Common data types for the storage of metadata and data for chart series.

All series are assumed to belong to an interface and to a data transfer within the interface

Raw data should be processed into this format from whatever source is available (CSV file
or streamed data, for example) and the actual charts will be built from this.
"""


class SeriesType(Enum):
    CONVERGENCE = 1
    SUM = 2
    WEIGHTED_AVERAGE = 3


@dataclass
class TransferSeriesInfo:
    """Information about the chart series data associated with a data transfer.

    Attributes
    ----------
    data_index : int
        This is used by the data source processor to associate this information (likely
        obtained from heading or other metadata) with the correct data series.
        It indexes into the full list of series associated with a given interface.
    series_type : SeriesType
        The type of line series.
    transfer_display_name : str
        The display name of the data transfer. This is a primary identifier for data
        transfers because CSV data sources do not currently include information about
        the underlying data model names of data transfers.
    disambiguation_index: int
        This should be set to 0, unless there is more than one data transfer with the
        same display name. A contiguous range of indexes starting at 0 should be assigned
        to the list of data transfers with the same display name.
    participant_display_name : str, optional
        The display name of the participant. This is required for transfer value series
        but not for convergence series.
    line_suffixes: list[str]
        This should always be empty for convergence series. For transfer value series,
        it should contain the suffixes for any component series that exist. That is,
        suffixes for complex components, "real" or "imag", and suffixes for vector
        components, "x", "y", "z", or a combination of complex and vector component
        types. The data indexes for individual components of the transfer are assumed
        to be contiguous from ``data_index``.
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
    """Information about the chart series data associated with a single interface.

    Attributes
    ----------
    name : str
        The name of the coupling interface data model object.
    display_name : str, optional
        The display name of the interface object. This may be unassigned initially.
    is_transient : bool
        Whether the data on this interface is associated with a transient analysis.
    transfer_info : list[TransferSeriesInfo]
        The list of ``TransferSeriesInfo`` associated with this interface.
    """

    name: str
    display_name: str = ""  # TODO: check whether this is actually needed.
    is_transient: bool = False
    transfer_info: list[TransferSeriesInfo] = field(default_factory=list)


@dataclass
class SeriesData:
    """The plot data for a single chart line series and information to allow
    it to be associated with chart metadata.

    An instance of this type is assumed to be associated externally with a
    single interface.

    Attributes
    ----------
    transfer_index : int
        Index of the ``TransferSeriesInfo`` metadata for this series within the
        ``InterfaceInfo`` for the interface this series is associated with.
    component_index : int, optional
        The component index if this series is one of a set of complex and/or
        vector components of the transfer. Otherwise is ``None``.
    start_index : int, optional
        The starting iteration of the ``data`` field. This defaults to 0 and
        only needs to be set to a different value if incremental data, such
        as might arise during "live" update of plots, has become available.
    data : list[float]
        The series data. This is always indexed by iteration. Extract time
        step-based data by using a time step to iteration mapping.
    """

    transfer_index: int  # Index into transfer_info of associated InterfaceInfo
    component_index: Optional[int] = None  # Component index if applicable

    start_index: int = 0  # Use when providing incremental data

    data: list[float] = field(default_factory=list)


@dataclass
class InterfaceSeriesData:
    """The series data for given interface.

    Attributes
    ----------
    info : InterfaceInfo
        The metadata for the interface.
    series : list[SeriesData]
        The data for all series associated with the interface.
    """

    info: InterfaceInfo
    series: list[SeriesData] = field(default_factory=list)


@dataclass
class TimestepData:
    """Mappings from iteration to time step and time.

    Attributes
    ----------
    timestep : list[int]
        Timestep indexes, indexed by iteration. Typically, multiple consecutive
        iteration indexes map to the same timestep index.
    time: list[float]
        Time values, indexed by iteration. Typically, multiple consecutive iteration
        indexes map to the same time value.
    """

    timestep: list[int] = field(default_factory=list)  # iter -> step index
    time: list[float] = field(default_factory=list)  # iter -> time
