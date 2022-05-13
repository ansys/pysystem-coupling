from ansys.systemcoupling.core.settings.command_data import process as process_cmd_data
from ansys.systemcoupling.core.settings.syc_proxy_interface import SycProxyInterface
from ansys.systemcoupling.core.state_util import adapt_native_named_object_keys


class SycProxyAdapter(SycProxyInterface):
    def __init__(self, rpc):
        self.__rpc = rpc

    def get_static_info(self):
        metadata = self.__rpc.GetMetadata()
        cmd_metadata = process_cmd_data(self.__rpc.GetCommandAndQueryMetadata())
        metadata["SystemCoupling"]["__commands"] = cmd_metadata
        return metadata

    def set_state(self, path, state):
        # XXX TODO nested state submission probably broken if it involves named objects
        self.__rpc.SetState(ObjectPath=path, State=state)

    def get_state(self, path):
        state = self.__rpc.GetState(ObjectPath=path)
        return adapt_native_named_object_keys(state)

    def delete(self, path):
        self.__rpc.DeleteObject(ObjectPath=path)

    def create_named_object(self, path, name):
        self.set_state(f"{path}:{name}", {})

    def get_object_names(self, path):
        return self.__rpc.GetChildNamesStr(ObjectPath=path)

    def execute_cmd(self, *args, **kwargs):
        cmd_name = args[1]
        return self.__rpc.execute_command(cmd_name, **kwargs)
