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
