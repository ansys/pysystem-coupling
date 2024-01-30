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


class mapping_control(Container):
    """
    'mapping_control' child.
    """

    syc_name = "MappingControl"

    property_names_types = [
        ("stop_if_poor_intersection", "StopIfPoorIntersection", "bool"),
        ("poor_intersection_threshold", "PoorIntersectionThreshold", "RealType"),
        ("face_alignment", "FaceAlignment", "str"),
        ("absolute_gap_tolerance", "AbsoluteGapTolerance", "RealType"),
        ("relative_gap_tolerance", "RelativeGapTolerance", "RealType"),
        ("small_weight_tolerance", "SmallWeightTolerance", "RealType"),
        ("corner_tolerance", "CornerTolerance", "RealType"),
        ("halo_tolerance", "HaloTolerance", "RealType"),
        (
            "conservative_reciprocity_factor",
            "ConservativeReciprocityFactor",
            "RealType",
        ),
        (
            "profile_preserving_reciprocity_factor",
            "ProfilePreservingReciprocityFactor",
            "RealType",
        ),
        ("conservative_intensive", "ConservativeIntensive", "str"),
        ("preserve_normal", "PreserveNormal", "str"),
        (
            "conservation_fix_tolerance_volume",
            "ConservationFixToleranceVolume",
            "RealType",
        ),
        ("rbf_option", "RBFOption", "str"),
        ("rbf_shape_parameter", "RBFShapeParameter", "RealType"),
        ("rbf_linear_correction", "RBFLinearCorrection", "bool"),
        ("rbf_clipping_scale", "RBFClippingScale", "RealType"),
    ]

    @property
    def stop_if_poor_intersection(self) -> bool:
        """'stop_if_poor_intersection' property of 'child_object_type' object"""
        return self.get_property_state("stop_if_poor_intersection")

    @stop_if_poor_intersection.setter
    def stop_if_poor_intersection(self, value: bool):
        self.set_property_state("stop_if_poor_intersection", value)

    @property
    def poor_intersection_threshold(self) -> RealType:
        """'poor_intersection_threshold' property of 'child_object_type' object"""
        return self.get_property_state("poor_intersection_threshold")

    @poor_intersection_threshold.setter
    def poor_intersection_threshold(self, value: RealType):
        self.set_property_state("poor_intersection_threshold", value)

    @property
    def face_alignment(self) -> str:
        """'face_alignment' property of 'child_object_type' object"""
        return self.get_property_state("face_alignment")

    @face_alignment.setter
    def face_alignment(self, value: str):
        self.set_property_state("face_alignment", value)

    @property
    def absolute_gap_tolerance(self) -> RealType:
        """'absolute_gap_tolerance' property of 'child_object_type' object"""
        return self.get_property_state("absolute_gap_tolerance")

    @absolute_gap_tolerance.setter
    def absolute_gap_tolerance(self, value: RealType):
        self.set_property_state("absolute_gap_tolerance", value)

    @property
    def relative_gap_tolerance(self) -> RealType:
        """'relative_gap_tolerance' property of 'child_object_type' object"""
        return self.get_property_state("relative_gap_tolerance")

    @relative_gap_tolerance.setter
    def relative_gap_tolerance(self, value: RealType):
        self.set_property_state("relative_gap_tolerance", value)

    @property
    def small_weight_tolerance(self) -> RealType:
        """'small_weight_tolerance' property of 'child_object_type' object"""
        return self.get_property_state("small_weight_tolerance")

    @small_weight_tolerance.setter
    def small_weight_tolerance(self, value: RealType):
        self.set_property_state("small_weight_tolerance", value)

    @property
    def corner_tolerance(self) -> RealType:
        """'corner_tolerance' property of 'child_object_type' object"""
        return self.get_property_state("corner_tolerance")

    @corner_tolerance.setter
    def corner_tolerance(self, value: RealType):
        self.set_property_state("corner_tolerance", value)

    @property
    def halo_tolerance(self) -> RealType:
        """'halo_tolerance' property of 'child_object_type' object"""
        return self.get_property_state("halo_tolerance")

    @halo_tolerance.setter
    def halo_tolerance(self, value: RealType):
        self.set_property_state("halo_tolerance", value)

    @property
    def conservative_reciprocity_factor(self) -> RealType:
        """'conservative_reciprocity_factor' property of 'child_object_type' object"""
        return self.get_property_state("conservative_reciprocity_factor")

    @conservative_reciprocity_factor.setter
    def conservative_reciprocity_factor(self, value: RealType):
        self.set_property_state("conservative_reciprocity_factor", value)

    @property
    def profile_preserving_reciprocity_factor(self) -> RealType:
        """'profile_preserving_reciprocity_factor' property of 'child_object_type' object"""
        return self.get_property_state("profile_preserving_reciprocity_factor")

    @profile_preserving_reciprocity_factor.setter
    def profile_preserving_reciprocity_factor(self, value: RealType):
        self.set_property_state("profile_preserving_reciprocity_factor", value)

    @property
    def conservative_intensive(self) -> str:
        """'conservative_intensive' property of 'child_object_type' object"""
        return self.get_property_state("conservative_intensive")

    @conservative_intensive.setter
    def conservative_intensive(self, value: str):
        self.set_property_state("conservative_intensive", value)

    @property
    def preserve_normal(self) -> str:
        """'preserve_normal' property of 'child_object_type' object"""
        return self.get_property_state("preserve_normal")

    @preserve_normal.setter
    def preserve_normal(self, value: str):
        self.set_property_state("preserve_normal", value)

    @property
    def conservation_fix_tolerance_volume(self) -> RealType:
        """'conservation_fix_tolerance_volume' property of 'child_object_type' object"""
        return self.get_property_state("conservation_fix_tolerance_volume")

    @conservation_fix_tolerance_volume.setter
    def conservation_fix_tolerance_volume(self, value: RealType):
        self.set_property_state("conservation_fix_tolerance_volume", value)

    @property
    def rbf_option(self) -> str:
        """'rbf_option' property of 'child_object_type' object"""
        return self.get_property_state("rbf_option")

    @rbf_option.setter
    def rbf_option(self, value: str):
        self.set_property_state("rbf_option", value)

    @property
    def rbf_shape_parameter(self) -> RealType:
        """'rbf_shape_parameter' property of 'child_object_type' object"""
        return self.get_property_state("rbf_shape_parameter")

    @rbf_shape_parameter.setter
    def rbf_shape_parameter(self, value: RealType):
        self.set_property_state("rbf_shape_parameter", value)

    @property
    def rbf_linear_correction(self) -> bool:
        """'rbf_linear_correction' property of 'child_object_type' object"""
        return self.get_property_state("rbf_linear_correction")

    @rbf_linear_correction.setter
    def rbf_linear_correction(self, value: bool):
        self.set_property_state("rbf_linear_correction", value)

    @property
    def rbf_clipping_scale(self) -> RealType:
        """'rbf_clipping_scale' property of 'child_object_type' object"""
        return self.get_property_state("rbf_clipping_scale")

    @rbf_clipping_scale.setter
    def rbf_clipping_scale(self, value: RealType):
        self.set_property_state("rbf_clipping_scale", value)
