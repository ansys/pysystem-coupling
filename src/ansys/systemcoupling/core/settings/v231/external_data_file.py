#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class external_data_file(Group):
    """
    Participant external data file settings.
    """

    syc_name = "ExternalDataFile"

    property_names_types = [("file_path", "FilePath", "String")]

    @property
    def file_path(self) -> String:
        """Path to file for communication with a coupling participant."""
        return self.get_property_state("file_path")

    @file_path.setter
    def file_path(self, value: String):
        self.set_property_state("file_path", value)
