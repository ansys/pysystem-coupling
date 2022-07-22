#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class apip(Group):
    """
    **CURRENTLY NOT DOCUMENTED**
    """

    syc_name = "Apip"

    property_names_types = [
        ("debug", "Debug", "Boolean"),
        ("disable", "Disable", "Boolean"),
    ]

    @property
    def debug(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("debug")

    @debug.setter
    def debug(self, value: Boolean):
        self.set_property_state("debug", value)

    @property
    def disable(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("disable")

    @disable.setter
    def disable(self, value: Boolean):
        self.set_property_state("disable", value)
