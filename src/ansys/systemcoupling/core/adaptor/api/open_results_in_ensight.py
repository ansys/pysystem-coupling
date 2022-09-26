#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class open_results_in_ensight(Command):
    """
    Allows for System Coupling results to be postprocessed in EnSight.

    When this command is issued, System Coupling looks for the ``results.enc``
    file in the ``SyC/results`` subdirectory of the current working directory.

    When System Coupling finds the file, it loads the file into EnSight and
    generates a confirmation message indicating that results are being opened.

    If System Coupling is unable to find the ``results.enc`` file and/or the
    EnSight executable, then it raises an error.

    The ``open_results_in_ensight`` command may be issued multiple times from the same
    instance of System Coupling. Each time the command is issued, a new
    instance of the EnSight application is opened. Any existing instances of
    EnSight remain open, both when additional instances are created and when
    System Coupling exits.
    """

    syc_name = "OpenResultsInEnSight"
