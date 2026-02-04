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

import math
import sys
from typing import Callable, Optional, Union

from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    SeriesData,
    TimestepBeginData,
    TimestepData,
    TimestepEndData,
)
from ansys.systemcoupling.core.charts.plotdefinition_manager import (
    PlotDefinitionManager,
    SubplotManager,
)
from ansys.systemcoupling.core.util.assertion import assert_

# from ansys.systemcoupling.core.util.logging import LOG


def _calc_new_ylimits_linear(
    ynew: list[float], old_lim: Optional[tuple[float, float]]
) -> tuple[float, float]:

    resize_factor = 0.1
    resize_tol = 0.01

    min_y = min(ynew)
    max_y = max(ynew)

    data_range = abs(max_y - min_y)
    if data_range == 0:
        # NB: min and max are equal - use the value to define the range
        if abs(min_y) > 0:
            delta_limits = abs(min_y) * resize_factor
        else:
            # Arbitrary value for now (will need to make sure it doesn't "stick")
            delta_limits = 1e-7
    else:
        delta_limits = data_range * resize_factor

    delta_tol = resize_tol * data_range
    force_tol = 2 * delta_tol + 1
    if old_lim is None:
        # Force calculation on first update
        old_l = min_y + force_tol
        old_u = max_y - force_tol
    else:
        new_l, new_u = old_l, old_u = old_lim
        # In the case where we guessed limits for zero data and now have
        # some non-zero data, need to adjust limits downwards if the actual
        # data range is significantly smaller than current limits range.
        old_delta = old_u - old_l
        if data_range < old_delta * resize_factor:
            # Force recalculation
            old_l = min_y + force_tol
            old_u = max_y - force_tol

    # Only extend the limits if we are getting close to the old ones
    if min_y < old_l + delta_tol:
        new_l = min_y - delta_limits
    if max_y > old_u - delta_tol:
        new_u = max_y + delta_limits

    return new_l, new_u


def _calc_new_ylimits_log(
    ynew: list[float], old_lim: Optional[tuple[float, float]]
) -> tuple[float, float]:

    min_y = min(ynew)
    max_y = max(ynew)

    if old_lim is not None:
        new_l, new_u = old_lim

    if old_lim is None or min_y < old_lim[0]:
        log_l = math.log10(min_y)
        exponent = math.floor(log_l)
        new_l = math.pow(10.0, exponent)
    if old_lim is None or max_y > old_lim[1]:
        log_u = math.log10(max_y)
        exponent = math.ceil(log_u)
        new_u = math.pow(10.0, exponent)
        # We do this in the GUI - is it needed?
        new_u *= 1.0 + 1.0e-7

    return new_l, new_u


def _update_xy_data(
    time_info: Optional[tuple[list[int], list[float]]],
    x_curr,  # ArrayLike
    y_curr,  # ArrayLike
    series_data: list[float],
    new_start_index: int,
    want_log: bool = False,
) -> tuple[Union[list[float], list[int]], list[float]]:

    if want_log:

        def logxy(msg):
            with open(f"xylog00.txt", "a") as f:
                f.write(msg + "\n")  # noqa: T201

        logxy(f"Called _update_xy_data with:\n")
        logxy(f"  series_data: {series_data}\n")
        logxy(f"  new_start_index: {new_start_index}\n")
        logxy(f"  time_info: {time_info if time_info else 'N/A'}\n")

    else:
        logxy = lambda msg: None

    new_total_data_len = new_start_index + len(series_data)
    x_new = []
    y_new = []
    if time_info:
        time_indexes, time_values = time_info
        # IMPORTANT: Assume that time data is updated ahead of any series data
        # This means that (new_data_len - 1) should always be <= maximum known
        # time index.
        # time_indexes[-1] is the latest known 0-based iteration index that belongs
        # to the latest timestep.

        # Loop over all known time steps and pick out the right data.
        # This is suboptimal because we have already done this for earlier time steps,
        # but it keeps the logic simple.
        for i, time_iter in enumerate(time_indexes):
            if time_iter == -1:
                # No end iteration known yet for this time step
                x_new.append(time_values[i])
                y_new.append(series_data[-1])
                logxy(
                    f"i = {i}, time_iter={time_iter}: Appending no end "
                    f"iteration data: x={x_new[-1]}, y={y_new[-1]}"
                )

            elif time_iter < new_start_index:
                # End of this timestep is before new data starts - just copy existing data
                x_new.append(time_values[i])
                y_new.append(y_curr[i])
                logxy(
                    f"i = {i}, time_iter={time_iter}: Appending "
                    f"straight copy data: x={x_new[-1]}, y={y_new[-1]}"
                )

            elif time_iter < new_total_data_len:
                # End of this timestep is within new data range - use new data
                x_new.append(time_values[i])
                y_new.append(series_data[time_iter - new_start_index])
                logxy(
                    f"i = {i}, time_iter={time_iter}: Appending "
                    f"new data: x={x_new[-1]}, y={y_new[-1]}"
                )
            else:
                # We don't have data for this time step yet
                pass

        logxy(f"Final x_new: {x_new}")
        logxy(f"Final y_new: {y_new}")
    else:
        for i in range(new_total_data_len):
            if i < new_start_index:
                x_new.append(x_curr[i])
                y_new.append(y_curr[i])
            else:
                x_new.append(i + 1)
                y_new.append(series_data[i - new_start_index])
    return (x_new, y_new)


