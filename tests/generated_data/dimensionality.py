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
        ("length", "Length", "Real"),
        ("time", "Time", "Real"),
        ("mass", "Mass", "Real"),
        ("temperature", "Temperature", "Real"),
        ("amount_of_substance", "AmountOfSubstance", "Real"),
        ("current", "Current", "Real"),
        ("luminous_intensity", "LuminousIntensity", "Real"),
        ("angle", "Angle", "Real"),
    ]

    @property
    def length(self) -> Real:
        """'length' property of 'child_object_type' object"""
        return self.get_property_state("length")

    @length.setter
    def length(self, value: Real):
        self.set_property_state("length", value)

    @property
    def time(self) -> Real:
        """'time' property of 'child_object_type' object"""
        return self.get_property_state("time")

    @time.setter
    def time(self, value: Real):
        self.set_property_state("time", value)

    @property
    def mass(self) -> Real:
        """'mass' property of 'child_object_type' object"""
        return self.get_property_state("mass")

    @mass.setter
    def mass(self, value: Real):
        self.set_property_state("mass", value)

    @property
    def temperature(self) -> Real:
        """'temperature' property of 'child_object_type' object"""
        return self.get_property_state("temperature")

    @temperature.setter
    def temperature(self, value: Real):
        self.set_property_state("temperature", value)

    @property
    def amount_of_substance(self) -> Real:
        """'amount_of_substance' property of 'child_object_type' object"""
        return self.get_property_state("amount_of_substance")

    @amount_of_substance.setter
    def amount_of_substance(self, value: Real):
        self.set_property_state("amount_of_substance", value)

    @property
    def current(self) -> Real:
        """'current' property of 'child_object_type' object"""
        return self.get_property_state("current")

    @current.setter
    def current(self, value: Real):
        self.set_property_state("current", value)

    @property
    def luminous_intensity(self) -> Real:
        """'luminous_intensity' property of 'child_object_type' object"""
        return self.get_property_state("luminous_intensity")

    @luminous_intensity.setter
    def luminous_intensity(self, value: Real):
        self.set_property_state("luminous_intensity", value)

    @property
    def angle(self) -> Real:
        """'angle' property of 'child_object_type' object"""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: Real):
        self.set_property_state("angle", value)
