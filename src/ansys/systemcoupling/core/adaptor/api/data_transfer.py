#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .data_transfer_child import data_transfer_child


class data_transfer(NamedContainer[data_transfer_child]):
    """
    Configure data transfers for a coupling interface.
    """

    syc_name = "DataTransfer"

    child_object_type: data_transfer_child = data_transfer_child
    """
    child_object_type of data_transfer.
    """