class FigurePlotter:
    def __init__(
        self,
        plot_number: int,
        mgr: SubplotManager,
        metadata: InterfaceInfo | None = None,
        request_update: Optional[Callable[[], None]] = None,
    ):
        self._mgr = mgr
        self._request_update = request_update

        self._fig: Figure = plt.figure(plot_number)
        self._subplot_lines: list[list[Line2D]] = []
        self._subplot_limits_set: list[bool] = []
        self._metadata = metadata

        # Empty if not transient:
        self._times: list[float] = []  # Time value at each time step
        self._time_indexes: list[int] = []  # Iteration to take value at time i from

        if metadata:
            self._init_from_metadata()

        self._animation: FuncAnimation | None = None

    def set_metadata(self, metadata: InterfaceInfo):
        if self._metadata:
            raise RuntimeError("Attempt to set metadata more than once per figure.")

        self._metadata = metadata
        self._init_from_metadata()

    def _init_from_metadata(self):
        self._mgr.set_metadata(self._metadata)
        # We now have enough information to create the (empty) plots
        self._init_plots()
        self._fig.suptitle(f"Interface: {self._metadata.name}", fontsize=10)
        self._log("Initialized plots for interface: " + self._metadata.name)

    def _log(self, msg: str):
        with open(f"figure_plotter_log_{self._metadata.name}.txt", "a") as f:
            f.write(msg + "\n")  # noqa: T201

    def set_timestep_data(self, timestep_data: TimestepData):
        self._time_indexes, self._times = (
            timestep_data.last_iterations,
            timestep_data.times,
        )

    # NB: either use set_timestep_data or these two methods; do not mix.
    def set_timestep_begin_data(self, timestep_begin_data: TimestepBeginData):
        self._times.append(timestep_begin_data.time)
        # We don't have an end iteration for this time step.
        # Logic using self._time_indexes needs to account for this.
        self._time_indexes.append(-1)

    def set_timestep_end_data(self, timestep_end_data: TimestepEndData):
        # We can fill in the iteration for the last time step now
        self._time_indexes[-1] = timestep_end_data.iteration

    def update_line_series(self, series_data: SeriesData):
        """Update the line series determined by the provided ``series_data`` with the
        incremental data that it contains.

        The ``series_data`` contains the "start index" in the full series, the index
        to start writing the new data.
        """
        if not self._metadata:
            raise RuntimeError(
                "Attempt to add series data to plot before metadata provided."
            )

        subplot_defn, subplot_line_index = self._mgr.subplot_for_data_index(
            series_data.transfer_index
        )
        if subplot_defn is None:
            # This can happen if the list of plots being show is filtered.
            return

        subplot_line = self._subplot_lines[subplot_defn.index][subplot_line_index]

        # We don't assume that all provided series_data are fully up to
        # date with the latest iteration or timestep that pertains globally
        # over all plots.

        if len(series_data.data) == 0:
            return

        x_curr, y_curr = subplot_line.get_data()
        want_log = (
            self._metadata.name == "Interface-1"
            and subplot_defn.index == 0
            and subplot_line_index == 0
        )

        x_new, y_new = _update_xy_data(
            ((self._time_indexes, self._times) if self._times else None),
            x_curr,
            y_curr,
            series_data.data,
            series_data.start_index,
            want_log,  # TODO get rid of this!!!!
        )
        x_vals = ", ".join(f"{x}" for x in x_new)
        y_vals = ", ".join(f"{y}" for y in y_new)
        self._log(
            f"Updating subplot {subplot_defn.index} "
            f"series {subplot_line_index}:\n"
            f"  x: {x_vals}\n"
            f"  y: {y_vals}\n"
        )

        self._update_limits(subplot_defn.index, subplot_defn.is_log_y, x_new, y_new)
        subplot_line.set_data(x_new, y_new)

    def _update_limits(self, subplot_index, is_log_y, x_new, y_new):
        axes = self._fig.axes[subplot_index]

        are_limits_initialised = self._subplot_limits_set[subplot_index]

        old_xlim = (0, 0)
        old_ylim = None
        if are_limits_initialised:
            old_xlim = axes.get_xlim()
            old_ylim = axes.get_ylim()

        new_ylimits = (
            _calc_new_ylimits_log(y_new, old_ylim)
            if is_log_y
            else _calc_new_ylimits_linear(y_new, old_ylim)
        )

        new_xlimits = old_xlim
        if self._times:
            if x_new[-1] >= old_xlim[1] * 0.95:
                new_xlimits = (0.0, x_new[-1] * 1.1)
        else:
            if len(x_new) >= old_xlim[1] - 1:
                new_xlimits = (1, len(x_new) + 1)

        axes.set_xlim(new_xlimits)
        axes.set_ylim(new_ylimits)
        self._log(
            f"Updated limits for subplot {subplot_index}: "
            f"xlim={new_xlimits}, ylim={new_ylimits}"
        )

        self._subplot_limits_set[subplot_index] = True

    def close(self):
        if self._fig:
            plt.close(self._fig)

    def show_animated(self):
        assert_(self._request_update is not None)

        if self._animation is not None:
            return

        self._animation = FuncAnimation(
            self._fig,
            self._update_animation,
            save_count=sys.maxsize,
            blit=False,
            interval=200,
            repeat=False,
        )

    def _update_animation(self, frame: int):
        # LOG.debug("FigurePlotter updating animation frame: %s", frame)
        return self._request_update()

    def _init_plots(self):
        # plt.ion()
        nrow, ncol = self._mgr.get_layout()
        self._fig.subplots(nrow, ncol, gridspec_kw={"hspace": 0.5})
        subplot_defns = self._mgr.subplots
        if len(subplot_defns) != 1 and len(subplot_defns) % 2 == 1:
            self._fig.delaxes(self._fig.axes[-1])

        # Add labels and legends
        for axes, subplot_defn in zip(self._fig.axes, subplot_defns):
            axes.set_title(subplot_defn.title, fontsize=8)
            if subplot_defn.is_log_y:
                axes.set_yscale("log")
            axes.set_xlabel(subplot_defn.x_axis_label, fontsize=8)
            axes.set_ylabel(subplot_defn.y_axis_label, fontsize=8)
            lines = []
            for label in subplot_defn.series_labels:
                (ln,) = axes.plot([], [], label=label)
                lines.append(ln)
            axes.legend(fontsize=6)

            # Set arbitrary axes limits
            if self._metadata.is_transient:
                axes.set_xlim(0.0, 1.0)
            else:
                axes.set_xlim(1, 5)
            if subplot_defn.is_log_y:
                axes.set_ylim(1e-20, 1)
            else:
                axes.set_ylim(0, 1.0)

            # Keep hold of lines so that we can assign data when it's available
            self._subplot_lines.append(lines)
            # The limits on this subplot are essentially unset until we start getting data
            self._subplot_limits_set.append(False)


