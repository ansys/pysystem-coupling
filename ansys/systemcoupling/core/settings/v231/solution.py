"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "6c562b714fa53edd83b0636a428c015cdb3db28d928f53ccde7cc1ed93a6f1ce"


class root(Group):
    """
    root object
    """

    syc_name = "SolutionCommands"
    command_names = [
        "start_participants",
        "initialize",
        "shutdown",
        "solve",
        "step",
        "partition_participants",
        "write_ensight",
        "create_restart_point",
        "write_csv_chart_files",
        "get_restarts",
        "is_analysis_initialized",
    ]

    class start_participants(Command):
        """
        Important: This command will be deprecated. Consider adopting workflows
        where participants are started by another method, such as the ??initialize??,
        ??step??, or ??solve?? commands.

        Interactive command that reads the participants' System Coupling
        Participant setup files (SCP) and starts participants on separate
        sub-processes. By default, automatically starts all participants and blocks
        solution progress until all participants are connected.

        If omitted and the ??solve??, ??initialize??, or ??step?? command is issued, then
        participants are started automatically during the execution of the command.

        Note that if the ??execution_control?? ??option?? for a participant is set to
        ExternallyManaged, then System Coupling will not start the participant
        using either this command or any of the other commands that automatically
        start participants. The user is expected to manually start the participant.
        This function will not return until all participants have been connected.

        Note that this command will raise an exception if another instance of
        System Coupling is solving in the current working directory.

        Parameters
        ----------
            participant_names : typing.List[str]
                This argument has been deprecated and will be removed in future releases.

        """

        syc_name = "StartParticipants"
        argument_names = ["participant_names"]
        essential_arguments = []

        class participant_names(StringList):
            """
            This argument has been deprecated and will be removed in future releases.
            """

            syc_name = "ParticipantNames"

    class initialize(Command):
        """
        Interactive command that initializes a coupled analysis.

        Initialization includes preparing System Coupling, making connections
        between System Coupling and all participants, starting participants (if
        necessary), and writing participant build information to the Transcript
        and Log.

        Note that if the ??execution_control?? ??option?? for a participant is set to
        ExternallyManaged, then System Coupling will not start the participant
        using either this command or any of the other commands that automatically
        start participants. The user is expected to manually start the participant.
        This function will not return until all participants have been connected.

        Note that this command will raise an exception if another instance of
        System Coupling is solving in the current working directory.
        """

        syc_name = "Initialize"

    class shutdown(Command):
        """
        Interactive command that shuts down a coupled analysis.

        ??shutdown?? includes ending the coupling run and signaling participants
        to end the run. This produces a clean shutdown, generating the final
        restart point and corresponding ??results?? file before disconnecting
        from participants.

        After participants are disconnected, the coupling service writes
        timing details to the transcript. If participants were started
        automatically, it ends participant processes.

        When System Coupling disconnects from the analysis and shuts down, the GUI
        Server file is removed from the working directory.
        """

        syc_name = "Shutdown"

    class solve(Command):
        """
        Starts the participants (if necessary) and solves the coupled analysis. By
        default, the solution runs straight through without pause unless stopped by
        an scStop file.

        Disabled when a solution is already in progress.

        For restarts, the ??open?? command must be run before the ??solve?? command.

        Note that if the ??execution_control?? ??option?? for a participant is set to
        ExternallyManaged, then System Coupling will not start the participant
        using either this command or any of the other commands that automatically
        start participants. The user is expected to manually start the participant.
        This function will not return until all participants have been connected.

        Note that this command will raise an exception if another instance of
        System Coupling is solving in the current working directory.
        """

        syc_name = "Solve"

    class step(Command):
        """
        Interactive command that initializes the analysis (if necessary) and
        runs the specified number of coupling steps before pausing the coupled
        analysis.

        Disabled when a solution is already in progress.

        Disabled for iterations-only steady analyses.

        By default, runs a single step. If given the optional '??count??' argument,
        then runs the specified number of steps.

        For restarts, the '??open??' command must be run before the '??step??' command.

        When you run this command, System Coupling initializes the analysis if
        needed and then begins the solution. When the specified number of coupling
        steps has been run, the solution is paused, providing you with an
        opportunity to interact with the analysis.

        Note that if the ??execution_control?? ??option?? for a participant is set to
        ExternallyManaged, then System Coupling will not start the participant
        using either this command or any of the other commands that automatically
        start participants. The user is expected to manually start the participant.
        This function will not return until all participants have been connected.

        When the solution is resumed, either by reissuing this command or by
        running the ??solve?? command, System Coupling restarts the analysis at the
        point it left off and continues the solution with the next step.

        Note that this command will raise an exception if another instance of
        System Coupling is solving in the current working directory.

        Parameters
        ----------
            count : int
                Integer specifying the number of steps to be run. Defaults to 1.

        """

        syc_name = "Step"
        argument_names = ["count"]
        essential_arguments = []

        class count(Integer):
            """
            Integer specifying the number of steps to be run. Defaults to 1.
            """

            syc_name = "Count"

    class partition_participants(Command):
        """
        Provide a utility for setting the parallel algorithm, parallel partitioning
        fractions for each participant, and machine list information.

        At least one participant must be defined for this command to be used. Use
        of this command is not recommended if participants are already running.

        Parameters
        ----------
            algorithm_name : str
                Name of the partitioning algorithm. Available algorithms are:
        'SharedAllocateMachines'(default), 'SharedAllocateCores',
        'DistributedAllocateMachines', and 'DistributedAllocateCores'

        The algorithms allow for both shared and distributed execution and for
        the allocation of machines or cores. The default value is generally the
        best choice, as it allows for each participant to take advantage of all
        the allocated resources. The other partitioning methods are provided to
        handle situations where not enough resources are available to run the
        same machines.

        See the System Coupling documentation for more details of the
        partitioning algorithms.
            names_and_fractions : typing.List[typing.Tuple[str, float]]
                List of tuples specifying the fractions of core count applied for
        each participant

        Each tuple must have the ParticipantName as its first item and the
        associated fraction as its second item. If this parameter is omitted,
        then cores will be allocated for all participants set in the
        data model.
            machine_list : typing.List[typing.Dict[str, typing.Union[str, int]]]
                List of dictionaries specifying machines available for distributed run.
        Each dictionary must have a key 'machine-name' with machine name as its
        value, and key 'core-count' with number of cores for that machine as
        its value. Providing this argument will over-ride any machine-list
        information detected from the scheduler environment and any information
        provided by the --cnf command-line argument.

        """

        syc_name = "PartitionParticipants"
        argument_names = ["algorithm_name", "names_and_fractions", "machine_list"]
        essential_arguments = []

        class algorithm_name(String):
            """
            Name of the partitioning algorithm. Available algorithms are:
            'SharedAllocateMachines'(default), 'SharedAllocateCores',
            'DistributedAllocateMachines', and 'DistributedAllocateCores'

            The algorithms allow for both shared and distributed execution and for
            the allocation of machines or cores. The default value is generally the
            best choice, as it allows for each participant to take advantage of all
            the allocated resources. The other partitioning methods are provided to
            handle situations where not enough resources are available to run the
            same machines.

            See the System Coupling documentation for more details of the
            partitioning algorithms.
            """

            syc_name = "AlgorithmName"

        class names_and_fractions(StrFloatPairList):
            """
            List of tuples specifying the fractions of core count applied for
            each participant

            Each tuple must have the ParticipantName as its first item and the
            associated fraction as its second item. If this parameter is omitted,
            then cores will be allocated for all participants set in the
            data model.
            """

            syc_name = "NamesAndFractions"

        class machine_list(StrOrIntDictList):
            """
            List of dictionaries specifying machines available for distributed run.
            Each dictionary must have a key 'machine-name' with machine name as its
            value, and key 'core-count' with number of cores for that machine as
            its value. Providing this argument will over-ride any machine-list
            information detected from the scheduler environment and any information
            provided by the --cnf command-line argument.
            """

            syc_name = "MachineList"

    class write_ensight(Command):
        """
        Write a file with mesh and results which can be loaded into Ensight for
        post processing.

        Parameters
        ----------
            file_name : str
                Base name for Ensight files. It will generate <base>.encas file which
        should be loaded into Ensight. Other files are generated for geometry
        and variables.
            binary : bool
                To control if file is to be written in binary format or ASCII. ASCII
        slows down performance, but may be useful for debugging and seeing
        raw data.

        """

        syc_name = "WriteEnSight"
        argument_names = ["file_name", "binary"]
        essential_arguments = ["file_name"]

        class file_name(String):
            """
            Base name for Ensight files. It will generate <base>.encas file which
            should be loaded into Ensight. Other files are generated for geometry
            and variables.
            """

            syc_name = "FileName"

        class binary(Boolean):
            """
            To control if file is to be written in binary format or ASCII. ASCII
            slows down performance, but may be useful for debugging and seeing
            raw data.
            """

            syc_name = "Binary"

    class create_restart_point(Command):
        """
        Interactive command that creates a restart point at the end of the
        last completed coupling step.

        Signals the System Coupling service and all coupling participants that a
        restart point should be created before the next coupling step begins. The
        restart point is created in addition to restart points created by the
        '??output_control??' setting in the data model.

        Note that some participants write their restart files only when the
        coupling run resumes, so their files will not be available immediately
        after the command is issued.

        ??results?? information for the coupling step is written to a file named
        according to the convention "Results_#.h5", where "_#" is the number of
        the coupling step. By default, the restart files are written to the "SyC"
        directory, which is automatically created by the System Coupling service
        when restart points are created.
        """

        syc_name = "CreateRestartPoint"

    class write_csv_chart_files(Command):
        """
        For each coupling interface, exports a CSV file containing chart data
        (convergence and source/target quantity transfer values) for
        that interface.

        Each file is named according to the convention <interface>.csv, where
        <interface> is the object name of the corresponding coupling interface.

        This command will overwrite any CSV charting files that already exist,
        including any that were written during the solution.
        """

        syc_name = "WriteCsvChartFiles"

    class get_restarts(Command):
        """
        Returns a dictionary of restart points and restart file names in
        a directory. If no file path is given, restart points from the SyC
        directory in the working directory will be returned. If no restart files
        exist, an empty dictionary will be returned. Note that the dictionary keys
        are not guaranteed to be ordered.

        Parameters
        ----------
            file_path : str
                Writeable directory in which the SyC directory containing the restart
        files reside.

        """

        syc_name = "GetRestarts"
        argument_names = ["file_path"]
        essential_arguments = []

        class file_path(String):
            """
            Writeable directory in which the SyC directory containing the restart
            files reside.
            """

            syc_name = "FilePath"

    class is_analysis_initialized(Command):
        """
        Returns whether the analysis is initialized.
        """

        syc_name = "IsAnalysisInitialized"
