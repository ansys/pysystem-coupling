#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .reference_frame_child import reference_frame_child


class reference_frame(NamedObject[reference_frame_child]):
    """
    Use ReferenceFrame objects to create transformations from the global (analysis-level) reference, which can then be defined for coupling interface sides.
    """

    syc_name = "ReferenceFrame"

    child_object_type: reference_frame_child = reference_frame_child
    """
    child_object_type of reference_frame.
    """
