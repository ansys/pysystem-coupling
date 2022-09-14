#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class apip(Group):
    """
    Apip-related expert settings.
    """

    syc_name = "Apip"

    property_names_types = [
        ("debug", "Debug", "Boolean"),
        ("disable", "Disable", "Boolean"),
    ]

    @property
    def debug(self) -> Boolean:
        """Debug apip data (sends to debug server, saves data locally)."""
        return self.get_property_state("debug")

    @debug.setter
    def debug(self, value: Boolean):
        self.set_property_state("debug", value)

    @property
    def disable(self) -> Boolean:
        """Disable apip collection (regardless of user settings)."""
        return self.get_property_state("disable")

    @disable.setter
    def disable(self, value: Boolean):
        self.set_property_state("disable", value)
