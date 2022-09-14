#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .binary import binary
from .file_name import file_name


class write_ensight(Command):
    """
    Write a file with mesh and results which can be loaded into Ensight for
    post processing.

    Parameters
    ----------
    file_name : str
        Base name for Ensight files. It will generate <base>.encas file which
        should be loaded into Ensight. Other files are generated for geometry
        and variables.
    binary : bool, optional
        To control if file is to be written in binary format or ASCII. ASCII
        slows down performance, but may be useful for debugging and seeing
        raw data.

    """

    syc_name = "WriteEnSight"

    argument_names = ["file_name", "binary"]

    file_name: file_name = file_name
    """
    file_name argument of write_ensight.
    """
    binary: binary = binary
    """
    binary argument of write_ensight.
    """
