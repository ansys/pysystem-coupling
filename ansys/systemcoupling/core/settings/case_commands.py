"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "fe67c5e67ce461434dcf4ceee00c23c296167687ce0efb5e8e9d445f69e510ed"


class case_commands(Group):
    """
    root object
    """

    syc_name = "CaseCommands"
    command_names = ["open", "save", "save_snapshot", "open_snapshot", "get_snapshots"]

    class open(Command):
        """
        'open' child of 'case_commands' object

        Parameters
        ----------
            coupling_step : int
                'coupling_step' child of 'open' object
            coupling_iteration : int
                'coupling_iteration' child of 'open' object
            file_path : str
                'file_path' child of 'open' object

        """

        syc_name = "Open"
        argument_names = ["coupling_step", "coupling_iteration", "file_path"]
        essential_arguments = []

        class coupling_step(Integer):
            """
            'coupling_step' child of 'open' object
            """

            syc_name = "CouplingStep"

        class coupling_iteration(Integer):
            """
            'coupling_iteration' child of 'open' object
            """

            syc_name = "CouplingIteration"

        class file_path(String):
            """
            'file_path' child of 'open' object
            """

            syc_name = "FilePath"

    class save(Command):
        """
        'save' child of 'case_commands' object

        Parameters
        ----------
            file_path : str
                'file_path' child of 'save' object

        """

        syc_name = "Save"
        argument_names = ["file_path"]
        essential_arguments = []

        class file_path(String):
            """
            'file_path' child of 'save' object
            """

            syc_name = "FilePath"

    class save_snapshot(Command):
        """
        'save_snapshot' child of 'case_commands' object

        Parameters
        ----------
            snapshot_name : str
                'snapshot_name' child of 'save_snapshot' object
            overwrite_existing : bool
                'overwrite_existing' child of 'save_snapshot' object

        """

        syc_name = "SaveSnapshot"
        argument_names = ["snapshot_name", "overwrite_existing"]
        essential_arguments = ["snapshot_name"]

        class snapshot_name(String):
            """
            'snapshot_name' child of 'save_snapshot' object
            """

            syc_name = "SnapshotName"

        class overwrite_existing(Boolean):
            """
            'overwrite_existing' child of 'save_snapshot' object
            """

            syc_name = "OverwriteExisting"

    class open_snapshot(Command):
        """
        'open_snapshot' child of 'case_commands' object

        Parameters
        ----------
            snapshot_name : str
                'snapshot_name' child of 'open_snapshot' object

        """

        syc_name = "OpenSnapshot"
        argument_names = ["snapshot_name"]
        essential_arguments = []

        class snapshot_name(String):
            """
            'snapshot_name' child of 'open_snapshot' object
            """

            syc_name = "SnapshotName"

    class get_snapshots(Command):
        """
        'get_snapshots' child of 'case_commands' object
        """

        syc_name = "GetSnapshots"
