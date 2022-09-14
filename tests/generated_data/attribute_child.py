#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .dimensionality import dimensionality


class attribute_child(Group):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    child_names = ["dimensionality"]

    dimensionality: dimensionality = dimensionality
    """
    dimensionality child of attribute_child.
    """
    property_names_types = [
        ("attribute_type", "AttributeType", "String"),
        ("real_value", "RealValue", "Real"),
        ("integer_value", "IntegerValue", "Integer"),
    ]

    @property
    def attribute_type(self) -> String:
        """'attribute_type' property of 'attribute' object"""
        return self.get_property_state("attribute_type")

    @attribute_type.setter
    def attribute_type(self, value: String):
        self.set_property_state("attribute_type", value)

    @property
    def real_value(self) -> Real:
        """'real_value' property of 'attribute' object"""
        return self.get_property_state("real_value")

    @real_value.setter
    def real_value(self, value: Real):
        self.set_property_state("real_value", value)

    @property
    def integer_value(self) -> Integer:
        """'integer_value' property of 'attribute' object"""
        return self.get_property_state("integer_value")

    @integer_value.setter
    def integer_value(self, value: Integer):
        self.set_property_state("integer_value", value)
