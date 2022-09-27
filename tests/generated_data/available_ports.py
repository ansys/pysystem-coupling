#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class available_ports(Container):
    """
    'available_ports' child.
    """

    syc_name = "AvailablePorts"

    property_names_types = [("option", "Option", "str"), ("range", "Range", "str")]

    @property
    def option(self) -> str:
        """'option' property of 'solution_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def range(self) -> str:
        """'range' property of 'solution_control' object"""
        return self.get_property_state("range")

    @range.setter
    def range(self, value: str):
        self.set_property_state("range", value)
