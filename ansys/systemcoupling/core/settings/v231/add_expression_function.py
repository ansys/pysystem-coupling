#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .function import function
from .function_name import function_name
from .module import module


class add_expression_function(Command):
    """
    Creates an expression function object in the data model that makes
    available an external Python function for use in expressions.

    The parameters specified should correspond to a module and function
    that exists and can successfully be loaded when the application
    starts. Otherwise, the data model object will be created but there
    will be validation errors and the function will not be available for
    use.

    Parameters
    ----------
        module : str
            The name of the Python module (in the 'Modules' sub-directory of
    the working directory) from which the function is to be obtained.
        function : str
            The name of the function in the module. If no ??function_name?? is
    specified, this will also be the name by which the function should
    be referenced when used in an expression.
        function_name : str
            Optionally specify a different name from ??function?? which should be
    the name used to reference the function in an expression.

    """

    syc_name = "AddExpressionFunction"

    argument_names = ["module", "function", "function_name"]

    module: module = module
    """
    module argument of add_expression_function.
    """
    function: function = function
    """
    function argument of add_expression_function.
    """
    function_name: function_name = function_name
    """
    function_name argument of add_expression_function.
    """