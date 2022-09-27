#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class transformation_child(Container):
    """
    'child_object_type' child.
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
        """'option' property of 'transformation' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def angle(self) -> RealType:
        """'angle' property of 'transformation' object"""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: RealType):
        self.set_property_state("angle", value)

    @property
    def axis(self) -> str:
        """'axis' property of 'transformation' object"""
        return self.get_property_state("axis")

    @axis.setter
    def axis(self, value: str):
        self.set_property_state("axis", value)

    @property
    def vector(self) -> RealVectorType:
        """'vector' property of 'transformation' object"""
        return self.get_property_state("vector")

    @vector.setter
    def vector(self, value: RealVectorType):
        self.set_property_state("vector", value)
