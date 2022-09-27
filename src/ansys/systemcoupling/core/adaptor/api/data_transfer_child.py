#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .stabilization import stabilization


class data_transfer_child(Container):
    """
    Configure data transfers for a coupling interface.
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
        """Display name of the data transfer."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def suppress(self) -> bool:
        """Controls whether this data transfer is suppressed"""
        return self.get_property_state("suppress")

    @suppress.setter
    def suppress(self, value: bool):
        self.set_property_state("suppress", value)

    @property
    def target_side(self) -> str:
        """Target side (\"One\" or \"Two\") of this data transfer."""
        return self.get_property_state("target_side")

    @target_side.setter
    def target_side(self, value: str):
        self.set_property_state("target_side", value)

    @property
    def option(self) -> str:
        """How the transfer data is specified.

        Allowed values:

        - \"UsingVariable\" - The data being transferred is defined as a
          single source-side variable.

        - \"UsingExpression\" - The data being transferred is defined as
          an expression in terms of source-side variables."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def source_variable(self) -> str:
        """Variable associated with the source side of the interface.

        Specified only for variable-based transfers (and not expression-based)."""
        return self.get_property_state("source_variable")

    @source_variable.setter
    def source_variable(self, value: str):
        self.set_property_state("source_variable", value)

    @property
    def target_variable(self) -> str:
        """Variable associated with the target side of the interface."""
        return self.get_property_state("target_variable")

    @target_variable.setter
    def target_variable(self, value: str):
        self.set_property_state("target_variable", value)

    @property
    def value(self) -> RealType:
        """Expression string (or constant real value) defining the data being
        transferred from the source.

        Specified only for expression-based transfers.

        Any variable referenced must be a source side variable."""
        return self.get_property_state("value")

    @value.setter
    def value(self, value: RealType):
        self.set_property_state("value", value)

    @property
    def ramping_option(self) -> str:
        """Specify whether to apply ramping to the data transfer.

        Ramping is used to slow the application of the source-side value on the
        target side of the interface.

        Allowed values:

        - \"None\" - No ramping to be applied.

        - \"Linear\" - Apply linear ramping."""
        return self.get_property_state("ramping_option")

    @ramping_option.setter
    def ramping_option(self, value: str):
        self.set_property_state("ramping_option", value)

    @property
    def relaxation_factor(self) -> RealType:
        """Factor multiplying the current data transfer values for specified quantity when
        under-relaxing them against the previous values."""
        return self.get_property_state("relaxation_factor")

    @relaxation_factor.setter
    def relaxation_factor(self, value: RealType):
        self.set_property_state("relaxation_factor", value)

    @property
    def convergence_target(self) -> RealType:
        """RMS-based target value used when evaluating convergence of the specified
        quantity within a coupling iteration."""
        return self.get_property_state("convergence_target")

    @convergence_target.setter
    def convergence_target(self, value: RealType):
        self.set_property_state("convergence_target", value)

    @property
    def mapping_type(self) -> str:
        """Type of mapping used for the data transfer. (**Read only**.)

        Possible values:

        - \"Conservative\" - A conservative mapping algorithm is used
          for transfers of `extensive` quantities.
        - \"ProfilePreserving\" - A profile-preserving mapping algorithm
          is used for transfers of `intensive` quantities."""
        return self.get_property_state("mapping_type")

    @mapping_type.setter
    def mapping_type(self, value: str):
        self.set_property_state("mapping_type", value)

    @property
    def unmapped_value_option(self) -> str:
        """Option to fill target values not mapped by the regular mapping algorithm"""
        return self.get_property_state("unmapped_value_option")

    @unmapped_value_option.setter
    def unmapped_value_option(self, value: str):
        self.set_property_state("unmapped_value_option", value)

    @property
    def time_step_initialization_option(self) -> str:
        """Method to initialize first transfer in new coupling step."""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: str):
        self.set_property_state("time_step_initialization_option", value)
