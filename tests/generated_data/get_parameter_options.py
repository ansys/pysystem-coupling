#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class get_parameter_options(PathCommand):
    """
    'get_parameter_options' child.

    Parameters
    ----------
    name : str, optional
        'name' child.

    """

    syc_name = "GetParameterOptions"

    argument_names = ["name"]

    class name(String):
        """
        'name' child.
        """

        syc_name = "Name"
