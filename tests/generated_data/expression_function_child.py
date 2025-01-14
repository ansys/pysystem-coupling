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


class expression_function_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("module", "Module", "str"),
        ("function", "Function", "str"),
        ("function_name", "FunctionName", "str"),
    ]

    @property
    def module(self) -> str:
        """'module' property of 'expression_function' object"""
        return self.get_property_state("module")

    @module.setter
    def module(self, value: str):
        self.set_property_state("module", value)

    @property
    def function(self) -> str:
        """'function' property of 'expression_function' object"""
        return self.get_property_state("function")

    @function.setter
    def function(self, value: str):
        self.set_property_state("function", value)

    @property
    def function_name(self) -> str:
        """'function_name' property of 'expression_function' object"""
        return self.get_property_state("function_name")

    @function_name.setter
    def function_name(self, value: str):
        self.set_property_state("function_name", value)
