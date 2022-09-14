#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class fluent_input(Group):
    """
    'fluent_input' child.
    """

    syc_name = "FluentInput"

    property_names_types = [
        ("option", "Option", "String"),
        ("case_file", "CaseFile", "String"),
        ("data_file", "DataFile", "String"),
        ("journal_file", "JournalFile", "String"),
    ]

    @property
    def option(self) -> String:
        """'option' property of 'execution_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def case_file(self) -> String:
        """'case_file' property of 'execution_control' object"""
        return self.get_property_state("case_file")

    @case_file.setter
    def case_file(self, value: String):
        self.set_property_state("case_file", value)

    @property
    def data_file(self) -> String:
        """'data_file' property of 'execution_control' object"""
        return self.get_property_state("data_file")

    @data_file.setter
    def data_file(self, value: String):
        self.set_property_state("data_file", value)

    @property
    def journal_file(self) -> String:
        """'journal_file' property of 'execution_control' object"""
        return self.get_property_state("journal_file")

    @journal_file.setter
    def journal_file(self, value: String):
        self.set_property_state("journal_file", value)
