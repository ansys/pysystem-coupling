#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .coupling_iteration import coupling_iteration
from .coupling_step import coupling_step
from .file_path import file_path


class open(Command):
    """
    Reads the state of a coupled analysis. The state consists of settings to
    populate the datamodel and results to restart the analysis at the end of
    a specified coupling step.

    Settings are stored in a file named Settings.h5. ??results?? files may
    correspond either to coupling iterations or coupling steps, depending on
    the analysis type and the types of participants involved.

    By default, this command looks for the "SyC" directory in the current
    working directory. By default, if multiple ??results?? files exist, the
    most recent one is opened.

    If given optional arguments, behaves as described below in "Optional
    Keyword Arguments".

    Cannot be run after the participants have been started.

    Parameters
    ----------
        file_path : str
            Working directory containing the SyC subdirectory (and its .h5
    file(s)) to be read.
        coupling_step : int
            Integer specifying the coupling step at which the coupled analysis is
    restarted. When used, System Coupling reads the corresponding
    Results_step<#>.h5 file in the specified directory and restarts the
    analysis at the end of the specified coupling step. When this argument
    is used, System Coupling automatically removes the output files related
    to all later coupling steps. If the files cannot be removed, then
    System Coupling generates an exception message instructing you to free
    up the files and reissue the ??open?? command with the ??coupling_step??
    argument. If the simulation's ??results?? files are associated with
    coupling iterations, then System Coupling prints an error message
    indicating this.
        coupling_iteration : int
            Integer specifying the coupling iteration at which the coupled analysis
    is restarted. When used, System Coupling reads the corresponding
    Results_iter<#>.h5 file in the specified directory and restarts the
    analysis at the end of the specified coupling iteration. When this
    argument is used, System Coupling automatically removes the output
    files related to all later coupling iterations. If the files cannot be
    removed, then System Coupling generates an exception message
    instructing you to free up the files and reissue the ??open?? command with
    the ??coupling_iteration?? argument. If the simulation's ??results?? files are
    associated with coupling steps, then System Coupling prints an error
    message indicating this.

    """

    syc_name = "Open"

    argument_names = ["file_path", "coupling_step", "coupling_iteration"]

    file_path: file_path = file_path
    """
    file_path argument of open.
    """
    coupling_step: coupling_step = coupling_step
    """
    coupling_step argument of open.
    """
    coupling_iteration: coupling_iteration = coupling_iteration
    """
    coupling_iteration argument of open.
    """