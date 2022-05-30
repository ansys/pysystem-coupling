from ansys.systemcoupling.core.settings.command_data import process as process_cmd_data
from ansys.systemcoupling.core.settings.syc_proxy_interface import SycProxyInterface
from ansys.systemcoupling.core.util.state_keys import adapt_native_named_object_keys


class SycProxyAdapter(SycProxyInterface):
    def __init__(self, rpc):
        self.__rpc = rpc

    def get_static_info(self, category):
        cmd_metadata = self.__rpc.GetCommandAndQueryMetadata()
        if category == "setup":
            metadata = self.__rpc.GetMetadata()
            setup_cmd_data = process_cmd_data(cmd_metadata)
            category_root = "SystemCoupling"
            metadata[category_root]["__commands"] = setup_cmd_data
        elif category in ("case", "solution"):
            cmd_data = process_cmd_data(cmd_metadata, category=category)
            category_root = category.title() + "Commands"
            # category root isn't a real data model object but we fake it
            # so that we can generate the command group under a common root.
            # Note extra properties to make it work as an object - these
            # need to be consistent with pre-generation code.
            metadata = {
                category_root: {
                    "__commands": cmd_data,
                    "isEntity": False,
                    "isNamed": False,
                    "ordinal": 0,
                }
            }
        else:
            raise RuntimeError(f"Unrecognised 'static info' category: '{category}'.")
        return metadata, category_root

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
