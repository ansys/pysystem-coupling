#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .side_one_participant import side_one_participant
from .side_one_regions import side_one_regions
from .side_two_participant import side_two_participant
from .side_two_regions_1 import side_two_regions


class add_interface_by_display_names(Command):
    """
    Adds an interface based on the participant and region display names specified
    as arguments for each side of the interface. This command requires that you
    specify participants and regions using their *display* names (see parameter
    descriptions for details).

    Cannot be run after participants have been started.

    Returns the name of the Interface created.

    Parameters
    ----------
    side_one_participant : str
        String indicating the name of the participant to be associated with
        side \"One\" of the interface.
    side_one_regions : typing.List[str]
        List specifying the name(s) of region(s) to be added to side \"One\" of
        the interface.
    side_two_participant : str
        String indicating the name of the participant to be associated with
        side \"Two\" of the interface.
    side_two_regions : typing.List[str]
        List specifying the name(s) of region(s) to be added to side \"Two\"
        of the interface.

    """

    syc_name = "AddInterfaceByDisplayNames"

    argument_names = [
        "side_one_participant",
        "side_one_regions",
        "side_two_participant",
        "side_two_regions",
    ]

    side_one_participant: side_one_participant = side_one_participant
    """
    side_one_participant argument of add_interface_by_display_names.
    """
    side_one_regions: side_one_regions = side_one_regions
    """
    side_one_regions argument of add_interface_by_display_names.
    """
    side_two_participant: side_two_participant = side_two_participant
    """
    side_two_participant argument of add_interface_by_display_names.
    """
    side_two_regions: side_two_regions = side_two_regions
    """
    side_two_regions argument of add_interface_by_display_names.
    """
