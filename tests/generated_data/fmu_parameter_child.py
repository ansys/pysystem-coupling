#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class fmu_parameter_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("data_type", "DataType", "str"),
        ("participant_display_name", "ParticipantDisplayName", "str"),
        ("display_name", "DisplayName", "str"),
        ("real_value", "RealValue", "RealType"),
        ("real_min", "RealMin", "RealType"),
        ("real_max", "RealMax", "RealType"),
        ("integer_value", "IntegerValue", "int"),
        ("integer_min", "IntegerMin", "int"),
        ("integer_max", "IntegerMax", "int"),
        ("logical_value", "LogicalValue", "bool"),
        ("string_value", "StringValue", "str"),
    ]

    @property
    def data_type(self) -> str:
        """'data_type' property of 'fmu_parameter' object"""
        return self.get_property_state("data_type")

    @data_type.setter
    def data_type(self, value: str):
        self.set_property_state("data_type", value)

    @property
    def participant_display_name(self) -> str:
        """'participant_display_name' property of 'fmu_parameter' object"""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: str):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> str:
        """'display_name' property of 'fmu_parameter' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def real_value(self) -> RealType:
        """'real_value' property of 'fmu_parameter' object"""
        return self.get_property_state("real_value")

    @real_value.setter
    def real_value(self, value: RealType):
        self.set_property_state("real_value", value)

    @property
    def real_min(self) -> RealType:
        """'real_min' property of 'fmu_parameter' object"""
        return self.get_property_state("real_min")

    @real_min.setter
    def real_min(self, value: RealType):
        self.set_property_state("real_min", value)

    @property
    def real_max(self) -> RealType:
        """'real_max' property of 'fmu_parameter' object"""
        return self.get_property_state("real_max")

    @real_max.setter
    def real_max(self, value: RealType):
        self.set_property_state("real_max", value)

    @property
    def integer_value(self) -> int:
        """'integer_value' property of 'fmu_parameter' object"""
        return self.get_property_state("integer_value")

    @integer_value.setter
    def integer_value(self, value: int):
        self.set_property_state("integer_value", value)

    @property
    def integer_min(self) -> int:
        """'integer_min' property of 'fmu_parameter' object"""
        return self.get_property_state("integer_min")

    @integer_min.setter
    def integer_min(self, value: int):
        self.set_property_state("integer_min", value)

    @property
    def integer_max(self) -> int:
        """'integer_max' property of 'fmu_parameter' object"""
        return self.get_property_state("integer_max")

    @integer_max.setter
    def integer_max(self, value: int):
        self.set_property_state("integer_max", value)

    @property
    def logical_value(self) -> bool:
        """'logical_value' property of 'fmu_parameter' object"""
        return self.get_property_state("logical_value")

    @logical_value.setter
    def logical_value(self, value: bool):
        self.set_property_state("logical_value", value)

    @property
    def string_value(self) -> str:
        """'string_value' property of 'fmu_parameter' object"""
        return self.get_property_state("string_value")

    @string_value.setter
    def string_value(self, value: str):
        self.set_property_state("string_value", value)
