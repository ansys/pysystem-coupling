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

from .dimensionality import dimensionality


class attribute_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    child_names = ["dimensionality"]

    dimensionality: dimensionality = dimensionality
    """
    dimensionality child of attribute_child.
    """
    property_names_types = [
        ("attribute_type", "AttributeType", "str"),
        ("real_value", "RealValue", "RealType"),
        ("integer_value", "IntegerValue", "int"),
    ]

    @property
    def attribute_type(self) -> str:
        """'attribute_type' property of 'attribute' object"""
        return self.get_property_state("attribute_type")

    @attribute_type.setter
    def attribute_type(self, value: str):
        self.set_property_state("attribute_type", value)

    @property
    def real_value(self) -> RealType:
        """'real_value' property of 'attribute' object"""
        return self.get_property_state("real_value")

    @real_value.setter
    def real_value(self, value: RealType):
        self.set_property_state("real_value", value)

    @property
    def integer_value(self) -> int:
        """'integer_value' property of 'attribute' object"""
        return self.get_property_state("integer_value")

    @integer_value.setter
    def integer_value(self, value: int):
        self.set_property_state("integer_value", value)
