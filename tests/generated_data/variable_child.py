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

from .attribute import attribute


class variable_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    child_names = ["attribute"]

    attribute: attribute = attribute
    """
    attribute child of variable_child.
    """
    property_names_types = [
        ("quantity_type", "QuantityType", "str"),
        ("location", "Location", "str"),
        ("participant_display_name", "ParticipantDisplayName", "str"),
        ("display_name", "DisplayName", "str"),
        ("data_type", "DataType", "str"),
        ("real_initial_value", "RealInitialValue", "RealType"),
        ("integer_initial_value", "IntegerInitialValue", "int"),
        ("logical_initial_value", "LogicalInitialValue", "bool"),
        ("string_initial_value", "StringInitialValue", "str"),
        ("real_min", "RealMin", "RealType"),
        ("real_max", "RealMax", "RealType"),
        ("integer_min", "IntegerMin", "int"),
        ("integer_max", "IntegerMax", "int"),
        ("tensor_type", "TensorType", "str"),
        ("is_extensive", "IsExtensive", "bool"),
    ]

    @property
    def quantity_type(self) -> str:
        """'quantity_type' property of 'variable' object"""
        return self.get_property_state("quantity_type")

    @quantity_type.setter
    def quantity_type(self, value: str):
        self.set_property_state("quantity_type", value)

    @property
    def location(self) -> str:
        """'location' property of 'variable' object"""
        return self.get_property_state("location")

    @location.setter
    def location(self, value: str):
        self.set_property_state("location", value)

    @property
    def participant_display_name(self) -> str:
        """'participant_display_name' property of 'variable' object"""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: str):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> str:
        """'display_name' property of 'variable' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def data_type(self) -> str:
        """'data_type' property of 'variable' object"""
        return self.get_property_state("data_type")

    @data_type.setter
    def data_type(self, value: str):
        self.set_property_state("data_type", value)

    @property
    def real_initial_value(self) -> RealType:
        """'real_initial_value' property of 'variable' object"""
        return self.get_property_state("real_initial_value")

    @real_initial_value.setter
    def real_initial_value(self, value: RealType):
        self.set_property_state("real_initial_value", value)

    @property
    def integer_initial_value(self) -> int:
        """'integer_initial_value' property of 'variable' object"""
        return self.get_property_state("integer_initial_value")

    @integer_initial_value.setter
    def integer_initial_value(self, value: int):
        self.set_property_state("integer_initial_value", value)

    @property
    def logical_initial_value(self) -> bool:
        """'logical_initial_value' property of 'variable' object"""
        return self.get_property_state("logical_initial_value")

    @logical_initial_value.setter
    def logical_initial_value(self, value: bool):
        self.set_property_state("logical_initial_value", value)

    @property
    def string_initial_value(self) -> str:
        """'string_initial_value' property of 'variable' object"""
        return self.get_property_state("string_initial_value")

    @string_initial_value.setter
    def string_initial_value(self, value: str):
        self.set_property_state("string_initial_value", value)

    @property
    def real_min(self) -> RealType:
        """'real_min' property of 'variable' object"""
        return self.get_property_state("real_min")

    @real_min.setter
    def real_min(self, value: RealType):
        self.set_property_state("real_min", value)

    @property
    def real_max(self) -> RealType:
        """'real_max' property of 'variable' object"""
        return self.get_property_state("real_max")

    @real_max.setter
    def real_max(self, value: RealType):
        self.set_property_state("real_max", value)

    @property
    def integer_min(self) -> int:
        """'integer_min' property of 'variable' object"""
        return self.get_property_state("integer_min")

    @integer_min.setter
    def integer_min(self, value: int):
        self.set_property_state("integer_min", value)

    @property
    def integer_max(self) -> int:
        """'integer_max' property of 'variable' object"""
        return self.get_property_state("integer_max")

    @integer_max.setter
    def integer_max(self, value: int):
        self.set_property_state("integer_max", value)

    @property
    def tensor_type(self) -> str:
        """'tensor_type' property of 'variable' object"""
        return self.get_property_state("tensor_type")

    @tensor_type.setter
    def tensor_type(self, value: str):
        self.set_property_state("tensor_type", value)

    @property
    def is_extensive(self) -> bool:
        """'is_extensive' property of 'variable' object"""
        return self.get_property_state("is_extensive")

    @is_extensive.setter
    def is_extensive(self, value: bool):
        self.set_property_state("is_extensive", value)
