#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .reference_frame_child import reference_frame_child


class reference_frame(NamedObject[reference_frame_child]):
    """
    Provide a transformation relative to a ParentReferenceFrame.
    """

    syc_name = "ReferenceFrame"

    child_object_type: reference_frame_child = reference_frame_child
    """
    child_object_type of reference_frame.
    """
