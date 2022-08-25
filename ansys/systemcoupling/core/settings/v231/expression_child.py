#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *


class expression_child(Group):
    """
    Define a named expression that can be referenced in other expressions.
    """

    syc_name = "child_object_type"

    property_names_types = [
        ("expression_name", "ExpressionName", "String"),
        ("expression_string", "ExpressionString", "String"),
    ]

    @property
    def expression_name(self) -> String:
        """Name used to reference this expression from another expression"""
        return self.get_property_state("expression_name")

    @expression_name.setter
    def expression_name(self, value: String):
        self.set_property_state("expression_name", value)

    @property
    def expression_string(self) -> String:
        """String defining the expression."""
        return self.get_property_state("expression_string")

    @expression_string.setter
    def expression_string(self, value: String):
        self.set_property_state("expression_string", value)
