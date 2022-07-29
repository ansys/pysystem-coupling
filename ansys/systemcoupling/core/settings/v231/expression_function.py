#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .expression_function_child import expression_function_child


class expression_function(NamedObject[expression_function_child]):
    """
    Use ExpressionFunction objects to make the return value(s) from external
    Python functions available for use in expressions. For example, an
    external Python function that parses simulation output and returns
    a real value could be used to adaptively set the time step size.
    """

    syc_name = "ExpressionFunction"

    child_object_type: expression_function_child = expression_function_child
    """
    child_object_type of expression_function.
    """
