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

from ansys.systemcoupling.core.charts.csv_chartdata import parse_csv_metadata
from ansys.systemcoupling.core.charts.plotdefinition_manager import (
    DataTransferSpec,
    InterfaceSpec,
    PlotDefinitionManager,
    PlotSpec,
)


@pytest.fixture
def spec():
    transfers = [
        DataTransferSpec(
            display_name="trans1", show_convergence=True, show_transfer_values=True
        ),
        DataTransferSpec(
            display_name="trans2", show_convergence=True, show_transfer_values=True
        ),
    ]

    intf = InterfaceSpec(name="intf1", display_name="Intf-1", transfers=transfers)
    return PlotSpec([intf], plot_time=True)


@pytest.fixture
def metadata():
    headers = [
        "Iteration",
        "Step",
        "Time",
        "Data Transfer Convergence (RMS Change in Target Value): Intf-1 - trans1",
        "trans1 (Weighted Average): rootFind",
        "trans1 (Weighted Average): rootFind 2",
        "Data Transfer Convergence (RMS Change in Target Value): Intf-1 - trans2",
        "trans2 (Weighted Average): rootFind 2",
        "trans2 (Weighted Average): rootFind",
    ]
    return parse_csv_metadata("intf1", headers)


def test_init_from_spec(spec):

    pdm = PlotDefinitionManager(spec)

    assert len(pdm.subplots) == 3
    assert pdm.get_layout() == (2, 2)

    assert pdm.subplots[0].is_log_y
    assert not pdm.subplots[1].is_log_y
    assert not pdm.subplots[2].is_log_y

    assert pdm.subplots[0].title == "Data transfer convergence on Intf-1"
    assert pdm.subplots[0].y_axis_label == "RMS Change in target value"
    assert pdm.subplots[1].title == "Intf-1 - trans1 (<VALUETYPE>)"
    assert pdm.subplots[2].title == "Intf-1 - trans2 (<VALUETYPE>)"
    assert (
        pdm.subplots[0].x_axis_label
        == pdm.subplots[1].x_axis_label
        == pdm.subplots[2].x_axis_label
        == "Time"
    )

    for sp in pdm.subplots:
        assert sp.series_labels == []


def test_set_metadata(spec, metadata):
    pdm = PlotDefinitionManager(spec)
    pdm.set_metadata(metadata)

    assert len(pdm.subplots) == 3

    assert pdm.subplots[1].title == "Intf-1 - trans1 (Weighted Average)"
    assert pdm.subplots[2].title == "Intf-1 - trans2 (Weighted Average)"

    assert pdm.subplots[0].series_labels == ["trans1", "trans2"]
    assert pdm.subplots[1].series_labels == ["rootFind", "rootFind 2"]
    assert pdm.subplots[2].series_labels == ["rootFind 2", "rootFind"]
