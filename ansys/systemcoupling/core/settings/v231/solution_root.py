#
# This is an auto-generated file.  DO NOT EDIT!
#

SHASH = "dd6c122be5eb1538f9ccc910b73d702025d7e936f5b1220892fc5e25de1e26d7"

from ansys.systemcoupling.core.settings.datamodel import *

from .create_restart_point import create_restart_point
from .initialize import initialize
from .open_results_in_ensight import open_results_in_ensight
from .partition_participants import partition_participants
from .shutdown import shutdown
from .solve import solve
from .start_participants import start_participants
from .step import step
from .write_csv_chart_files import write_csv_chart_files
from .write_ensight import write_ensight


class solution_root(Group):
    """
    'root' object
    """

    syc_name = "SolutionCommands"

    command_names = [
        "start_participants",
        "initialize",
        "shutdown",
        "solve",
        "step",
        "partition_participants",
        "open_results_in_ensight",
        "write_ensight",
        "create_restart_point",
        "write_csv_chart_files",
    ]

    start_participants: start_participants = start_participants
    """
    start_participants command of solution_root.
    """
    initialize: initialize = initialize
    """
    initialize command of solution_root.
    """
    shutdown: shutdown = shutdown
    """
    shutdown command of solution_root.
    """
    solve: solve = solve
    """
    solve command of solution_root.
    """
    step: step = step
    """
    step command of solution_root.
    """
    partition_participants: partition_participants = partition_participants
    """
    partition_participants command of solution_root.
    """
    open_results_in_ensight: open_results_in_ensight = open_results_in_ensight
    """
    open_results_in_ensight command of solution_root.
    """
    write_ensight: write_ensight = write_ensight
    """
    write_ensight command of solution_root.
    """
    create_restart_point: create_restart_point = create_restart_point
    """
    create_restart_point command of solution_root.
    """
    write_csv_chart_files: write_csv_chart_files = write_csv_chart_files
    """
    write_csv_chart_files command of solution_root.
    """
