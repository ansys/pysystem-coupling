#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .transformation_child import transformation_child


class transformation(NamedObject[transformation_child]):
    """
    Use Transformation objects to apply transformations to coupling interfaces sides to control the positioning of the geometry.
    """

    syc_name = "Transformation"

    child_object_type: transformation_child = transformation_child
    """
    child_object_type of transformation.
    """
