#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class dimensionality(Group):
    """
    Configure attribute dimensionality.
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
        """Exponent of length dimension."""
        return self.get_property_state("length")

    @length.setter
    def length(self, value: Real):
        self.set_property_state("length", value)

    @property
    def time(self) -> Real:
        """Exponent of time dimension."""
        return self.get_property_state("time")

    @time.setter
    def time(self, value: Real):
        self.set_property_state("time", value)

    @property
    def mass(self) -> Real:
        """Exponent of mass dimension."""
        return self.get_property_state("mass")

    @mass.setter
    def mass(self, value: Real):
        self.set_property_state("mass", value)

    @property
    def temperature(self) -> Real:
        """Exponent of temperature dimension."""
        return self.get_property_state("temperature")

    @temperature.setter
    def temperature(self, value: Real):
        self.set_property_state("temperature", value)

    @property
    def amount_of_substance(self) -> Real:
        """Exponent of amount of substance dimension."""
        return self.get_property_state("amount_of_substance")

    @amount_of_substance.setter
    def amount_of_substance(self, value: Real):
        self.set_property_state("amount_of_substance", value)

    @property
    def current(self) -> Real:
        """Exponent of electric current dimension."""
        return self.get_property_state("current")

    @current.setter
    def current(self, value: Real):
        self.set_property_state("current", value)

    @property
    def luminous_intensity(self) -> Real:
        """Exponent of luminous intensity dimension."""
        return self.get_property_state("luminous_intensity")

    @luminous_intensity.setter
    def luminous_intensity(self, value: Real):
        self.set_property_state("luminous_intensity", value)

    @property
    def angle(self) -> Real:
        """Exponent of angle dimension."""
        return self.get_property_state("angle")

    @angle.setter
    def angle(self, value: Real):
        self.set_property_state("angle", value)
