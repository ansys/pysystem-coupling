#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .stabilization import stabilization


class data_transfer_child(Group):
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
        """Display name of the data transfer."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def suppress(self) -> Boolean:
        """Controls whether this data transfer is suppressed"""
        return self.get_property_state("suppress")

    @suppress.setter
    def suppress(self, value: Boolean):
        self.set_property_state("suppress", value)

    @property
    def target_side(self) -> String:
        """Target side (\"One\" or \"Two\") of this data transfer."""
        return self.get_property_state("target_side")

    @target_side.setter
    def target_side(self, value: String):
        self.set_property_state("target_side", value)

    @property
    def option(self) -> String:
        """How the transfer data is specified.

        Allowed values:

        - \"UsingVariable\" - The data being transferred is defined as a
          single source-side variable.

        - \"UsingExpression\" - The data being transferred is defined as
          an expression in terms of source-side variables."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def source_variable(self) -> String:
        """Variable associated with the source side of the interface.

        Specified only for variable-based transfers (and not expression-based)."""
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
        """Expression string (or constant real value) defining the data being
        transferred from the source.

        Specified only for expression-based transfers.

        Any variable referenced must be a source side variable."""
        return self.get_property_state("value")

    @value.setter
    def value(self, value: Real):
        self.set_property_state("value", value)

    @property
    def ramping_option(self) -> String:
        """Specify whether to apply ramping to the data transfer.

        Ramping is used to slow the application of the source-side value on the
        target side of the interface.

        Allowed values:

        - \"None\" - No ramping to be applied.

        - \"Linear\" - Apply linear ramping."""
        return self.get_property_state("ramping_option")

    @ramping_option.setter
    def ramping_option(self, value: String):
        self.set_property_state("ramping_option", value)

    @property
    def relaxation_factor(self) -> Real:
        """Factor multiplying the current data transfer values for specified quantity when
        under-relaxing them against the previous values."""
        return self.get_property_state("relaxation_factor")

    @relaxation_factor.setter
    def relaxation_factor(self, value: Real):
        self.set_property_state("relaxation_factor", value)

    @property
    def convergence_target(self) -> Real:
        """RMS-based target value used when evaluating convergence of the specified
        quantity within a coupling iteration."""
        return self.get_property_state("convergence_target")

    @convergence_target.setter
    def convergence_target(self, value: Real):
        self.set_property_state("convergence_target", value)

    @property
    def mapping_type(self) -> String:
        """Type of mapping used for the data transfer. (**Read only**.)

        Possible values:

        - \"Conservative\" - A conservative mapping algorithm is used
          for transfers of `extensive` quantities.
        - \"ProfilePreserving\" - A profile-preserving mapping algorithm
          is used for transfers of `intensive` quantities."""
        return self.get_property_state("mapping_type")

    @mapping_type.setter
    def mapping_type(self, value: String):
        self.set_property_state("mapping_type", value)

    @property
    def unmapped_value_option(self) -> String:
        """Option to fill target values not mapped by the regular mapping algorithm"""
        return self.get_property_state("unmapped_value_option")

    @unmapped_value_option.setter
    def unmapped_value_option(self, value: String):
        self.set_property_state("unmapped_value_option", value)

    @property
    def time_step_initialization_option(self) -> String:
        """Method to initialize first transfer in new coupling step."""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: String):
        self.set_property_state("time_step_initialization_option", value)
