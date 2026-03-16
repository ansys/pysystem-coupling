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

from dataclasses import dataclass, field
from enum import Enum

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
    series_type : SeriesType
        The type of line series.
    transfer_display_name : str
        The display name of the data transfer. This is a primary identifier for data
        transfers because CSV data sources do not currently include information about
        the underlying data model names of data transfers.
    transfer_id : str
        The internal unique identifier of the data transfer. This could be the internal
        datamodel name. In the CSV case, the internal name cannot be determined from the
        data, so an ID based on the display name and an integer suffix is used.
    participant_display_name : str, optional
        The display name of the participant. This is required for transfer value series
        but not for convergence series.
    component_suffix: str, optional
        The suffix for this component series, if applicable. This is only needed for
        transfer value series that have multiple components, such as complex or vector
        values, and is otherwise None. Suffixes for complex components are "real" and
        "imag", and suffixes for vector components are "x", "y", and "z". A combination
        of complex and vector suffixes is possible, such as "y real" and "x imag".
    """

    series_type: SeriesType
    transfer_display_name: str
    transfer_id: str
    # Remainder for non-CONVERGENCE series only
    participant_display_name: str | None = None
    component_suffix: str | None = None


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
    interface_name: str
        The name of the interface this series is associated with.
    transfer_index : int
        Index of the ``TransferSeriesInfo`` metadata for this series within the
        ``InterfaceInfo`` for the interface this series is associated with.
    start_index : int, optional
        The starting iteration of the ``data`` field. This defaults to 0 and
        only needs to be set to a different value if incremental data, such
        as might arise during "live" update of plots, has become available.
    data : list[float]
        The series data. This is always indexed by iteration. Extract time
        step-based data by using a time step to iteration mapping.
    """

    interface_name: str
    transfer_index: int  # Index into transfer_info of associated InterfaceInfo
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
    """Mappings from time step to last iteration of timestep and time.

    This is more suited to bulk chart data queries where the complete
    data is available following the simulation. For live plotting, see
    TimestepBeginData and TimestepEndData for incremental updates.

    (Note: in the CSV case this data structure is currently also used
    with live plotting but this needs to be migrated to the other
    approach. In any case, only one of the two approaches should be used
    at a time.)

    Attributes
    ----------
    last_iterations : list[int]
        The last iteration index for each (zero-based) time step. Iterations are zero-based.
    times: list[float]
        Time values, indexed by (zero-based) time step.
    """

    last_iterations: list[int] = field(default_factory=list)  # step -> iteration
    times: list[float] = field(default_factory=list)  # step -> time


@dataclass
class TimestepBeginData:
    """Data pertaining to the beginning of a time step in a transient analysis.

    This is intended for use in live plotting to provide incremental timestep data
    as the simulation proceeds. See TimestepEndData for data at the end of a time
    step and TimestepData for the cumulative mapping of iterations to simulation time.

    Attributes
    ----------
    timestep : int
        The time step index.
    time : float
        The simulation time value at the beginning of the time step.
    """

    timestep: int
    time: float


@dataclass
class TimestepEndData:
    """Data pertaining to the end of a time step in a transient analysis.

    This is intended for use in live plotting to provide incremental timestep data
    as the simulation proceeds. See TimestepBeginData for data at the beginning of a
    time step and TimestepData for the cumulative mapping of iterations to time steps.

    Attributes
    ----------
    timestep : int
        The time step index.
    iteration : int
        The iteration index at the end of the time step.
    """

    timestep: int
    iteration: int
