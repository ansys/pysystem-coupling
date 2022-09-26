#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class update_participant(Command):
    """
    Given the name of a server participant, updates the state of the participant.

    Available for server participants. Currently, only ``DEFAULT-SRV``,
    ``CFD-SRV``, and ``MECH-SRV`` participants may be updated.

    As part of the update, System Coupling updates all regions and
    variables defined in the participant, including all variable
    attributes. Variables and regions may be added to the participant but
    may not be removed.

    You may specify an input file using an optional argument. If an input
    file is not provided, then the original input file will be reimported.

    If the update process fails, System Coupling displays an error. In this
    case, you can either update the setup in the participant application to
    remove any issues with the update process or delete the participant
    from the analysis and then re-add it using the updated input file.

    Parameters
    ----------
    participant_name : str
        Participant name. Must be the name of an existing participant.
        Participant type can be either DEFAULT-SRV, MECH-SRV, or CFD-SRV.
    input_file : str, optional
        Name of the input file for the participant to be added.
        Currently supported formats are SCP files, Forte input (FTSIM)
        files, mechanical server (*.rst) files, cfd server (*.csv) files,
        and FMU (.fmu) files (Beta).

    """

    syc_name = "UpdateParticipant"

    argument_names = ["participant_name", "input_file"]

    class participant_name(String):
        """
        Participant name. Must be the name of an existing participant.
        Participant type can be either DEFAULT-SRV, MECH-SRV, or CFD-SRV.
        """

        syc_name = "ParticipantName"

    class input_file(String):
        """
        Name of the input file for the participant to be added.
        Currently supported formats are SCP files, Forte input (FTSIM)
        files, mechanical server (*.rst) files, cfd server (*.csv) files,
        and FMU (.fmu) files (Beta).
        """

        syc_name = "InputFile"
