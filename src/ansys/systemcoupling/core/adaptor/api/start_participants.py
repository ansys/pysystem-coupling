#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class start_participants(Command):
    """
    Important: This command will be deprecated. Consider adopting workflows
    where participants are started by another method, such as the ``initialize``,
    ``step``, or ``solve`` commands.

    Interactive command that reads the participants' System Coupling
    Participant setup files (SCP) and starts participants on separate
    sub-processes. By default, automatically starts all participants and blocks
    solution progress until all participants are connected.

    If omitted and the ``solve``, ``initialize``, or ``step`` command is issued, then
    participants are started automatically during the execution of the command.

    Note that if the ``execution_control`` option for a participant is set to
    ExternallyManaged, then System Coupling will not start the participant
    using either this command or any of the other commands that automatically
    start participants. The user is expected to manually start the participant.
    This function will not return until all participants have been connected.

    Note that this command will raise an exception if another instance of
    System Coupling is solving in the current working directory.

    Parameters
    ----------
    participant_names : typing.List[str], optional
        This argument has been deprecated and will be removed in future releases.

    """

    syc_name = "StartParticipants"

    argument_names = ["participant_names"]

    class participant_names(StringList):
        """
        This argument has been deprecated and will be removed in future releases.
        """

        syc_name = "ParticipantNames"
