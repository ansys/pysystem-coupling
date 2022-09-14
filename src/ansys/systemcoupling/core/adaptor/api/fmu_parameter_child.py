#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class fmu_parameter_child(Group):
    """
    Configure a parameter for an FMU coupling participant.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("data_type", "DataType", "String"),
        ("participant_display_name", "ParticipantDisplayName", "String"),
        ("display_name", "DisplayName", "String"),
        ("real_value", "RealValue", "Real"),
        ("real_min", "RealMin", "Real"),
        ("real_max", "RealMax", "Real"),
        ("integer_value", "IntegerValue", "Integer"),
        ("integer_min", "IntegerMin", "Integer"),
        ("integer_max", "IntegerMax", "Integer"),
        ("logical_value", "LogicalValue", "Boolean"),
        ("string_value", "StringValue", "String"),
    ]

    @property
    def data_type(self) -> String:
        """UNDOCUMENTED"""
        return self.get_property_state("data_type")

    @data_type.setter
    def data_type(self, value: String):
        self.set_property_state("data_type", value)

    @property
    def participant_display_name(self) -> String:
        """Parameter's display name as defined by the participant solver."""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: String):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> String:
        """Parameter's display name as defined in System Coupling."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def real_value(self) -> Real:
        """Real data start value."""
        return self.get_property_state("real_value")

    @real_value.setter
    def real_value(self, value: Real):
        self.set_property_state("real_value", value)

    @property
    def real_min(self) -> Real:
        """Real data minimum value."""
        return self.get_property_state("real_min")

    @real_min.setter
    def real_min(self, value: Real):
        self.set_property_state("real_min", value)

    @property
    def real_max(self) -> Real:
        """Real data maximum value."""
        return self.get_property_state("real_max")

    @real_max.setter
    def real_max(self, value: Real):
        self.set_property_state("real_max", value)

    @property
    def integer_value(self) -> Integer:
        """Integer data start value."""
        return self.get_property_state("integer_value")

    @integer_value.setter
    def integer_value(self, value: Integer):
        self.set_property_state("integer_value", value)

    @property
    def integer_min(self) -> Integer:
        """Integer data minimum value."""
        return self.get_property_state("integer_min")

    @integer_min.setter
    def integer_min(self, value: Integer):
        self.set_property_state("integer_min", value)

    @property
    def integer_max(self) -> Integer:
        """Integer data maximum value."""
        return self.get_property_state("integer_max")

    @integer_max.setter
    def integer_max(self, value: Integer):
        self.set_property_state("integer_max", value)

    @property
    def logical_value(self) -> Boolean:
        """Logical data start value."""
        return self.get_property_state("logical_value")

    @logical_value.setter
    def logical_value(self, value: Boolean):
        self.set_property_state("logical_value", value)

    @property
    def string_value(self) -> String:
        """String data start value."""
        return self.get_property_state("string_value")

    @string_value.setter
    def string_value(self, value: String):
        self.set_property_state("string_value", value)
