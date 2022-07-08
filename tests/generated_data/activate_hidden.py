#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class activate_hidden(Group):
    """
    'activate_hidden' child.
    """

    syc_name = "ActivateHidden"

    property_names_types = [
        ("beta_features", "BetaFeatures", "Boolean"),
        ("alpha_features", "AlphaFeatures", "Boolean"),
        ("lenient_validation", "LenientValidation", "Boolean"),
    ]

    @property
    def beta_features(self) -> Boolean:
        """'beta_features' property of 'setup_root' object"""
        return self.get_property_state("beta_features")

    @beta_features.setter
    def beta_features(self, value: Boolean):
        self.set_property_state("beta_features", value)

    @property
    def alpha_features(self) -> Boolean:
        """'alpha_features' property of 'setup_root' object"""
        return self.get_property_state("alpha_features")

    @alpha_features.setter
    def alpha_features(self, value: Boolean):
        self.set_property_state("alpha_features", value)

    @property
    def lenient_validation(self) -> Boolean:
        """'lenient_validation' property of 'setup_root' object"""
        return self.get_property_state("lenient_validation")

    @lenient_validation.setter
    def lenient_validation(self, value: Boolean):
        self.set_property_state("lenient_validation", value)
