#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


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

    class additional_arguments(String):
        """
        'additional_arguments' child.
        """

        syc_name = "AdditionalArguments"

    class executable(String):
        """
        'executable' child.
        """

        syc_name = "Executable"

    class input_file(String):
        """
        'input_file' child.
        """

        syc_name = "InputFile"

    class participant_type(String):
        """
        'participant_type' child.
        """

        syc_name = "ParticipantType"

    class working_directory(String):
        """
        'working_directory' child.
        """

        syc_name = "WorkingDirectory"
