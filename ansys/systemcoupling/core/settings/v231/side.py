#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .side_child import side_child


class side(NamedObject[side_child]):
    """
    Side of the coupling interface.
    """

    syc_name = "Side"

    child_object_type: side_child = side_child
    """
    child_object_type of side.
    """
