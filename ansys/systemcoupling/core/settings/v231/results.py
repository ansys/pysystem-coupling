#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .type import type


class results(Group):
    """
    Settings defined under the Results singleton control the output of postprocessing results.
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
        """Specifies whether and when results files are generated."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def include_instances(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("include_instances")

    @include_instances.setter
    def include_instances(self, value: String):
        self.set_property_state("include_instances", value)

    @property
    def output_frequency(self) -> Integer:
        """Available when OutputControl.Results.Option is set to StepInterval or IterationInterval."""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: Integer):
        self.set_property_state("output_frequency", value)
