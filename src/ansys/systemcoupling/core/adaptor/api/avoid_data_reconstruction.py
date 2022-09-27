#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class avoid_data_reconstruction(Container):
    """
    Control whether data reconstruction should be done for elemental intensive data.
    """

    syc_name = "AvoidDataReconstruction"

    property_names_types = [
        ("volume_mapping", "VolumeMapping", "bool"),
        ("surface_mapping", "SurfaceMapping", "bool"),
    ]

    @property
    def volume_mapping(self) -> bool:
        """UNDOCUMENTED"""
        return self.get_property_state("volume_mapping")

    @volume_mapping.setter
    def volume_mapping(self, value: bool):
        self.set_property_state("volume_mapping", value)

    @property
    def surface_mapping(self) -> bool:
        """UNDOCUMENTED"""
        return self.get_property_state("surface_mapping")

    @surface_mapping.setter
    def surface_mapping(self, value: bool):
        self.set_property_state("surface_mapping", value)
