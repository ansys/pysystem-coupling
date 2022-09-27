#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .apip import apip
from .avoid_data_reconstruction import avoid_data_reconstruction
from .global_stabilization import global_stabilization
from .unmapped_value_options import unmapped_value_options


class analysis_control(Container):
    """
    Configure coupling controls.
    """

    syc_name = "AnalysisControl"

    child_names = [
        "global_stabilization",
        "apip",
        "avoid_data_reconstruction",
        "unmapped_value_options",
    ]

    global_stabilization: global_stabilization = global_stabilization
    """
    global_stabilization child of analysis_control.
    """
    apip: apip = apip
    """
    apip child of analysis_control.
    """
    avoid_data_reconstruction: avoid_data_reconstruction = avoid_data_reconstruction
    """
    avoid_data_reconstruction child of analysis_control.
    """
    unmapped_value_options: unmapped_value_options = unmapped_value_options
    """
    unmapped_value_options child of analysis_control.
    """
    property_names_types = [
        ("analysis_type", "AnalysisType", "str"),
        ("optimize_if_one_way", "OptimizeIfOneWay", "bool"),
        ("warped_face_tolerance", "WarpedFaceTolerance", "RealType"),
        ("allow_simultaneous_update", "AllowSimultaneousUpdate", "bool"),
        ("simultaneous_participants", "SimultaneousParticipants", "str"),
        ("partitioning_algorithm", "PartitioningAlgorithm", "str"),
        ("allow_iterations_only_mode", "AllowIterationsOnlyMode", "bool"),
        ("target_initialization_option", "TargetInitializationOption", "str"),
        ("fluent_region_update_at_step", "FluentRegionUpdateAtStep", "bool"),
        ("mesh_import_on_initialization", "MeshImportOnInitialization", "bool"),
        ("import_all_regions", "ImportAllRegions", "bool"),
        ("bypass_fluent_adapter", "BypassFluentAdapter", "bool"),
        ("variable_to_expression_transfer", "VariableToExpressionTransfer", "bool"),
        ("update_mapping_weights", "UpdateMappingWeights", "str"),
        (
            "solve_incremental_displacement_first",
            "SolveIncrementalDisplacementFirst",
            "bool",
        ),
        ("write_scs_file", "WriteScsFile", "bool"),
        ("check_for_input_files_changes", "CheckForInputFilesChanges", "str"),
    ]

    @property
    def analysis_type(self) -> str:
        """Analysis type.

        Allowed values:
        - \"Steady\"
        - \"Transient\" """
        return self.get_property_state("analysis_type")

    @analysis_type.setter
    def analysis_type(self, value: str):
        self.set_property_state("analysis_type", value)

    @property
    def optimize_if_one_way(self) -> bool:
        """Optimizes various controls for a one-way workflow, if the
        data transfers form a unidirectional graph."""
        return self.get_property_state("optimize_if_one_way")

    @optimize_if_one_way.setter
    def optimize_if_one_way(self, value: bool):
        self.set_property_state("optimize_if_one_way", value)

    @property
    def warped_face_tolerance(self) -> RealType:
        """Set warped face detection tolerance (1e-6 is default value, 1.0 means disabled)."""
        return self.get_property_state("warped_face_tolerance")

    @warped_face_tolerance.setter
    def warped_face_tolerance(self, value: RealType):
        self.set_property_state("warped_face_tolerance", value)

    @property
    def allow_simultaneous_update(self) -> bool:
        """Allow simultaneous update of independent participants."""
        return self.get_property_state("allow_simultaneous_update")

    @allow_simultaneous_update.setter
    def allow_simultaneous_update(self, value: bool):
        self.set_property_state("allow_simultaneous_update", value)

    @property
    def simultaneous_participants(self) -> str:
        """Controls which participants are updated simultaneously."""
        return self.get_property_state("simultaneous_participants")

    @simultaneous_participants.setter
    def simultaneous_participants(self, value: str):
        self.set_property_state("simultaneous_participants", value)

    @property
    def partitioning_algorithm(self) -> str:
        """Partitioning algorithm used when participants are running in parallel.

        Allowed values:

        - \"SharedAllocateMachines\" - Participants share both machines and cores.

        - \"SharedAllocateCores\" - Participants share machines but not cores.

        - \"DistributedAllocateCores\" - Participants minimally share cores and machines. (Linux only)

        - \"DistributedAllocateMachines\" - Participants never share cores or machines. (Linux only)

        - \"Custom\" - Custom algorithm."""
        return self.get_property_state("partitioning_algorithm")

    @partitioning_algorithm.setter
    def partitioning_algorithm(self, value: str):
        self.set_property_state("partitioning_algorithm", value)

    @property
    def allow_iterations_only_mode(self) -> bool:
        """Explicitly set whether iterations-only mode is allowed."""
        return self.get_property_state("allow_iterations_only_mode")

    @allow_iterations_only_mode.setter
    def allow_iterations_only_mode(self, value: bool):
        self.set_property_state("allow_iterations_only_mode", value)

    @property
    def target_initialization_option(self) -> str:
        """Select option for target initialization."""
        return self.get_property_state("target_initialization_option")

    @target_initialization_option.setter
    def target_initialization_option(self, value: str):
        self.set_property_state("target_initialization_option", value)

    @property
    def fluent_region_update_at_step(self) -> bool:
        """Allow update of Fluent regions at the beginning of a step."""
        return self.get_property_state("fluent_region_update_at_step")

    @fluent_region_update_at_step.setter
    def fluent_region_update_at_step(self, value: bool):
        self.set_property_state("fluent_region_update_at_step", value)

    @property
    def mesh_import_on_initialization(self) -> bool:
        """Select whether to import the mesh during the analysis initialization."""
        return self.get_property_state("mesh_import_on_initialization")

    @mesh_import_on_initialization.setter
    def mesh_import_on_initialization(self, value: bool):
        self.set_property_state("mesh_import_on_initialization", value)

    @property
    def import_all_regions(self) -> bool:
        """Select whether to import mesh for all defined regions."""
        return self.get_property_state("import_all_regions")

    @import_all_regions.setter
    def import_all_regions(self, value: bool):
        self.set_property_state("import_all_regions", value)

    @property
    def bypass_fluent_adapter(self) -> bool:
        """Switch to bypass Fluent adapter."""
        return self.get_property_state("bypass_fluent_adapter")

    @bypass_fluent_adapter.setter
    def bypass_fluent_adapter(self, value: bool):
        self.set_property_state("bypass_fluent_adapter", value)

    @property
    def variable_to_expression_transfer(self) -> bool:
        """Convert variable-based data transfers to expression transfers."""
        return self.get_property_state("variable_to_expression_transfer")

    @variable_to_expression_transfer.setter
    def variable_to_expression_transfer(self, value: bool):
        self.set_property_state("variable_to_expression_transfer", value)

    @property
    def update_mapping_weights(self) -> str:
        """Weight factor when multiple transfers are stabilized.

        Allowed values:

        - \"Off\" (default)
        - \"EveryStep\"
        - \"EveryIteration\" """
        return self.get_property_state("update_mapping_weights")

    @update_mapping_weights.setter
    def update_mapping_weights(self, value: str):
        self.set_property_state("update_mapping_weights", value)

    @property
    def solve_incremental_displacement_first(self) -> bool:
        """Force participants serving incremental displacement to solve first."""
        return self.get_property_state("solve_incremental_displacement_first")

    @solve_incremental_displacement_first.setter
    def solve_incremental_displacement_first(self, value: bool):
        self.set_property_state("solve_incremental_displacement_first", value)

    @property
    def write_scs_file(self) -> bool:
        """Force writing of scs file even if participants are auto-started."""
        return self.get_property_state("write_scs_file")

    @write_scs_file.setter
    def write_scs_file(self, value: bool):
        self.set_property_state("write_scs_file", value)

    @property
    def check_for_input_files_changes(self) -> str:
        """Controls whether System Coupling will check for changes in participant input files."""
        return self.get_property_state("check_for_input_files_changes")

    @check_for_input_files_changes.setter
    def check_for_input_files_changes(self, value: str):
        self.set_property_state("check_for_input_files_changes", value)
