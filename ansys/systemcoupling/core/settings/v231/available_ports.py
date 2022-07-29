#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class available_ports(Group):
    """
    **CURRENTLY NOT DOCUMENTED**
    """

    syc_name = "AvailablePorts"

    property_names_types = [
        ("option", "Option", "String"),
        ("range", "Range", "String"),
    ]

    @property
    def option(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def range(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("range")

    @range.setter
    def range(self, value: String):
        self.set_property_state("range", value)
