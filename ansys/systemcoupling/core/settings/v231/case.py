"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "d7f6737520f140622a0f9f2dd2bf3e7189955ef9503e64ce405404a20604c8e8"


class root(Group):
    """
    root object
    """

    syc_name = "CaseCommands"
    command_names = ["open", "save", "save_snapshot", "open_snapshot", "get_snapshots"]

    class open(Command):
        """
        'open' child of 'root' object

        Parameters
        ----------
            file_path : str
                'file_path' child of 'open' object
            coupling_step : int
                'coupling_step' child of 'open' object
            coupling_iteration : int
                'coupling_iteration' child of 'open' object

        """

        syc_name = "Open"
        argument_names = ["file_path", "coupling_step", "coupling_iteration"]
        essential_arguments = []

        class file_path(String):
            """
            'file_path' child of 'open' object
            """

            syc_name = "FilePath"

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

    class save(Command):
        """
        'save' child of 'root' object

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
        'save_snapshot' child of 'root' object

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
        'open_snapshot' child of 'root' object

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
        'get_snapshots' child of 'root' object
        """

        syc_name = "GetSnapshots"
