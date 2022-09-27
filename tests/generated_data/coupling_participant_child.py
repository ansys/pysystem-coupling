#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .execution_control import execution_control
from .external_data_file import external_data_file
from .fmu_parameter import fmu_parameter
from .region import region
from .update_control import update_control
from .variable import variable


class coupling_participant_child(Container):
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
        ("participant_type", "ParticipantType", "str"),
        ("participant_display_name", "ParticipantDisplayName", "str"),
        ("display_name", "DisplayName", "str"),
        ("participant_file_loaded", "ParticipantFileLoaded", "str"),
        ("logging_on", "LoggingOn", "bool"),
        ("participant_analysis_type", "ParticipantAnalysisType", "str"),
        ("use_new_ap_is", "UseNewAPIs", "bool"),
        ("restarts_supported", "RestartsSupported", "bool"),
    ]

    @property
    def participant_type(self) -> str:
        """'participant_type' property of 'coupling_participant' object"""
        return self.get_property_state("participant_type")

    @participant_type.setter
    def participant_type(self, value: str):
        self.set_property_state("participant_type", value)

    @property
    def participant_display_name(self) -> str:
        """'participant_display_name' property of 'coupling_participant' object"""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: str):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> str:
        """'display_name' property of 'coupling_participant' object"""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def participant_file_loaded(self) -> str:
        """'participant_file_loaded' property of 'coupling_participant' object"""
        return self.get_property_state("participant_file_loaded")

    @participant_file_loaded.setter
    def participant_file_loaded(self, value: str):
        self.set_property_state("participant_file_loaded", value)

    @property
    def logging_on(self) -> bool:
        """'logging_on' property of 'coupling_participant' object"""
        return self.get_property_state("logging_on")

    @logging_on.setter
    def logging_on(self, value: bool):
        self.set_property_state("logging_on", value)

    @property
    def participant_analysis_type(self) -> str:
        """'participant_analysis_type' property of 'coupling_participant' object"""
        return self.get_property_state("participant_analysis_type")

    @participant_analysis_type.setter
    def participant_analysis_type(self, value: str):
        self.set_property_state("participant_analysis_type", value)

    @property
    def use_new_ap_is(self) -> bool:
        """'use_new_ap_is' property of 'coupling_participant' object"""
        return self.get_property_state("use_new_ap_is")

    @use_new_ap_is.setter
    def use_new_ap_is(self, value: bool):
        self.set_property_state("use_new_ap_is", value)

    @property
    def restarts_supported(self) -> bool:
        """'restarts_supported' property of 'coupling_participant' object"""
        return self.get_property_state("restarts_supported")

    @restarts_supported.setter
    def restarts_supported(self, value: bool):
        self.set_property_state("restarts_supported", value)
