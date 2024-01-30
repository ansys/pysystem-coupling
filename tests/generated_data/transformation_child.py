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


class transformation_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("option", "Option", "str"),
        ("angle", "Angle", "RealType"),
        ("axis", "Axis", "str"),
        ("vector", "Vector", "RealVectorType"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'transformation' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def angle(self) -> RealType:
        """'angle' property of 'transformation' object"""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: RealType):
        self.set_property_state("angle", value)

    @property
    def axis(self) -> str:
        """'axis' property of 'transformation' object"""
        return self.get_property_state("axis")

    @axis.setter
    def axis(self, value: str):
        self.set_property_state("axis", value)

    @property
    def vector(self) -> RealVectorType:
        """'vector' property of 'transformation' object"""
        return self.get_property_state("vector")

    @vector.setter
    def vector(self, value: RealVectorType):
        self.set_property_state("vector", value)
