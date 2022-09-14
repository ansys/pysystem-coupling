#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .side_child import side_child


class side(NamedObject[side_child]):
    """
    Configure one side of a coupling interface.
    """

    syc_name = "Side"

    child_object_type: side_child = side_child
    """
    child_object_type of side.
    """
