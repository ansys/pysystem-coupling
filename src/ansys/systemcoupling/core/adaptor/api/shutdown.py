#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class shutdown(Command):
    """
    Interactive command that shuts down a coupled analysis.

    ``shutdown`` includes ending the coupling run and signaling participants
    to end the run. This produces a clean shutdown, generating the final
    restart point and corresponding results file before disconnecting
    from participants.

    After participants are disconnected, the coupling service writes
    timing details to the transcript. If participants were started
    automatically, it ends participant processes.

    When System Coupling disconnects from the analysis and shuts down, the GUI
    Server file is removed from the working directory.
    """

    syc_name = "Shutdown"
