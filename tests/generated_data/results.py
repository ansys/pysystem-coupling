#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .type import type


class results(Container):
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
        ("option", "Option", "str"),
        ("include_instances", "IncludeInstances", "str"),
        ("output_frequency", "OutputFrequency", "int"),
    ]

    @property
    def option(self) -> str:
        """'option' property of 'output_control' object"""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def include_instances(self) -> str:
        """'include_instances' property of 'output_control' object"""
        return self.get_property_state("include_instances")

    @include_instances.setter
    def include_instances(self, value: str):
        self.set_property_state("include_instances", value)

    @property
    def output_frequency(self) -> int:
        """'output_frequency' property of 'output_control' object"""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: int):
        self.set_property_state("output_frequency", value)
