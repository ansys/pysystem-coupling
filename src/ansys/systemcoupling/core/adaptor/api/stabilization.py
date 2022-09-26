#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class stabilization(Container):
    """
    Stabilization and Acceleration method.
    """

    syc_name = "Stabilization"

    property_names_types = [
        ("option", "Option", "String"),
        (
            "couple_with_global_stabilization",
            "CoupleWithGlobalStabilization",
            "Boolean",
        ),
        ("initial_iterations", "InitialIterations", "Integer"),
        ("initial_relaxation_factor", "InitialRelaxationFactor", "Real"),
        ("maximum_retained_time_steps", "MaximumRetainedTimeSteps", "Integer"),
        ("maximum_retained_iterations", "MaximumRetainedIterations", "Integer"),
        ("weight_factor", "WeightFactor", "Real"),
        ("diagnostics_level", "DiagnosticsLevel", "Integer"),
        ("weight_option", "WeightOption", "String"),
        ("qr_tol_this_step", "QRTolThisStep", "Real"),
        ("qr_tol_old_steps", "QRTolOldSteps", "Real"),
        ("time_step_initialization_option", "TimeStepInitializationOption", "String"),
    ]

    @property
    def option(self) -> String:
        """Allowed values:

        - \"ProgramControlled\"
        - \"None\"
        - \"Quasi-Newton\"
        - \"Aitken\" (Alpha only)"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def couple_with_global_stabilization(self) -> Boolean:
        """Controls whether the stabilization for this data transfer is coupled with the global stabilization."""
        return self.get_property_state("couple_with_global_stabilization")

    @couple_with_global_stabilization.setter
    def couple_with_global_stabilization(self, value: Boolean):
        self.set_property_state("couple_with_global_stabilization", value)

    @property
    def initial_iterations(self) -> Integer:
        """Number of pre-stabilization iterations to perform."""
        return self.get_property_state("initial_iterations")

    @initial_iterations.setter
    def initial_iterations(self, value: Integer):
        self.set_property_state("initial_iterations", value)

    @property
    def initial_relaxation_factor(self) -> Real:
        """Relaxation factor applied for pre-stabilization iterations."""
        return self.get_property_state("initial_relaxation_factor")

    @initial_relaxation_factor.setter
    def initial_relaxation_factor(self, value: Real):
        self.set_property_state("initial_relaxation_factor", value)

    @property
    def maximum_retained_time_steps(self) -> Integer:
        """Controls the maximum number of timesteps to retain."""
        return self.get_property_state("maximum_retained_time_steps")

    @maximum_retained_time_steps.setter
    def maximum_retained_time_steps(self, value: Integer):
        self.set_property_state("maximum_retained_time_steps", value)

    @property
    def maximum_retained_iterations(self) -> Integer:
        """Controls the maximum number of iterations to retain."""
        return self.get_property_state("maximum_retained_iterations")

    @maximum_retained_iterations.setter
    def maximum_retained_iterations(self, value: Integer):
        self.set_property_state("maximum_retained_iterations", value)

    @property
    def weight_factor(self) -> Real:
        """Weighting factor to use for this data transfer in IQN-ILS."""
        return self.get_property_state("weight_factor")

    @weight_factor.setter
    def weight_factor(self, value: Real):
        self.set_property_state("weight_factor", value)

    @property
    def diagnostics_level(self) -> Integer:
        """Controls the maximum number of timesteps to retain.

        Values are interpreted as:

        - 0 : none
        - 1 : basic
        - 2 : advanced
        - 3 : write matrix files"""
        return self.get_property_state("diagnostics_level")

    @diagnostics_level.setter
    def diagnostics_level(self, value: Integer):
        self.set_property_state("diagnostics_level", value)

    @property
    def weight_option(self) -> String:
        """Weight factor when multiple transfers are stabilized.

        Allowed values:

        - \"Constant\"
        - \"Value\"
        - \"Residual\"
        - \"ResidualSum\"
        - \"InverseResidual\"
        - \"InverseResidualSum\" """
        return self.get_property_state("weight_option")

    @weight_option.setter
    def weight_option(self, value: String):
        self.set_property_state("weight_option", value)

    @property
    def qr_tol_this_step(self) -> Real:
        """QR filter tolerance for current step."""
        return self.get_property_state("qr_tol_this_step")

    @qr_tol_this_step.setter
    def qr_tol_this_step(self, value: Real):
        self.set_property_state("qr_tol_this_step", value)

    @property
    def qr_tol_old_steps(self) -> Real:
        """QR filter tolerance for old steps."""
        return self.get_property_state("qr_tol_old_steps")

    @qr_tol_old_steps.setter
    def qr_tol_old_steps(self, value: Real):
        self.set_property_state("qr_tol_old_steps", value)

    @property
    def time_step_initialization_option(self) -> String:
        """Controls how Aitken relaxation factor is initialized at start of new timestep."""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: String):
        self.set_property_state("time_step_initialization_option", value)
