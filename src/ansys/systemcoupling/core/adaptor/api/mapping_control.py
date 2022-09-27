#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class mapping_control(Container):
    """
    Configure controls for mapping.
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
        """Controls whether to stop if the intersection is poor"""
        return self.get_property_state("stop_if_poor_intersection")

    @stop_if_poor_intersection.setter
    def stop_if_poor_intersection(self, value: bool):
        self.set_property_state("stop_if_poor_intersection", value)

    @property
    def poor_intersection_threshold(self) -> RealType:
        """System Coupling terminates with an error if the intersected fractions are below this threshold (in both directions)"""
        return self.get_property_state("poor_intersection_threshold")

    @poor_intersection_threshold.setter
    def poor_intersection_threshold(self, value: RealType):
        self.set_property_state("poor_intersection_threshold", value)

    @property
    def face_alignment(self) -> str:
        """Controls how face alignment is used during mapping.

        Allowed values:

        - \"ProgramControlled\" (default)
        - \"OppositeOrientation\"
        - \"SameOrientation\"
        - \"AnyOrientation\" """
        return self.get_property_state("face_alignment")

    @face_alignment.setter
    def face_alignment(self, value: str):
        self.set_property_state("face_alignment", value)

    @property
    def absolute_gap_tolerance(self) -> RealType:
        """Absolute gap tolerance value."""
        return self.get_property_state("absolute_gap_tolerance")

    @absolute_gap_tolerance.setter
    def absolute_gap_tolerance(self, value: RealType):
        self.set_property_state("absolute_gap_tolerance", value)

    @property
    def relative_gap_tolerance(self) -> RealType:
        """Maximum gap size relative to face size."""
        return self.get_property_state("relative_gap_tolerance")

    @relative_gap_tolerance.setter
    def relative_gap_tolerance(self, value: RealType):
        self.set_property_state("relative_gap_tolerance", value)

    @property
    def small_weight_tolerance(self) -> RealType:
        """Relative tolerance used to control when weights are dropped."""
        return self.get_property_state("small_weight_tolerance")

    @small_weight_tolerance.setter
    def small_weight_tolerance(self, value: RealType):
        self.set_property_state("small_weight_tolerance", value)

    @property
    def corner_tolerance(self) -> RealType:
        """Angle [degrees] between adjacent source mesh faces above which the
        mapping algorithm will stop searching for mapping candidates."""
        return self.get_property_state("corner_tolerance")

    @corner_tolerance.setter
    def corner_tolerance(self, value: RealType):
        self.set_property_state("corner_tolerance", value)

    @property
    def halo_tolerance(self) -> RealType:
        """If a face intersects but a target node lies outside of the source face, then
        map the node if the projected distance to the face / sqrt(srcArea) is less
        than this tolerance, otherwise leave as unmapped."""
        return self.get_property_state("halo_tolerance")

    @halo_tolerance.setter
    def halo_tolerance(self, value: RealType):
        self.set_property_state("halo_tolerance", value)

    @property
    def conservative_reciprocity_factor(self) -> RealType:
        """Reciprocity blend factor for conservative mapping."""
        return self.get_property_state("conservative_reciprocity_factor")

    @conservative_reciprocity_factor.setter
    def conservative_reciprocity_factor(self, value: RealType):
        self.set_property_state("conservative_reciprocity_factor", value)

    @property
    def profile_preserving_reciprocity_factor(self) -> RealType:
        """Reciprocity blend factor for profile-preserving mapping."""
        return self.get_property_state("profile_preserving_reciprocity_factor")

    @profile_preserving_reciprocity_factor.setter
    def profile_preserving_reciprocity_factor(self, value: RealType):
        self.set_property_state("profile_preserving_reciprocity_factor", value)

    @property
    def conservative_intensive(self) -> str:
        """Determines when the Intensive option is used for conservative mapping.

        Allowed values:

        - \"ProgramControlled\" (default)
        - \"Off\"
        - \"On\" """
        return self.get_property_state("conservative_intensive")

    @conservative_intensive.setter
    def conservative_intensive(self, value: str):
        self.set_property_state("conservative_intensive", value)

    @property
    def preserve_normal(self) -> str:
        """Determines if the normal component of a vector is preserved.

        Allowed values:

        - \"ProgramControlled\" (default)
        - \"Off\"
        - \"On\" """
        return self.get_property_state("preserve_normal")

    @preserve_normal.setter
    def preserve_normal(self, value: str):
        self.set_property_state("preserve_normal", value)

    @property
    def conservation_fix_tolerance_volume(self) -> RealType:
        """Source element overlap fraction to trigger volume mapping conservation fix.

        0.0 is default. 1.0 effectively disables it."""
        return self.get_property_state("conservation_fix_tolerance_volume")

    @conservation_fix_tolerance_volume.setter
    def conservation_fix_tolerance_volume(self, value: RealType):
        self.set_property_state("conservation_fix_tolerance_volume", value)

    @property
    def rbf_option(self) -> str:
        """Controls radial basis function formulation.

        Allowed values:

        - \"Gaussian\" (default)
        - \"ThinPlateSpline\" """
        return self.get_property_state("rbf_option")

    @rbf_option.setter
    def rbf_option(self, value: str):
        self.set_property_state("rbf_option", value)

    @property
    def rbf_shape_parameter(self) -> RealType:
        """Sets the shape parameter beta when using Gaussian radial basis functions."""
        return self.get_property_state("rbf_shape_parameter")

    @rbf_shape_parameter.setter
    def rbf_shape_parameter(self, value: RealType):
        self.set_property_state("rbf_shape_parameter", value)

    @property
    def rbf_linear_correction(self) -> bool:
        """Controls whether linear polynomial augmentation is added to the RBF stencil for
        low order regular element types (tet, hex, pyramid, wedge)."""
        return self.get_property_state("rbf_linear_correction")

    @rbf_linear_correction.setter
    def rbf_linear_correction(self, value: bool):
        self.set_property_state("rbf_linear_correction", value)

    @property
    def rbf_clipping_scale(self) -> RealType:
        """Length scale factor used to determine if source nodes are removed from RBF
        stencil when too close."""
        return self.get_property_state("rbf_clipping_scale")

    @rbf_clipping_scale.setter
    def rbf_clipping_scale(self, value: RealType):
        self.set_property_state("rbf_clipping_scale", value)
