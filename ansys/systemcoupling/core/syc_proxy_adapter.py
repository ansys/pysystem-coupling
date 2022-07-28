from ansys.systemcoupling.core.settings.command_data import process as process_cmd_data
from ansys.systemcoupling.core.settings.syc_proxy_interface import SycProxyInterface
from ansys.systemcoupling.core.util.state_keys import adapt_native_named_object_keys


class SycProxyAdapter(SycProxyInterface):
    def __init__(self, rpc):
        self.__rpc = rpc

    def get_static_info(self, category):
        cmd_metadata = get_cmd_metadata(self.__rpc)
        if category == "setup":
            root_type = "SystemCoupling"
            metadata = get_dm_metadata(self.__rpc, root_type)
            setup_cmd_data = process_cmd_data(cmd_metadata, category=category)
            metadata[root_type]["__commands"] = setup_cmd_data
            metadata[root_type]["category_root"] = f"{category}_root"
        elif category in ("case", "solution"):
            cmd_data = process_cmd_data(cmd_metadata, category=category)
            root_type = category.title() + "Commands"
            # root_type isn't a real SyC data model object but we fake it
            # so that we can generate the command group under a common root.
            # Note extra properties to make it work as an object - these
            # need to be consistent with pre-generation code.
            metadata = {
                root_type: {
                    "__commands": cmd_data,
                    "isEntity": False,
                    "isNamed": False,
                    "ordinal": 0,
                    "category_root": f"{category}_root",
                }
            }
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


# TODO need these in generate_datamodel
#   - probably do not belong in here - find a better way to share


def get_dm_metadata(api, root_type):
    dm_metadata = api.GetMetadata(json_ret=True)
    dm_metadata_ex = api.GetPySycDatamodelMetadata()

    def get_update(name, data_ex):
        # Adapt extended data to expected form
        if name not in data_ex:
            return None
        item_ex = data_ex[name]
        ret = {"help": item_ex["doc"]}
        if "pyname" in item_ex:
            ret["py_sycname"] = item_ex["pyname"]
        return ret

    def merge_metadata(data, data_ex):
        for k, v in data.items():
            if k == "__children":
                for c, cdata in v.items():
                    update = get_update(c, data_ex)
                    if update is not None:
                        cdata.update(update)
                        # Note that we only bother recursing
                        # as long as there is a corresponding
                        # item in the extended data
                        merge_metadata(cdata, data_ex[c])
            if k == "__parameters":
                for p, pdata in v.items():
                    update = get_update(p, data_ex)
                    if update is not None:
                        pdata.update(update)

    merge_metadata(dm_metadata[root_type], dm_metadata_ex[root_type])
    return dm_metadata


def get_cmd_metadata(api):
    """Adapt command metadata queried from System Coupling to the
    form that is needed for the client implementation.

    System Coupling currently splits this data across two separate
    queries. One is the purely native System Coupling data, which
    provides the core information. The other is information
    specific to how the commands should be exposed into
    pySystemCoupling. This function blends the data into a single
    structure that is compatible with the datamodel class
    generation code.
    """
    cmd_metadata_in = api.GetCommandAndQueryMetadata()
    cmd_metadata_ex = api.GetPySycCommandMetadata()
    cmd_metdata_out = []
    for info in cmd_metadata_in:
        name = info["name"]
        info_ex = cmd_metadata_ex.get(name)
        if not info_ex:
            continue

        exposure = info_ex.get("exposure")
        if not exposure or exposure == "unexposed":
            continue
        info["exposure"] = exposure

        info["doc"] = info_ex["doc"]

        pyname = info_ex.get("pyname")
        if pyname:
            info["pyname"] = pyname

        args_ex = {arg_ex["name"]: arg_ex for arg_ex in info_ex["args"]}
        args_out = []
        for arg, arg_info in info["args"]:
            arg_info_ex = args_ex[arg]
            arg_exposure = arg_info_ex.get("exposure")
            if arg_exposure == "unexposed":
                continue
            arg_info["type"] = arg_info_ex["type"]
            arg_info["doc"] = arg_info_ex["doc"]
            pyname = arg_info_ex.get("pyname")
            if pyname:
                arg_info["pyname"] = pyname
            args_out.append((arg, arg_info))

        info["args"] = args_out
        cmd_metdata_out.append(info)
    return cmd_metdata_out
