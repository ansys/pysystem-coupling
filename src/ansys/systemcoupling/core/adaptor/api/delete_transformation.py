#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class delete_transformation(Command):
    """
    Delete a transformation from a reference frame

    In addition to deleting the transformation object, it will also remove the
    transformation from ``transformation_order`` (if it exists in that list).

    Parameters
    ----------
    reference_frame : str
        Name of the reference frame from which the transformation will be
        deleted.
    transformation_name : str
        Name of the transformation which will be deleted.

    """

    syc_name = "DeleteTransformation"

    argument_names = ["reference_frame", "transformation_name"]

    class reference_frame(String):
        """
        Name of the reference frame from which the transformation will be
        deleted.
        """

        syc_name = "ReferenceFrame"

    class transformation_name(String):
        """
        Name of the transformation which will be deleted.
        """

        syc_name = "TransformationName"
