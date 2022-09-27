#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class expression_function_child(Container):
    """
    Makes an external Python function accessible from expressions.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("module", "Module", "str"),
        ("function", "Function", "str"),
        ("function_name", "FunctionName", "str"),
    ]

    @property
    def module(self) -> str:
        """Name of the Python module that exports the function."""
        return self.get_property_state("module")

    @module.setter
    def module(self, value: str):
        self.set_property_state("module", value)

    @property
    def function(self) -> str:
        """Name of the function in the module."""
        return self.get_property_state("function")

    @function.setter
    def function(self, value: str):
        self.set_property_state("function", value)

    @property
    def function_name(self) -> str:
        """Name to use when referencing the function in an expression."""
        return self.get_property_state("function_name")

    @function_name.setter
    def function_name(self, value: str):
        self.set_property_state("function_name", value)
