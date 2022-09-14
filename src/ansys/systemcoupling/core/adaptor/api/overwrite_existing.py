#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.systemcoupling.core.adaptor.datamodel import *


class overwrite_existing(Boolean):
    """
    Boolean argument controlling whether an existing snapshot should be
    overwritten. If ``True``, then an existing snapshot named ``snapshot_name`` will
    be overwritten if it exists. If ``False`` (default), then if ``snapshot_name`` is
    shared with an existing snapshot, a warning will be written and the
    command will return without saving the snapshot.
    """

    syc_name = "OverwriteExisting"
