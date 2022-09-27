#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .type import type


class results(Container):
    """
    Configures output of postprocessing results data.
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
        """Specifies whether and when results files are generated.

        Allowed values:

        - \"ProgramControlled\" - Generate postprocessing results at the same
          frequency as restart points, as defined by the output control option
          setting. If no restart frequency is defined, then results are
          generated at the end of the last coupling step.

        -  \"Off\" - Generation of postprocessing results is disabled.

        Allowed values for step-based analyses:

        - \"LastStep\" - Generate results only for the last coupling step completed.

        - \"EveryStep\" - Generate results at the end of every coupling step.

        - \"StepInterval\" - Generate results at the end of coupling steps at
          the interval specified by the output frequency setting.

        Allowed values for iteration-based analyses:

        - \"LastIteration\" - Generate results only for the last coupling
          iteration completed.

        - \"EveryIteration\" - Generate results at the end of every coupling
          iteration.

        - \"IterationInterval\" - Generate results at the end of coupling
          iterations at the interval specified by the output frequency setting."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def include_instances(self) -> str:
        """Control whether instances are output.

        Allowed values:

        - \"ProgramControlled\"
        - \"ReferenceOnly\"
        - \"All\" """
        return self.get_property_state("include_instances")

    @include_instances.setter
    def include_instances(self, value: str):
        self.set_property_state("include_instances", value)

    @property
    def output_frequency(self) -> int:
        """Specify output frequency."""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: int):
        self.set_property_state("output_frequency", value)
