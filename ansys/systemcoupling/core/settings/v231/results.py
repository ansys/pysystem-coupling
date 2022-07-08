#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .type import type


class results(Group):
    """
    'results' child.
    """

    syc_name = "Results"

    child_names = ["type"]

    type: type = type
    """
    type child of results.
    """
    property_names_types = [
        ("option", "Option", "String"),
        ("include_instances", "IncludeInstances", "String"),
        ("output_frequency", "OutputFrequency", "Integer"),
    ]

    @property
    def option(self) -> String:
        """'option' property of 'output_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def include_instances(self) -> String:
        """'include_instances' property of 'output_control' object"""
        return self.get_property_state("include_instances")

    @include_instances.setter
    def include_instances(self, value: String):
        self.set_property_state("include_instances", value)

    @property
    def output_frequency(self) -> Integer:
        """'output_frequency' property of 'output_control' object"""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: Integer):
        self.set_property_state("output_frequency", value)
