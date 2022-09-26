#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class add_named_expression(Command):
    """
    Creates a named expression object in the data model.
    If there is already an object in the data model whose ``expression_name``
    matches the provided ``expression_name``, its ``expression_string`` will be
    overwritten with the provided ``expression_string``

    Parameters
    ----------
    expression_name : str
        The name by which this expression should be referenced when used in
        another expression.
    expression_string : str
        String containing the definition of the expression.

    """

    syc_name = "AddNamedExpression"

    argument_names = ["expression_name", "expression_string"]

    class expression_name(String):
        """
        The name by which this expression should be referenced when used in
        another expression.
        """

        syc_name = "ExpressionName"

    class expression_string(String):
        """
        String containing the definition of the expression.
        """

        syc_name = "ExpressionString"
