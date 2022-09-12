#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.settings.datamodel import *

from .file_path import file_path


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

    file_path: file_path = file_path
    """
    file_path argument of save.
    """
