#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .region_child import region_child


class region(NamedObject[region_child]):
    """
    Define the region's settings.
    """

    syc_name = "Region"

    child_object_type: region_child = region_child
    """
    child_object_type of region.
    """
