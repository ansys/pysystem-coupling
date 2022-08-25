#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class fluent_input(Group):
    """
    Fluent input.
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
        """Type of solver input file(s) to be used for the Fluent run.

        Possible options:

        InitialCaseFile
            The default. A case file will be defined as a solver input for the
            coupled analysis run.

        InitialCaseAndDataFile
            A Fluent case file and data file will be defined as solver inputs
            for the coupled analysis run.

        JournalFile
            A journal file will be defined as the solver input for the coupled
            analysis run."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def case_file(self) -> String:
        """Set Fluent initial case file."""
        return self.get_property_state("case_file")

    @case_file.setter
    def case_file(self, value: String):
        self.set_property_state("case_file", value)

    @property
    def data_file(self) -> String:
        """Set Fluent initial data file."""
        return self.get_property_state("data_file")

    @data_file.setter
    def data_file(self, value: String):
        self.set_property_state("data_file", value)

    @property
    def journal_file(self) -> String:
        """Set Fluent journal file."""
        return self.get_property_state("journal_file")

    @journal_file.setter
    def journal_file(self, value: String):
        self.set_property_state("journal_file", value)
