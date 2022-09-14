#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *

from .snapshot_name_2 import snapshot_name


class delete_snapshot(Command):
    """
    Deletes a snapshot if it exists.

    Parameters
    ----------
    snapshot_name : str
        Name of the snapshot to be deleted.

    """

    syc_name = "DeleteSnapshot"

    argument_names = ["snapshot_name"]

    snapshot_name: snapshot_name = snapshot_name
    """
    snapshot_name argument of delete_snapshot.
    """
