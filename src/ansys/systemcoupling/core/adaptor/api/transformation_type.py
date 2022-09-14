#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class transformation_type(String):
    """
    Type of transformation to be added. Available options are \"Rotation\" or
    \"Translation\".

    Required Parameters for Transformation Types:
        Rotation: ``angle``, ``axis``, ``vector`` (if ``axis`` is \"UserDefined\")
        Translation: ``vector``
    """

    syc_name = "TransformationType"
