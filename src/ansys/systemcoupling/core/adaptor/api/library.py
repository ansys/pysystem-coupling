#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .expression import expression
from .expression_function import expression_function
from .instancing import instancing
from .reference_frame import reference_frame


class library(Container):
    """
    Contains objects that can be referenced from elsewhere in the data model.
    """

    syc_name = "Library"

    child_names = ["expression", "expression_function", "reference_frame", "instancing"]

    expression: expression = expression
    """
    expression child of library.
    """
    expression_function: expression_function = expression_function
    """
    expression_function child of library.
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of library.
    """
    instancing: instancing = instancing
    """
    instancing child of library.
    """
