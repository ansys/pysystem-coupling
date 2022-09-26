#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class side_child(Container):
    """
    Configure one side of a coupling interface.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("coupling_participant", "CouplingParticipant", "String"),
        ("region_list", "RegionList", "StringList"),
        ("reference_frame", "ReferenceFrame", "String"),
        ("instancing", "Instancing", "String"),
    ]

    @property
    def coupling_participant(self) -> String:
        """Name of the participant on this interface side."""
        return self.get_property_state("coupling_participant")

    @coupling_participant.setter
    def coupling_participant(self, value: String):
        self.set_property_state("coupling_participant", value)

    @property
    def region_list(self) -> StringList:
        """List of participant regions involved in this interface side."""
        return self.get_property_state("region_list")

    @region_list.setter
    def region_list(self, value: StringList):
        self.set_property_state("region_list", value)

    @property
    def reference_frame(self) -> String:
        """Reference frame of this side."""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: String):
        self.set_property_state("reference_frame", value)

    @property
    def instancing(self) -> String:
        """Instancing name for this side (leave unset if not required)."""
        return self.get_property_state("instancing")

    @instancing.setter
    def instancing(self, value: String):
        self.set_property_state("instancing", value)
