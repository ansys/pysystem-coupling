#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .dimensionality import dimensionality


class attribute_child(Container):
    """
    Configure a variable's attributes.
    """

    syc_name = "child_object_type"

    child_names = ["dimensionality"]

    dimensionality: dimensionality = dimensionality
    """
    dimensionality child of attribute_child.
    """
    property_names_types = [
        ("attribute_type", "AttributeType", "str"),
        ("real_value", "RealValue", "RealType"),
        ("integer_value", "IntegerValue", "int"),
    ]

    @property
    def attribute_type(self) -> str:
        """The type of the attribute (\"Real\" or \"Integer\")."""
        return self.get_property_state("attribute_type")

    @attribute_type.setter
    def attribute_type(self, value: str):
        self.set_property_state("attribute_type", value)

    @property
    def real_value(self) -> RealType:
        """Real attribute value."""
        return self.get_property_state("real_value")

    @real_value.setter
    def real_value(self, value: RealType):
        self.set_property_state("real_value", value)

    @property
    def integer_value(self) -> int:
        """Integer attribute value."""
        return self.get_property_state("integer_value")

    @integer_value.setter
    def integer_value(self, value: int):
        self.set_property_state("integer_value", value)
