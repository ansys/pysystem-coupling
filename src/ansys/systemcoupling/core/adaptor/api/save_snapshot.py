#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.impl.types import *


class save_snapshot(Command):
    """
    Saves a snapshot of the current state of the simulation. Snapshot will
    contain all files and directories within the working directory that are
    tracked by System Coupling: the SyC directory and the working directories
    of all loaded participants. Before saving the snapshot, the current
    datamodel will be saved.

    Note: Snapshot cannot be saved if participants have been started.

    Note: If files required for cosimulation are not stored within the working
    directory, then they will not be included in the snapshot.

    Parameters
    ----------
    snapshot_name : str
        Name of the snapshot to be saved.
    overwrite_existing : bool, optional
        Boolean argument controlling whether an existing snapshot should be
        overwritten. If ``True``, then an existing snapshot named ``snapshot_name`` will
        be overwritten if it exists. If ``False`` (default), then if ``snapshot_name`` is
        shared with an existing snapshot, a warning will be written and the
        command will return without saving the snapshot.

    """

    syc_name = "SaveSnapshot"

    argument_names = ["snapshot_name", "overwrite_existing"]

    class snapshot_name(String):
        """
        Name of the snapshot to be saved.
        """

        syc_name = "SnapshotName"

    class overwrite_existing(Boolean):
        """
        Boolean argument controlling whether an existing snapshot should be
        overwritten. If ``True``, then an existing snapshot named ``snapshot_name`` will
        be overwritten if it exists. If ``False`` (default), then if ``snapshot_name`` is
        shared with an existing snapshot, a warning will be written and the
        command will return without saving the snapshot.
        """

        syc_name = "OverwriteExisting"
