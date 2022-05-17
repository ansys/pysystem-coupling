from ansys.systemcoupling.core.native_api.command_metadata import CommandMetadata
from ansys.systemcoupling.core.native_api.datamodel_metadata import (
    build as build_dm_meta,
)
from ansys.systemcoupling.core.path_util import join_path_strs

from .meta_wrapper import MetaWrapper
from .object_path import ObjectPath


class NativeApi:
    def __init__(self, rpc_impl):
        self.__rpc_impl = rpc_impl
        self._init_datamodel()
        self._init_cmds()
        self.__meta_wrapper = MetaWrapper(self.__dm_meta, self.__cmd_meta)
        self.__root = ObjectPath(
            "/" + self.__dm_meta.root_type(), self, self.__meta_wrapper
        )
        self.__top_level_types = set(self.__dm_meta.child_types(self.__root))

    def _exit(self, rpc_impl=None):
        self.__rpc_impl = rpc_impl

    def execute_command(self, name, **kwargs):
        """Execute the named command or query and return the result.

        All commands and queries take one or many keyword arguments. Some
        of these can be optional, depending on the command or query.

        A query will return a value of a type that is dependent on the
        query.

        A few commands return a value (again with a type dependent on
        the command), but most return ``None``.
        """
        return self.__rpc_impl.execute_command(name, **kwargs)

    def __getattr__(self, name):
        """Provides access to the native System Coupling commands and queries API
        (and, implicitly thereby, the data model settings) as attributes of
        this class's instance.

        For example, the System Coupling command ``Solve()`` may be invoked on an
        instance of this class, ``syc`` as follows:

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
                return self.__rpc_impl.execute_command(name, **kwargs)

            def objpath_cmd(**kwargs):
                if "ObjectPath" not in kwargs:
                    return self.__rpc_impl.execute_command(
                        name, ObjectPath=self.__root, **kwargs
                    )
                return self.__rpc_impl.execute_command(name, **kwargs)

            if not self.__cmd_meta.is_objpath_command_or_query(name):
                return non_objpath_cmd
            else:
                return objpath_cmd

        if not name in self.__top_level_types:
            raise AttributeError(f"Unknown attribute of System Coupling API: '{name}'")

        # Can assume accessing a datamodel path
        return self.__root.make_path(join_path_strs(self.__root, name))

    def _init_datamodel(self):
        dm_meta_raw = self.__rpc_impl.GetMetadata()
        self.__dm_meta = build_dm_meta(dm_meta_raw)

    def _init_cmds(self):
        cmd_meta = self.__rpc_impl.GetCommandAndQueryMetadata()
        self.__cmd_meta = CommandMetadata(cmd_meta)
