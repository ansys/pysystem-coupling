#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class add_participant(Command):
    """
    Adds a coupling participant to the data model.

    When executed, this command adds the new participant to the analysis
    without removing any interfaces or data transfers created previously.

    Cannot be called after participants have been started.

    Returns the name of the participant.

    There are two options to add the participant - via a file, or via a
    participant executable.

    Option 1: Using an input file
        Given an input file containing participant coupling information, reads the
        specified file, pushes the participant's information to the data model.

    Option 2: Using a participant executable
        Given the path to the executable for this participant (and optionally,
        additional arguments and/or working directory), start the participant
        executable, connect to the participant using the socket connection,
        and get the participant's information and add it to the data model.

    Parameters
    ----------
    participant_type : str, optional
        Participant type. Currently supported types are:

        - \"DEFAULT\"
        - \"CFX\"
        - \"FLUENT\"
        - \"MAPDL\"
        - \"AEDT\"
        - \"FMU\"
        - \"FORTE\"
        - \"DEFAULT-SRV\"
        - \"MECH-SRV\"
        - \"CFD-SRV\"

        If unspecified, ``add_participant`` will attempt to deduce
        the type from ``input_file``.
    input_file : str, optional
        Name of the input file for the participant to be added.
        Currently supported formats are SCP files, Forte input (FTSIM)
        files, mechanical server (*.rst) files, cfd server (*.csv) files,
        and FMU (.fmu) files (Beta).
    executable : str, optional
        Path to the executable file for the participant to be added.
    additional_arguments : str, optional
        Any additional arguments to be passed to the participant's executable.
    working_directory : str, optional
        Path to the working directory for this participant.

    """

    syc_name = "AddParticipant"

    argument_names = [
        "participant_type",
        "input_file",
        "executable",
        "additional_arguments",
        "working_directory",
    ]

    class participant_type(String):
        """
        Participant type. Currently supported types are:

        - \"DEFAULT\"
        - \"CFX\"
        - \"FLUENT\"
        - \"MAPDL\"
        - \"AEDT\"
        - \"FMU\"
        - \"FORTE\"
        - \"DEFAULT-SRV\"
        - \"MECH-SRV\"
        - \"CFD-SRV\"

        If unspecified, ``add_participant`` will attempt to deduce
        the type from ``input_file``.
        """

        syc_name = "ParticipantType"

    class input_file(String):
        """
        Name of the input file for the participant to be added.
        Currently supported formats are SCP files, Forte input (FTSIM)
        files, mechanical server (*.rst) files, cfd server (*.csv) files,
        and FMU (.fmu) files (Beta).
        """

        syc_name = "InputFile"

    class executable(String):
        """
        Path to the executable file for the participant to be added.
        """

        syc_name = "Executable"

    class additional_arguments(String):
        """
        Any additional arguments to be passed to the participant's executable.
        """

        syc_name = "AdditionalArguments"

    class working_directory(String):
        """
        Path to the working directory for this participant.
        """

        syc_name = "WorkingDirectory"
