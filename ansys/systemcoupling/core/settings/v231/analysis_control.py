#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .apip import apip
from .global_stabilization import global_stabilization
from .unmapped_value_options import unmapped_value_options


class analysis_control(Group):
    """
    Control the characteristics and behavior of the coupled analysis.
    """

    syc_name = "AnalysisControl"

    child_names = ["global_stabilization", "apip", "unmapped_value_options"]

    global_stabilization: global_stabilization = global_stabilization
    """
    global_stabilization child of analysis_control.
    """
    apip: apip = apip
    """
    apip child of analysis_control.
    """
    unmapped_value_options: unmapped_value_options = unmapped_value_options
    """
    unmapped_value_options child of analysis_control.
    """
    property_names_types = [
        ("analysis_type", "AnalysisType", "String"),
        ("optimize_if_one_way", "OptimizeIfOneWay", "Boolean"),
        ("warped_face_tolerance", "WarpedFaceTolerance", "Real"),
        ("allow_simultaneous_update", "AllowSimultaneousUpdate", "Boolean"),
        ("simultaneous_participants", "SimultaneousParticipants", "String"),
        ("partitioning_algorithm", "PartitioningAlgorithm", "String"),
        ("allow_iterations_only_mode", "AllowIterationsOnlyMode", "Boolean"),
        ("avoid_data_reconstruction", "AvoidDataReconstruction", "Boolean"),
        ("target_initialization_option", "TargetInitializationOption", "String"),
        ("fluent_region_update_at_step", "FluentRegionUpdateAtStep", "Boolean"),
        ("mesh_import_on_initialization", "MeshImportOnInitialization", "Boolean"),
        ("import_all_regions", "ImportAllRegions", "Boolean"),
        ("bypass_fluent_adapter", "BypassFluentAdapter", "Boolean"),
        ("variable_to_expression_transfer", "VariableToExpressionTransfer", "Boolean"),
        ("update_mapping_weights", "UpdateMappingWeights", "String"),
        (
            "solve_incremental_displacement_first",
            "SolveIncrementalDisplacementFirst",
            "Boolean",
        ),
        ("write_scs_file", "WriteScsFile", "Boolean"),
        ("check_for_input_files_changes", "CheckForInputFilesChanges", "String"),
    ]

    @property
    def analysis_type(self) -> String:
        """Type of analysis to be run."""
        return self.get_property_state("analysis_type")

    @analysis_type.setter
    def analysis_type(self, value: String):
        self.set_property_state("analysis_type", value)

    @property
    def optimize_if_one_way(self) -> Boolean:
        """Whether settings are optimized when System Coupling detects that the data transfers are one-way."""
        return self.get_property_state("optimize_if_one_way")

    @optimize_if_one_way.setter
    def optimize_if_one_way(self, value: Boolean):
        self.set_property_state("optimize_if_one_way", value)

    @property
    def warped_face_tolerance(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("warped_face_tolerance")

    @warped_face_tolerance.setter
    def warped_face_tolerance(self, value: Real):
        self.set_property_state("warped_face_tolerance", value)

    @property
    def allow_simultaneous_update(self) -> Boolean:
        """Whether independent participants run simultaneous solutions."""
        return self.get_property_state("allow_simultaneous_update")

    @allow_simultaneous_update.setter
    def allow_simultaneous_update(self, value: Boolean):
        self.set_property_state("allow_simultaneous_update", value)

    @property
    def simultaneous_participants(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("simultaneous_participants")

    @simultaneous_participants.setter
    def simultaneous_participants(self, value: String):
        self.set_property_state("simultaneous_participants", value)

    @property
    def partitioning_algorithm(self) -> String:
        """Partitioning algorithm used when participants are running in parallel."""
        return self.get_property_state("partitioning_algorithm")

    @partitioning_algorithm.setter
    def partitioning_algorithm(self, value: String):
        self.set_property_state("partitioning_algorithm", value)

    @property
    def allow_iterations_only_mode(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("allow_iterations_only_mode")

    @allow_iterations_only_mode.setter
    def allow_iterations_only_mode(self, value: Boolean):
        self.set_property_state("allow_iterations_only_mode", value)

    @property
    def avoid_data_reconstruction(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("avoid_data_reconstruction")

    @avoid_data_reconstruction.setter
    def avoid_data_reconstruction(self, value: Boolean):
        self.set_property_state("avoid_data_reconstruction", value)

    @property
    def target_initialization_option(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("target_initialization_option")

    @target_initialization_option.setter
    def target_initialization_option(self, value: String):
        self.set_property_state("target_initialization_option", value)

    @property
    def fluent_region_update_at_step(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("fluent_region_update_at_step")

    @fluent_region_update_at_step.setter
    def fluent_region_update_at_step(self, value: Boolean):
        self.set_property_state("fluent_region_update_at_step", value)

    @property
    def mesh_import_on_initialization(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("mesh_import_on_initialization")

    @mesh_import_on_initialization.setter
    def mesh_import_on_initialization(self, value: Boolean):
        self.set_property_state("mesh_import_on_initialization", value)

    @property
    def import_all_regions(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("import_all_regions")

    @import_all_regions.setter
    def import_all_regions(self, value: Boolean):
        self.set_property_state("import_all_regions", value)

    @property
    def bypass_fluent_adapter(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("bypass_fluent_adapter")

    @bypass_fluent_adapter.setter
    def bypass_fluent_adapter(self, value: Boolean):
        self.set_property_state("bypass_fluent_adapter", value)

    @property
    def variable_to_expression_transfer(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("variable_to_expression_transfer")

    @variable_to_expression_transfer.setter
    def variable_to_expression_transfer(self, value: Boolean):
        self.set_property_state("variable_to_expression_transfer", value)

    @property
    def update_mapping_weights(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("update_mapping_weights")

    @update_mapping_weights.setter
    def update_mapping_weights(self, value: String):
        self.set_property_state("update_mapping_weights", value)

    @property
    def solve_incremental_displacement_first(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("solve_incremental_displacement_first")

    @solve_incremental_displacement_first.setter
    def solve_incremental_displacement_first(self, value: Boolean):
        self.set_property_state("solve_incremental_displacement_first", value)

    @property
    def write_scs_file(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("write_scs_file")

    @write_scs_file.setter
    def write_scs_file(self, value: Boolean):
        self.set_property_state("write_scs_file", value)

    @property
    def check_for_input_files_changes(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("check_for_input_files_changes")

    @check_for_input_files_changes.setter
    def check_for_input_files_changes(self, value: String):
        self.set_property_state("check_for_input_files_changes", value)
