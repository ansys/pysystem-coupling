#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .ascii_output import ascii_output
from .results import results


class output_control(Group):
    """
    The OutputControl singleton is available when a coupling participant object has been added to the data model. Settings defined under the OutputControl singleton control the generation of System Coupling's output (such as restart points and EnSight-compatible results).
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
        ("option", "Option", "String"),
        ("generate_csv_chart_output", "GenerateCSVChartOutput", "Boolean"),
        ("write_initial_snapshot", "WriteInitialSnapshot", "Boolean"),
        ("transcript_precision", "TranscriptPrecision", "Integer"),
        ("write_diagnostics", "WriteDiagnostics", "Boolean"),
        ("write_weights_matrix", "WriteWeightsMatrix", "Boolean"),
        ("write_residuals", "WriteResiduals", "Boolean"),
        ("output_frequency", "OutputFrequency", "Integer"),
    ]

    @property
    def option(self) -> String:
        """Available when all coupling participants support restarts."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def generate_csv_chart_output(self) -> Boolean:
        """Specifies whether System Coupling writes convergence charting data to .csv files during the execution of a solution."""
        return self.get_property_state("generate_csv_chart_output")

    @generate_csv_chart_output.setter
    def generate_csv_chart_output(self, value: Boolean):
        self.set_property_state("generate_csv_chart_output", value)

    @property
    def write_initial_snapshot(self) -> Boolean:
        """Controls whether System Coupling writes an initial snapshot of the coupled analysis state when the solution is started."""
        return self.get_property_state("write_initial_snapshot")

    @write_initial_snapshot.setter
    def write_initial_snapshot(self, value: Boolean):
        self.set_property_state("write_initial_snapshot", value)

    @property
    def transcript_precision(self) -> Integer:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("transcript_precision")

    @transcript_precision.setter
    def transcript_precision(self, value: Integer):
        self.set_property_state("transcript_precision", value)

    @property
    def write_diagnostics(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("write_diagnostics")

    @write_diagnostics.setter
    def write_diagnostics(self, value: Boolean):
        self.set_property_state("write_diagnostics", value)

    @property
    def write_weights_matrix(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("write_weights_matrix")

    @write_weights_matrix.setter
    def write_weights_matrix(self, value: Boolean):
        self.set_property_state("write_weights_matrix", value)

    @property
    def write_residuals(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("write_residuals")

    @write_residuals.setter
    def write_residuals(self, value: Boolean):
        self.set_property_state("write_residuals", value)

    @property
    def output_frequency(self) -> Integer:
        """Available when the OutputControl.Option is set to StepInterval or IterationInterval. Determines the frequency at which restart points are generated."""
        return self.get_property_state("output_frequency")

    @output_frequency.setter
    def output_frequency(self, value: Integer):
        self.set_property_state("output_frequency", value)
