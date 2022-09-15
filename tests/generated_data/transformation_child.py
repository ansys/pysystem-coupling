#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class transformation_child(Group):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("option", "Option", "String"),
        ("angle", "Angle", "Real"),
        ("axis", "Axis", "String"),
        ("vector", "Vector", "RealVector"),
    ]

    @property
    def option(self) -> String:
        """'option' property of 'transformation' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def angle(self) -> Real:
        """'angle' property of 'transformation' object"""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: Real):
        self.set_property_state("angle", value)

    @property
    def axis(self) -> String:
        """'axis' property of 'transformation' object"""
        return self.get_property_state("axis")

    @axis.setter
    def axis(self, value: String):
        self.set_property_state("axis", value)

    @property
    def vector(self) -> RealVector:
        """'vector' property of 'transformation' object"""
        return self.get_property_state("vector")

    @vector.setter
    def vector(self, value: RealVector):
        self.set_property_state("vector", value)
