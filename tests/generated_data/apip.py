#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class apip(Container):
    """
    'apip' child.
    """

    syc_name = "Apip"

    property_names_types = [("debug", "Debug", "bool"), ("disable", "Disable", "bool")]

    @property
    def debug(self) -> bool:
        """'debug' property of 'analysis_control' object"""
        return self.get_property_state("debug")

    @debug.setter
    def debug(self, value: bool):
        self.set_property_state("debug", value)

    @property
    def disable(self) -> bool:
        """'disable' property of 'analysis_control' object"""
        return self.get_property_state("disable")

    @disable.setter
    def disable(self, value: bool):
        self.set_property_state("disable", value)
