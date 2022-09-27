#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class ascii_output(Container):
    """
    Output interface data as ASCII.
    """

    syc_name = "AsciiOutput"

    property_names_types = [("option", "Option", "str"), ("format", "Format", "str")]

    @property
    def option(self) -> str:
        """Control ASCII interface data output.

        Allowed values:

        - \"Off\"
        - \"EveryStep\" (for step-based analyses)
        - \"EveryIteration\" (for iteration-based analyses)"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def format(self) -> str:
        """ASCII output format type.

        Allowed values:

        - \"Axdt\"
        - \"Csv\" """
        return self.get_property_state("format")

    @format.setter
    def format(self, value: str):
        self.set_property_state("format", value)
