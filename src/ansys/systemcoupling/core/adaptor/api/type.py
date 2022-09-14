#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class type(Group):
    """
    File type for result output.
    """

    syc_name = "Type"

    property_names_types = [
        ("option", "Option", "String"),
        ("binary_format", "BinaryFormat", "Boolean"),
    ]

    @property
    def option(self) -> String:
        """Allowed values:

        - \"EnsightGold\" (beta only)"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def binary_format(self) -> Boolean:
        """Output in Binary or ASCII format."""
        return self.get_property_state("binary_format")

    @binary_format.setter
    def binary_format(self, value: Boolean):
        self.set_property_state("binary_format", value)
