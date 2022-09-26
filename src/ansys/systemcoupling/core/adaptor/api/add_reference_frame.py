#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class add_reference_frame(Command):
    """
    Add a reference frame to the datamodel

    The function will add a blank reference frame to the datamodel. Any
    transformations must be added separately.

    Reference frame name will be "Frame-#" where # is the first positive
    integer which yields a unique frame name.

    Returns the name of the reference frame.

    Parameters
    ----------
    parent_reference_frame : str, optional
        Name of a reference frame that the added frame should use as the
        parent. If the argument is not provided, the default parent reference
        frame "GlobalReferenceFrame" will be added.

    """

    syc_name = "AddReferenceFrame"

    argument_names = ["parent_reference_frame"]

    class parent_reference_frame(String):
        """
        Name of a reference frame that the added frame should use as the
        parent. If the argument is not provided, the default parent reference
        frame "GlobalReferenceFrame" will be added.
        """

        syc_name = "ParentReferenceFrame"
