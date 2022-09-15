#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .execution_control import execution_control
from .external_data_file import external_data_file
from .fmu_parameter import fmu_parameter
from .region import region
from .update_control import update_control
from .variable import variable


class coupling_participant_child(Group):
    """
    'child_object_type' child.
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
        ("participant_file_loaded", "ParticipantFileLoaded", "String"),
        ("logging_on", "LoggingOn", "Boolean"),
        ("participant_analysis_type", "ParticipantAnalysisType", "String"),
        ("use_new_ap_is", "UseNewAPIs", "Boolean"),
        ("restarts_supported", "RestartsSupported", "Boolean"),
    ]

    @property
    def participant_type(self) -> String:
        """'participant_type' property of 'coupling_participant' object"""
        return self.get_property_state("participant_type")

    @participant_type.setter
    def participant_type(self, value: String):
        self.set_property_state("participant_type", value)

    @property
    def participant_display_name(self) -> String:
        """'participant_display_name' property of 'coupling_participant' object"""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: String):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> String:
        """'display_name' property of 'coupling_participant' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: String):
        self.set_property_state("display_name", value)

    @property
    def participant_file_loaded(self) -> String:
        """'participant_file_loaded' property of 'coupling_participant' object"""
        return self.get_property_state("participant_file_loaded")

    @participant_file_loaded.setter
    def participant_file_loaded(self, value: String):
        self.set_property_state("participant_file_loaded", value)

    @property
    def logging_on(self) -> Boolean:
        """'logging_on' property of 'coupling_participant' object"""
        return self.get_property_state("logging_on")

    @logging_on.setter
    def logging_on(self, value: Boolean):
        self.set_property_state("logging_on", value)

    @property
    def participant_analysis_type(self) -> String:
        """'participant_analysis_type' property of 'coupling_participant' object"""
        return self.get_property_state("participant_analysis_type")

    @participant_analysis_type.setter
    def participant_analysis_type(self, value: String):
        self.set_property_state("participant_analysis_type", value)

    @property
    def use_new_ap_is(self) -> Boolean:
        """'use_new_ap_is' property of 'coupling_participant' object"""
        return self.get_property_state("use_new_ap_is")

    @use_new_ap_is.setter
    def use_new_ap_is(self, value: Boolean):
        self.set_property_state("use_new_ap_is", value)

    @property
    def restarts_supported(self) -> Boolean:
        """'restarts_supported' property of 'coupling_participant' object"""
        return self.get_property_state("restarts_supported")

    @restarts_supported.setter
    def restarts_supported(self, value: Boolean):
        self.set_property_state("restarts_supported", value)
