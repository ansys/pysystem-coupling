#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class transformation_child(Group):
    """
    Use Transformation objects to apply transformations to coupling interfaces sides to control the positioning of the geometry.
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
        """Type of transformation to be performed."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def angle(self) -> Real:
        """Available when the Transformation.Option setting is set to Rotation."""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: Real):
        self.set_property_state("angle", value)

    @property
    def axis(self) -> String:
        """Available when the Transformation.Option setting is set to Rotation."""
        return self.get_property_state("axis")

    @axis.setter
    def axis(self, value: String):
        self.set_property_state("axis", value)

    @property
    def vector(self) -> RealVector:
        """Available when Transformation.Option is set to Translation or when Transformation.Axis is set to UserDefined."""
        return self.get_property_state("vector")

    @vector.setter
    def vector(self, value: RealVector):
        self.set_property_state("vector", value)
