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
