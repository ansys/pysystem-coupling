#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


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

    class snapshot_name(String):
        """
        Name of the snapshot to be deleted.
        """

        syc_name = "SnapshotName"
