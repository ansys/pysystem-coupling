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

import math
import sys
from typing import Callable, Optional

from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from ansys.systemcoupling.core.charts.chart_datatypes import (
    InterfaceInfo,
    SeriesData,
    TimestepData,
)
from ansys.systemcoupling.core.charts.plotdata_manager import PlotDataManager


# TODO: Only handles one interface at the moment! Generalise to multiple
class Plotter:
    def __init__(
        self, mgr: PlotDataManager, request_update: Optional[Callable[[], None]] = None
    ):
        self._mgr = mgr
        self._request_update = request_update

        self._fig: Figure = plt.figure()
        self._subplot_lines: list[list[Line2D]] = []
        self._subplot_limits_set: list[bool] = []
        self._metadata: Optional[InterfaceInfo] = None

        # Empty if not transient:
        self._times: list[float] = []  # Time value at each time step
        self._time_indexes: list[int] = []  # Iteration to take value at time i from

    def set_metadata(self, metadata: InterfaceInfo):
        self._metadata = metadata
        self._mgr.set_metadata(metadata)
        # We now have enough information to create the (empty) plots
        self._init_plots()

    def set_timestep_data(
        self, timestep_data: TimestepData
    ) -> tuple[list[float], list[int]]:
        if not timestep_data.timestep:
            return [], []

        if not self._metadata.is_transient:
            raise RuntimeError("Attempt to set timestep data on non-transient case")

        # NB: for dynamically updating case, should be possible to do partial update
        self._time_indexes = [0]
        curr_step = timestep_data.timestep[0]
        self._times = [None]
        for i, step in enumerate(timestep_data.timestep):
            time = timestep_data.time[i]
            if step == curr_step:
                # Still in the same step, update
                self._times[-1] = time
                self._time_indexes[-1] = i
            else:
                # new step
                self._times.append(time)
                self._time_indexes.append(i)
                curr_step = step

    def update_line_series(self, series_data: SeriesData):

        if not self._metadata:
            raise RuntimeError(
                "Attempt to add series data to plot before metadata provided."
            )

        trans = self._metadata.transfer_info[series_data.transfer_index]
        offset = (
            series_data.component_index
            if series_data.component_index is not None
            else 0
        )
        subplot_defn, subplot_line_index = self._mgr.subplot_for_data_index(
            self._metadata.name, trans.data_index + offset
        )

        subplot_line = self._subplot_lines[subplot_defn.index][subplot_line_index]

        x_curr, y_curr = subplot_line.get_data()

        # We don't assume that all provided series_data are fully up to
        # date with the latest iteration or timestep that pertains globally
        # over all plots.

        x_new = []
        y_new = []

        new_start_index = series_data.start_index
        new_data_len = new_start_index + len(series_data.data)

        if new_data_len == 0:
            return

        if self._times:
            # IMPORTANT: Assume that time data is updated ahead of any series data
            # This means that new_data_len - 1 should always be <= maximum known
            # time index.
            # _time_indexes[-1] is the latest known 0-based iteration index that belongs
            # to the latest timestep.

            for i, time_iter in enumerate(self._time_indexes):
                # Straight copy if not overlapping with new data yet
                if time_iter < new_start_index:
                    x_new.append(self._times[i])
                    y_new.append(y_curr[i])

                # Don't assume we have data yet for all known timesteps
                elif time_iter < new_data_len:
                    x_new.append(self._times[i])
                    y_new.append(series_data.data[time_iter - new_start_index])
        else:
            for i in range(new_data_len):
                if i < new_start_index:
                    x_new.append(x_curr[i])
                    y_new.append(y_curr[i])
                else:
                    x_new.append(i + 1)
                    y_new.append(series_data.data[i - new_start_index])

        self.update_limits(subplot_defn.index, subplot_defn.is_log_y, x_new, y_new)

        subplot_line.set_data(x_new, y_new)

    def update_limits(self, subplot_index, is_log_y, x_new, y_new):
        axes = self._fig.axes[subplot_index]

        are_limits_initialised = self._subplot_limits_set[subplot_index]

        old_xlim = (0, 0)
        old_ylim = None
        if are_limits_initialised:
            old_xlim = axes.get_xlim()
            old_ylim = axes.get_ylim()

        new_ylimits = (
            self._new_ylim_log(y_new, old_ylim)
            if is_log_y
            else self._new_ylim_lin(y_new, old_ylim)
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

        self._subplot_limits_set[subplot_index] = True

    def close(self):
        if self._fig:
            plt.close(self._fig)

    def _new_ylim_lin(self, ynew: list[float], old_lim: Optional[tuple[float, float]]):

        resize_tol = 0.02
        resize_delta = 0.1

        min_y = min(ynew)
        max_y = max(ynew)

        data_range = min_y if abs(max_y - min_y) < 1.0e-7 else max_y - min_y
        delta_limits = resize_delta * data_range

        if old_lim is None:
            # First update - force calculation
            old_l = min_y + 1
            old_u = max_y - 1
        else:
            new_l, new_u = old_l, old_u = old_lim

        if min_y < old_l + resize_tol * data_range:
            new_l = min_y - delta_limits
        if max_y > old_u - resize_tol * data_range:
            new_u = max_y + delta_limits

        return new_l, new_u

    def _new_ylim_log(self, ynew: list[float], old_lim: Optional[tuple[float, float]]):

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

    def show_plot(self, noblock=False):
        if noblock:
            plt.ion()
        plt.show()

    def show_animated(self):
        # NB: if using the wait_for_metadata() approach
        # supported by MessageDispatcher, do it here like
        # this (assume the wait function is stored as an
        # attribute):
        #
        # assert self._wait_for_metadata is not None
        # metadata = self._wait_for_metadata()
        # if metadata is not None:
        #     self.set_metadata(metadata)
        # else:
        #     return
        assert self._request_update is not None

        self.ani = FuncAnimation(
            self._fig,
            self._update_animation,
            # frames=x_axis_pts,
            save_count=sys.maxsize,
            # init_func=self._init_plots,
            blit=False,
            interval=200,
            repeat=False,
        )
        plt.show()

    def _update_animation(self, frame: int):
        # print("calling update animation")
        return self._request_update()

    def _init_plots(self):
        # plt.ion()
        nrow, ncol = self._mgr.get_layout()
        self._fig.subplots(nrow, ncol, gridspec_kw={"hspace": 0.5})
        subplot_defns = self._mgr.subplots
        if len(subplot_defns) % 2 == 1:
            self._fig.delaxes(self._fig.axes[-1])

        # Add labels and legends
        for axes, subplot_defn in zip(self._fig.axes, subplot_defns):
            axes.set_title(subplot_defn.title, fontsize=8)
            if subplot_defn.is_log_y:
                axes.set_yscale("log")
            axes.set_xlabel(subplot_defn.x_axis_label, fontsize=8)
            axes.set_ylabel(subplot_defn.y_axis_label, fontsize=8)
            lines = []
            for label in subplot_defn.y_labels:
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
