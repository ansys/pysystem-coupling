#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class mapping_control(Group):
    """
    Control mapping settings for the coupling interface.
    """

    syc_name = "MappingControl"

    property_names_types = [
        ("stop_if_poor_intersection", "StopIfPoorIntersection", "Boolean"),
        ("poor_intersection_threshold", "PoorIntersectionThreshold", "Real"),
        ("face_alignment", "FaceAlignment", "String"),
        ("absolute_gap_tolerance", "AbsoluteGapTolerance", "Real"),
        ("relative_gap_tolerance", "RelativeGapTolerance", "Real"),
        ("small_weight_tolerance", "SmallWeightTolerance", "Real"),
        ("corner_tolerance", "CornerTolerance", "Real"),
        ("halo_tolerance", "HaloTolerance", "Real"),
        ("conservative_reciprocity_factor", "ConservativeReciprocityFactor", "Real"),
        (
            "profile_preserving_reciprocity_factor",
            "ProfilePreservingReciprocityFactor",
            "Real",
        ),
        ("conservative_intensive", "ConservativeIntensive", "String"),
        ("preserve_normal", "PreserveNormal", "String"),
        ("conservation_fix_tolerance_volume", "ConservationFixToleranceVolume", "Real"),
        ("rbf_option", "RBFOption", "String"),
        ("rbf_shape_parameter", "RBFShapeParameter", "Real"),
        ("rbf_linear_correction", "RBFLinearCorrection", "Boolean"),
        ("rbf_clipping_scale", "RBFClippingScale", "Real"),
    ]

    @property
    def stop_if_poor_intersection(self) -> Boolean:
        """Control whether System Coupling stops when the intersection between coupling interface sides is below a specified threshold, indicating a possible setup error."""
        return self.get_property_state("stop_if_poor_intersection")

    @stop_if_poor_intersection.setter
    def stop_if_poor_intersection(self, value: Boolean):
        self.set_property_state("stop_if_poor_intersection", value)

    @property
    def poor_intersection_threshold(self) -> Real:
        """Defines the threshold at which System Coupling stops if the intersection between coupling interface sides is low."""
        return self.get_property_state("poor_intersection_threshold")

    @poor_intersection_threshold.setter
    def poor_intersection_threshold(self, value: Real):
        self.set_property_state("poor_intersection_threshold", value)

    @property
    def face_alignment(self) -> String:
        """Available for coupling interfaces between surfaces."""
        return self.get_property_state("face_alignment")

    @face_alignment.setter
    def face_alignment(self, value: String):
        self.set_property_state("face_alignment", value)

    @property
    def absolute_gap_tolerance(self) -> Real:
        """Available only for coupling interfaces between surfaces."""
        return self.get_property_state("absolute_gap_tolerance")

    @absolute_gap_tolerance.setter
    def absolute_gap_tolerance(self, value: Real):
        self.set_property_state("absolute_gap_tolerance", value)

    @property
    def relative_gap_tolerance(self) -> Real:
        """Available for coupling interfaces between surfaces."""
        return self.get_property_state("relative_gap_tolerance")

    @relative_gap_tolerance.setter
    def relative_gap_tolerance(self, value: Real):
        self.set_property_state("relative_gap_tolerance", value)

    @property
    def small_weight_tolerance(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("small_weight_tolerance")

    @small_weight_tolerance.setter
    def small_weight_tolerance(self, value: Real):
        self.set_property_state("small_weight_tolerance", value)

    @property
    def corner_tolerance(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("corner_tolerance")

    @corner_tolerance.setter
    def corner_tolerance(self, value: Real):
        self.set_property_state("corner_tolerance", value)

    @property
    def halo_tolerance(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("halo_tolerance")

    @halo_tolerance.setter
    def halo_tolerance(self, value: Real):
        self.set_property_state("halo_tolerance", value)

    @property
    def conservative_reciprocity_factor(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("conservative_reciprocity_factor")

    @conservative_reciprocity_factor.setter
    def conservative_reciprocity_factor(self, value: Real):
        self.set_property_state("conservative_reciprocity_factor", value)

    @property
    def profile_preserving_reciprocity_factor(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("profile_preserving_reciprocity_factor")

    @profile_preserving_reciprocity_factor.setter
    def profile_preserving_reciprocity_factor(self, value: Real):
        self.set_property_state("profile_preserving_reciprocity_factor", value)

    @property
    def conservative_intensive(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("conservative_intensive")

    @conservative_intensive.setter
    def conservative_intensive(self, value: String):
        self.set_property_state("conservative_intensive", value)

    @property
    def preserve_normal(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("preserve_normal")

    @preserve_normal.setter
    def preserve_normal(self, value: String):
        self.set_property_state("preserve_normal", value)

    @property
    def conservation_fix_tolerance_volume(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("conservation_fix_tolerance_volume")

    @conservation_fix_tolerance_volume.setter
    def conservation_fix_tolerance_volume(self, value: Real):
        self.set_property_state("conservation_fix_tolerance_volume", value)

    @property
    def rbf_option(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("rbf_option")

    @rbf_option.setter
    def rbf_option(self, value: String):
        self.set_property_state("rbf_option", value)

    @property
    def rbf_shape_parameter(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("rbf_shape_parameter")

    @rbf_shape_parameter.setter
    def rbf_shape_parameter(self, value: Real):
        self.set_property_state("rbf_shape_parameter", value)

    @property
    def rbf_linear_correction(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("rbf_linear_correction")

    @rbf_linear_correction.setter
    def rbf_linear_correction(self, value: Boolean):
        self.set_property_state("rbf_linear_correction", value)

    @property
    def rbf_clipping_scale(self) -> Real:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("rbf_clipping_scale")

    @rbf_clipping_scale.setter
    def rbf_clipping_scale(self, value: Real):
        self.set_property_state("rbf_clipping_scale", value)
