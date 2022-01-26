from ansys.systemcoupling.core.command_metadata import CommandMetadata
from ansys.systemcoupling.core.datamodel_metadata import build as build_dm_meta
from ansys.systemcoupling.core.object_path import ObjectPath
from ansys.systemcoupling.core.path_util import join_path_strs


class _MetaWrapper:
    def __init__(self, dm_meta, cmd_meta):
        self.__dm_meta = dm_meta
        self.__cmd_meta = cmd_meta

    def __getattr__(self, name):
        try:
            return getattr(self.__dm_meta, name)
        except AttributeError:
            return getattr(self.__cmd_meta, name)

class SycApi:
    """Provides access to the System Coupling command and query API and
    data model.

    System Coupling is presumed to be running remotely and is accessed
    via the provided "command executor" which services command and query
    requests made via ``SycApi``.
    """

    def __init__(self, command_executor):
        self.__cmd_exec = command_executor
        self._init_datamodel()
        self._init_cmds()
        self.__meta_wrapper = _MetaWrapper(self.__dm_meta, self.__cmd_meta)
        self.__root = ObjectPath('/' + self.__dm_meta.root_type(), self, self.__meta_wrapper)
        self.__top_level_types = set(self.__dm_meta.child_types(self.__root))

    def execute_command(self, name, **kwargs):
        """Execute the named command or query and return the result.

        All commands and queries take one or many keyword arguments. Some
        of these can be optional, depending on the command or query.

        A query will return a value of a type that is dependent on the
        query.

        A few commands return a value (again with a type dependent on
        the command), but most return ``None``.
        """
        return self.__cmd_exec.execute_command(name, **kwargs)

    def exit(self):
        """Close the remote System Coupling instance.

        Following this, the current instance of this class will not
        be usable. Create a new instance if required.
        """
        # xx TODO - can we find a better arrangement than this?
        self.__cmd_exec.exit()
        self.__cmd_exec = None

    def __getattr__(self, name):
        """Provides access to commands, queries and data model as attributes of
        this class's instance.

        If System Coupling exposes a command, ``Solve()`` say, then if we
        have an instance of this class, ``syc``, the following call is enabled
        by the present method:

        ``syc.Solve()``

        This is an alternative to

        ``syc.execute_command('Solve')``

        If System Coupling exposes a data model object, ``SolutionControl``
        say, then the following interactions are enabled by the present
        method.

        Query state of object:
        ``state = syc.SolutionControl.GetState()``

        (Note that this is an alternative to:
        ``state = syc.execute_command('GetState',
            ObjectPath='/SystemCoupling/SolutionControl')``)

        Query value of object property:
        ``option = syc.SolutionControl.DurationOption``

        Set multiple object object properties:
        ``syc.SolutionControl = {
            'DurationOption': 'NumberOfSteps',
            'NumberofSteps': 5
          }``

        Set single property:
        ``syc.SolutionControl.NumberOfSteps = 6``

        Full "path" syntax for the data model is supported. Thus:
        ``syc.CouplingInterface['intf1'].DataTransfer['temp']...``
        """
        if self.__cmd_meta.is_command_or_query(name):
            # Looks like an API command/query call
            def non_objpath_cmd(**kwargs):
                return self.__cmd_exec.execute_command(name, **kwargs)
            def objpath_cmd(**kwargs):
                if 'ObjectPath' not in kwargs:
                    return self.__cmd_exec.execute_command(name, ObjectPath=self.__root, **kwargs)
                return self.__cmd_exec.execute_command(name, **kwargs)
            if not self.__cmd_meta.is_objpath_command_or_query(name):
                return non_objpath_cmd
            else:
                return objpath_cmd

        if not name in self.__top_level_types:
            raise AttributeError(f'Unknown attribute of System Coupling API: \'{name}\'')

        # Can assume accessing a datamodel path
        return self.__root.make_path(join_path_strs(self.__root, name))

    def _init_datamodel(self):
        dm_meta_raw = self.__cmd_exec.GetMetadata()
        self.__dm_meta = build_dm_meta(dm_meta_raw)

    def _init_cmds(self):
        cmd_meta = self.__cmd_exec.GetCommandAndQueryMetadata()
        self.__cmd_meta = CommandMetadata(cmd_meta)
