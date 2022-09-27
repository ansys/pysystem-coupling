#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class ascii_output(Container):
    """
    'ascii_output' child.
    """

    syc_name = "AsciiOutput"

    property_names_types = [("option", "Option", "str"), ("format", "Format", "str")]

    @property
    def option(self) -> str:
        """'option' property of 'output_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def format(self) -> str:
        """'format' property of 'output_control' object"""
        return self.get_property_state("format")

    @format.setter
    def format(self, value: str):
        self.set_property_state("format", value)
