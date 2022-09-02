#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


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
