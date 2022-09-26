#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .fluent_input import fluent_input


class execution_control(Container):
    """
    'execution_control' child.
    """

    syc_name = "ExecutionControl"

    child_names = ["fluent_input"]

    fluent_input: fluent_input = fluent_input
    """
    fluent_input child of execution_control.
    """
    property_names_types = [
        ("option", "Option", "String"),
        ("working_directory", "WorkingDirectory", "String"),
        ("executable", "Executable", "String"),
        ("additional_arguments", "AdditionalArguments", "String"),
        ("parallel_fraction", "ParallelFraction", "Real"),
        ("initial_input", "InitialInput", "String"),
        ("additional_restart_input_file", "AdditionalRestartInputFile", "String"),
        ("gui_mode", "GuiMode", "Boolean"),
    ]

    @property
    def option(self) -> String:
        """'option' property of 'child_object_type' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def working_directory(self) -> String:
        """'working_directory' property of 'child_object_type' object"""
        return self.get_property_state("working_directory")

    @working_directory.setter
    def working_directory(self, value: String):
        self.set_property_state("working_directory", value)

    @property
    def executable(self) -> String:
        """'executable' property of 'child_object_type' object"""
        return self.get_property_state("executable")

    @executable.setter
    def executable(self, value: String):
        self.set_property_state("executable", value)

    @property
    def additional_arguments(self) -> String:
        """'additional_arguments' property of 'child_object_type' object"""
        return self.get_property_state("additional_arguments")

    @additional_arguments.setter
    def additional_arguments(self, value: String):
        self.set_property_state("additional_arguments", value)

    @property
    def parallel_fraction(self) -> Real:
        """'parallel_fraction' property of 'child_object_type' object"""
        return self.get_property_state("parallel_fraction")

    @parallel_fraction.setter
    def parallel_fraction(self, value: Real):
        self.set_property_state("parallel_fraction", value)

    @property
    def initial_input(self) -> String:
        """'initial_input' property of 'child_object_type' object"""
        return self.get_property_state("initial_input")

    @initial_input.setter
    def initial_input(self, value: String):
        self.set_property_state("initial_input", value)

    @property
    def additional_restart_input_file(self) -> String:
        """'additional_restart_input_file' property of 'child_object_type' object"""
        return self.get_property_state("additional_restart_input_file")

    @additional_restart_input_file.setter
    def additional_restart_input_file(self, value: String):
        self.set_property_state("additional_restart_input_file", value)

    @property
    def gui_mode(self) -> Boolean:
        """'gui_mode' property of 'child_object_type' object"""
        return self.get_property_state("gui_mode")

    @gui_mode.setter
    def gui_mode(self, value: Boolean):
        self.set_property_state("gui_mode", value)
