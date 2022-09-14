#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class value(String):
    """
    String specifying the expression to use on the source side of the data
    transfer. Used when creating an expression-based data transfer if the
    ``target_variable`` is a scalar. (If the ``target_variable`` is a vector,
    ``value_x``, ``value_y``, ``value_z`` must be used instead.)
    """

    syc_name = "Value"
