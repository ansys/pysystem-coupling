#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class open_snapshot(Command):
    """
    Opens a snapshot containing a previously saved state of the simulation.
    All state (files and directories) stored in the snapshot will be restored.
    If other state exists in the working directory, then it will not be
    modified by this command.

    Note: Snapshot cannot be opened if participants have been started.

    Parameters
    ----------
    snapshot_name : str, optional
        The name of the snapshot to be opened. This is optional if and only if
        there is only one snapshot available to be loaded. If multiple
        snapshots exist, then the snapshot name must be specified.

    """

    syc_name = "OpenSnapshot"

    argument_names = ["snapshot_name"]

    class snapshot_name(String):
        """
        The name of the snapshot to be opened. This is optional if and only if
        there is only one snapshot available to be loaded. If multiple
        snapshots exist, then the snapshot name must be specified.
        """

        syc_name = "SnapshotName"
