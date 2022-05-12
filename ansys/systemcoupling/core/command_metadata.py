def _is_objpath_cmd(info):
    args = info["args"]
    if isinstance(args, dict):
        # old format XXX TODO retire this when test data updated
        return "ObjectPath" in info["args"]
    else:
        # new [(arg, info), ...] format that preserves order
        return any(arg == "ObjectPath" for arg, _ in info["args"])


class CommandMetadata:
    def __init__(self, raw_data):
        self._init_data(raw_data)
        self.__objpath_cmds = set(
            name for name, info in self.__data.items() if _is_objpath_cmd(info)
        )

    def _init_data(self, raw_data):
        self.__data = {item["name"]: item for item in raw_data}

    def get_objpath_command_and_query_names(self):
        return list(self.__data.keys())

    def is_command_or_query(self, name):
        return name in self.__data

    def is_objpath_command_or_query(self, name):
        return name in self.__objpath_cmds
