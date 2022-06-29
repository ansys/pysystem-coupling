"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "50b62d4fe1d82d8d54b2b40edc7c5a86b7d288a875962168ff1aee92197aca7b"


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

    class clear_state(Command):
        """
        Clears the state of the entire System Coupling service, removing all
        data model items, parameter values, and calculated values.

        Cannot be run after participants have been started.
        """

        syc_name = "ClearState"

    class open(Command):
        """
        Reads the state of a coupled analysis. The state consists of settings to
        populate the datamodel and results to restart the analysis at the end of
        a specified coupling step.

        Settings are stored in a file named Settings.h5. ??results?? files may
        correspond either to coupling iterations or coupling steps, depending on
        the analysis type and the types of participants involved.

        By default, this command looks for the "SyC" directory in the current
        working directory. By default, if multiple ??results?? files exist, the
        most recent one is opened.

        If given optional arguments, behaves as described below in "Optional
        Keyword Arguments".

        Cannot be run after the participants have been started.

        Parameters
        ----------
            file_path : str
                Working directory containing the SyC subdirectory (and its .h5
        file(s)) to be read.
            coupling_step : int
                Integer specifying the coupling step at which the coupled analysis is
        restarted. When used, System Coupling reads the corresponding
        Results_step<#>.h5 file in the specified directory and restarts the
        analysis at the end of the specified coupling step. When this argument
        is used, System Coupling automatically removes the output files related
        to all later coupling steps. If the files cannot be removed, then
        System Coupling generates an exception message instructing you to free
        up the files and reissue the ??open?? command with the ??coupling_step??
        argument. If the simulation's ??results?? files are associated with
        coupling iterations, then System Coupling prints an error message
        indicating this.
            coupling_iteration : int
                Integer specifying the coupling iteration at which the coupled analysis
        is restarted. When used, System Coupling reads the corresponding
        Results_iter<#>.h5 file in the specified directory and restarts the
        analysis at the end of the specified coupling iteration. When this
        argument is used, System Coupling automatically removes the output
        files related to all later coupling iterations. If the files cannot be
        removed, then System Coupling generates an exception message
        instructing you to free up the files and reissue the ??open?? command with
        the ??coupling_iteration?? argument. If the simulation's ??results?? files are
        associated with coupling steps, then System Coupling prints an error
        message indicating this.

        """

        syc_name = "Open"
        argument_names = ["file_path", "coupling_step", "coupling_iteration"]
        essential_arguments = []

        class file_path(String):
            """
            Working directory containing the SyC subdirectory (and its .h5
            file(s)) to be read.
            """

            syc_name = "FilePath"

        class coupling_step(Integer):
            """
            Integer specifying the coupling step at which the coupled analysis is
            restarted. When used, System Coupling reads the corresponding
            Results_step<#>.h5 file in the specified directory and restarts the
            analysis at the end of the specified coupling step. When this argument
            is used, System Coupling automatically removes the output files related
            to all later coupling steps. If the files cannot be removed, then
            System Coupling generates an exception message instructing you to free
            up the files and reissue the ??open?? command with the ??coupling_step??
            argument. If the simulation's ??results?? files are associated with
            coupling iterations, then System Coupling prints an error message
            indicating this.
            """

            syc_name = "CouplingStep"

        class coupling_iteration(Integer):
            """
            Integer specifying the coupling iteration at which the coupled analysis
            is restarted. When used, System Coupling reads the corresponding
            Results_iter<#>.h5 file in the specified directory and restarts the
            analysis at the end of the specified coupling iteration. When this
            argument is used, System Coupling automatically removes the output
            files related to all later coupling iterations. If the files cannot be
            removed, then System Coupling generates an exception message
            instructing you to free up the files and reissue the ??open?? command with
            the ??coupling_iteration?? argument. If the simulation's ??results?? files are
            associated with coupling steps, then System Coupling prints an error
            message indicating this.
            """

            syc_name = "CouplingIteration"

    class save(Command):
        """
        Saves the state of the coupled analysis data model.

        --  Analysis settings are written to a single Settings.h5 file which
            can be used to reload analysis settings.

        --  Restart files for all restart points in the current co-simulation will
            be written when this command is called. Existing restart files from
            previous System Coupling versions will be renamed to conform to the new
            naming scheme.

        --  Restart files are named according to the convention
            Restart_step#.h5 or Restart_iter#.h5, where "#" is the index of
            the corresponding coupling step or iteration.

        Returns a Boolean value of 'True' if the files were saved successfully;
        otherwise, returns a value of 'False'.

        Note that this command will raise an exception if another instance of
        System Coupling is solving in the current working directory.

        If given optional arguments, then behaves as described below in "Optional
        Keyword Arguments."

        Parameters
        ----------
            file_path : str
                Writeable directory to which the SyC directory is added. (Settings and
        ??results?? .h5 files will be written to the SyC directory.)

        """

        syc_name = "Save"
        argument_names = ["file_path"]
        essential_arguments = []

        class file_path(String):
            """
            Writeable directory to which the SyC directory is added. (Settings and
            ??results?? .h5 files will be written to the SyC directory.)
            """

            syc_name = "FilePath"

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
            overwrite_existing : bool
                Boolean argument controlling whether an existing snapshot should be
        overwritten. If True, then an existing snapshot named ??snapshot_name?? will
        be overwritten if it exists. If False (default), then if ??snapshot_name?? is
        shared with an existing snapshot, a warning will be written and the
        command will return without saving the snapshot.

        """

        syc_name = "SaveSnapshot"
        argument_names = ["snapshot_name", "overwrite_existing"]
        essential_arguments = ["snapshot_name"]

        class snapshot_name(String):
            """
            Name of the snapshot to be saved.
            """

            syc_name = "SnapshotName"

        class overwrite_existing(Boolean):
            """
            Boolean argument controlling whether an existing snapshot should be
            overwritten. If True, then an existing snapshot named ??snapshot_name?? will
            be overwritten if it exists. If False (default), then if ??snapshot_name?? is
            shared with an existing snapshot, a warning will be written and the
            command will return without saving the snapshot.
            """

            syc_name = "OverwriteExisting"

    class open_snapshot(Command):
        """
        Opens a snapshot containing a previously saved state of the simulation.
        All state (files and directories) stored in the snapshot will be restored.
        If other state exists in the working directory, then it will not be
        modified by this command.

        Note: Snapshot cannot be opened if participants have been started.

        Parameters
        ----------
            snapshot_name : str
                The name of the snapshot to be opened. This is optional if and only if
        there is only one snapshot available to be loaded. If multiple
        snapshots exist, then the snapshot name must be specified.

        """

        syc_name = "OpenSnapshot"
        argument_names = ["snapshot_name"]
        essential_arguments = []

        class snapshot_name(String):
            """
            The name of the snapshot to be opened. This is optional if and only if
            there is only one snapshot available to be loaded. If multiple
            snapshots exist, then the snapshot name must be specified.
            """

            syc_name = "SnapshotName"

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
        essential_arguments = ["snapshot_name"]

        class snapshot_name(String):
            """
            Name of the snapshot to be deleted.
            """

            syc_name = "SnapshotName"

    class get_snapshots(Command):
        """
        Return a dictionary of available snapshots and metadata associated with
        them.
        """

        syc_name = "GetSnapshots"
