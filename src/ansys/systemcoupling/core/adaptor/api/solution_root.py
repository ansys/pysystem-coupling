#
# This is an auto-generated file.  DO NOT EDIT!
#

SHASH = "27c8965e90341cbb34e5988228cec247cbb77badd07a8d3141434a9c39a95416"

from ansys.systemcoupling.core.adaptor.datamodel import *

from .abort import abort
from .create_restart_point import create_restart_point
from .get_machines import get_machines
from .initialize import initialize
from .interrupt import interrupt
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
        "get_machines",
        "interrupt",
        "abort",
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
    get_machines: get_machines = get_machines
    """
    get_machines command of solution_root.
    """
    interrupt: interrupt = interrupt
    """
    interrupt command of solution_root.
    """
    abort: abort = abort
    """
    abort command of solution_root.
    """
