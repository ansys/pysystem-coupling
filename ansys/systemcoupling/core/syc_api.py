
from ansys.systemcoupling.core.metadata import build as build_dm_meta

class SycApi:

    def __init__(self, command_executor):
        self.__cmd_exec = command_executor
        self._init_datamodel()
        self._init_cmds()
        
        
    def __getattr__(self, name):
        if name not in self.__cmd_meta:
            # Assume a datamodel type
            
    
        def f(**kwargs):
            return self.__cmd_exec.execute_command(name, **kwargs)
        return f

    def _init_datamodel(self):
        dm_meta_raw = self.__cmd_exec.GetMetadata()
        self.__dm_meta = build_dm_meta(dm_meta_raw)

    def _init_cmds(self):
        cmd_meta = self.__cmd_exec.GetCommandAndQueryMetadata()
        self.__cmd_meta = {meta['name']]: meta for meta in cmd_meta}