#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class value_x(String):
    """
    String specifying the X component of the expression to use on the
    source side of the data transfer. This may optionally be used when creating
    an expression-based data transfer if the ``arget_variable`` is a vector as an
    alternative to specifying a vector-valued expression in ``value`. ``value_y`` and
    ``value_z`` are also required if ``value_x`` is used.
    """

    syc_name = "ValueX"
