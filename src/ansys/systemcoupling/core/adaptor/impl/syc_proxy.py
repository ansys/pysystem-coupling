from ansys.systemcoupling.core.adaptor.impl.static_info import (
    get_dm_metadata,
    get_extended_cmd_metadata,
    make_cmdonly_metadata,
    make_combined_metadata,
)
from ansys.systemcoupling.core.adaptor.impl.syc_proxy_interface import SycProxyInterface
from ansys.systemcoupling.core.util.state_keys import adapt_native_named_object_keys


class SycProxy(SycProxyInterface):
    def __init__(self, rpc):
        self.__rpc = rpc
        self.__injected_cmds = {}

    def set_injected_commands(self, cmd_dict: dict) -> None:
        """Sets a dictionary of names mapped to locally defined "injected commands".

        This will be used to find the function to be called
        in ``execute_injected_command`` if that method is called.
        """
        self.__injected_cmds = cmd_dict

    def get_static_info(self, category):
        if category == "setup":
            cmd_metadata = get_extended_cmd_metadata(self.__rpc)
            root_type = "SystemCoupling"
            dm_metadata = get_dm_metadata(self.__rpc, root_type)
            metadata = make_combined_metadata(dm_metadata, cmd_metadata, category)
        elif category in ("case", "solution"):
            cmd_metadata = get_extended_cmd_metadata(self.__rpc)
            metadata, root_type = make_cmdonly_metadata(cmd_metadata, category)
        else:
            raise RuntimeError(f"Unrecognised 'static info' category: '{category}'.")
        return metadata, root_type

    def set_state(self, path, state):
        # XXX TODO nested state submission probably broken if it involves named objects
        self.__rpc.SetState(ObjectPath=path, State=state)

    def get_state(self, path):
        state = self.__rpc.GetState(ObjectPath=path)
        if isinstance(state, dict):
            return adapt_native_named_object_keys(state)
        return state

    def delete(self, path):
        self.__rpc.DeleteObject(ObjectPath=path)

    def create_named_object(self, path, name):
        self.set_state(f"{path}:{name}", {})

    def get_object_names(self, path):
        return self.__rpc.GetChildNamesStr(ObjectPath=path)

    def get_property_options(self, path, name):
        return self.__rpc.GetParameterOptions(ObjectPath=path, Name=name)

    def execute_cmd(self, *args, **kwargs):
        cmd_name = args[1]
        return self.__rpc.execute_command(cmd_name, **kwargs)

    def execute_injected_cmd(self, *args, **kwargs):
        cmd_name = args[1]
        cmd = self.__injected_cmds.get(cmd_name, None)
        return cmd(**kwargs)
