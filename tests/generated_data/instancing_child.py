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


class instancing_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("reference_frame", "ReferenceFrame", "str"),
        ("instances_in_full_circle", "InstancesInFullCircle", "int"),
        ("instances_for_mapping", "InstancesForMapping", "int"),
    ]

    @property
    def reference_frame(self) -> str:
        """'reference_frame' property of 'instancing' object"""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: str):
        self.set_property_state("reference_frame", value)

    @property
    def instances_in_full_circle(self) -> int:
        """'instances_in_full_circle' property of 'instancing' object"""
        return self.get_property_state("instances_in_full_circle")

    @instances_in_full_circle.setter
    def instances_in_full_circle(self, value: int):
        self.set_property_state("instances_in_full_circle", value)

    @property
    def instances_for_mapping(self) -> int:
        """'instances_for_mapping' property of 'instancing' object"""
        return self.get_property_state("instances_for_mapping")

    @instances_for_mapping.setter
    def instances_for_mapping(self, value: int):
        self.set_property_state("instances_for_mapping", value)
