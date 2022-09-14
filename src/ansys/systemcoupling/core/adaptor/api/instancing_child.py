#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class instancing_child(Group):
    """
    Define instancing for an interface side.

    Available when cylindrical geometry instancing has been added to
    the data model.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("reference_frame", "ReferenceFrame", "String"),
        ("instances_in_full_circle", "InstancesInFullCircle", "Integer"),
        ("instances_for_mapping", "InstancesForMapping", "Integer"),
    ]

    @property
    def reference_frame(self) -> String:
        """Reference frame that defines the orientation of the instancing.

        Rotation will be around the z-axis of the reference frame,
        following the right-hand rule."""
        return self.get_property_state("reference_frame")

    @reference_frame.setter
    def reference_frame(self, value: String):
        self.set_property_state("reference_frame", value)

    @property
    def instances_in_full_circle(self) -> Integer:
        """Total number of instances (including the first instance) in
        a full 360 degree rotation of the participant mesh. This value
        includes the reference instance (with the participant mesh).
        All instances defined for the instancing object have identical
        angles."""
        return self.get_property_state("instances_in_full_circle")

    @instances_in_full_circle.setter
    def instances_in_full_circle(self, value: Integer):
        self.set_property_state("instances_in_full_circle", value)

    @property
    def instances_for_mapping(self) -> Integer:
        """Number of instances to be included in the mapping when instancing
        is applied.

        Required when the number of instances to be used for mapping does
        not match the number of instances in a full circle. Default
        assumes a 360 degree rotation of the participant mesh. This value
        includes the reference instance (with the participant mesh)."""
        return self.get_property_state("instances_for_mapping")

    @instances_for_mapping.setter
    def instances_for_mapping(self, value: Integer):
        self.set_property_state("instances_for_mapping", value)
