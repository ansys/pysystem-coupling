#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class expression_function_child(Group):
    """
    Use ExpressionFunction objects to make the return value(s) from external
    Python functions available for use in expressions. For example, an
    external Python function that parses simulation output and returns
    a real value could be used to adaptively set the time step size.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("module", "Module", "String"),
        ("function", "Function", "String"),
        ("function_name", "FunctionName", "String"),
    ]

    @property
    def module(self) -> String:
        """Python module containing the definition of the Function to be added to the coupled analysis."""
        return self.get_property_state("module")

    @module.setter
    def module(self, value: String):
        self.set_property_state("module", value)

    @property
    def function(self) -> String:
        """Python name of the function to be added to the coupled analysis."""
        return self.get_property_state("function")

    @function.setter
    def function(self, value: String):
        self.set_property_state("function", value)

    @property
    def function_name(self) -> String:
        """Name to be referenced when using the function in an expression."""
        return self.get_property_state("function_name")

    @function_name.setter
    def function_name(self, value: String):
        self.set_property_state("function_name", value)
