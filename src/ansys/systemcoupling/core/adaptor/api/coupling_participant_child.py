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
    Configure a coupling participant.

    These settings are typically populated by using the ``add_participant``
    command.
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
        ("dimension", "Dimension", "str"),
        ("participant_file_loaded", "ParticipantFileLoaded", "str"),
        ("logging_on", "LoggingOn", "bool"),
        ("participant_analysis_type", "ParticipantAnalysisType", "str"),
        ("use_new_apis", "UseNewAPIs", "bool"),
        ("restarts_supported", "RestartsSupported", "bool"),
        ("instancing", "Instancing", "str"),
    ]

    @property
    def participant_type(self) -> str:
        """Coupling participant type.

        Allowed values:
        - \"DEFAULT\"
        - \"CFX\"
        - \"FLUENT\"
        - \"MAPDL\"
        - \"AEDT\"
        - \"FMU\"
        - \"EXTERNALDATA\"
        - \"FORTE\"
        - \"DEFAULT-SRV\"
        - \"MECH-SRV\"
        - \"CFD-SRV\" """
        return self.get_property_state("participant_type")

    @participant_type.setter
    def participant_type(self, value: str):
        self.set_property_state("participant_type", value)

    @property
    def participant_display_name(self) -> str:
        """Participant's display name as defined by the participant solver (as
        opposed to System Coupling's ``display_name`` for the participant)."""
        return self.get_property_state("participant_display_name")

    @participant_display_name.setter
    def participant_display_name(self, value: str):
        self.set_property_state("participant_display_name", value)

    @property
    def display_name(self) -> str:
        """Participant's display name as defined in System Coupling."""
        return self.get_property_state("display_name")

    @display_name.setter
    def display_name(self, value: str):
        self.set_property_state("display_name", value)

    @property
    def dimension(self) -> str:
        """Dimension of the participant (\"2D\" or \"3D\")."""
        return self.get_property_state("dimension")

    @dimension.setter
    def dimension(self, value: str):
        self.set_property_state("dimension", value)

    @property
    def participant_file_loaded(self) -> str:
        """File used to generate the participant."""
        return self.get_property_state("participant_file_loaded")

    @participant_file_loaded.setter
    def participant_file_loaded(self, value: str):
        self.set_property_state("participant_file_loaded", value)

    @property
    def logging_on(self) -> bool:
        """Specifies whether logging is activated for the participant."""
        return self.get_property_state("logging_on")

    @logging_on.setter
    def logging_on(self, value: bool):
        self.set_property_state("logging_on", value)

    @property
    def participant_analysis_type(self) -> str:
        """Coupling participant analysis type (\"Steady\" or \"Transient\")."""
        return self.get_property_state("participant_analysis_type")

    @participant_analysis_type.setter
    def participant_analysis_type(self, value: str):
        self.set_property_state("participant_analysis_type", value)

    @property
    def use_new_apis(self) -> bool:
        """Controls whether a Fluent or MAPDL participant should communicate using new APIs."""
        return self.get_property_state("use_new_apis")

    @use_new_apis.setter
    def use_new_apis(self, value: bool):
        self.set_property_state("use_new_apis", value)

    @property
    def restarts_supported(self) -> bool:
        """Indicates whether the participant supports restarts."""
        return self.get_property_state("restarts_supported")

    @restarts_supported.setter
    def restarts_supported(self, value: bool):
        self.set_property_state("restarts_supported", value)

    @property
    def instancing(self) -> str:
        """Set instancing on the participant."""
        return self.get_property_state("instancing")

    @instancing.setter
    def instancing(self, value: str):
        self.set_property_state("instancing", value)
