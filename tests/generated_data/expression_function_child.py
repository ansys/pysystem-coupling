#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class expression_function_child(Group):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("module", "Module", "String"),
        ("function", "Function", "String"),
        ("function_name", "FunctionName", "String"),
    ]

    @property
    def module(self) -> String:
        """'module' property of 'expression_function' object"""
        return self.get_property_state("module")

    @module.setter
    def module(self, value: String):
        self.set_property_state("module", value)

    @property
    def function(self) -> String:
        """'function' property of 'expression_function' object"""
        return self.get_property_state("function")

    @function.setter
    def function(self, value: String):
        self.set_property_state("function", value)

    @property
    def function_name(self) -> String:
        """'function_name' property of 'expression_function' object"""
        return self.get_property_state("function_name")

    @function_name.setter
    def function_name(self, value: String):
        self.set_property_state("function_name", value)
