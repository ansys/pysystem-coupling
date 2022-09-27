#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .ascii_output import ascii_output
from .results import results


class output_control(Container):
    """
    Configure output controls.
    """

    syc_name = "OutputControl"

    child_names = ["results", "ascii_output"]

    results: results = results
    """
    results child of output_control.
    """
    ascii_output: ascii_output = ascii_output
    """
    ascii_output child of output_control.
    """
    property_names_types = [
        ("option", "Option", "str"),
        ("generate_csv_chart_output", "GenerateCSVChartOutput", "bool"),
        ("write_initial_snapshot", "WriteInitialSnapshot", "bool"),
        ("transcript_precision", "TranscriptPrecision", "int"),
        ("write_diagnostics", "WriteDiagnostics", "bool"),
        ("write_weights_matrix", "WriteWeightsMatrix", "bool"),
        ("write_residuals", "WriteResiduals", "bool"),
        ("output_frequency", "OutputFrequency", "int"),
    ]

    @property
    def option(self) -> str:
        """Specifies when restart points are generated.

        Allowed values (step-based analyses only):

        - \"LastStep\" - Generates a restart point only for the last
          coupling step completed.
        - \"EveryStep\" -
          Generate a restart point at the end of every coupling step.
        - \"StepInterval\" - Generates a restart point at the end of
          coupling steps at the interval specified by the output
          frequency setting.

        Allowed values (iteration-based analyses only):

        - \"LastIteration\" - Generates a restart point only for the
          last coupling iteration completed.
        - \"EveryIteration\" - Generate a restart point at the end
          of every coupling iteration.
        - \"IterationInterval\" - Generates a restart point at the
          end of coupling iterations at the interval specified by
          the output frequency setting."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def generate_csv_chart_output(self) -> bool:
        """Write chart data in CSV format during solve."""
        return self.get_property_state("generate_csv_chart_output")

    @generate_csv_chart_output.setter
    def generate_csv_chart_output(self, value: bool):
        self.set_property_state("generate_csv_chart_output", value)

    @property
    def write_initial_snapshot(self) -> bool:
        """Write initial snapshot."""
        return self.get_property_state("write_initial_snapshot")

    @write_initial_snapshot.setter
    def write_initial_snapshot(self, value: bool):
        self.set_property_state("write_initial_snapshot", value)

    @property
    def transcript_precision(self) -> int:
        """Number of digits after decimal point in transcript."""
        return self.get_property_state("transcript_precision")

    @transcript_precision.setter
    def transcript_precision(self, value: int):
        self.set_property_state("transcript_precision", value)

    @property
    def write_diagnostics(self) -> bool:
        """Write transfer diagnostics dictionary to file."""
        return self.get_property_state("write_diagnostics")

    @write_diagnostics.setter
    def write_diagnostics(self, value: bool):
        self.set_property_state("write_diagnostics", value)

    @property
    def write_weights_matrix(self) -> bool:
        """Write mapping weights to file after calculation."""
        return self.get_property_state("write_weights_matrix")

    @write_weights_matrix.setter
    def write_weights_matrix(self, value: bool):
        self.set_property_state("write_weights_matrix", value)

    @property
    def write_residuals(self) -> bool:
        """Write residuals to results files."""
        return self.get_property_state("write_residuals")

    @write_residuals.setter
    def write_residuals(self, value: bool):
        self.set_property_state("write_residuals", value)

    @property
    def output_frequency(self) -> int:
        """Specify output frequency."""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: int):
        self.set_property_state("output_frequency", value)
