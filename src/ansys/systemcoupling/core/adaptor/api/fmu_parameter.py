#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *

from .fmu_parameter_child import fmu_parameter_child


class fmu_parameter(NamedContainer[fmu_parameter_child]):
    """
    Configure a parameter for an FMU coupling participant.
    """

    syc_name = "FMUParameter"

    child_object_type: fmu_parameter_child = fmu_parameter_child
    """
    child_object_type of fmu_parameter.
    """
