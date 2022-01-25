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
    def __init__(self, command_executor):
        self.__cmd_exec = command_executor
        self._init_datamodel()
        self._init_cmds()
        self.__meta_wrapper = _MetaWrapper(self.__dm_meta, self.__cmd_meta)
        self.__root = ObjectPath('/' + self.__dm_meta.root_type(), self, self.__meta_wrapper)
        self.__top_level_types = set(self.__dm_meta.child_types(self.__root))

    def execute_command(self, name, **kwargs):
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
