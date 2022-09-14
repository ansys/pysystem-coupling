#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class mapping_control(Group):
    """
    Configure controls for mapping.
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
        """Controls whether to stop if the intersection is poor"""
        return self.get_property_state("stop_if_poor_intersection")

    @stop_if_poor_intersection.setter
    def stop_if_poor_intersection(self, value: Boolean):
        self.set_property_state("stop_if_poor_intersection", value)

    @property
    def poor_intersection_threshold(self) -> Real:
        """System Coupling terminates with an error if the intersected fractions are below this threshold (in both directions)"""
        return self.get_property_state("poor_intersection_threshold")

    @poor_intersection_threshold.setter
    def poor_intersection_threshold(self, value: Real):
        self.set_property_state("poor_intersection_threshold", value)

    @property
    def face_alignment(self) -> String:
        """Controls how face alignment is used during mapping.

        Allowed values:

        - \"ProgramControlled\" (default)
        - \"OppositeOrientation\"
        - \"SameOrientation\"
        - \"AnyOrientation\" """
        return self.get_property_state("face_alignment")

    @face_alignment.setter
    def face_alignment(self, value: String):
        self.set_property_state("face_alignment", value)

    @property
    def absolute_gap_tolerance(self) -> Real:
        """Absolute gap tolerance value."""
        return self.get_property_state("absolute_gap_tolerance")

    @absolute_gap_tolerance.setter
    def absolute_gap_tolerance(self, value: Real):
        self.set_property_state("absolute_gap_tolerance", value)

    @property
    def relative_gap_tolerance(self) -> Real:
        """Maximum gap size relative to face size."""
        return self.get_property_state("relative_gap_tolerance")

    @relative_gap_tolerance.setter
    def relative_gap_tolerance(self, value: Real):
        self.set_property_state("relative_gap_tolerance", value)

    @property
    def small_weight_tolerance(self) -> Real:
        """Relative tolerance used to control when weights are dropped."""
        return self.get_property_state("small_weight_tolerance")

    @small_weight_tolerance.setter
    def small_weight_tolerance(self, value: Real):
        self.set_property_state("small_weight_tolerance", value)

    @property
    def corner_tolerance(self) -> Real:
        """Angle [degrees] between adjacent source mesh faces above which the
        mapping algorithm will stop searching for mapping candidates."""
        return self.get_property_state("corner_tolerance")

    @corner_tolerance.setter
    def corner_tolerance(self, value: Real):
        self.set_property_state("corner_tolerance", value)

    @property
    def halo_tolerance(self) -> Real:
        """If a face intersects but a target node lies outside of the source face, then
        map the node if the projected distance to the face / sqrt(srcArea) is less
        than this tolerance, otherwise leave as unmapped."""
        return self.get_property_state("halo_tolerance")

    @halo_tolerance.setter
    def halo_tolerance(self, value: Real):
        self.set_property_state("halo_tolerance", value)

    @property
    def conservative_reciprocity_factor(self) -> Real:
        """Reciprocity blend factor for conservative mapping."""
        return self.get_property_state("conservative_reciprocity_factor")

    @conservative_reciprocity_factor.setter
    def conservative_reciprocity_factor(self, value: Real):
        self.set_property_state("conservative_reciprocity_factor", value)

    @property
    def profile_preserving_reciprocity_factor(self) -> Real:
        """Reciprocity blend factor for profile-preserving mapping."""
        return self.get_property_state("profile_preserving_reciprocity_factor")

    @profile_preserving_reciprocity_factor.setter
    def profile_preserving_reciprocity_factor(self, value: Real):
        self.set_property_state("profile_preserving_reciprocity_factor", value)

    @property
    def conservative_intensive(self) -> String:
        """Determines when the Intensive option is used for conservative mapping.

        Allowed values:

        - \"ProgramControlled\" (default)
        - \"Off\"
        - \"On\" """
        return self.get_property_state("conservative_intensive")

    @conservative_intensive.setter
    def conservative_intensive(self, value: String):
        self.set_property_state("conservative_intensive", value)

    @property
    def preserve_normal(self) -> String:
        """Determines if the normal component of a vector is preserved.

        Allowed values:

        - \"ProgramControlled\" (default)
        - \"Off\"
        - \"On\" """
        return self.get_property_state("preserve_normal")

    @preserve_normal.setter
    def preserve_normal(self, value: String):
        self.set_property_state("preserve_normal", value)

    @property
    def conservation_fix_tolerance_volume(self) -> Real:
        """Source element overlap fraction to trigger volume mapping conservation fix.

        0.0 is default. 1.0 effectively disables it."""
        return self.get_property_state("conservation_fix_tolerance_volume")

    @conservation_fix_tolerance_volume.setter
    def conservation_fix_tolerance_volume(self, value: Real):
        self.set_property_state("conservation_fix_tolerance_volume", value)

    @property
    def rbf_option(self) -> String:
        """Controls radial basis function formulation.

        Allowed values:

        - \"Gaussian\" (default)
        - \"ThinPlateSpline\" """
        return self.get_property_state("rbf_option")

    @rbf_option.setter
    def rbf_option(self, value: String):
        self.set_property_state("rbf_option", value)

    @property
    def rbf_shape_parameter(self) -> Real:
        """Sets the shape parameter beta when using Gaussian radial basis functions."""
        return self.get_property_state("rbf_shape_parameter")

    @rbf_shape_parameter.setter
    def rbf_shape_parameter(self, value: Real):
        self.set_property_state("rbf_shape_parameter", value)

    @property
    def rbf_linear_correction(self) -> Boolean:
        """Controls whether linear polynomial augmentation is added to the RBF stencil for
        low order regular element types (tet, hex, pyramid, wedge)."""
        return self.get_property_state("rbf_linear_correction")

    @rbf_linear_correction.setter
    def rbf_linear_correction(self, value: Boolean):
        self.set_property_state("rbf_linear_correction", value)

    @property
    def rbf_clipping_scale(self) -> Real:
        """Length scale factor used to determine if source nodes are removed from RBF
        stencil when too close."""
        return self.get_property_state("rbf_clipping_scale")

    @rbf_clipping_scale.setter
    def rbf_clipping_scale(self, value: Real):
        self.set_property_state("rbf_clipping_scale", value)
