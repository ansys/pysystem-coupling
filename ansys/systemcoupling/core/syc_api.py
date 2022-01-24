from ansys.systemcoupling.core.command_metadata import CommandMetadata
from ansys.systemcoupling.core.metadata import build as build_dm_meta
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

    def execute_command(self, name, **kwargs):
        return self.__cmd_exec.execute_command(name, **kwargs)

    def __getattr__(self, name):
        if self.__cmd_meta.is_command_or_query(name):
            # Looks like an API command/query call
            def f(**kwargs):
                return self.__cmd_exec.execute_command(name, **kwargs)
            return f

        # Otherwise, assume a datamodel type
        return self.__root.make_path(join_path_strs(self.__root, name))         

    def _init_datamodel(self):
        dm_meta_raw = self.__cmd_exec.GetMetadata()
        self.__dm_meta = build_dm_meta(dm_meta_raw)

    def _init_cmds(self):
        cmd_meta = self.__cmd_exec.GetCommandAndQueryMetadata()
        self.__cmd_meta = CommandMetadata(cmd_meta)

