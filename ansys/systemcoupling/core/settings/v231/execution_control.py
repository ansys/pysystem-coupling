#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .fluent_input import fluent_input


class execution_control(Group):
    """
    Available when ParticipantType is set to a value other than EXTERNALDATA.
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
        """Method used by System Coupling to find the solver executable file to be used to start the participant."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def working_directory(self) -> String:
        """Participant's working directory for the coupled analysis."""
        return self.get_property_state("working_directory")

    @working_directory.setter
    def working_directory(self, value: String):
        self.set_property_state("working_directory", value)

    @property
    def executable(self) -> String:
        """Available when the ExecutionControl.Option is set to UserDefined or the AddParticipant() command's Executable argument is used in the CLI."""
        return self.get_property_state("executable")

    @executable.setter
    def executable(self, value: String):
        self.set_property_state("executable", value)

    @property
    def auto_distribution_settings(self) -> Boolean:
        """Available for AEDT participants when ExecutionControl.Option is set to UserDefined or ProgramControlled."""
        return self.get_property_state("auto_distribution_settings")

    @auto_distribution_settings.setter
    def auto_distribution_settings(self, value: Boolean):
        self.set_property_state("auto_distribution_settings", value)

    @property
    def include_hpc_distribution_types(self) -> StringList:
        """Available for AEDT participants when ExecutionControl.AutoDistributionSettings is set to False."""
        return self.get_property_state("include_hpc_distribution_types")

    @include_hpc_distribution_types.setter
    def include_hpc_distribution_types(self, value: StringList):
        self.set_property_state("include_hpc_distribution_types", value)

    @property
    def number_of_cores_per_task(self) -> Integer:
        """Available for AEDT participants when ExecutionControl.AutoDistributionSettings is set to False."""
        return self.get_property_state("number_of_cores_per_task")

    @number_of_cores_per_task.setter
    def number_of_cores_per_task(self, value: Integer):
        self.set_property_state("number_of_cores_per_task", value)

    @property
    def batch_options(self) -> String:
        """Available for AEDT participants when ExecutionControl.AutoDistributionSettings is set to False."""
        return self.get_property_state("batch_options")

    @batch_options.setter
    def batch_options(self, value: String):
        self.set_property_state("batch_options", value)

    @property
    def additional_arguments(self) -> String:
        """Arguments to be appended to the participant's executable."""
        return self.get_property_state("additional_arguments")

    @additional_arguments.setter
    def additional_arguments(self, value: String):
        self.set_property_state("additional_arguments", value)

    @property
    def parallel_fraction(self) -> Real:
        """Core count or fraction of compute resources to be allocated to the participant. Used to partition resources across coupling participants that are running in parallel."""
        return self.get_property_state("parallel_fraction")

    @parallel_fraction.setter
    def parallel_fraction(self, value: Real):
        self.set_property_state("parallel_fraction", value)

    @property
    def initial_input(self) -> String:
        """Available for AEDT, CFD Server, CFX, Forte, Mechanical, and Mechanical Server participants."""
        return self.get_property_state("initial_input")

    @initial_input.setter
    def initial_input(self, value: String):
        self.set_property_state("initial_input", value)

    @property
    def additional_restart_input_file(self) -> String:
        """Available for Mechanical participants for restart runs."""
        return self.get_property_state("additional_restart_input_file")

    @additional_restart_input_file.setter
    def additional_restart_input_file(self, value: String):
        self.set_property_state("additional_restart_input_file", value)

    @property
    def gui_mode(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("gui_mode")

    @gui_mode.setter
    def gui_mode(self, value: Boolean):
        self.set_property_state("gui_mode", value)

    @property
    def base_output_file_name(self) -> String:
        """Available for CFD Server participants."""
        return self.get_property_state("base_output_file_name")

    @base_output_file_name.setter
    def base_output_file_name(self, value: String):
        self.set_property_state("base_output_file_name", value)

    @property
    def overwrite_existing_files(self) -> Boolean:
        """Available for CFD Server participants."""
        return self.get_property_state("overwrite_existing_files")

    @overwrite_existing_files.setter
    def overwrite_existing_files(self, value: Boolean):
        self.set_property_state("overwrite_existing_files", value)
