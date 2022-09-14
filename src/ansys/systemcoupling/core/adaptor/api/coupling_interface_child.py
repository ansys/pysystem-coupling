#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .data_transfer import data_transfer
from .mapping_control import mapping_control
from .side import side


class coupling_interface_child(Group):
    """
    Configure a coupling interface.
    """

    syc_name = "child_object_type"

    child_names = ["side", "data_transfer", "mapping_control"]

    side: side = side
    """
    side child of coupling_interface_child.
    """
    data_transfer: data_transfer = data_transfer
    """
    data_transfer child of coupling_interface_child.
    """
    mapping_control: mapping_control = mapping_control
    """
    mapping_control child of coupling_interface_child.
    """
    property_names_types = [("display_name", "DisplayName", "String")]

    @property
    def display_name(self) -> String:
        """Set the display name of an object."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)
