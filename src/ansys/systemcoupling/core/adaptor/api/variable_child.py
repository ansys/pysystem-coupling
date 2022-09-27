#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .attribute import attribute


class variable_child(Container):
    """
    Configure a variable for the coupling participant.
    """

    syc_name = "child_object_type"

    child_names = ["attribute"]

    attribute: attribute = attribute
    """
    attribute child of variable_child.
    """
    property_names_types = [
        ("quantity_type", "QuantityType", "str"),
        ("location", "Location", "str"),
        ("participant_display_name", "ParticipantDisplayName", "str"),
        ("display_name", "DisplayName", "str"),
        ("data_type", "DataType", "str"),
        ("real_initial_value", "RealInitialValue", "RealType"),
        ("integer_initial_value", "IntegerInitialValue", "int"),
        ("logical_initial_value", "LogicalInitialValue", "bool"),
        ("string_initial_value", "StringInitialValue", "str"),
        ("real_min", "RealMin", "RealType"),
        ("real_max", "RealMax", "RealType"),
        ("integer_min", "IntegerMin", "int"),
        ("integer_max", "IntegerMax", "int"),
        ("tensor_type", "TensorType", "str"),
        ("is_extensive", "IsExtensive", "bool"),
    ]

    @property
    def quantity_type(self) -> str:
        """Quantity type of the variable.

        Allowed values:

        - \"Unspecified\"
        - \"Force\"
        - \"Incremental Displacement\"
        - \"Temperature\"
        - \"Heat Rate\"
        - \"Heat Transfer Coefficient\"
        - \"Convection Reference Temperature\"
        - \"Mode Shape\"
        - \"Electrical Conductivity\" """
        return self.get_property_state("quantity_type")

    @quantity_type.setter
    def quantity_type(self, value: str):
        self.set_property_state("quantity_type", value)

    @property
    def location(self) -> str:
        """Data location of the variable (\"Node\" or \"Element\")."""
        return self.get_property_state("location")

    @location.setter
    def location(self, value: str):
        self.set_property_state("location", value)

    @property
    def participant_display_name(self) -> str:
        """Variable's display name as defined by the participant solver."""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: str):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> str:
        """Variable's display name as defined in System Coupling."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def data_type(self) -> str:
        """Variable's data type as reported by the participant.

        Allowed values (non-FMU case):

        - Real
        - Complex

        Allowed values (FMU):

        - Real
        - Integer
        - Logical
        - String
        - None"""
        return self.get_property_state("data_type")

    @data_type.setter
    def data_type(self, value: str):
        self.set_property_state("data_type", value)

    @property
    def real_initial_value(self) -> RealType:
        """Real data start value."""
        return self.get_property_state("real_initial_value")

    @real_initial_value.setter
    def real_initial_value(self, value: RealType):
        self.set_property_state("real_initial_value", value)

    @property
    def integer_initial_value(self) -> int:
        """Integer data start value."""
        return self.get_property_state("integer_initial_value")

    @integer_initial_value.setter
    def integer_initial_value(self, value: int):
        self.set_property_state("integer_initial_value", value)

    @property
    def logical_initial_value(self) -> bool:
        """Logical data start value."""
        return self.get_property_state("logical_initial_value")

    @logical_initial_value.setter
    def logical_initial_value(self, value: bool):
        self.set_property_state("logical_initial_value", value)

    @property
    def string_initial_value(self) -> str:
        """String data start value."""
        return self.get_property_state("string_initial_value")

    @string_initial_value.setter
    def string_initial_value(self, value: str):
        self.set_property_state("string_initial_value", value)

    @property
    def real_min(self) -> RealType:
        """Real data minimum value."""
        return self.get_property_state("real_min")

    @real_min.setter
    def real_min(self, value: RealType):
        self.set_property_state("real_min", value)

    @property
    def real_max(self) -> RealType:
        """Real data maximum value."""
        return self.get_property_state("real_max")

    @real_max.setter
    def real_max(self, value: RealType):
        self.set_property_state("real_max", value)

    @property
    def integer_min(self) -> int:
        """Integer data minimum value."""
        return self.get_property_state("integer_min")

    @integer_min.setter
    def integer_min(self, value: int):
        self.set_property_state("integer_min", value)

    @property
    def integer_max(self) -> int:
        """Integer data maximum value."""
        return self.get_property_state("integer_max")

    @integer_max.setter
    def integer_max(self, value: int):
        self.set_property_state("integer_max", value)

    @property
    def tensor_type(self) -> str:
        """Indicates the variable tensor type (\"Scalar\" or \"Vector\").

        \"Vector\" is not supported for the FMU case."""
        return self.get_property_state("tensor_type")

    @tensor_type.setter
    def tensor_type(self, value: str):
        self.set_property_state("tensor_type", value)

    @property
    def is_extensive(self) -> bool:
        """Indicates whether this is an extensive property."""
        return self.get_property_state("is_extensive")

    @is_extensive.setter
    def is_extensive(self, value: bool):
        self.set_property_state("is_extensive", value)
