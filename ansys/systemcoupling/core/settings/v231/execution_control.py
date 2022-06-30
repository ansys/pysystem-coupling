#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .fluent_input import fluent_input


class execution_control(Group):
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
        ("auto_distribution_settings", "AutoDistributionSettings", "Boolean"),
        ("include_hpc_distribution_types", "IncludeHPCDistributionTypes", "StringList"),
        ("number_of_cores_per_task", "NumberOfCoresPerTask", "Integer"),
        ("batch_options", "BatchOptions", "String"),
        ("additional_arguments", "AdditionalArguments", "String"),
        ("parallel_fraction", "ParallelFraction", "Real"),
        ("initial_input", "InitialInput", "String"),
        ("additional_restart_input_file", "AdditionalRestartInputFile", "String"),
        ("gui_mode", "GuiMode", "Boolean"),
        ("base_output_file_name", "BaseOutputFileName", "String"),
        ("overwrite_existing_files", "OverwriteExistingFiles", "Boolean"),
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
    def auto_distribution_settings(self) -> Boolean:
        """'auto_distribution_settings' property of 'child_object_type' object"""
        return self.get_property_state("auto_distribution_settings")

    @auto_distribution_settings.setter
    def auto_distribution_settings(self, value: Boolean):
        self.set_property_state("auto_distribution_settings", value)

    @property
    def include_hpc_distribution_types(self) -> StringList:
        """'include_hpc_distribution_types' property of 'child_object_type' object"""
        return self.get_property_state("include_hpc_distribution_types")

    @include_hpc_distribution_types.setter
    def include_hpc_distribution_types(self, value: StringList):
        self.set_property_state("include_hpc_distribution_types", value)

    @property
    def number_of_cores_per_task(self) -> Integer:
        """'number_of_cores_per_task' property of 'child_object_type' object"""
        return self.get_property_state("number_of_cores_per_task")

    @number_of_cores_per_task.setter
    def number_of_cores_per_task(self, value: Integer):
        self.set_property_state("number_of_cores_per_task", value)

    @property
    def batch_options(self) -> String:
        """'batch_options' property of 'child_object_type' object"""
        return self.get_property_state("batch_options")

    @batch_options.setter
    def batch_options(self, value: String):
        self.set_property_state("batch_options", value)

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

    @property
    def base_output_file_name(self) -> String:
        """'base_output_file_name' property of 'child_object_type' object"""
        return self.get_property_state("base_output_file_name")

    @base_output_file_name.setter
    def base_output_file_name(self, value: String):
        self.set_property_state("base_output_file_name", value)

    @property
    def overwrite_existing_files(self) -> Boolean:
        """'overwrite_existing_files' property of 'child_object_type' object"""
        return self.get_property_state("overwrite_existing_files")

    @overwrite_existing_files.setter
    def overwrite_existing_files(self, value: Boolean):
        self.set_property_state("overwrite_existing_files", value)
