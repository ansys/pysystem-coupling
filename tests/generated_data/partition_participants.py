#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class partition_participants(Command):
    """
    'partition_participants' child.

    Parameters
    ----------
    algorithm_name : str, optional
        'algorithm_name' child.
    machine_list : typing.List[typing.Dict[str, typing.Union[str, int]]], optional
        'machine_list' child.
    names_and_fractions : typing.List[typing.Tuple[str, float]], optional
        'names_and_fractions' child.

    """

    syc_name = "PartitionParticipants"

    argument_names = ["algorithm_name", "machine_list", "names_and_fractions"]

    class algorithm_name(String):
        """
        'algorithm_name' child.
        """

        syc_name = "AlgorithmName"

    class machine_list(StrOrIntDictList):
        """
        'machine_list' child.
        """

        syc_name = "MachineList"

    class names_and_fractions(StrFloatPairList):
        """
        'names_and_fractions' child.
        """

        syc_name = "NamesAndFractions"
