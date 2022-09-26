#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class create_restart_point(Command):
    """
    Interactive command that creates a restart point at the end of the
    last completed coupling step.

    Signals the System Coupling service and all coupling participants that a
    restart point should be created before the next coupling step begins. The
    restart point is created in addition to restart points created by the
    ``output_control`` setting in the data model.

    Note that some participants write their restart files only when the
    coupling run resumes, so their files will not be available immediately
    after the command is issued.

    Results information for the coupling step is written to a file named
    according to the convention ``Results_#.h5``, where ``_#`` is the number of
    the coupling step. By default, the restart files are written to the ``SyC``
    directory, which is automatically created by the System Coupling service
    when restart points are created.
    """

    syc_name = "CreateRestartPoint"
