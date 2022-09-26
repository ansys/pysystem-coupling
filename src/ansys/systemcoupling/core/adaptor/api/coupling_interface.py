#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .coupling_interface_child import coupling_interface_child


class coupling_interface(NamedContainer[coupling_interface_child]):
    """
    Configure a coupling interface.
    """

    syc_name = "CouplingInterface"

    child_object_type: coupling_interface_child = coupling_interface_child
    """
    child_object_type of coupling_interface.
    """
