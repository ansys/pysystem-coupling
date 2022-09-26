#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .attribute_child import attribute_child


class attribute(NamedContainer[attribute_child]):
    """
    Configure a variable's attributes.
    """

    syc_name = "Attribute"

    child_object_type: attribute_child = attribute_child
    """
    child_object_type of attribute.
    """
