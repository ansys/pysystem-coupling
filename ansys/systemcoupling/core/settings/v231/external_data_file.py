#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class external_data_file(Group):
    """
    Available when the ParticipantType is set to EXTERNALDATA (that is, only for workflows involving a Workbench setup using static data).
    """

    syc_name = "ExternalDataFile"

    property_names_types = [("file_path", "FilePath", "String")]

    @property
    def file_path(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("file_path")

    @file_path.setter
    def file_path(self, value: String):
        self.set_property_state("file_path", value)
