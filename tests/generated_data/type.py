#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class type(Group):
    """
    'type' child.
    """

    syc_name = "Type"

    property_names_types = [
        ("option", "Option", "String"),
        ("binary_format", "BinaryFormat", "Boolean"),
    ]

    @property
    def option(self) -> String:
        """'option' property of 'results' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def binary_format(self) -> Boolean:
        """'binary_format' property of 'results' object"""
        return self.get_property_state("binary_format")

    @binary_format.setter
    def binary_format(self, value: Boolean):
        self.set_property_state("binary_format", value)
