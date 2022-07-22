#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .stabilization import stabilization


class data_transfer_child(Group):
    """
    Set data transfer details.
    """

    syc_name = "child_object_type"

    child_names = ["stabilization"]

    stabilization: stabilization = stabilization
    """
    stabilization child of data_transfer_child.
    """
    property_names_types = [
        ("display_name", "DisplayName", "String"),
        ("suppress", "Suppress", "Boolean"),
        ("target_side", "TargetSide", "String"),
        ("option", "Option", "String"),
        ("source_variable", "SourceVariable", "String"),
        ("target_variable", "TargetVariable", "String"),
        ("value", "Value", "Real"),
        ("ramping_option", "RampingOption", "String"),
        ("relaxation_factor", "RelaxationFactor", "Real"),
        ("convergence_target", "ConvergenceTarget", "Real"),
        ("mapping_type", "MappingType", "String"),
        ("unmapped_value_option", "UnmappedValueOption", "String"),
        ("time_step_initialization_option", "TimeStepInitializationOption", "String"),
    ]

    @property
    def display_name(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def suppress(self) -> Boolean:
        """Whether the data transfer is suppressed."""
        return self.get_property_state("suppress")

    @suppress.setter
    def suppress(self, value: Boolean):
        self.set_property_state("suppress", value)

    @property
    def target_side(self) -> String:
        """Side of the coupling interface to receive the data transfer."""
        return self.get_property_state("target_side")

    @target_side.setter
    def target_side(self, value: String):
        self.set_property_state("target_side", value)

    @property
    def option(self) -> String:
        """Method used to set the value of the data transfer's source variable."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def source_variable(self) -> String:
        """Available when DataTransfer.Option is set to UsingVariable."""
        return self.get_property_state("source_variable")

    @source_variable.setter
    def source_variable(self, value: String):
        self.set_property_state("source_variable", value)

    @property
    def target_variable(self) -> String:
        """Variable associated with the target side of the interface."""
        return self.get_property_state("target_variable")

    @target_variable.setter
    def target_variable(self, value: String):
        self.set_property_state("target_variable", value)

    @property
    def value(self) -> Real:
        """Available when DataTransfer.Option is set to UsingExpression and DataTransfer.TargetVariable has a scalar value."""
        return self.get_property_state("value")

    @value.setter
    def value(self, value: Real):
        self.set_property_state("value", value)

    @property
    def ramping_option(self) -> String:
        """Whether the ramping algorithm is applied to specified quantity."""
        return self.get_property_state("ramping_option")

    @ramping_option.setter
    def ramping_option(self, value: String):
        self.set_property_state("ramping_option", value)

    @property
    def relaxation_factor(self) -> Real:
        """Factor multiplying the current data transfer values for specified quantity when under-relaxing them against the previous values."""
        return self.get_property_state("relaxation_factor")

    @relaxation_factor.setter
    def relaxation_factor(self, value: Real):
        self.set_property_state("relaxation_factor", value)

    @property
    def convergence_target(self) -> Real:
        """RMS-based target value used when evaluating convergence of the specified quantity within a coupling iteration."""
        return self.get_property_state("convergence_target")

    @convergence_target.setter
    def convergence_target(self, value: Real):
        self.set_property_state("convergence_target", value)

    @property
    def mapping_type(self) -> String:
        """Type of mapping used for the data transfer. Read only."""
        return self.get_property_state("mapping_type")

    @mapping_type.setter
    def mapping_type(self, value: String):
        self.set_property_state("mapping_type", value)

    @property
    def unmapped_value_option(self) -> String:
        """Available when profile-preserving mapping is used to transfer data onto a target surface in one of System Coupling's user interfaces."""
        return self.get_property_state("unmapped_value_option")

    @unmapped_value_option.setter
    def unmapped_value_option(self, value: String):
        self.set_property_state("unmapped_value_option", value)

    @property
    def time_step_initialization_option(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: String):
        self.set_property_state("time_step_initialization_option", value)
