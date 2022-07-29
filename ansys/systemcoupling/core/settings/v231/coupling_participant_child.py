#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .execution_control import execution_control
from .external_data_file import external_data_file
from .fmu_parameter import fmu_parameter
from .region import region
from .update_control import update_control
from .variable import variable


class coupling_participant_child(Group):
    """
    Use CouplingParticipant objects to define coupling participant details.
    """

    syc_name = "child_object_type"

    child_names = [
        "variable",
        "region",
        "update_control",
        "fmu_parameter",
        "execution_control",
        "external_data_file",
    ]

    variable: variable = variable
    """
    variable child of coupling_participant_child.
    """
    region: region = region
    """
    region child of coupling_participant_child.
    """
    update_control: update_control = update_control
    """
    update_control child of coupling_participant_child.
    """
    fmu_parameter: fmu_parameter = fmu_parameter
    """
    fmu_parameter child of coupling_participant_child.
    """
    execution_control: execution_control = execution_control
    """
    execution_control child of coupling_participant_child.
    """
    external_data_file: external_data_file = external_data_file
    """
    external_data_file child of coupling_participant_child.
    """
    property_names_types = [
        ("participant_type", "ParticipantType", "String"),
        ("participant_display_name", "ParticipantDisplayName", "String"),
        ("display_name", "DisplayName", "String"),
        ("dimension", "Dimension", "String"),
        ("participant_file_loaded", "ParticipantFileLoaded", "String"),
        ("logging_on", "LoggingOn", "Boolean"),
        ("participant_analysis_type", "ParticipantAnalysisType", "String"),
        ("use_new_ap_is", "UseNewAPIs", "Boolean"),
        ("restarts_supported", "RestartsSupported", "Boolean"),
    ]

    @property
    def participant_type(self) -> String:
        """Type of application participating in the coupled analysis."""
        return self.get_property_state("participant_type")

    @participant_type.setter
    def participant_type(self, value: String):
        self.set_property_state("participant_type", value)

    @property
    def participant_display_name(self) -> String:
        """Participant's display name as defined by the participant solver (as opposed to System Coupling's DisplayName for the participant)."""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: String):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> String:
        """Participant's display name as defined in System Coupling."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def dimension(self) -> String:
        """Dimension of the coupling participant."""
        return self.get_property_state("dimension")

    @dimension.setter
    def dimension(self, value: String):
        self.set_property_state("dimension", value)

    @property
    def participant_file_loaded(self) -> String:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("participant_file_loaded")

    @participant_file_loaded.setter
    def participant_file_loaded(self, value: String):
        self.set_property_state("participant_file_loaded", value)

    @property
    def logging_on(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("logging_on")

    @logging_on.setter
    def logging_on(self, value: Boolean):
        self.set_property_state("logging_on", value)

    @property
    def participant_analysis_type(self) -> String:
        """Type of analysis the participant is running."""
        return self.get_property_state("participant_analysis_type")

    @participant_analysis_type.setter
    def participant_analysis_type(self, value: String):
        self.set_property_state("participant_analysis_type", value)

    @property
    def use_new_ap_is(self) -> Boolean:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("use_new_ap_is")

    @use_new_ap_is.setter
    def use_new_ap_is(self, value: Boolean):
        self.set_property_state("use_new_ap_is", value)

    @property
    def restarts_supported(self) -> Boolean:
        """Whether the participant supports restarts for this type of coupled analysis."""
        return self.get_property_state("restarts_supported")

    @restarts_supported.setter
    def restarts_supported(self, value: Boolean):
        self.set_property_state("restarts_supported", value)
