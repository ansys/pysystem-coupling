#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .participant_name_2 import participant_name


class get_execution_command(Command):
    """
    Gets the execution command needed to start the specified participant

    Parameters
    ----------
    participant_name : str
        Name of the participant for which the execution command will
        be returned.

    """

    syc_name = "GetExecutionCommand"

    argument_names = ["participant_name"]

    participant_name: participant_name = participant_name
    """
    participant_name argument of get_execution_command.
    """
