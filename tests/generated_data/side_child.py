#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class side_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("coupling_participant", "CouplingParticipant", "str"),
        ("region_list", "RegionList", "StringListType"),
        ("reference_frame", "ReferenceFrame", "str"),
        ("instancing", "Instancing", "str"),
    ]

    @property
    def coupling_participant(self) -> str:
        """'coupling_participant' property of 'side' object"""
        return self.get_property_state("coupling_participant")

    @coupling_participant.setter
    def coupling_participant(self, value: str):
        self.set_property_state("coupling_participant", value)

    @property
    def region_list(self) -> StringListType:
        """'region_list' property of 'side' object"""
        return self.get_property_state("region_list")

    @region_list.setter
    def region_list(self, value: StringListType):
        self.set_property_state("region_list", value)

    @property
    def reference_frame(self) -> str:
        """'reference_frame' property of 'side' object"""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: str):
        self.set_property_state("reference_frame", value)

    @property
    def instancing(self) -> str:
        """'instancing' property of 'side' object"""
        return self.get_property_state("instancing")

    @instancing.setter
    def instancing(self, value: str):
        self.set_property_state("instancing", value)
