#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class region_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("topology", "Topology", "String"),
        ("input_variables", "InputVariables", "StringList"),
        ("output_variables", "OutputVariables", "StringList"),
        ("display_name", "DisplayName", "String"),
    ]

    @property
    def topology(self) -> String:
        """'topology' property of 'region' object"""
        return self.get_property_state("topology")

    @topology.setter
    def topology(self, value: String):
        self.set_property_state("topology", value)

    @property
    def input_variables(self) -> StringList:
        """'input_variables' property of 'region' object"""
        return self.get_property_state("input_variables")

    @input_variables.setter
    def input_variables(self, value: StringList):
        self.set_property_state("input_variables", value)

    @property
    def output_variables(self) -> StringList:
        """'output_variables' property of 'region' object"""
        return self.get_property_state("output_variables")

    @output_variables.setter
    def output_variables(self, value: StringList):
        self.set_property_state("output_variables", value)

    @property
    def display_name(self) -> String:
        """'display_name' property of 'region' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)
