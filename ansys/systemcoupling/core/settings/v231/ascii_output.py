#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class ascii_output(Group):
    """
    **CURRENTLY NOT DOCUMENTED**
    """

    syc_name = "AsciiOutput"

    property_names_types = [
        ("option", "Option", "String"),
        ("format", "Format", "String"),
    ]

    @property
    def option(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def format(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("format")

    @format.setter
    def format(self, value: String):
        self.set_property_state("format", value)
