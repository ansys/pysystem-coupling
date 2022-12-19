from ansys.systemcoupling.core.adaptor.impl.static_info import (
    get_dm_metadata,
    get_extended_cmd_metadata,
    get_syc_version,
    make_cmdonly_metadata,
    make_combined_metadata,
)
from ansys.systemcoupling.core.adaptor.impl.syc_proxy_interface import SycProxyInterface
from ansys.systemcoupling.core.util.state_keys import adapt_native_named_object_keys


class SycProxy(SycProxyInterface):
    def __init__(self, rpc):
        self.__rpc = rpc
        self.__injected_cmds = {}
        self.__version = None
        self.__defunct = False

    def reset_rpc(self, rpc):
        """Call when the remote connection is lost, providing an
        `rpc` instance which replaces the original one from the
        initializer and which raises a sensible error if any attempt
        is made to use it.

        The motivating use case is to catch attempted uses of stale
        objects after the current session has ended.
        """
        self.__rpc = rpc
        # We rely on attempted attribute access on self.__rpc to catch
        # most cases, but this "defunct" flag can be used to mop up
        # other cases.
        self.__defunct = True

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

    def get_version(self):
        if self.__version is None:
            self.__version = get_syc_version(self.__rpc)
        return self.__version

    def set_state(self, path, state):
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
        if self.__defunct:
            # The name of the 'rpc' here is arbitrary - we are just
            # forcing it to raise its usual error.
            self.__rpc.trigger_error
        cmd_name = args[1]
        cmd = self.__injected_cmds.get(cmd_name, None)
        return cmd(**kwargs)
