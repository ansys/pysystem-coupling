#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class instancing_child(Group):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("reference_frame", "ReferenceFrame", "String"),
        ("instances_in_full_circle", "InstancesInFullCircle", "Integer"),
        ("instances_for_mapping", "InstancesForMapping", "Integer"),
    ]

    @property
    def reference_frame(self) -> String:
        """'reference_frame' property of 'instancing' object"""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: String):
        self.set_property_state("reference_frame", value)

    @property
    def instances_in_full_circle(self) -> Integer:
        """'instances_in_full_circle' property of 'instancing' object"""
        return self.get_property_state("instances_in_full_circle")

    @instances_in_full_circle.setter
    def instances_in_full_circle(self, value: Integer):
        self.set_property_state("instances_in_full_circle", value)

    @property
    def instances_for_mapping(self) -> Integer:
        """'instances_for_mapping' property of 'instancing' object"""
        return self.get_property_state("instances_for_mapping")

    @instances_for_mapping.setter
    def instances_for_mapping(self, value: Integer):
        self.set_property_state("instances_for_mapping", value)
