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

#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class region_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("topology", "Topology", "str"),
        ("input_variables", "InputVariables", "StringListType"),
        ("output_variables", "OutputVariables", "StringListType"),
        ("display_name", "DisplayName", "str"),
    ]

    @property
    def topology(self) -> str:
        """'topology' property of 'region' object"""
        return self.get_property_state("topology")

    @topology.setter
    def topology(self, value: str):
        self.set_property_state("topology", value)

    @property
    def input_variables(self) -> StringListType:
        """'input_variables' property of 'region' object"""
        return self.get_property_state("input_variables")

    @input_variables.setter
    def input_variables(self, value: StringListType):
        self.set_property_state("input_variables", value)

    @property
    def output_variables(self) -> StringListType:
        """'output_variables' property of 'region' object"""
        return self.get_property_state("output_variables")

    @output_variables.setter
    def output_variables(self, value: StringListType):
        self.set_property_state("output_variables", value)

    @property
    def display_name(self) -> str:
        """'display_name' property of 'region' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)
