#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class algorithm_name(String):
    """
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
    """

    syc_name = "AlgorithmName"