#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class side_child(Group):
    """
    Side of the coupling interface.
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
        """Object name assigned and used by System Coupling to identify the participant associated with the interface side."""
        return self.get_property_state("coupling_participant")

    @coupling_participant.setter
    def coupling_participant(self, value: String):
        self.set_property_state("coupling_participant", value)

    @property
    def region_list(self) -> StringList:
        """Collection of regions on the interface side that can send or receive data. Required for the creation of data transfers."""
        return self.get_property_state("region_list")

    @region_list.setter
    def region_list(self, value: StringList):
        self.set_property_state("region_list", value)

    @property
    def reference_frame(self) -> String:
        """Global reference frame to be used for transformations of the interface side."""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: String):
        self.set_property_state("reference_frame", value)

    @property
    def instancing(self) -> String:
        """Instancing object defined for the interface side."""
        return self.get_property_state("instancing")

    @instancing.setter
    def instancing(self, value: String):
        self.set_property_state("instancing", value)
