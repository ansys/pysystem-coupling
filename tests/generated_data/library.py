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

from .expression import expression
from .expression_function import expression_function
from .instancing import instancing
from .reference_frame import reference_frame


class library(Container):
    """
    'library' child.
    """

    syc_name = "Library"

    child_names = ["expression", "expression_function", "reference_frame", "instancing"]

    expression: expression = expression
    """
    expression child of library.
    """
    expression_function: expression_function = expression_function
    """
    expression_function child of library.
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of library.
    """
    instancing: instancing = instancing
    """
    instancing child of library.
    """
