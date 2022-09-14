#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .transformation import transformation


class reference_frame_child(Group):
    """
    Provide a transformation relative to a ParentReferenceFrame.
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
        """Method used to define the transformation from the parent reference frame.

        - \"ByTransformation\" - Define the reference frame by one or more
          transformation operations.
        - \"Automatic\" - Only available if Alpha features are activated.
        - \"ByMatrix\" - Only available if Alpha features are activated."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: String):
        self.set_property_state("option", value)

    @property
    def parent_reference_frame(self) -> String:
        """Set the parent reference frame."""
        return self.get_property_state("parent_reference_frame")

    @parent_reference_frame.setter
    def parent_reference_frame(self, value: String):
        self.set_property_state("parent_reference_frame", value)

    @property
    def transformation_order(self) -> StringList:
        """List names of transformations in the order in which they apply.

        Available for the ``ByTransformation`` option."""
        return self.get_property_state("transformation_order")

    @transformation_order.setter
    def transformation_order(self, value: StringList):
        self.set_property_state("transformation_order", value)

    @property
    def transformation_matrix(self) -> RealList:
        """Define the transformation matrix when ``ByTransformation`` option is active."""
        return self.get_property_state("transformation_matrix")

    @transformation_matrix.setter
    def transformation_matrix(self, value: RealList):
        self.set_property_state("transformation_matrix", value)
