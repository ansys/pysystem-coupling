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

from .type import type


class results(Container):
    """
    'results' child.
    """

    syc_name = "Results"

    child_names = ["type"]

    type: type = type
    """
    type child of results.
    """
    property_names_types = [
        ("option", "Option", "str"),
        ("include_instances", "IncludeInstances", "str"),
        ("output_frequency", "OutputFrequency", "int"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'output_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def include_instances(self) -> str:
        """'include_instances' property of 'output_control' object"""
        return self.get_property_state("include_instances")

    @include_instances.setter
    def include_instances(self, value: str):
        self.set_property_state("include_instances", value)

    @property
    def output_frequency(self) -> int:
        """'output_frequency' property of 'output_control' object"""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: int):
        self.set_property_state("output_frequency", value)
