#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .region_child import region_child


class region(NamedContainer[region_child]):
    """
    Configure a region for the coupling participant.
    """

    syc_name = "Region"

    child_object_type: region_child = region_child
    """
    child_object_type of region.
    """
