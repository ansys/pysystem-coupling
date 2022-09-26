#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class partition_participants(Command):
    """
    Provide a utility for setting the parallel algorithm, parallel partitioning
    fractions for each participant, and machine list information.

    At least one participant must be defined for this command to be used. Use
    of this command is not recommended if participants are already running.

    Parameters
    ----------
    algorithm_name : str, optional
        Name of the partitioning algorithm. Available algorithms are:

        - \"SharedAllocateMachines\" (default)
        - \"SharedAllocateCores\"
        - \"DistributedAllocateMachines\"
        - \"DistributedAllocateCores\"
        - \"Custom\" (see ``partitioning_info`` for more details)

        The algorithms allow for both shared and distributed execution and for
        the allocation of machines or cores. The default value is generally the
        best choice, as it allows for each participant to take advantage of all
        the allocated resources. The other partitioning methods are provided to
        handle situations where not enough resources are available to run the
        same machines.

        See the System Coupling documentation for more details of the
        partitioning algorithms.
    names_and_fractions : typing.List[typing.Tuple[str, float]], optional
        List of tuples specifying the fractions of core count applied for
        each participant

        Each tuple must have the participant name as its first item and the
        associated fraction as its second item. If this parameter is omitted,
        then cores will be allocated for all participants set in the
        data model.
    machine_list : typing.List[typing.Dict[str, typing.Union[str, int]]], optional
        List of dictionaries specifying machines available for distributed run.
        Each dictionary must have a key \"machine-name\" with machine name as its
        value, and key \"core-count\" with number of cores for that machine as
        its value. Providing this argument will override any machine list
        information detected from the scheduler environment and any information
        provided by the ``--cnf`` command-line argument.
    partitioning_info : typing.Dict[str, typing.List[typing.Dict[str, typing.Union[str, int]]]], optional
        Dictionary specifying machines resources assigned to each participant by user.
        Dictionary must have participant names as keys and machine lists containing
        machine resources as values. The value of a ``partitioning_info`` machine list is
        a list of dictionaries specifying machines assigned to corresponding participants.
        Each dictionary of the machine list must have a key \"machine-name\" with the
        machine name as its value, and key \"core-count\" with number of cores for that
        machine as its value.

        Providing this argument will disallow other arguments except ``algorithm_name``,
        which must set as \"Custom\" if provided. Otherwise, ``algorithm_name`` will be
        set as \"Custom\" internally if ``partitioning_info`` is provided.

    """

    syc_name = "PartitionParticipants"

    argument_names = [
        "algorithm_name",
        "names_and_fractions",
        "machine_list",
        "partitioning_info",
    ]

    class algorithm_name(String):
        """
        Name of the partitioning algorithm. Available algorithms are:

        - \"SharedAllocateMachines\" (default)
        - \"SharedAllocateCores\"
        - \"DistributedAllocateMachines\"
        - \"DistributedAllocateCores\"
        - \"Custom\" (see ``partitioning_info`` for more details)

        The algorithms allow for both shared and distributed execution and for
        the allocation of machines or cores. The default value is generally the
        best choice, as it allows for each participant to take advantage of all
        the allocated resources. The other partitioning methods are provided to
        handle situations where not enough resources are available to run the
        same machines.

        See the System Coupling documentation for more details of the
        partitioning algorithms.
        """

        syc_name = "AlgorithmName"

    class names_and_fractions(StrFloatPairList):
        """
        List of tuples specifying the fractions of core count applied for
        each participant

        Each tuple must have the participant name as its first item and the
        associated fraction as its second item. If this parameter is omitted,
        then cores will be allocated for all participants set in the
        data model.
        """

        syc_name = "NamesAndFractions"

    class machine_list(StrOrIntDictList):
        """
        List of dictionaries specifying machines available for distributed run.
        Each dictionary must have a key \"machine-name\" with machine name as its
        value, and key \"core-count\" with number of cores for that machine as
        its value. Providing this argument will override any machine list
        information detected from the scheduler environment and any information
        provided by the ``--cnf`` command-line argument.
        """

        syc_name = "MachineList"

    class partitioning_info(StrOrIntDictListDict):
        """
        Dictionary specifying machines resources assigned to each participant by user.
        Dictionary must have participant names as keys and machine lists containing
        machine resources as values. The value of a ``partitioning_info`` machine list is
        a list of dictionaries specifying machines assigned to corresponding participants.
        Each dictionary of the machine list must have a key \"machine-name\" with the
        machine name as its value, and key \"core-count\" with number of cores for that
        machine as its value.

        Providing this argument will disallow other arguments except ``algorithm_name``,
        which must set as \"Custom\" if provided. Otherwise, ``algorithm_name`` will be
        set as \"Custom\" internally if ``partitioning_info`` is provided.
        """

        syc_name = "PartitioningInfo"
