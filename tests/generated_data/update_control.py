#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class update_control(Container):
    """
    'update_control' child.
    """

    syc_name = "UpdateControl"

    property_names_types = [
        ("option", "Option", "String"),
        ("update_frequency", "UpdateFrequency", "Integer"),
    ]

    @property
    def option(self) -> String:
        """'option' property of 'child_object_type' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def update_frequency(self) -> Integer:
        """'update_frequency' property of 'child_object_type' object"""
        return self.get_property_state("update_frequency")

    @update_frequency.setter
    def update_frequency(self, value: Integer):
        self.set_property_state("update_frequency", value)
