#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class transformation_child(Group):
    """
    Use to apply transformations to coupling interface sides to control
    positioning of the geometry.
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
        """Specifies the type of transformation, ``Rotation`` or ``Translation``."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def angle(self) -> Real:
        """The angle of rotation for a rotation transformation."""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: Real):
        self.set_property_state("angle", value)

    @property
    def axis(self) -> String:
        """The axis of rotation to be used for a rotation transformation.

        XAxis
            Rotation is about the x-axis.

        YAxis
            Rotation is about the y-axis.

        ZAxis
            Rotatation is about the z-axis.

        UserDefined
            Rotation is about a user defined vector."""
        return self.get_property_state("axis")

    @axis.setter
    def axis(self, value: String):
        self.set_property_state("axis", value)

    @property
    def vector(self) -> RealVector:
        """Define an axis of rotation vector in the ``UserDefined`` case."""
        return self.get_property_state("vector")

    @vector.setter
    def vector(self, value: RealVector):
        self.set_property_state("vector", value)
