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
    def quantity_type(self, value: String):
        self.set_property_state("quantity_type", value)

    @property
    def location(self) -> String:
        """Data location of the variable (\"Node\" or \"Element\")."""
        return self.get_property_state("location")

    @location.setter
    def location(self, value: String):
        self.set_property_state("location", value)

    @property
    def participant_display_name(self) -> String:
        """Variable's display name as defined by the participant solver."""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: String):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> String:
        """Variable's display name as defined in System Coupling."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def data_type(self) -> String:
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
    def data_type(self, value: String):
        self.set_property_state("data_type", value)

    @property
    def real_initial_value(self) -> Real:
        """Real data start value."""
        return self.get_property_state("real_initial_value")

    @real_initial_value.setter
    def real_initial_value(self, value: Real):
        self.set_property_state("real_initial_value", value)

    @property
    def integer_initial_value(self) -> Integer:
        """Integer data start value."""
        return self.get_property_state("integer_initial_value")

    @integer_initial_value.setter
    def integer_initial_value(self, value: Integer):
        self.set_property_state("integer_initial_value", value)

    @property
    def logical_initial_value(self) -> Boolean:
        """Logical data start value."""
        return self.get_property_state("logical_initial_value")

    @logical_initial_value.setter
    def logical_initial_value(self, value: Boolean):
        self.set_property_state("logical_initial_value", value)

    @property
    def string_initial_value(self) -> String:
        """String data start value."""
        return self.get_property_state("string_initial_value")

    @string_initial_value.setter
    def string_initial_value(self, value: String):
        self.set_property_state("string_initial_value", value)

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
    def tensor_type(self) -> String:
        """Indicates the variable tensor type (\"Scalar\" or \"Vector\").

        \"Vector\" is not supported for the FMU case."""
        return self.get_property_state("tensor_type")

    @tensor_type.setter
    def tensor_type(self, value: String):
        self.set_property_state("tensor_type", value)

    @property
    def is_extensive(self) -> Boolean:
        """Indicates whether this is an extensive property."""
        return self.get_property_state("is_extensive")

    @is_extensive.setter
    def is_extensive(self, value: Boolean):
        self.set_property_state("is_extensive", value)
