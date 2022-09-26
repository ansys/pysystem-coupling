#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class import_system_coupling_input_file(Command):
    """
    Reads the specified System Coupling SCI file and pushes its information
    into the data model. The SCI file is the required System Coupling input
    format for the initial run of a coupled analysis set up in Workbench.

    After the initial run based on an imported SCI file, a reissue
    of the ``import_system_coupling_input_file`` command is unnecessary and is
    not recommended unless the setup has changed.

    Cannot be run after participants have been started.

    Parameters
    ----------
    file_path : str
        Path and file name for the SCI file to be read.

    """

    syc_name = "ImportSystemCouplingInputFile"

    argument_names = ["file_path"]

    class file_path(String):
        """
        Path and file name for the SCI file to be read.
        """

        syc_name = "FilePath"
