#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .side_child import side_child


class side(NamedContainer[side_child]):
    """
    Configure one side of a coupling interface.
    """

    syc_name = "Side"

    child_object_type: side_child = side_child
    """
    child_object_type of side.
    """
