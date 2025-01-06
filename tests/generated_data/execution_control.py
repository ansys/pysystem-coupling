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

#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .fluent_input import fluent_input


class execution_control(Container):
    """
    'execution_control' child.
    """

    syc_name = "ExecutionControl"

    child_names = ["fluent_input"]

    fluent_input: fluent_input = fluent_input
    """
    fluent_input child of execution_control.
    """
    property_names_types = [
        ("option", "Option", "str"),
        ("working_directory", "WorkingDirectory", "str"),
        ("executable", "Executable", "str"),
        ("additional_arguments", "AdditionalArguments", "str"),
        ("parallel_fraction", "ParallelFraction", "RealType"),
        ("initial_input", "InitialInput", "str"),
        ("additional_restart_input_file", "AdditionalRestartInputFile", "str"),
        ("gui_mode", "GuiMode", "bool"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'child_object_type' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def working_directory(self) -> str:
        """'working_directory' property of 'child_object_type' object"""
        return self.get_property_state("working_directory")

    @working_directory.setter
    def working_directory(self, value: str):
        self.set_property_state("working_directory", value)

    @property
    def executable(self) -> str:
        """'executable' property of 'child_object_type' object"""
        return self.get_property_state("executable")

    @executable.setter
    def executable(self, value: str):
        self.set_property_state("executable", value)

    @property
    def additional_arguments(self) -> str:
        """'additional_arguments' property of 'child_object_type' object"""
        return self.get_property_state("additional_arguments")

    @additional_arguments.setter
    def additional_arguments(self, value: str):
        self.set_property_state("additional_arguments", value)

    @property
    def parallel_fraction(self) -> RealType:
        """'parallel_fraction' property of 'child_object_type' object"""
        return self.get_property_state("parallel_fraction")

    @parallel_fraction.setter
    def parallel_fraction(self, value: RealType):
        self.set_property_state("parallel_fraction", value)

    @property
    def initial_input(self) -> str:
        """'initial_input' property of 'child_object_type' object"""
        return self.get_property_state("initial_input")

    @initial_input.setter
    def initial_input(self, value: str):
        self.set_property_state("initial_input", value)

    @property
    def additional_restart_input_file(self) -> str:
        """'additional_restart_input_file' property of 'child_object_type' object"""
        return self.get_property_state("additional_restart_input_file")

    @additional_restart_input_file.setter
    def additional_restart_input_file(self, value: str):
        self.set_property_state("additional_restart_input_file", value)

    @property
    def gui_mode(self) -> bool:
        """'gui_mode' property of 'child_object_type' object"""
        return self.get_property_state("gui_mode")

    @gui_mode.setter
    def gui_mode(self, value: bool):
        self.set_property_state("gui_mode", value)
