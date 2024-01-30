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

#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .ascii_output import ascii_output
from .results import results


class output_control(Container):
    """
    'output_control' child.
    """

    syc_name = "OutputControl"

    child_names = ["results", "ascii_output"]

    results: results = results
    """
    results child of output_control.
    """
    ascii_output: ascii_output = ascii_output
    """
    ascii_output child of output_control.
    """
    property_names_types = [
        ("option", "Option", "str"),
        ("generate_csv_chart_output", "GenerateCSVChartOutput", "bool"),
        ("write_initial_snapshot", "WriteInitialSnapshot", "bool"),
        ("transcript_precision", "TranscriptPrecision", "int"),
        ("write_diagnostics", "WriteDiagnostics", "bool"),
        ("write_weights_matrix", "WriteWeightsMatrix", "bool"),
        ("write_residuals", "WriteResiduals", "bool"),
        ("output_frequency", "OutputFrequency", "int"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'setup_root' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def generate_csv_chart_output(self) -> bool:
        """'generate_csv_chart_output' property of 'setup_root' object"""
        return self.get_property_state("generate_csv_chart_output")

    @generate_csv_chart_output.setter
    def generate_csv_chart_output(self, value: bool):
        self.set_property_state("generate_csv_chart_output", value)

    @property
    def write_initial_snapshot(self) -> bool:
        """'write_initial_snapshot' property of 'setup_root' object"""
        return self.get_property_state("write_initial_snapshot")

    @write_initial_snapshot.setter
    def write_initial_snapshot(self, value: bool):
        self.set_property_state("write_initial_snapshot", value)

    @property
    def transcript_precision(self) -> int:
        """'transcript_precision' property of 'setup_root' object"""
        return self.get_property_state("transcript_precision")

    @transcript_precision.setter
    def transcript_precision(self, value: int):
        self.set_property_state("transcript_precision", value)

    @property
    def write_diagnostics(self) -> bool:
        """'write_diagnostics' property of 'setup_root' object"""
        return self.get_property_state("write_diagnostics")

    @write_diagnostics.setter
    def write_diagnostics(self, value: bool):
        self.set_property_state("write_diagnostics", value)

    @property
    def write_weights_matrix(self) -> bool:
        """'write_weights_matrix' property of 'setup_root' object"""
        return self.get_property_state("write_weights_matrix")

    @write_weights_matrix.setter
    def write_weights_matrix(self, value: bool):
        self.set_property_state("write_weights_matrix", value)

    @property
    def write_residuals(self) -> bool:
        """'write_residuals' property of 'setup_root' object"""
        return self.get_property_state("write_residuals")

    @write_residuals.setter
    def write_residuals(self, value: bool):
        self.set_property_state("write_residuals", value)

    @property
    def output_frequency(self) -> int:
        """'output_frequency' property of 'setup_root' object"""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: int):
        self.set_property_state("output_frequency", value)
