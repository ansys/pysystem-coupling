#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .attribute import attribute


class variable_child(Group):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    child_names = ["attribute"]

    attribute: attribute = attribute
    """
    attribute child of variable_child.
    """
    property_names_types = [
        ("quantity_type", "QuantityType", "String"),
        ("location", "Location", "String"),
        ("participant_display_name", "ParticipantDisplayName", "String"),
        ("display_name", "DisplayName", "String"),
        ("data_type", "DataType", "String"),
        ("real_initial_value", "RealInitialValue", "Real"),
        ("integer_initial_value", "IntegerInitialValue", "Integer"),
        ("logical_initial_value", "LogicalInitialValue", "Boolean"),
        ("string_initial_value", "StringInitialValue", "String"),
        ("real_min", "RealMin", "Real"),
        ("real_max", "RealMax", "Real"),
        ("integer_min", "IntegerMin", "Integer"),
        ("integer_max", "IntegerMax", "Integer"),
        ("tensor_type", "TensorType", "String"),
        ("is_extensive", "IsExtensive", "Boolean"),
    ]

    @property
    def quantity_type(self) -> String:
        """'quantity_type' property of 'variable' object"""
        return self.get_property_state("quantity_type")

    @quantity_type.setter
    def quantity_type(self, value: String):
        self.set_property_state("quantity_type", value)

    @property
    def location(self) -> String:
        """'location' property of 'variable' object"""
        return self.get_property_state("location")

    @location.setter
    def location(self, value: String):
        self.set_property_state("location", value)

    @property
    def participant_display_name(self) -> String:
        """'participant_display_name' property of 'variable' object"""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: String):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> String:
        """'display_name' property of 'variable' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def data_type(self) -> String:
        """'data_type' property of 'variable' object"""
        return self.get_property_state("data_type")

    @data_type.setter
    def data_type(self, value: String):
        self.set_property_state("data_type", value)

    @property
    def real_initial_value(self) -> Real:
        """'real_initial_value' property of 'variable' object"""
        return self.get_property_state("real_initial_value")

    @real_initial_value.setter
    def real_initial_value(self, value: Real):
        self.set_property_state("real_initial_value", value)

    @property
    def integer_initial_value(self) -> Integer:
        """'integer_initial_value' property of 'variable' object"""
        return self.get_property_state("integer_initial_value")

    @integer_initial_value.setter
    def integer_initial_value(self, value: Integer):
        self.set_property_state("integer_initial_value", value)

    @property
    def logical_initial_value(self) -> Boolean:
        """'logical_initial_value' property of 'variable' object"""
        return self.get_property_state("logical_initial_value")

    @logical_initial_value.setter
    def logical_initial_value(self, value: Boolean):
        self.set_property_state("logical_initial_value", value)

    @property
    def string_initial_value(self) -> String:
        """'string_initial_value' property of 'variable' object"""
        return self.get_property_state("string_initial_value")

    @string_initial_value.setter
    def string_initial_value(self, value: String):
        self.set_property_state("string_initial_value", value)

    @property
    def real_min(self) -> Real:
        """'real_min' property of 'variable' object"""
        return self.get_property_state("real_min")

    @real_min.setter
    def real_min(self, value: Real):
        self.set_property_state("real_min", value)

    @property
    def real_max(self) -> Real:
        """'real_max' property of 'variable' object"""
        return self.get_property_state("real_max")

    @real_max.setter
    def real_max(self, value: Real):
        self.set_property_state("real_max", value)

    @property
    def integer_min(self) -> Integer:
        """'integer_min' property of 'variable' object"""
        return self.get_property_state("integer_min")

    @integer_min.setter
    def integer_min(self, value: Integer):
        self.set_property_state("integer_min", value)

    @property
    def integer_max(self) -> Integer:
        """'integer_max' property of 'variable' object"""
        return self.get_property_state("integer_max")

    @integer_max.setter
    def integer_max(self, value: Integer):
        self.set_property_state("integer_max", value)

    @property
    def tensor_type(self) -> String:
        """'tensor_type' property of 'variable' object"""
        return self.get_property_state("tensor_type")

    @tensor_type.setter
    def tensor_type(self, value: String):
        self.set_property_state("tensor_type", value)

    @property
    def is_extensive(self) -> Boolean:
        """'is_extensive' property of 'variable' object"""
        return self.get_property_state("is_extensive")

    @is_extensive.setter
    def is_extensive(self, value: Boolean):
        self.set_property_state("is_extensive", value)