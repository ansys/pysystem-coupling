#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class value_y(String):
    """
    String specifying the Y component of the expression to use on the
    source side of the data transfer. Used when crating an expression-based
    data transfer if the ``target_variable`` is a vector. (If the ``target_variable``
    is scalar, ``value`` must be used instead.) ``value_x`` and ``value_z`` are also
    required if ``value_y`` is used.
    """

    syc_name = "ValueY"