#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class side_child(Group):
    """
    'child_object_type' child.
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
        """'coupling_participant' property of 'side' object"""
        return self.get_property_state("coupling_participant")

    @coupling_participant.setter
    def coupling_participant(self, value: String):
        self.set_property_state("coupling_participant", value)

    @property
    def region_list(self) -> StringList:
        """'region_list' property of 'side' object"""
        return self.get_property_state("region_list")

    @region_list.setter
    def region_list(self, value: StringList):
        self.set_property_state("region_list", value)

    @property
    def reference_frame(self) -> String:
        """'reference_frame' property of 'side' object"""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: String):
        self.set_property_state("reference_frame", value)

    @property
    def instancing(self) -> String:
        """'instancing' property of 'side' object"""
        return self.get_property_state("instancing")

    @instancing.setter
    def instancing(self, value: String):
        self.set_property_state("instancing", value)
