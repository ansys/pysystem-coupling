#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .name import name


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

    name: name = name
    """
    name argument of get_parameter_options.
    """
