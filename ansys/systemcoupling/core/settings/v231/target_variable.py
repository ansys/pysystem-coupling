#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class target_variable(String):
    """
    String specifying the name of the variable on the target side of
    the data transfer. Must be combined with either ``source_variable`` (when
    creating a variable-based data transfer) or with ``value`` (or
    ``value_{x|y|z}`` (when creating an expression-based data transfer).
    """

    syc_name = "TargetVariable"
