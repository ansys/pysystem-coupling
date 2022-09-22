#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.datamodel import *


class save(Command):
    """
    'save' child.

    Parameters
    ----------
    file_path : str, optional
        'file_path' child.

    """

    syc_name = "Save"

    argument_names = ["file_path"]

    class file_path(String):
        """
        'file_path' child.
        """

        syc_name = "FilePath"
