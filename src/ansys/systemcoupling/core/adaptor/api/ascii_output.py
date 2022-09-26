#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class ascii_output(Container):
    """
    Output interface data as ASCII.
    """

    syc_name = "AsciiOutput"

    property_names_types = [
        ("option", "Option", "String"),
        ("format", "Format", "String"),
    ]

    @property
    def option(self) -> String:
        """Control ASCII interface data output.

        Allowed values:

        - \"Off\"
        - \"EveryStep\" (for step-based analyses)
        - \"EveryIteration\" (for iteration-based analyses)"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def format(self) -> String:
        """ASCII output format type.

        Allowed values:

        - \"Axdt\"
        - \"Csv\" """
        return self.get_property_state("format")

    @format.setter
    def format(self, value: String):
        self.set_property_state("format", value)
