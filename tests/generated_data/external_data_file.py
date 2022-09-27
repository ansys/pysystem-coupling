#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class external_data_file(Container):
    """
    'external_data_file' child.
    """

    syc_name = "ExternalDataFile"

    property_names_types = [("file_path", "FilePath", "str")]

    @property
    def file_path(self) -> str:
        """'file_path' property of 'child_object_type' object"""
        return self.get_property_state("file_path")

    @file_path.setter
    def file_path(self, value: str):
        self.set_property_state("file_path", value)
