#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class external_data_file(Group):
    """
    'external_data_file' child.
    """

    syc_name = "ExternalDataFile"

    property_names_types = [("file_path", "FilePath", "String")]

    @property
    def file_path(self) -> String:
        """'file_path' property of 'child_object_type' object"""
        return self.get_property_state("file_path")

    @file_path.setter
    def file_path(self, value: String):
        self.set_property_state("file_path", value)
