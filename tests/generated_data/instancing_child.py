#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class instancing_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("reference_frame", "ReferenceFrame", "str"),
        ("instances_in_full_circle", "InstancesInFullCircle", "int"),
        ("instances_for_mapping", "InstancesForMapping", "int"),
    ]

    @property
    def reference_frame(self) -> str:
        """'reference_frame' property of 'instancing' object"""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: str):
        self.set_property_state("reference_frame", value)

    @property
    def instances_in_full_circle(self) -> int:
        """'instances_in_full_circle' property of 'instancing' object"""
        return self.get_property_state("instances_in_full_circle")

    @instances_in_full_circle.setter
    def instances_in_full_circle(self, value: int):
        self.set_property_state("instances_in_full_circle", value)

    @property
    def instances_for_mapping(self) -> int:
        """'instances_for_mapping' property of 'instancing' object"""
        return self.get_property_state("instances_for_mapping")

    @instances_for_mapping.setter
    def instances_for_mapping(self, value: int):
        self.set_property_state("instances_for_mapping", value)
