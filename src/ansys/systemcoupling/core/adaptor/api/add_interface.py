#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class add_interface(Command):
    """
    Adds an interface based on the participant and region names specified
    as arguments for each side of the interface. This command requires that you
    specify participants and regions using their names (see parameter
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
        List specifying the name(s) of region(s) to be added to side \"Two\" of
        the interface.

    """

    syc_name = "AddInterface"

    argument_names = [
        "side_one_participant",
        "side_one_regions",
        "side_two_participant",
        "side_two_regions",
    ]

    class side_one_participant(String):
        """
        String indicating the name of the participant to be associated with
        side \"One\" of the interface.
        """

        syc_name = "SideOneParticipant"

    class side_one_regions(StringList):
        """
        List specifying the name(s) of region(s) to be added to side \"One\" of
        the interface.
        """

        syc_name = "SideOneRegions"

    class side_two_participant(String):
        """
        String indicating the name of the participant to be associated with
        side \"Two\" of the interface.
        """

        syc_name = "SideTwoParticipant"

    class side_two_regions(StringList):
        """
        List specifying the name(s) of region(s) to be added to side \"Two\" of
        the interface.
        """

        syc_name = "SideTwoRegions"
