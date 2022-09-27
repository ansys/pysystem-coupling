#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class fluent_input(Container):
    """
    Fluent input.
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
        """Type of solver input file(s) to be used for the Fluent run.

        Allowed values:

        - \"InitialCaseFile\" - (Default) A case file will be defined as a
          solver input for the coupled analysis run.

        - \"InitialCaseAndDataFile\" - A Fluent case file and data file
          will be defined as solver inputs for the coupled analysis run.

        - \"JournalFile\" - A journal file will be defined as the solver
          input for the coupled analysis run."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def case_file(self) -> str:
        """Set Fluent initial case file."""
        return self.get_property_state("case_file")

    @case_file.setter
    def case_file(self, value: str):
        self.set_property_state("case_file", value)

    @property
    def data_file(self) -> str:
        """Set Fluent initial data file."""
        return self.get_property_state("data_file")

    @data_file.setter
    def data_file(self, value: str):
        self.set_property_state("data_file", value)

    @property
    def journal_file(self) -> str:
        """Set Fluent journal file."""
        return self.get_property_state("journal_file")

    @journal_file.setter
    def journal_file(self, value: str):
        self.set_property_state("journal_file", value)
