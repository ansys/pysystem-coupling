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

import pytest

from ansys.systemcoupling.core.charts.plotter import (
    _calc_new_ylimits_linear,
    _calc_new_ylimits_log,
    _update_xy_data,
)


@pytest.mark.parametrize(
    "ynew, expected",
    [
        (
            [0.0],
            (-1e-7, 1e-7),
        ),
        (
            [0.5],
            (0.45, 0.55),
        ),
        ([0.0, 0.0], (-1e-7, 1e-7)),
        ([0.0, 1e-8], (-1e-9, 1.1e-8)),
        ([0.5, 0.5], (0.45, 0.55)),
        ([-0.1, 10.0], (-1.11, 11.01)),
        ([0.1, 0.5, 0.92], (0.018, 1.002)),
        ([0.0, 1.0], (-0.1, 1.1)),
        (
            [0.0, 1.0, 0.9],
            (-0.1, 1.1),
        ),
        (
            [0.0, 1.0, 0.9],
            (-0.1, 1.1),
        ),
    ],
)
def test_new_linear_limits_uninitialised(ynew, expected):

    new_limits = _calc_new_ylimits_linear(ynew=ynew, old_lim=None)
    assert new_limits == pytest.approx(expected)


@pytest.mark.parametrize(
    "old_limits, ynew, expected",
    [
        (
            (0.018, 1.002),
            [0.1, 0.5, 0.92],
            (0.018, 1.002),
        ),
        (
            (0.018, 1.002),
            [0.1, 0.5, 0.92, 1.1],
            (0.018, 1.2),
        ),
        (
            (-0.1, 1.1),
            [0.0, 1.0, 0.9],
            (-0.1, 1.1),
        ),
        (
            (-0.1, 1.1),
            [0.0, 1.0, 0.9, 1.05],
            (-0.1, 1.1),
        ),
        (
            (-0.1, 1.1),
            [0.0, 1.0, 0.9, 1.09],
            (-0.1, 1.199),
        ),
        (
            (0.0, 0.9),
            [1.0],
            (0.9, 1.1),
        ),
    ],
)
def test_new_linear_limits_initialised(old_limits, ynew, expected):

    new_limits = _calc_new_ylimits_linear(ynew=ynew, old_lim=old_limits)
    assert new_limits == pytest.approx(expected)


@pytest.mark.parametrize(
    "ynew, expected",
    [
        (
            [1e-5],
            (1e-5, 1e-5),
        ),
        (
            [1e-5, 1.1e-5],
            (1e-5, 1e-4),
        ),
        (
            [1e-5, 1.1e-5, 0.9e-5],
            (1e-6, 1e-4),
        ),
    ],
)
def test_new_log_limits_uninitialised(ynew, expected):

    new_limits = _calc_new_ylimits_log(ynew=ynew, old_lim=None)
    assert new_limits == pytest.approx(expected)


@pytest.mark.parametrize(
    "old_limits, ynew, expected",
    [
        (
            (1e-5, 1e-5),
            [1e-5, 1.1e-5],
            (1e-5, 1e-4),
        ),
        (
            (1e-5, 1e-5),
            [1e-5, 1.1e-5, 0.9e-5],
            (1e-6, 1e-4),
        ),
    ],
)
def test_new_log_limits_initialised(old_limits, ynew, expected):

    new_limits = _calc_new_ylimits_log(ynew=ynew, old_lim=old_limits)
    assert new_limits == pytest.approx(expected)


def test_update_xy_no_time():

    x_curr = [1, 2, 3, 4, 5]

    new_data = _update_xy_data(
        time_info=None,
        x_curr=x_curr,
        y_curr=[x * 0.1 for x in x_curr],
        series_data=[0.3, 0.4, 0.5],
        new_start_index=3,
    )

    assert new_data[0] == [1, 2, 3, 4, 5, 6]
    assert new_data[1] == pytest.approx([0.1, 0.2, 0.3, 0.3, 0.4, 0.5])


def test_update_xy_time():
    x_curr = [0.1 * i for i in range(1, 5)]
    y_curr = [x + 0.1 * x * x for x in x_curr]

    assert y_curr[0] == pytest.approx(0.101)
    assert y_curr[1] == pytest.approx(0.204)
    assert y_curr[2] == pytest.approx(0.309)
    assert y_curr[3] == pytest.approx(0.416)

    step_iter = [2, 5, 7, 10, 12, 13]
    step_time = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

    # Only write the "wanted" values in the end of timestep positions
    # Everything else is -1, with the aim of showing up any off by one type issues.
    series_data = [-1.0] * 5
    series_data[1] = 5.0
    series_data[3] = 5.5
    series_data[4] = 6.0

    new_data = _update_xy_data(
        time_info=(step_iter, step_time),
        x_curr=x_curr,
        y_curr=y_curr,
        series_data=series_data,
        new_start_index=9,
    )

    assert new_data[0] == pytest.approx([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    assert new_data[1][0] == pytest.approx(0.101)
    assert new_data[1][1] == pytest.approx(0.204)
    assert new_data[1][2] == pytest.approx(0.309)
    assert new_data[1][3] == pytest.approx(5.0)
    assert new_data[1][4] == pytest.approx(5.5)
    assert new_data[1][5] == pytest.approx(6.0)


def test_update_xy_time_live_incremental():

    x_curr = []
    y_curr = []

    new_start_index = 0
    iter = 0

    n_step = 5
    n_iter_per_step = 3
    step_size = 0.025

    step_iter = []
    times = []
    all_series_data = []

    for step in range(n_step):
        step_iter.append(-1)  # Placeholder for live incremental
        times.append(step_size * (step + 1))
        for i in range(n_iter_per_step):
            series_data = [0.1 * (iter + 1)]
            all_series_data += series_data
            new_data = _update_xy_data(
                time_info=(step_iter, times),
                x_curr=x_curr,
                y_curr=y_curr,
                series_data=series_data,
                new_start_index=new_start_index,
            )

            x_curr = new_data[0]
            y_curr = new_data[1]
            new_start_index += 1
            iter += 1
        # Update step_iter to final iteration of this time step
        # bearing in mind that iter has already been incremented
        step_iter[-1] = iter - 1

    print(f"step_iter: {step_iter}")
    print(f"all_series_data: {all_series_data}")
    assert x_curr == pytest.approx([0.025, 0.05, 0.075, 0.1, 0.125])
    assert y_curr == pytest.approx([0.3, 0.6, 0.9, 1.2, 1.5])
