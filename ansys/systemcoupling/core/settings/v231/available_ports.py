#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class available_ports(Group):
    """
    Specify ports available for co-simulation.
    """

    syc_name = "AvailablePorts"

    property_names_types = [
        ("option", "Option", "String"),
        ("range", "Range", "String"),
    ]

    @property
    def option(self) -> String:
        """Specify how available ports are determined.

        - \"ProgramControlled\" - System Coupling will find an
          available port.
        - \"UserDefined\" - An available port will be chosen,
          if possible, from a specified range."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def range(self) -> String:
        """Port range expressed as a comma-separated list of integers and/or
        integer ranges. An integer range is a pair of integers separated
        with a "-" character, specify an inclusive range of port numbers."""
        return self.get_property_state("range")

    @range.setter
    def range(self, value: String):
        self.set_property_state("range", value)