class Plotter:
    def __init__(
        self,
        mgr: PlotDefinitionManager,
        request_update: Optional[Callable[[], None]] = None,
    ):
        self._mgr = mgr
        self._request_update = request_update

        self._figures: list[FigurePlotter] = []
        self._interface_to_figure_index: dict[str, int] = {}

        self._is_transient: bool | None = None

        self._init_figures()

    def _init_figures(self):
        for ifig, intf_name in enumerate(self._mgr.interface_names):
            self._interface_to_figure_index[intf_name] = ifig
            self._figures.append(
                FigurePlotter(
                    ifig + 1,
                    self._mgr.subplot_mgr(intf_name),
                    request_update=self._request_update,
                )
            )

    def set_metadata(self, metadata: InterfaceInfo):
        if self._is_transient is None:
            self._is_transient = metadata.is_transient
        elif self._is_transient != metadata.is_transient:
            raise RuntimeError(
                "Attempt to set metadata with inconsistent transient setting."
            )

        ifig = self._fig_index(metadata.name)
        self._figures[ifig].set_metadata(metadata)

    def set_timestep_data(self, timestep_data: TimestepData):

        if timestep_data.times and not self._is_transient:
            raise RuntimeError("Attempt to set timestep data on non-transient case")

        for fig in self._figures:
            fig.set_timestep_data(timestep_data)

    def set_timestep_begin_data(self, timestep_begin_data: TimestepBeginData):

        if not self._is_transient:
            raise RuntimeError("Attempt to set timestep data on non-transient case")

        for fig in self._figures:
            fig.set_timestep_begin_data(timestep_begin_data)

    def set_timestep_end_data(self, timestep_end_data: TimestepEndData):

        if not self._is_transient:
            raise RuntimeError("Attempt to set timestep data on non-transient case")

        for fig in self._figures:
            fig.set_timestep_end_data(timestep_end_data)

    def update_line_series(self, series_data: SeriesData):
        """Update the line series determined by the provided ``series_data`` with the
        incremental data that it contains.

        The ``series_data`` contains the "start index" in the full series, the index
        to start writing the new data.
        """
        ifig = self._fig_index(series_data.interface_name)
        self._figures[ifig].update_line_series(series_data)

    def close(self):
        for fig in self._figures:
            fig.close()

    def show_plot(self, noblock=False):
        if noblock:
            with plt.ion():
                plt.show()
        else:
            plt.show()

    def show_animated(self):
        assert_(self._request_update is not None)

        for fig in self._figures:
            fig.show_animated()
        plt.show()

    def _fig_index(self, interface_name: str) -> int:
        if interface_name not in self._interface_to_figure_index:
            raise RuntimeError(
                f"Attempt to set or update plot data for unknown interface "
                f"'{interface_name}'."
            )
        return self._interface_to_figure_index[interface_name]
