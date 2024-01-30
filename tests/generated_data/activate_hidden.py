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


class activate_hidden(Container):
    """
    'activate_hidden' child.
    """

    syc_name = "ActivateHidden"

    property_names_types = [
        ("beta_features", "BetaFeatures", "bool"),
        ("alpha_features", "AlphaFeatures", "bool"),
        ("lenient_validation", "LenientValidation", "bool"),
    ]

    @property
    def beta_features(self) -> bool:
        """'beta_features' property of 'setup_root' object"""
        return self.get_property_state("beta_features")

    @beta_features.setter
    def beta_features(self, value: bool):
        self.set_property_state("beta_features", value)

    @property
    def alpha_features(self) -> bool:
        """'alpha_features' property of 'setup_root' object"""
        return self.get_property_state("alpha_features")

    @alpha_features.setter
    def alpha_features(self, value: bool):
        self.set_property_state("alpha_features", value)

    @property
    def lenient_validation(self) -> bool:
        """'lenient_validation' property of 'setup_root' object"""
        return self.get_property_state("lenient_validation")

    @lenient_validation.setter
    def lenient_validation(self, value: bool):
        self.set_property_state("lenient_validation", value)
