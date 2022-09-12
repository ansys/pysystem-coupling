#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .file_name import file_name
from .participant_name_2 import participant_name


class generate_input_file(Command):
    """
    Generates the input journal file for a given Fluent participant.

    Parameters
    ----------
    participant_name : str
        Name of the participant for which the execution command will
        be returned.
    file_name : str
        Name of the journal script to be written. Note that this name is relative
        to the participant's working directory.

    """

    syc_name = "GenerateInputFile"

    argument_names = ["participant_name", "file_name"]

    participant_name: participant_name = participant_name
    """
    participant_name argument of generate_input_file.
    """
    file_name: file_name = file_name
    """
    file_name argument of generate_input_file.
    """
