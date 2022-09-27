#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class transformation_child(Container):
    """
    Use to apply transformations to coupling interface sides to control
    positioning of the geometry.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("option", "Option", "str"),
        ("angle", "Angle", "RealType"),
        ("axis", "Axis", "str"),
        ("vector", "Vector", "RealVectorType"),
    ]

    @property
    def option(self) -> str:
        """Specifies the type of transformation, ``Rotation`` or ``Translation``."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def angle(self) -> RealType:
        """The angle of rotation for a rotation transformation."""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: RealType):
        self.set_property_state("angle", value)

    @property
    def axis(self) -> str:
        """The axis of rotation to be used for a rotation transformation.

        - \"XAxis\" - Rotation is about the x-axis.
        - \"YAxis\" - Rotation is about the y-axis.
        - \"ZAxis\" - Rotation is about the z-axis.
        - \"UserDefined\" - Rotation is about a user defined vector."""
        return self.get_property_state("axis")

    @axis.setter
    def axis(self, value: str):
        self.set_property_state("axis", value)

    @property
    def vector(self) -> RealVectorType:
        """Define an axis of rotation vector in the ``UserDefined`` case."""
        return self.get_property_state("vector")

    @vector.setter
    def vector(self, value: RealVectorType):
        self.set_property_state("vector", value)
