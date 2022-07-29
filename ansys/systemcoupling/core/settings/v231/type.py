#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class type(Group):
    """
    Settings defined under the Type singleton control the type of output to be generated.
    """

    syc_name = "Type"

    property_names_types = [
        ("option", "Option", "String"),
        ("binary_format", "BinaryFormat", "Boolean"),
    ]

    @property
    def option(self) -> String:
        """Specifies the type of output to be generated."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def binary_format(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("binary_format")

    @binary_format.setter
    def binary_format(self, value: Boolean):
        self.set_property_state("binary_format", value)
