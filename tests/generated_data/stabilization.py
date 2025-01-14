# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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


class stabilization(Container):
    """
    'stabilization' child.
    """

    syc_name = "Stabilization"

    property_names_types = [
        ("option", "Option", "str"),
        ("couple_with_global_stabilization", "CoupleWithGlobalStabilization", "bool"),
        ("initial_iterations", "InitialIterations", "int"),
        ("initial_relaxation_factor", "InitialRelaxationFactor", "RealType"),
        ("maximum_retained_time_steps", "MaximumRetainedTimeSteps", "int"),
        ("maximum_retained_iterations", "MaximumRetainedIterations", "int"),
        ("weight_factor", "WeightFactor", "RealType"),
        ("diagnostics_level", "DiagnosticsLevel", "int"),
        ("weight_option", "WeightOption", "str"),
        ("qr_tol_this_step", "QRTolThisStep", "RealType"),
        ("qr_tol_old_steps", "QRTolOldSteps", "RealType"),
        ("time_step_initialization_option", "TimeStepInitializationOption", "str"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'child_object_type' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def couple_with_global_stabilization(self) -> bool:
        """'couple_with_global_stabilization' property of 'child_object_type' object"""
        return self.get_property_state("couple_with_global_stabilization")

    @couple_with_global_stabilization.setter
    def couple_with_global_stabilization(self, value: bool):
        self.set_property_state("couple_with_global_stabilization", value)

    @property
    def initial_iterations(self) -> int:
        """'initial_iterations' property of 'child_object_type' object"""
        return self.get_property_state("initial_iterations")

    @initial_iterations.setter
    def initial_iterations(self, value: int):
        self.set_property_state("initial_iterations", value)

    @property
    def initial_relaxation_factor(self) -> RealType:
        """'initial_relaxation_factor' property of 'child_object_type' object"""
        return self.get_property_state("initial_relaxation_factor")

    @initial_relaxation_factor.setter
    def initial_relaxation_factor(self, value: RealType):
        self.set_property_state("initial_relaxation_factor", value)

    @property
    def maximum_retained_time_steps(self) -> int:
        """'maximum_retained_time_steps' property of 'child_object_type' object"""
        return self.get_property_state("maximum_retained_time_steps")

    @maximum_retained_time_steps.setter
    def maximum_retained_time_steps(self, value: int):
        self.set_property_state("maximum_retained_time_steps", value)

    @property
    def maximum_retained_iterations(self) -> int:
        """'maximum_retained_iterations' property of 'child_object_type' object"""
        return self.get_property_state("maximum_retained_iterations")

    @maximum_retained_iterations.setter
    def maximum_retained_iterations(self, value: int):
        self.set_property_state("maximum_retained_iterations", value)

    @property
    def weight_factor(self) -> RealType:
        """'weight_factor' property of 'child_object_type' object"""
        return self.get_property_state("weight_factor")

    @weight_factor.setter
    def weight_factor(self, value: RealType):
        self.set_property_state("weight_factor", value)

    @property
    def diagnostics_level(self) -> int:
        """'diagnostics_level' property of 'child_object_type' object"""
        return self.get_property_state("diagnostics_level")

    @diagnostics_level.setter
    def diagnostics_level(self, value: int):
        self.set_property_state("diagnostics_level", value)

    @property
    def weight_option(self) -> str:
        """'weight_option' property of 'child_object_type' object"""
        return self.get_property_state("weight_option")

    @weight_option.setter
    def weight_option(self, value: str):
        self.set_property_state("weight_option", value)

    @property
    def qr_tol_this_step(self) -> RealType:
        """'qr_tol_this_step' property of 'child_object_type' object"""
        return self.get_property_state("qr_tol_this_step")

    @qr_tol_this_step.setter
    def qr_tol_this_step(self, value: RealType):
        self.set_property_state("qr_tol_this_step", value)

    @property
    def qr_tol_old_steps(self) -> RealType:
        """'qr_tol_old_steps' property of 'child_object_type' object"""
        return self.get_property_state("qr_tol_old_steps")

    @qr_tol_old_steps.setter
    def qr_tol_old_steps(self, value: RealType):
        self.set_property_state("qr_tol_old_steps", value)

    @property
    def time_step_initialization_option(self) -> str:
        """'time_step_initialization_option' property of 'child_object_type' object"""
        return self.get_property_state("time_step_initialization_option")

    @time_step_initialization_option.setter
    def time_step_initialization_option(self, value: str):
        self.set_property_state("time_step_initialization_option", value)
