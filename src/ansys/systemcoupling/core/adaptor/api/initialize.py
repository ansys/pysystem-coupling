#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class initialize(Command):
    """
    Interactive command that initializes a coupled analysis.

    Initialization includes preparing System Coupling, making connections
    between System Coupling and all participants, starting participants (if
    necessary), and writing participant build information to the Transcript
    and Log.

    Note that if the ``execution_control`` ``option`` for a participant is set to
    \"ExternallyManaged\", then System Coupling will not start the participant
    using either this command or any of the other commands that automatically
    start participants. The user is expected to manually start the participant.
    This function will not return until all participants have been connected.

    Note that this command will raise an exception if another instance of
    System Coupling is solving in the current working directory.
    """

    syc_name = "Initialize"
