from ansys.systemcoupling.core.settings.syc_proxy_interface import SycProxyInterface
from ansys.systemcoupling.core.state_util import adapt_native_named_object_keys


class SycProxyAdapter(SycProxyInterface):
    def __init__(self, rpc):
        self.__rpc = rpc

    def get_static_info(self):
        metadata = self.__rpc.GetMetadata()
        # Merge in hard coded command metadata for now
        metadata["SystemCoupling"]["__commands"] = _command_metadata
        return metadata

    def set_state(self, path, state):
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


_command_metadata = {
    "AddParticipant": {
        "args": {
            "AdditionalArguments": {"type": "String"},
            "Executable": {"type": "String"},  # FileName
            "InputFile": {"type": "String"},  # FileName
            "ParticipantType": {"type": "String"},
            "WorkingDirectory": {"type": "String"},  # FileName (dir name)
        },
        "essentialArgNames": [],
        "optionalArgNames": [
            "ParticipantType",
            "InputFile",
            "Executable",
            "AdditionalArguments",
            "WorkingDirectory",
        ],
        "defaults": (None, None, None, None, None),
        "isInternal": False,
        "isQuery": False,
        "retType": "String",
    },
    "Save": {
        "args": {"FilePath": {"type": "String"}},  # FilePath
        "essentialArgNames": [],
        "optionalArgNames": [],
        "defaults": (".",),
        "isInternal": False,
        "isQuery": False,
        "name": "Save",
        "retType": "Logical",
    },
}
