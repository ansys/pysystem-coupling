#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class region_child(Container):
    """
    Configure a region for the coupling participant.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("topology", "Topology", "str"),
        ("input_variables", "InputVariables", "StringListType"),
        ("output_variables", "OutputVariables", "StringListType"),
        ("display_name", "DisplayName", "str"),
        ("region_discretization_type", "RegionDiscretizationType", "str"),
    ]

    @property
    def topology(self) -> str:
        """Region topology type.

        Allowed values:

        - \"Undefined\" (FMU participants only)
        - \"Surface\"
        - \"Volume\" (3D participants only)"""
        return self.get_property_state("topology")

    @topology.setter
    def topology(self, value: str):
        self.set_property_state("topology", value)

    @property
    def input_variables(self) -> StringListType:
        """Input variables for the region."""
        return self.get_property_state("input_variables")

    @input_variables.setter
    def input_variables(self, value: StringListType):
        self.set_property_state("input_variables", value)

    @property
    def output_variables(self) -> StringListType:
        """Output variables for the region."""
        return self.get_property_state("output_variables")

    @output_variables.setter
    def output_variables(self, value: StringListType):
        self.set_property_state("output_variables", value)

    @property
    def display_name(self) -> str:
        """Display name of the region."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def region_discretization_type(self) -> str:
        """Region discretization type (\"Mesh Region\" or \"Point Cloud Region\")."""
        return self.get_property_state("region_discretization_type")

    @region_discretization_type.setter
    def region_discretization_type(self, value: str):
        self.set_property_state("region_discretization_type", value)
