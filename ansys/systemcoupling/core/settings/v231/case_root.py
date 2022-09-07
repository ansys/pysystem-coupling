#
# This is an auto-generated file.  DO NOT EDIT!
#

SHASH = "c974aba9f7923acbc59ebba97a68b584121a95c1aec277efd11334a328f5b757"

from ansys.systemcoupling.core.settings.datamodel import *

from .clear_state import clear_state
from .delete_snapshot import delete_snapshot
from .get_snapshots import get_snapshots
from .open import open
from .open_snapshot import open_snapshot
from .save import save
from .save_snapshot import save_snapshot


class case_root(Group):
    """
    'root' object
    """

    syc_name = "CaseCommands"

    command_names = [
        "clear_state",
        "open",
        "save",
        "save_snapshot",
        "open_snapshot",
        "delete_snapshot",
        "get_snapshots",
    ]

    clear_state: clear_state = clear_state
    """
    clear_state command of case_root.
    """
    open: open = open
    """
    open command of case_root.
    """
    save: save = save
    """
    save command of case_root.
    """
    save_snapshot: save_snapshot = save_snapshot
    """
    save_snapshot command of case_root.
    """
    open_snapshot: open_snapshot = open_snapshot
    """
    open_snapshot command of case_root.
    """
    delete_snapshot: delete_snapshot = delete_snapshot
    """
    delete_snapshot command of case_root.
    """
    get_snapshots: get_snapshots = get_snapshots
    """
    get_snapshots command of case_root.
    """
