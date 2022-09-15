#
# This is an auto-generated file.  DO NOT EDIT!
#

SHASH = "87c9632e542b91b2a30e1f912a825b5f952a9a5fd12ca367367686cdc2cfe296"

from ansys.systemcoupling.core.adaptor.impl.datamodel import *

from .activate_hidden import activate_hidden
from .add_participant import add_participant
from .analysis_control import analysis_control
from .coupling_interface import coupling_interface
from .coupling_participant import coupling_participant
from .get_parameter_options import get_parameter_options
from .library import library
from .output_control import output_control
from .partition_participants import partition_participants
from .save import save
from .solution_control import solution_control
from .solve import solve


class setup_root(Group):
    """
    'root' object
    """

    syc_name = "SystemCoupling"

    child_names = [
        "activate_hidden",
        "library",
        "coupling_participant",
        "analysis_control",
        "coupling_interface",
        "solution_control",
        "output_control",
    ]

    activate_hidden: activate_hidden = activate_hidden
    """
    activate_hidden child of setup_root.
    """
    library: library = library
    """
    library child of setup_root.
    """
    coupling_participant: coupling_participant = coupling_participant
    """
    coupling_participant child of setup_root.
    """
    analysis_control: analysis_control = analysis_control
    """
    analysis_control child of setup_root.
    """
    coupling_interface: coupling_interface = coupling_interface
    """
    coupling_interface child of setup_root.
    """
    solution_control: solution_control = solution_control
    """
    solution_control child of setup_root.
    """
    output_control: output_control = output_control
    """
    output_control child of setup_root.
    """
    command_names = [
        "add_participant",
        "solve",
        "save",
        "get_parameter_options",
        "partition_participants",
    ]

    add_participant: add_participant = add_participant
    """
    add_participant command of setup_root.
    """
    solve: solve = solve
    """
    solve command of setup_root.
    """
    save: save = save
    """
    save command of setup_root.
    """
    get_parameter_options: get_parameter_options = get_parameter_options
    """
    get_parameter_options command of setup_root.
    """
    partition_participants: partition_participants = partition_participants
    """
    partition_participants command of setup_root.
    """
