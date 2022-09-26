#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .coupling_participant_child import coupling_participant_child


class coupling_participant(NamedContainer[coupling_participant_child]):
    """
    Configure a coupling participant.

    These settings are typically populated by using the ``add_participant``
    command.
    """

    syc_name = "CouplingParticipant"

    child_object_type: coupling_participant_child = coupling_participant_child
    """
    child_object_type of coupling_participant.
    """
