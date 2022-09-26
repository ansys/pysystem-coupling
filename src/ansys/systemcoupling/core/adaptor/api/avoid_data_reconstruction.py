#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class avoid_data_reconstruction(Group):
    """
    Control whether data reconstruction should be done for elemental intensive data.
    """

    syc_name = "AvoidDataReconstruction"

    property_names_types = [
        ("volume_mapping", "VolumeMapping", "Boolean"),
        ("surface_mapping", "SurfaceMapping", "Boolean"),
    ]

    @property
    def volume_mapping(self) -> Boolean:
        """UNDOCUMENTED"""
        return self.get_property_state("volume_mapping")

    @volume_mapping.setter
    def volume_mapping(self, value: Boolean):
        self.set_property_state("volume_mapping", value)

    @property
    def surface_mapping(self) -> Boolean:
        """UNDOCUMENTED"""
        return self.get_property_state("surface_mapping")

    @surface_mapping.setter
    def surface_mapping(self, value: Boolean):
        self.set_property_state("surface_mapping", value)
