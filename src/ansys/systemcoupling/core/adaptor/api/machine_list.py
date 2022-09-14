#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


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
