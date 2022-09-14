#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class value(String):
    """
    String specifying the expression to use on the source side of the data
    transfer. Used when creating an expression-based data transfer. If the
    ``target_variable`` is a vector, a vector-valued expression must be provided.
    Alternatively, ``value_x``, ``value_y``, ``value_z`` may be used to specify the
    individual components of the vector expression.
    """

    syc_name = "Value"
