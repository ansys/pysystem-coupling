#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class save(Command):
    """
    Saves the state of the coupled analysis data model.

    -  Analysis settings are written to a single Settings.h5 file which
       can be used to reload analysis settings.

    -  Restart files for all restart points in the current co-simulation will
       be written when this command is called. Existing restart files from
       previous System Coupling versions will be renamed to conform to the new
       naming scheme.

    -  Restart files are named according to the convention
       ``Restart_step#.h5`` or ``Restart_iter#.h5``, where ``#`` is the index of
       the corresponding coupling step or iteration.

    Returns a Boolean value of ``True`` if the files were saved successfully;
    otherwise, returns a value of ``False``.

    Note that this command will raise an exception if another instance of
    System Coupling is solving in the current working directory.

    By default, writes to the ``SyC`` sub-directory of the current working
    directory. This behavior may be modified by providing ``file_path``.

    Parameters
    ----------
    file_path : str, optional
        Writeable directory to which the SyC directory is added. (Settings and
        results .h5 files will be written to the SyC directory.)

    """

    syc_name = "Save"

    argument_names = ["file_path"]

    class file_path(String):
        """
        Writeable directory to which the SyC directory is added. (Settings and
        results .h5 files will be written to the SyC directory.)
        """

        syc_name = "FilePath"
