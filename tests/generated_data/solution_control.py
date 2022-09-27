#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .available_ports import available_ports
from .get_parameter_options import get_parameter_options


class solution_control(Container):
    """
    'solution_control' child.
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
        """'duration_option' property of 'setup_root' object"""
        return self.get_property_state("duration_option")

    @duration_option.setter
    def duration_option(self, value: str):
        self.set_property_state("duration_option", value)

    @property
    def end_time(self) -> RealType:
        """'end_time' property of 'setup_root' object"""
        return self.get_property_state("end_time")

    @end_time.setter
    def end_time(self, value: RealType):
        self.set_property_state("end_time", value)

    @property
    def number_of_steps(self) -> int:
        """'number_of_steps' property of 'setup_root' object"""
        return self.get_property_state("number_of_steps")

    @number_of_steps.setter
    def number_of_steps(self, value: int):
        self.set_property_state("number_of_steps", value)

    @property
    def time_step_size(self) -> RealType:
        """'time_step_size' property of 'setup_root' object"""
        return self.get_property_state("time_step_size")

    @time_step_size.setter
    def time_step_size(self, value: RealType):
        self.set_property_state("time_step_size", value)

    @property
    def minimum_iterations(self) -> int:
        """'minimum_iterations' property of 'setup_root' object"""
        return self.get_property_state("minimum_iterations")

    @minimum_iterations.setter
    def minimum_iterations(self, value: int):
        self.set_property_state("minimum_iterations", value)

    @property
    def maximum_iterations(self) -> int:
        """'maximum_iterations' property of 'setup_root' object"""
        return self.get_property_state("maximum_iterations")

    @maximum_iterations.setter
    def maximum_iterations(self, value: int):
        self.set_property_state("maximum_iterations", value)

    command_names = ["get_parameter_options"]

    get_parameter_options: get_parameter_options = get_parameter_options
    """
    get_parameter_options command of solution_control.
    """
