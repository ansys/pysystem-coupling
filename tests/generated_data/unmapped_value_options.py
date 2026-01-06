# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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


class unmapped_value_options(Container):
    """
    'unmapped_value_options' child.
    """

    syc_name = "UnmappedValueOptions"

    property_names_types = [
        ("matrix_verbosity", "MatrixVerbosity", "int"),
        ("solver_verbosity", "SolverVerbosity", "int"),
        ("solver", "Solver", "str"),
        ("solver_relative_tolerance", "SolverRelativeTolerance", "RealType"),
        ("solver_max_iterations", "SolverMaxIterations", "int"),
        ("solver_max_search_directions", "SolverMaxSearchDirections", "int"),
        ("preconditioner", "Preconditioner", "str"),
        ("ilut_tau", "IlutTau", "RealType"),
        ("ilut_max_fill", "IlutMaxFill", "int"),
        ("ilut_pivot_tol", "IlutPivotTol", "RealType"),
        ("face_filter_tolerance", "FaceFilterTolerance", "RealType"),
        ("rbf_shape_parameter", "RbfShapeParameter", "RealType"),
        ("rbf_linear_correction", "RbfLinearCorrection", "bool"),
        ("rbf_colinearity_tolerance", "RbfColinearityTolerance", "RealType"),
    ]

    @property
    def matrix_verbosity(self) -> int:
        """'matrix_verbosity' property of 'analysis_control' object"""
        return self.get_property_state("matrix_verbosity")

    @matrix_verbosity.setter
    def matrix_verbosity(self, value: int):
        self.set_property_state("matrix_verbosity", value)

    @property
    def solver_verbosity(self) -> int:
        """'solver_verbosity' property of 'analysis_control' object"""
        return self.get_property_state("solver_verbosity")

    @solver_verbosity.setter
    def solver_verbosity(self, value: int):
        self.set_property_state("solver_verbosity", value)

    @property
    def solver(self) -> str:
        """'solver' property of 'analysis_control' object"""
        return self.get_property_state("solver")

    @solver.setter
    def solver(self, value: str):
        self.set_property_state("solver", value)

    @property
    def solver_relative_tolerance(self) -> RealType:
        """'solver_relative_tolerance' property of 'analysis_control' object"""
        return self.get_property_state("solver_relative_tolerance")

    @solver_relative_tolerance.setter
    def solver_relative_tolerance(self, value: RealType):
        self.set_property_state("solver_relative_tolerance", value)

    @property
    def solver_max_iterations(self) -> int:
        """'solver_max_iterations' property of 'analysis_control' object"""
        return self.get_property_state("solver_max_iterations")

    @solver_max_iterations.setter
    def solver_max_iterations(self, value: int):
        self.set_property_state("solver_max_iterations", value)

    @property
    def solver_max_search_directions(self) -> int:
        """'solver_max_search_directions' property of 'analysis_control' object"""
        return self.get_property_state("solver_max_search_directions")

    @solver_max_search_directions.setter
    def solver_max_search_directions(self, value: int):
        self.set_property_state("solver_max_search_directions", value)

    @property
    def preconditioner(self) -> str:
        """'preconditioner' property of 'analysis_control' object"""
        return self.get_property_state("preconditioner")

    @preconditioner.setter
    def preconditioner(self, value: str):
        self.set_property_state("preconditioner", value)

    @property
    def ilut_tau(self) -> RealType:
        """'ilut_tau' property of 'analysis_control' object"""
        return self.get_property_state("ilut_tau")

    @ilut_tau.setter
    def ilut_tau(self, value: RealType):
        self.set_property_state("ilut_tau", value)

    @property
    def ilut_max_fill(self) -> int:
        """'ilut_max_fill' property of 'analysis_control' object"""
        return self.get_property_state("ilut_max_fill")

    @ilut_max_fill.setter
    def ilut_max_fill(self, value: int):
        self.set_property_state("ilut_max_fill", value)

    @property
    def ilut_pivot_tol(self) -> RealType:
        """'ilut_pivot_tol' property of 'analysis_control' object"""
        return self.get_property_state("ilut_pivot_tol")

    @ilut_pivot_tol.setter
    def ilut_pivot_tol(self, value: RealType):
        self.set_property_state("ilut_pivot_tol", value)

    @property
    def face_filter_tolerance(self) -> RealType:
        """'face_filter_tolerance' property of 'analysis_control' object"""
        return self.get_property_state("face_filter_tolerance")

    @face_filter_tolerance.setter
    def face_filter_tolerance(self, value: RealType):
        self.set_property_state("face_filter_tolerance", value)

    @property
    def rbf_shape_parameter(self) -> RealType:
        """'rbf_shape_parameter' property of 'analysis_control' object"""
        return self.get_property_state("rbf_shape_parameter")

    @rbf_shape_parameter.setter
    def rbf_shape_parameter(self, value: RealType):
        self.set_property_state("rbf_shape_parameter", value)

    @property
    def rbf_linear_correction(self) -> bool:
        """'rbf_linear_correction' property of 'analysis_control' object"""
        return self.get_property_state("rbf_linear_correction")

    @rbf_linear_correction.setter
    def rbf_linear_correction(self, value: bool):
        self.set_property_state("rbf_linear_correction", value)

    @property
    def rbf_colinearity_tolerance(self) -> RealType:
        """'rbf_colinearity_tolerance' property of 'analysis_control' object"""
        return self.get_property_state("rbf_colinearity_tolerance")

    @rbf_colinearity_tolerance.setter
    def rbf_colinearity_tolerance(self, value: RealType):
        self.set_property_state("rbf_colinearity_tolerance", value)
