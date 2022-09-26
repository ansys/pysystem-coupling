#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class has_input_file_changed(Command):
    """
    Given the name of a participant, checks whether the input file has changed.

    Available for server participants. Currently, only input files for
    DEFAULT-SRV, CFD-SRV, and MECH-SRV participants are tracked by
    System Coupling.

    If a participant's input files are not tracked by System Coupling, this
    command will return ``False`` in all cases, even if changes have been made
    to the participant input file.

    Parameters
    ----------
    participant_name : str
        Name of the participant

    """

    syc_name = "HasInputFileChanged"

    argument_names = ["participant_name"]

    class participant_name(String):
        """
        Name of the participant
        """

        syc_name = "ParticipantName"
