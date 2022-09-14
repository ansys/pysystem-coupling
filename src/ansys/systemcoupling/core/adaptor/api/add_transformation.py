#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .angle import angle
from .axis import axis
from .reference_frame_1 import reference_frame
from .transformation_type import transformation_type
from .vector import vector


class add_transformation(Command):
    """
    Add a transformation to a reference frame defined in the datamodel

    Given the reference frame to add to the transform to, the type of transform
    to be added, and any required information for the transformation, add the
    transformation to the referenceFrame. Not all parameters are required for
    every transformation.

    The name of the transformation will be based on the type of transformation.
    The name will be of the form ``<transformation_type>-#`` where ``#`` is the first
    positive integer which yields a unique frame name.

    The transformation will also be added to the end of the ``transformation_order``
    list for the reference frame.

    Returns the name of the transformation.

    Parameters
    ----------
    reference_frame : str
        Name of the reference frame to which the transformation will be added.
    transformation_type : str
        Type of transformation to be added. Available options are \"Rotation\" or
        \"Translation\".

        Required Parameters for Transformation Types:
            Rotation: ``angle``, ``axis``, ``vector`` (if ``axis`` is \"UserDefined\")
            Translation: ``vector``
    angle : real, optional
        Angle to rotate a reference frame. Used with \"Rotation\"
        ``transformation_type``. Default unit is Radians.
    axis : str, optional
        Axis about which a rotation is applied. Used with
        Rotation ``transformation_type``. Available options are: \"XAxis\", \"YAxis\",
        \"ZAxis\", and \"UserDefined\".
    vector : typing.Tuple[real, real, real], optional
        A vector for use with \"Translation\" ``transformation_type`` or \"Rotation\"
        ``transformation_type`` if the ``axis`` is \"UserDefined\".

    """

    syc_name = "AddTransformation"

    argument_names = [
        "reference_frame",
        "transformation_type",
        "angle",
        "axis",
        "vector",
    ]

    reference_frame: reference_frame = reference_frame
    """
    reference_frame argument of add_transformation.
    """
    transformation_type: transformation_type = transformation_type
    """
    transformation_type argument of add_transformation.
    """
    angle: angle = angle
    """
    angle argument of add_transformation.
    """
    axis: axis = axis
    """
    axis argument of add_transformation.
    """
    vector: vector = vector
    """
    vector argument of add_transformation.
    """
