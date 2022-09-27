#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .stabilization import stabilization


class data_transfer_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    child_names = ["stabilization"]

    stabilization: stabilization = stabilization
    """
    stabilization child of data_transfer_child.
    """
    property_names_types = [
        ("display_name", "DisplayName", "str"),
        ("suppress", "Suppress", "bool"),
        ("target_side", "TargetSide", "str"),
        ("option", "Option", "str"),
        ("source_variable", "SourceVariable", "str"),
        ("target_variable", "TargetVariable", "str"),
        ("value", "Value", "RealType"),
        ("ramping_option", "RampingOption", "str"),
        ("relaxation_factor", "RelaxationFactor", "RealType"),
        ("convergence_target", "ConvergenceTarget", "RealType"),
        ("mapping_type", "MappingType", "str"),
        ("unmapped_value_option", "UnmappedValueOption", "str"),
        ("time_step_initialization_option", "TimeStepInitializationOption", "str"),
    ]

    @property
    def display_name(self) -> str:
        """'display_name' property of 'data_transfer' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def suppress(self) -> bool:
        """'suppress' property of 'data_transfer' object"""
        return self.get_property_state("suppress")

    @suppress.setter
    def suppress(self, value: bool):
        self.set_property_state("suppress", value)

    @property
    def target_side(self) -> str:
        """'target_side' property of 'data_transfer' object"""
        return self.get_property_state("target_side")

    @target_side.setter
    def target_side(self, value: str):
        self.set_property_state("target_side", value)

    @property
    def option(self) -> str:
        """'option' property of 'data_transfer' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def source_variable(self) -> str:
        """'source_variable' property of 'data_transfer' object"""
        return self.get_property_state("source_variable")

    @source_variable.setter
    def source_variable(self, value: str):
        self.set_property_state("source_variable", value)

    @property
    def target_variable(self) -> str:
        """'target_variable' property of 'data_transfer' object"""
        return self.get_property_state("target_variable")

    @target_variable.setter
    def target_variable(self, value: str):
        self.set_property_state("target_variable", value)

    @property
    def value(self) -> RealType:
        """'value' property of 'data_transfer' object"""
        return self.get_property_state("value")

    @value.setter
    def value(self, value: RealType):
        self.set_property_state("value", value)

    @property
    def ramping_option(self) -> str:
        """'ramping_option' property of 'data_transfer' object"""
        return self.get_property_state("ramping_option")

    @ramping_option.setter
    def ramping_option(self, value: str):
        self.set_property_state("ramping_option", value)

    @property
    def relaxation_factor(self) -> RealType:
        """'relaxation_factor' property of 'data_transfer' object"""
        return self.get_property_state("relaxation_factor")

    @relaxation_factor.setter
    def relaxation_factor(self, value: RealType):
        self.set_property_state("relaxation_factor", value)

    @property
    def convergence_target(self) -> RealType:
        """'convergence_target' property of 'data_transfer' object"""
        return self.get_property_state("convergence_target")

    @convergence_target.setter
    def convergence_target(self, value: RealType):
        self.set_property_state("convergence_target", value)

    @property
    def mapping_type(self) -> str:
        """'mapping_type' property of 'data_transfer' object"""
        return self.get_property_state("mapping_type")

    @mapping_type.setter
    def mapping_type(self, value: str):
        self.set_property_state("mapping_type", value)

    @property
    def unmapped_value_option(self) -> str:
        """'unmapped_value_option' property of 'data_transfer' object"""
        return self.get_property_state("unmapped_value_option")

    @unmapped_value_option.setter
    def unmapped_value_option(self, value: str):
        self.set_property_state("unmapped_value_option", value)

    @property
    def time_step_initialization_option(self) -> str:
        """'time_step_initialization_option' property of 'data_transfer' object"""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: str):
        self.set_property_state("time_step_initialization_option", value)
