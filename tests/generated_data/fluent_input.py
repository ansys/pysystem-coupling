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


class fluent_input(Container):
    """
    'fluent_input' child.
    """

    syc_name = "FluentInput"

    property_names_types = [
        ("option", "Option", "str"),
        ("case_file", "CaseFile", "str"),
        ("data_file", "DataFile", "str"),
        ("journal_file", "JournalFile", "str"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'execution_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def case_file(self) -> str:
        """'case_file' property of 'execution_control' object"""
        return self.get_property_state("case_file")

    @case_file.setter
    def case_file(self, value: str):
        self.set_property_state("case_file", value)

    @property
    def data_file(self) -> str:
        """'data_file' property of 'execution_control' object"""
        return self.get_property_state("data_file")

    @data_file.setter
    def data_file(self, value: str):
        self.set_property_state("data_file", value)

    @property
    def journal_file(self) -> str:
        """'journal_file' property of 'execution_control' object"""
        return self.get_property_state("journal_file")

    @journal_file.setter
    def journal_file(self, value: str):
        self.set_property_state("journal_file", value)
