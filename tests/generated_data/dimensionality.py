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


class dimensionality(Container):
    """
    'dimensionality' child.
    """

    syc_name = "Dimensionality"

    property_names_types = [
        ("length", "Length", "RealType"),
        ("time", "Time", "RealType"),
        ("mass", "Mass", "RealType"),
        ("temperature", "Temperature", "RealType"),
        ("amount_of_substance", "AmountOfSubstance", "RealType"),
        ("current", "Current", "RealType"),
        ("luminous_intensity", "LuminousIntensity", "RealType"),
        ("angle", "Angle", "RealType"),
    ]

    @property
    def length(self) -> RealType:
        """'length' property of 'child_object_type' object"""
        return self.get_property_state("length")

    @length.setter
    def length(self, value: RealType):
        self.set_property_state("length", value)

    @property
    def time(self) -> RealType:
        """'time' property of 'child_object_type' object"""
        return self.get_property_state("time")

    @time.setter
    def time(self, value: RealType):
        self.set_property_state("time", value)

    @property
    def mass(self) -> RealType:
        """'mass' property of 'child_object_type' object"""
        return self.get_property_state("mass")

    @mass.setter
    def mass(self, value: RealType):
        self.set_property_state("mass", value)

    @property
    def temperature(self) -> RealType:
        """'temperature' property of 'child_object_type' object"""
        return self.get_property_state("temperature")

    @temperature.setter
    def temperature(self, value: RealType):
        self.set_property_state("temperature", value)

    @property
    def amount_of_substance(self) -> RealType:
        """'amount_of_substance' property of 'child_object_type' object"""
        return self.get_property_state("amount_of_substance")

    @amount_of_substance.setter
    def amount_of_substance(self, value: RealType):
        self.set_property_state("amount_of_substance", value)

    @property
    def current(self) -> RealType:
        """'current' property of 'child_object_type' object"""
        return self.get_property_state("current")

    @current.setter
    def current(self, value: RealType):
        self.set_property_state("current", value)

    @property
    def luminous_intensity(self) -> RealType:
        """'luminous_intensity' property of 'child_object_type' object"""
        return self.get_property_state("luminous_intensity")

    @luminous_intensity.setter
    def luminous_intensity(self, value: RealType):
        self.set_property_state("luminous_intensity", value)

    @property
    def angle(self) -> RealType:
        """'angle' property of 'child_object_type' object"""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: RealType):
        self.set_property_state("angle", value)
