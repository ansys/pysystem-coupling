#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .coupling_participant_child import coupling_participant_child


class coupling_participant(NamedObject[coupling_participant_child]):
    """
    'coupling_participant' child.
    """

    syc_name = "CouplingParticipant"

    child_object_type: coupling_participant_child = coupling_participant_child
    """
    child_object_type of coupling_participant.
    """
