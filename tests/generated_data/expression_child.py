#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class expression_child(Container):
    """
    'child_object_type' child.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("expression_name", "ExpressionName", "String"),
        ("expression_string", "ExpressionString", "String"),
    ]

    @property
    def expression_name(self) -> String:
        """'expression_name' property of 'expression' object"""
        return self.get_property_state("expression_name")

    @expression_name.setter
    def expression_name(self, value: String):
        self.set_property_state("expression_name", value)

    @property
    def expression_string(self) -> String:
        """'expression_string' property of 'expression' object"""
        return self.get_property_state("expression_string")

    @expression_string.setter
    def expression_string(self, value: String):
        self.set_property_state("expression_string", value)
