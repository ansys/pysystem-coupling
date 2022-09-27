#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class type(Container):
    """
    File type for result output.
    """

    syc_name = "Type"

    property_names_types = [
        ("option", "Option", "str"),
        ("binary_format", "BinaryFormat", "bool"),
    ]

    @property
    def option(self) -> str:
        """Allowed values:

        - \"EnsightGold\" (beta only)"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def binary_format(self) -> bool:
        """Output in Binary or ASCII format."""
        return self.get_property_state("binary_format")

    @binary_format.setter
    def binary_format(self, value: bool):
        self.set_property_state("binary_format", value)
