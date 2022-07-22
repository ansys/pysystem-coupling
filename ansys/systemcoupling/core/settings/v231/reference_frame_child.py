#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .transformation import transformation


class reference_frame_child(Group):
    """
    Use ReferenceFrame objects to create transformations from the global (analysis-level) reference, which can then be defined for coupling interface sides.
    """

    syc_name = "child_object_type"

    child_names = ["transformation"]

    transformation: transformation = transformation
    """
    transformation child of reference_frame_child.
    """
    property_names_types = [
        ("option", "Option", "String"),
        ("parent_reference_frame", "ParentReferenceFrame", "String"),
        ("transformation_order", "TransformationOrder", "StringList"),
        ("transformation_matrix", "TransformationMatrix", "RealList"),
    ]

    @property
    def option(self) -> String:
        """Method used to define transformations from the global reference frame."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def parent_reference_frame(self) -> String:
        """Parent reference frame for the current ReferenceFrame object."""
        return self.get_property_state("parent_reference_frame")

    @parent_reference_frame.setter
    def parent_reference_frame(self, value: String):
        self.set_property_state("parent_reference_frame", value)

    @property
    def transformation_order(self) -> StringList:
        """Available when ReferenceFrame.Option is set to ByTransformation. Relevant only when multiple transformations from the same parent reference frame are defined."""
        return self.get_property_state("transformation_order")

    @transformation_order.setter
    def transformation_order(self, value: StringList):
        self.set_property_state("transformation_order", value)

    @property
    def transformation_matrix(self) -> RealList:
        """**CURRENTLY NOT DOCUMENTED**"""
        return self.get_property_state("transformation_matrix")

    @transformation_matrix.setter
    def transformation_matrix(self, value: RealList):
        self.set_property_state("transformation_matrix", value)
