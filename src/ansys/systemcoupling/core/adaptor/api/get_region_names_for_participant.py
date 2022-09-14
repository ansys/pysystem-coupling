#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .participant_name import participant_name


class get_region_names_for_participant(Command):
    """
    Gets all of the specified participant's regions.

    Returns a dictionary with the regions as keys and the corresponding
    display names as values.

    Parameters
    ----------
    participant_name : str
        String indicating the participant for which regions are returned.

    """

    syc_name = "GetRegionNamesForParticipant"

    argument_names = ["participant_name"]

    participant_name: participant_name = participant_name
    """
    participant_name argument of get_region_names_for_participant.
    """
