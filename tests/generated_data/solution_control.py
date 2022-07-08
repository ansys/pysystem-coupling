#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .available_ports import available_ports
from .get_parameter_options import get_parameter_options


class solution_control(Group):
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
        ("duration_option", "DurationOption", "String"),
        ("end_time", "EndTime", "Real"),
        ("number_of_steps", "NumberOfSteps", "Integer"),
        ("time_step_size", "TimeStepSize", "Real"),
        ("minimum_iterations", "MinimumIterations", "Integer"),
        ("maximum_iterations", "MaximumIterations", "Integer"),
    ]

    @property
    def duration_option(self) -> String:
        """'duration_option' property of 'setup_root' object"""
        return self.get_property_state("duration_option")

    @duration_option.setter
    def duration_option(self, value: String):
        self.set_property_state("duration_option", value)

    @property
    def end_time(self) -> Real:
        """'end_time' property of 'setup_root' object"""
        return self.get_property_state("end_time")

    @end_time.setter
    def end_time(self, value: Real):
        self.set_property_state("end_time", value)

    @property
    def number_of_steps(self) -> Integer:
        """'number_of_steps' property of 'setup_root' object"""
        return self.get_property_state("number_of_steps")

    @number_of_steps.setter
    def number_of_steps(self, value: Integer):
        self.set_property_state("number_of_steps", value)

    @property
    def time_step_size(self) -> Real:
        """'time_step_size' property of 'setup_root' object"""
        return self.get_property_state("time_step_size")

    @time_step_size.setter
    def time_step_size(self, value: Real):
        self.set_property_state("time_step_size", value)

    @property
    def minimum_iterations(self) -> Integer:
        """'minimum_iterations' property of 'setup_root' object"""
        return self.get_property_state("minimum_iterations")

    @minimum_iterations.setter
    def minimum_iterations(self, value: Integer):
        self.set_property_state("minimum_iterations", value)

    @property
    def maximum_iterations(self) -> Integer:
        """'maximum_iterations' property of 'setup_root' object"""
        return self.get_property_state("maximum_iterations")

    @maximum_iterations.setter
    def maximum_iterations(self, value: Integer):
        self.set_property_state("maximum_iterations", value)

    command_names = ["get_parameter_options"]

    get_parameter_options: get_parameter_options = get_parameter_options
    """
    get_parameter_options command of solution_control.
    """
