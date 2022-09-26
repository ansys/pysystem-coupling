#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class step(Command):
    """
    Interactive command that initializes the analysis (if necessary) and
    runs the specified number of coupling steps before pausing the coupled
    analysis.

    Disabled when a solution is already in progress.

    Disabled for iterations-only steady analyses.

    By default, runs a single step. If given the optional ``count`` argument,
    then runs the specified number of steps.

    For restarts, the ``open`` command must be run before the ``step`` command.

    When you run this command, System Coupling initializes the analysis if
    needed and then begins the solution. When the specified number of coupling
    steps has been run, the solution is paused, providing you with an
    opportunity to interact with the analysis.

    Note that if the ``execution_control`` option for a participant is set to
    ExternallyManaged, then System Coupling will not start the participant
    using either this command or any of the other commands that automatically
    start participants. The user is expected to manually start the participant.
    This function will not return until all participants have been connected.

    When the solution is resumed, either by reissuing this command or by
    running the ``solve`` command, System Coupling restarts the analysis at the
    point it left off and continues the solution with the next step.

    Note that this command will raise an exception if another instance of
    System Coupling is solving in the current working directory.

    Parameters
    ----------
    count : int, optional
        Integer specifying the number of steps to be run. Defaults to 1.

    """

    syc_name = "Step"

    argument_names = ["count"]

    class count(Integer):
        """
        Integer specifying the number of steps to be run. Defaults to 1.
        """

        syc_name = "Count"
