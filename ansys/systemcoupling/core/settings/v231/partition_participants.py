#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .algorithm_name import algorithm_name
from .machine_list import machine_list
from .names_and_fractions import names_and_fractions
from .partitioning_info import partitioning_info


class partition_participants(Command):
    """
    Provide a utility for setting the parallel algorithm, parallel partitioning
    fractions for each participant, and machine list information.

    At least one participant must be defined for this command to be used. Use
    of this command is not recommended if participants are already running.

    Parameters
    ----------
        algorithm_name : str
            Name of the partitioning algorithm. Available algorithms are:
    'SharedAllocateMachines'(default), 'SharedAllocateCores',
    'DistributedAllocateMachines', 'DistributedAllocateCores',
    and 'Custom' (please see ??partitioning_info?? section below for more details
    for this algorithm)

    The algorithms allow for both shared and distributed execution and for
    the allocation of machines or cores. The default value is generally the
    best choice, as it allows for each participant to take advantage of all
    the allocated resources. The other partitioning methods are provided to
    handle situations where not enough resources are available to run the
    same machines.

    See the System Coupling documentation for more details of the
    partitioning algorithms.
        names_and_fractions : typing.List[typing.Tuple[str, float]]
            List of tuples specifying the fractions of core count applied for
    each participant

    Each tuple must have the ParticipantName as its first item and the
    associated fraction as its second item. If this parameter is omitted,
    then cores will be allocated for all participants set in the
    data model.
        machine_list : typing.List[typing.Dict[str, typing.Union[str, int]]]
            List of dictionaries specifying machines available for distributed run.
    Each dictionary must have a key 'machine-name' with machine name as its
    value, and key 'core-count' with number of cores for that machine as
    its value. Providing this argument will over-ride any machine-list
    information detected from the scheduler environment and any information
    provided by the --cnf command-line argument.
        partitioning_info : typing.Dict[str, typing.List[typing.Dict[str, typing.Union[str, int]]]]
            Dictionary specifying machines resources assigned to each participant by user.
    Dictionary must have participant names as keys and machineLists containing
    machine resources as values. The value of ??partitioning_info?? machineList is
    a list of dictionaries specifying machines assigned to corresponding participants.
    Each dictionary of machineList must have a key 'machine-name' with machine name
    as its value, and key 'core-count' with number of cores for that machine as its value.
    Providing this argument will disallow other arguments except ??algorithm_name??,
    which must set as 'Custom' if provided. Otherwise, ??algorithm_name?? will be set as
    'Custom' internally if ??partitioning_info?? is provided.

    """

    syc_name = "PartitionParticipants"

    argument_names = [
        "algorithm_name",
        "names_and_fractions",
        "machine_list",
        "partitioning_info",
    ]

    algorithm_name: algorithm_name = algorithm_name
    """
    algorithm_name argument of partition_participants.
    """
    names_and_fractions: names_and_fractions = names_and_fractions
    """
    names_and_fractions argument of partition_participants.
    """
    machine_list: machine_list = machine_list
    """
    machine_list argument of partition_participants.
    """
    partitioning_info: partitioning_info = partitioning_info
    """
    partitioning_info argument of partition_participants.
    """
