#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .algorithm_name import algorithm_name
from .machine_list import machine_list
from .names_and_fractions import names_and_fractions


class partition_participants(Command):
    """
    'partition_participants' child.

    Parameters
    ----------
        algorithm_name : str
            'algorithm_name' child.
        machine_list : typing.List[typing.Dict[str, typing.Union[str, int]]]
            'machine_list' child.
        names_and_fractions : typing.List[typing.Tuple[str, float]]
            'names_and_fractions' child.

    """

    syc_name = "PartitionParticipants"

    argument_names = ["algorithm_name", "machine_list", "names_and_fractions"]

    algorithm_name: algorithm_name = algorithm_name
    """
    algorithm_name argument of partition_participants.
    """
    machine_list: machine_list = machine_list
    """
    machine_list argument of partition_participants.
    """
    names_and_fractions: names_and_fractions = names_and_fractions
    """
    names_and_fractions argument of partition_participants.
    """
