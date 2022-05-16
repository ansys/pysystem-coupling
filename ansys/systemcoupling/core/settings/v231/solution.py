"""This is an auto-generated file.  DO NOT EDIT!"""

from ansys.systemcoupling.core.settings.datamodel import *

SHASH = "3845dd105ba7661206f9568f9f65be5b7bbc69d6d1f7fb773aefe2e43642b2da"


class root(Group):
    """
    root object
    """

    syc_name = "SolutionCommands"
    command_names = [
        "start_participants",
        "shutdown",
        "solve",
        "step",
        "open_results_in_ensight",
        "write_ensight",
        "get_restarts",
    ]

    class start_participants(Command):
        """
        'start_participants' child of 'root' object

        Parameters
        ----------
            participant_names : typing.List[str]
                'participant_names' child of 'start_participants' object

        """

        syc_name = "StartParticipants"
        argument_names = ["participant_names"]
        essential_arguments = []

        class participant_names(StringList):
            """
            'participant_names' child of 'start_participants' object
            """

            syc_name = "ParticipantNames"

    class shutdown(Command):
        """
        'shutdown' child of 'root' object
        """

        syc_name = "Shutdown"

    class solve(Command):
        """
        'solve' child of 'root' object
        """

        syc_name = "Solve"

    class step(Command):
        """
        'step' child of 'root' object

        Parameters
        ----------
            count : int
                'count' child of 'step' object

        """

        syc_name = "Step"
        argument_names = ["count"]
        essential_arguments = []

        class count(Integer):
            """
            'count' child of 'step' object
            """

            syc_name = "Count"

    class open_results_in_ensight(Command):
        """
        'open_results_in_ensight' child of 'root' object
        """

        syc_name = "OpenResultsInEnSight"

    class write_ensight(Command):
        """
        'write_ensight' child of 'root' object

        Parameters
        ----------
            file_name : str
                'file_name' child of 'write_ensight' object
            binary : bool
                'binary' child of 'write_ensight' object

        """

        syc_name = "WriteEnSight"
        argument_names = ["file_name", "binary"]
        essential_arguments = ["file_name"]

        class file_name(String):
            """
            'file_name' child of 'write_ensight' object
            """

            syc_name = "FileName"

        class binary(Boolean):
            """
            'binary' child of 'write_ensight' object
            """

            syc_name = "Binary"

    class get_restarts(Command):
        """
        'get_restarts' child of 'root' object

        Parameters
        ----------
            file_path : str
                'file_path' child of 'get_restarts' object

        """

        syc_name = "GetRestarts"
        argument_names = ["file_path"]
        essential_arguments = []

        class file_path(String):
            """
            'file_path' child of 'get_restarts' object
            """

            syc_name = "FilePath"
