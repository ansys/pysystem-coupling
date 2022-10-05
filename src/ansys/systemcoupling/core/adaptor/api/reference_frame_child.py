#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .transformation import transformation


class reference_frame_child(Container):
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
        ("option", "Option", "str"),
        ("parent_reference_frame", "ParentReferenceFrame", "str"),
        ("transformation_order", "TransformationOrder", "StringListType"),
        ("transformation_matrix", "TransformationMatrix", "RealListType"),
    ]

    @property
    def option(self) -> str:
        """Method used to define the transformation from the parent reference frame.

        - \"ByTransformation\" - Define the reference frame by one or more
          transformation operations.
        - \"Automatic\" - Align source and target automatically.
        - \"ByMatrix\" - Only available if Alpha features are activated."""
        return self.get_property_state("option")

    @option.setter
    def option(self, value: str):
        self.set_property_state("option", value)

    @property
    def parent_reference_frame(self) -> str:
        """Set the parent reference frame."""
        return self.get_property_state("parent_reference_frame")

    @parent_reference_frame.setter
    def parent_reference_frame(self, value: str):
        self.set_property_state("parent_reference_frame", value)

    @property
    def transformation_order(self) -> StringListType:
        """List names of transformations in the order in which they apply.

        Available for the ``ByTransformation`` option."""
        return self.get_property_state("transformation_order")

    @transformation_order.setter
    def transformation_order(self, value: StringListType):
        self.set_property_state("transformation_order", value)

    @property
    def transformation_matrix(self) -> RealListType:
        """Define the transformation matrix when ``ByTransformation`` option is active."""
        return self.get_property_state("transformation_matrix")

    @transformation_matrix.setter
    def transformation_matrix(self, value: RealListType):
        self.set_property_state("transformation_matrix", value)
