#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .available_ports import available_ports


class solution_control(Container):
    """
    Configure solution controls.
    """

    syc_name = "SolutionControl"

    child_names = ["available_ports"]

    available_ports: available_ports = available_ports
    """
    available_ports child of solution_control.
    """
    property_names_types = [
        ("duration_option", "DurationOption", "str"),
        ("end_time", "EndTime", "RealType"),
        ("number_of_steps", "NumberOfSteps", "int"),
        ("time_step_size", "TimeStepSize", "RealType"),
        ("minimum_iterations", "MinimumIterations", "int"),
        ("maximum_iterations", "MaximumIterations", "int"),
    ]

    @property
    def duration_option(self) -> str:
        """Determine how the analysis duration is specified.

        Allowed values:

        - \"EndTime\" - Available for transient analyses. Execute coupling
          steps until the analysis reaches the specified end time.
        - \"NumberOfSteps\" - Perform coupling steps until the specified
          number of steps is reached."""
        return self.get_property_state("duration_option")

    @duration_option.setter
    def duration_option(self, value: str):
        self.set_property_state("duration_option", value)

    @property
    def end_time(self) -> RealType:
        """Set co-simulation end time."""
        return self.get_property_state("end_time")

    @end_time.setter
    def end_time(self, value: RealType):
        self.set_property_state("end_time", value)

    @property
    def number_of_steps(self) -> int:
        """Set number of coupling steps."""
        return self.get_property_state("number_of_steps")

    @number_of_steps.setter
    def number_of_steps(self, value: int):
        self.set_property_state("number_of_steps", value)

    @property
    def time_step_size(self) -> RealType:
        """Set coupling time step size."""
        return self.get_property_state("time_step_size")

    @time_step_size.setter
    def time_step_size(self, value: RealType):
        self.set_property_state("time_step_size", value)

    @property
    def minimum_iterations(self) -> int:
        """Set minimum iterations within coupling step."""
        return self.get_property_state("minimum_iterations")

    @minimum_iterations.setter
    def minimum_iterations(self, value: int):
        self.set_property_state("minimum_iterations", value)

    @property
    def maximum_iterations(self) -> int:
        """Set maximum iterations within coupling step."""
        return self.get_property_state("maximum_iterations")

    @maximum_iterations.setter
    def maximum_iterations(self, value: int):
        self.set_property_state("maximum_iterations", value)
