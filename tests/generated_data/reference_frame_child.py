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

from .transformation import transformation


class reference_frame_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    child_names = ["transformation"]

    transformation: transformation = transformation
    """
    transformation child of reference_frame_child.
    """
    property_names_types = [
        ("option", "Option", "str"),
        ("parent_reference_frame", "ParentReferenceFrame", "str"),
        ("transformation_order", "TransformationOrder", "StringListType"),
        ("transformation_matrix", "TransformationMatrix", "RealListType"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'reference_frame' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def parent_reference_frame(self) -> str:
        """'parent_reference_frame' property of 'reference_frame' object"""
        return self.get_property_state("parent_reference_frame")

    @parent_reference_frame.setter
    def parent_reference_frame(self, value: str):
        self.set_property_state("parent_reference_frame", value)

    @property
    def transformation_order(self) -> StringListType:
        """'transformation_order' property of 'reference_frame' object"""
        return self.get_property_state("transformation_order")

    @transformation_order.setter
    def transformation_order(self, value: StringListType):
        self.set_property_state("transformation_order", value)

    @property
    def transformation_matrix(self) -> RealListType:
        """'transformation_matrix' property of 'reference_frame' object"""
        return self.get_property_state("transformation_matrix")

    @transformation_matrix.setter
    def transformation_matrix(self, value: RealListType):
        self.set_property_state("transformation_matrix", value)
