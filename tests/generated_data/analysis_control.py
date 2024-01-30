# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .apip import apip
from .global_stabilization import global_stabilization
from .unmapped_value_options import unmapped_value_options


class analysis_control(Container):
    """
    'analysis_control' child.
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
        ("analysis_type", "AnalysisType", "str"),
        ("optimize_if_one_way", "OptimizeIfOneWay", "bool"),
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
        ("rotate_follower_forces", "RotateFollowerForces", "str"),
        (
            "solve_incremental_displacement_first",
            "SolveIncrementalDisplacementFirst",
            "bool",
        ),
        ("write_scs_file", "WriteScsFile", "bool"),
    ]

    @property
    def analysis_type(self) -> str:
        """'analysis_type' property of 'setup_root' object"""
        return self.get_property_state("analysis_type")

    @analysis_type.setter
    def analysis_type(self, value: str):
        self.set_property_state("analysis_type", value)

    @property
    def optimize_if_one_way(self) -> bool:
        """'optimize_if_one_way' property of 'setup_root' object"""
        return self.get_property_state("optimize_if_one_way")

    @optimize_if_one_way.setter
    def optimize_if_one_way(self, value: bool):
        self.set_property_state("optimize_if_one_way", value)

    @property
    def allow_simultaneous_update(self) -> bool:
        """'allow_simultaneous_update' property of 'setup_root' object"""
        return self.get_property_state("allow_simultaneous_update")

    @allow_simultaneous_update.setter
    def allow_simultaneous_update(self, value: bool):
        self.set_property_state("allow_simultaneous_update", value)

    @property
    def simultaneous_participants(self) -> str:
        """'simultaneous_participants' property of 'setup_root' object"""
        return self.get_property_state("simultaneous_participants")

    @simultaneous_participants.setter
    def simultaneous_participants(self, value: str):
        self.set_property_state("simultaneous_participants", value)

    @property
    def partitioning_algorithm(self) -> str:
        """'partitioning_algorithm' property of 'setup_root' object"""
        return self.get_property_state("partitioning_algorithm")

    @partitioning_algorithm.setter
    def partitioning_algorithm(self, value: str):
        self.set_property_state("partitioning_algorithm", value)

    @property
    def allow_iterations_only_mode(self) -> bool:
        """'allow_iterations_only_mode' property of 'setup_root' object"""
        return self.get_property_state("allow_iterations_only_mode")

    @allow_iterations_only_mode.setter
    def allow_iterations_only_mode(self, value: bool):
        self.set_property_state("allow_iterations_only_mode", value)

    @property
    def target_initialization_option(self) -> str:
        """'target_initialization_option' property of 'setup_root' object"""
        return self.get_property_state("target_initialization_option")

    @target_initialization_option.setter
    def target_initialization_option(self, value: str):
        self.set_property_state("target_initialization_option", value)

    @property
    def fluent_region_update_at_step(self) -> bool:
        """'fluent_region_update_at_step' property of 'setup_root' object"""
        return self.get_property_state("fluent_region_update_at_step")

    @fluent_region_update_at_step.setter
    def fluent_region_update_at_step(self, value: bool):
        self.set_property_state("fluent_region_update_at_step", value)

    @property
    def mesh_import_on_initialization(self) -> bool:
        """'mesh_import_on_initialization' property of 'setup_root' object"""
        return self.get_property_state("mesh_import_on_initialization")

    @mesh_import_on_initialization.setter
    def mesh_import_on_initialization(self, value: bool):
        self.set_property_state("mesh_import_on_initialization", value)

    @property
    def import_all_regions(self) -> bool:
        """'import_all_regions' property of 'setup_root' object"""
        return self.get_property_state("import_all_regions")

    @import_all_regions.setter
    def import_all_regions(self, value: bool):
        self.set_property_state("import_all_regions", value)

    @property
    def bypass_fluent_adapter(self) -> bool:
        """'bypass_fluent_adapter' property of 'setup_root' object"""
        return self.get_property_state("bypass_fluent_adapter")

    @bypass_fluent_adapter.setter
    def bypass_fluent_adapter(self, value: bool):
        self.set_property_state("bypass_fluent_adapter", value)

    @property
    def variable_to_expression_transfer(self) -> bool:
        """'variable_to_expression_transfer' property of 'setup_root' object"""
        return self.get_property_state("variable_to_expression_transfer")

    @variable_to_expression_transfer.setter
    def variable_to_expression_transfer(self, value: bool):
        self.set_property_state("variable_to_expression_transfer", value)

    @property
    def update_mapping_weights(self) -> str:
        """'update_mapping_weights' property of 'setup_root' object"""
        return self.get_property_state("update_mapping_weights")

    @update_mapping_weights.setter
    def update_mapping_weights(self, value: str):
        self.set_property_state("update_mapping_weights", value)

    @property
    def rotate_follower_forces(self) -> str:
        """'rotate_follower_forces' property of 'setup_root' object"""
        return self.get_property_state("rotate_follower_forces")

    @rotate_follower_forces.setter
    def rotate_follower_forces(self, value: str):
        self.set_property_state("rotate_follower_forces", value)

    @property
    def solve_incremental_displacement_first(self) -> bool:
        """'solve_incremental_displacement_first' property of 'setup_root' object"""
        return self.get_property_state("solve_incremental_displacement_first")

    @solve_incremental_displacement_first.setter
    def solve_incremental_displacement_first(self, value: bool):
        self.set_property_state("solve_incremental_displacement_first", value)

    @property
    def write_scs_file(self) -> bool:
        """'write_scs_file' property of 'setup_root' object"""
        return self.get_property_state("write_scs_file")

    @write_scs_file.setter
    def write_scs_file(self, value: bool):
        self.set_property_state("write_scs_file", value)
