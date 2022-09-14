#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .additional_arguments import additional_arguments
from .executable import executable
from .input_file import input_file
from .participant_type import participant_type
from .working_directory import working_directory


class add_participant(Command):
    """
    'add_participant' child.

    Parameters
    ----------
    additional_arguments : str, optional
        'additional_arguments' child.
    executable : str, optional
        'executable' child.
    input_file : str, optional
        'input_file' child.
    participant_type : str, optional
        'participant_type' child.
    working_directory : str, optional
        'working_directory' child.

    """

    syc_name = "AddParticipant"

    argument_names = [
        "additional_arguments",
        "executable",
        "input_file",
        "participant_type",
        "working_directory",
    ]

    additional_arguments: additional_arguments = additional_arguments
    """
    additional_arguments argument of add_participant.
    """
    executable: executable = executable
    """
    executable argument of add_participant.
    """
    input_file: input_file = input_file
    """
    input_file argument of add_participant.
    """
    participant_type: participant_type = participant_type
    """
    participant_type argument of add_participant.
    """
    working_directory: working_directory = working_directory
    """
    working_directory argument of add_participant.
    """
