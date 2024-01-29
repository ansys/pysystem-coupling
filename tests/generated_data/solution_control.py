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

from .available_ports import available_ports
from .get_parameter_options import get_parameter_options


class solution_control(Container):
    """
    'solution_control' child.
    """

    syc_name = "SolutionControl"

    child_names = ["available_ports"]

    available_ports: available_ports = available_ports
    """
    available_ports child of solution_control.
    """
    property_names_types = [
        ("duration_option", "DurationOption", "str"),
        ("end_time", "EndTime", "RealType"),
        ("number_of_steps", "NumberOfSteps", "int"),
        ("time_step_size", "TimeStepSize", "RealType"),
        ("minimum_iterations", "MinimumIterations", "int"),
        ("maximum_iterations", "MaximumIterations", "int"),
    ]

    @property
    def duration_option(self) -> str:
        """'duration_option' property of 'setup_root' object"""
        return self.get_property_state("duration_option")

    @duration_option.setter
    def duration_option(self, value: str):
        self.set_property_state("duration_option", value)

    @property
    def end_time(self) -> RealType:
        """'end_time' property of 'setup_root' object"""
        return self.get_property_state("end_time")

    @end_time.setter
    def end_time(self, value: RealType):
        self.set_property_state("end_time", value)

    @property
    def number_of_steps(self) -> int:
        """'number_of_steps' property of 'setup_root' object"""
        return self.get_property_state("number_of_steps")

    @number_of_steps.setter
    def number_of_steps(self, value: int):
        self.set_property_state("number_of_steps", value)

    @property
    def time_step_size(self) -> RealType:
        """'time_step_size' property of 'setup_root' object"""
        return self.get_property_state("time_step_size")

    @time_step_size.setter
    def time_step_size(self, value: RealType):
        self.set_property_state("time_step_size", value)

    @property
    def minimum_iterations(self) -> int:
        """'minimum_iterations' property of 'setup_root' object"""
        return self.get_property_state("minimum_iterations")

    @minimum_iterations.setter
    def minimum_iterations(self, value: int):
        self.set_property_state("minimum_iterations", value)

    @property
    def maximum_iterations(self) -> int:
        """'maximum_iterations' property of 'setup_root' object"""
        return self.get_property_state("maximum_iterations")

    @maximum_iterations.setter
    def maximum_iterations(self, value: int):
        self.set_property_state("maximum_iterations", value)

    command_names = ["get_parameter_options"]

    get_parameter_options: get_parameter_options = get_parameter_options
    """
    get_parameter_options command of solution_control.
    """
