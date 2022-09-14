#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .instancing_child import instancing_child


class instancing(NamedObject[instancing_child]):
    """
    Define instancing for an interface side.

    Available when cylindrical geometry instancing has been added to
    the data model.
    """

    syc_name = "Instancing"

    child_object_type: instancing_child = instancing_child
    """
    child_object_type of instancing.
    """
