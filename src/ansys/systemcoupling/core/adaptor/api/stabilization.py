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
        ("option", "Option", "str"),
        ("couple_with_global_stabilization", "CoupleWithGlobalStabilization", "bool"),
        ("initial_iterations", "InitialIterations", "int"),
        ("initial_relaxation_factor", "InitialRelaxationFactor", "RealType"),
        ("maximum_retained_time_steps", "MaximumRetainedTimeSteps", "int"),
        ("maximum_retained_iterations", "MaximumRetainedIterations", "int"),
        ("weight_factor", "WeightFactor", "RealType"),
        ("diagnostics_level", "DiagnosticsLevel", "int"),
        ("weight_option", "WeightOption", "str"),
        ("qr_tol_this_step", "QRTolThisStep", "RealType"),
        ("qr_tol_old_steps", "QRTolOldSteps", "RealType"),
        ("time_step_initialization_option", "TimeStepInitializationOption", "str"),
    ]

    @property
    def option(self) -> str:
        """Allowed values:

        - \"ProgramControlled\"
        - \"None\"
        - \"Quasi-Newton\"
        - \"Aitken\" (Alpha only)"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def couple_with_global_stabilization(self) -> bool:
        """Controls whether the stabilization for this data transfer is coupled with the global stabilization."""
        return self.get_property_state("couple_with_global_stabilization")

    @couple_with_global_stabilization.setter
    def couple_with_global_stabilization(self, value: bool):
        self.set_property_state("couple_with_global_stabilization", value)

    @property
    def initial_iterations(self) -> int:
        """Number of pre-stabilization iterations to perform."""
        return self.get_property_state("initial_iterations")

    @initial_iterations.setter
    def initial_iterations(self, value: int):
        self.set_property_state("initial_iterations", value)

    @property
    def initial_relaxation_factor(self) -> RealType:
        """Relaxation factor applied for pre-stabilization iterations."""
        return self.get_property_state("initial_relaxation_factor")

    @initial_relaxation_factor.setter
    def initial_relaxation_factor(self, value: RealType):
        self.set_property_state("initial_relaxation_factor", value)

    @property
    def maximum_retained_time_steps(self) -> int:
        """Controls the maximum number of timesteps to retain."""
        return self.get_property_state("maximum_retained_time_steps")

    @maximum_retained_time_steps.setter
    def maximum_retained_time_steps(self, value: int):
        self.set_property_state("maximum_retained_time_steps", value)

    @property
    def maximum_retained_iterations(self) -> int:
        """Controls the maximum number of iterations to retain."""
        return self.get_property_state("maximum_retained_iterations")

    @maximum_retained_iterations.setter
    def maximum_retained_iterations(self, value: int):
        self.set_property_state("maximum_retained_iterations", value)

    @property
    def weight_factor(self) -> RealType:
        """Weighting factor to use for this data transfer in IQN-ILS."""
        return self.get_property_state("weight_factor")

    @weight_factor.setter
    def weight_factor(self, value: RealType):
        self.set_property_state("weight_factor", value)

    @property
    def diagnostics_level(self) -> int:
        """Controls the maximum number of timesteps to retain.

        Values are interpreted as:

        - 0 : none
        - 1 : basic
        - 2 : advanced
        - 3 : write matrix files"""
        return self.get_property_state("diagnostics_level")

    @diagnostics_level.setter
    def diagnostics_level(self, value: int):
        self.set_property_state("diagnostics_level", value)

    @property
    def weight_option(self) -> str:
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
    def weight_option(self, value: str):
        self.set_property_state("weight_option", value)

    @property
    def qr_tol_this_step(self) -> RealType:
        """QR filter tolerance for current step."""
        return self.get_property_state("qr_tol_this_step")

    @qr_tol_this_step.setter
    def qr_tol_this_step(self, value: RealType):
        self.set_property_state("qr_tol_this_step", value)

    @property
    def qr_tol_old_steps(self) -> RealType:
        """QR filter tolerance for old steps."""
        return self.get_property_state("qr_tol_old_steps")

    @qr_tol_old_steps.setter
    def qr_tol_old_steps(self, value: RealType):
        self.set_property_state("qr_tol_old_steps", value)

    @property
    def time_step_initialization_option(self) -> str:
        """Controls how Aitken relaxation factor is initialized at start of new timestep."""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: str):
        self.set_property_state("time_step_initialization_option", value)
