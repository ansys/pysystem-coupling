#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .reference_frame_child import reference_frame_child


class reference_frame(NamedContainer[reference_frame_child]):
    """
    Provide a transformation relative to a ParentReferenceFrame.
    """

    syc_name = "ReferenceFrame"

    child_object_type: reference_frame_child = reference_frame_child
    """
    child_object_type of reference_frame.
    """
