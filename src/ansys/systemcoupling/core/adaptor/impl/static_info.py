from copy import deepcopy
from typing import Tuple

from ansys.systemcoupling.core.adaptor.impl.injected_commands import (
    get_injected_cmd_data,
)
from ansys.systemcoupling.core.util.name_util import to_python_name


def process_cmd_data(raw_data: list, category: str = None) -> dict:
    """Takes the raw command and query metadata provided by System Coupling
    and manipulates it into a form that can be used by the datamodel
    generation functionality.

    Returns a dictionary keyed by System Coupling native name to a dict
    of relevant attributes. If the ``category`` is provided, it is used
    to filter the commands that are processed.

    Parameters
    ----------
    raw_data : list
        List of dict objects, each of which contains the attributes defining
        a command or query.
    category : str, optional
        If not None, used to filter the category of commands to process,
        otherwise all commands are processed.
    """

    cmds_out = {}
    for cmd_info in raw_data:
        name = cmd_info["name"]
        if category and cmd_info["exposure"] != category:
            continue

        essential_args = cmd_info["essentialArgNames"]
        args_out = []
        is_path_cmd = False
        for arg, arg_info in cmd_info["args"]:
            if arg == "ObjectPath":
                is_path_cmd = True
                continue

            arg_info_out = {}

            pysyc_arg_name = arg_info.get("pyname", None)
            if not pysyc_arg_name:
                pysyc_arg_name = to_python_name(arg)
            arg_info_out["pysyc_name"] = pysyc_arg_name

            arg_type = arg_info.get("type")
            if not arg_type:
                raise Exception("Missing argument type")
            arg_info_out["type"] = arg_type

            doc = arg_info.get("doc")
            if doc:
                arg_info_out["help"] = doc

            args_out.append((arg, arg_info_out))

        cmds_out[name] = {
            "args": args_out,
            "isPathCommand": is_path_cmd,
            "isQuery": cmd_info["isQuery"],
            "isInjected": cmd_info.get("isInjected", False),
            "essentialArgs": essential_args,
        }

        doc = cmd_info.get("doc")
        if doc:
            cmds_out[name]["help"] = doc

        pysyc_cmd_name = cmd_info.get("pyname", None)
        if not pysyc_cmd_name:
            pysyc_cmd_name = to_python_name(name)
        if pysyc_cmd_name is not None:
            cmds_out[name]["pysyc_name"] = pysyc_cmd_name

    return cmds_out


def make_combined_metadata(
    dm_metadata: dict, cmd_metadata: list, category: str
) -> Tuple[dict, str]:
    """Combines pre-processed datamodel and command metadata into a single structure.

    This is the final form of the "static info" that is used to generate the adaptor API classes.

    Returns metadata dictionary in which the command data is rooted under the root
    "SystemCoupling" element.

    Parameters
    ----------
    dm_metadata : dict
        Metadata describing the data model content.
    cmd_metadata : list
        Metadata describing the commands and queries to be exposed.
    category : str
        The API category to extract metadata for.
    """
    root_type = "SystemCoupling"
    metadata = deepcopy(dm_metadata)
    cmd_meta = process_cmd_data(cmd_metadata, category=category)
    metadata[root_type]["__commands"] = cmd_meta
    metadata[root_type]["category_root"] = f"{category}_root"
    return metadata


def make_cmdonly_metadata(cmd_metadata: dict, category: str) -> Tuple[dict, str]:
    """Similar to ``make_combined_metadata`` but covers the case where the
    category only contains commands and no hierarchical data model content.

    Returns a tuple comprising a metadata dictionary and a "root type" to be used as a key
    into the dictionary for the command data.

    Parameters
    ----------
    cmd_metadata : list
        Metadata describing the commands and queries to be exposed.
    category : str
        The API category to extract metadata for.
    """
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
    return metadata, root_type


def get_dm_metadata(api, root_type: str) -> dict:
    """Queries System Coupling server for sources of metadata defining the data
    model content and combines into a single structure.

    Queries are performed on the direct, "native API" to System Coupling.
    System Coupling has a pre-existing query that provides the bulk of the
    metadata, but this is geared to System Coupling requirements. A second
    query is made for PySystemCoupling-specific data exposed by the server
    instance.

    A simple process is performed to merge the extended data into the main
    data.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling "native API" - i.e.
        the commands and queries available in the System Coupling command line
        application.
    root_type : str
        The root object type accessed in the queried metadata.
    """

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


def get_cmd_metadata(api) -> list:
    """Adapt command metadata queried from System Coupling to the
    form that is needed for the client implementation.

    System Coupling currently splits this data across two separate
    queries. One is the purely native System Coupling data, which
    provides the core information. The other is information
    specific to how the commands should be exposed into
    pySystemCoupling. This function blends the data into a single
    structure that is compatible with the datamodel class
    generation code.

    The output is a list of dictionary objects where each object
    contains the details of a command to be exposed.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling "native API" .
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


def get_extended_cmd_metadata(api) -> list:
    """Adapt command metadata queried from System Coupling to the
    form that is needed for the client implementation, including
    locally defined "commands" that are injected into the API.

    This is essentially an extension of ``get_cmd_metadata`` that
    inserts "injected command data" into the queried data.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling "native API" .
    """

    def merge_data(target: list, source: list) -> None:
        target_names = set(d["name"] for d in target)
        source_names = set(d["name"] for d in source)
        new_names = source_names - target_names
        common_names = source_names & target_names

        for src_item in source:
            name = src_item["name"]
            if name in new_names:
                target.append(src_item)
            elif name in common_names:
                tgt_item = None
                for titem in target:
                    if titem["name"] == name:
                        tgt_item = titem
                        break

                # Single level merge of source item dict into
                # target item dict. In particular if any
                # aspect of args is different then they need
                # to be fully redefined (this should suffice
                # for now)
                for k, v in src_item.items():
                    tgt_item[k] = v

    cmd_metadata = get_cmd_metadata(api)
    injected_data = get_injected_cmd_data()
    merge_data(cmd_metadata, injected_data)
    return cmd_metadata


def get_syc_version(api) -> str:
    """Query System Coupling for its version.

    This is returned in the form of a string such as "23.2".

    System Coupling prior to 23.2 did not expose a version query. Since
    the server that PySystemCoupling connects to did not exist prior to
    23.1, we may assume the version is 23.1 if no version query exists.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling "native API" .
    """

    def clean_version_string(version_in: str) -> str:
        year, _, release = version_in.partition(" ")
        if len(year) == 4 and year.startswith("20") and release.startswith("R"):
            try:
                year = int(year[2:])
                release = int(release[1:])
                return f"{year}.{release}"
            except:
                pass
        raise RuntimeError(
            f"Version string {version_in} has invalid format (expect '20yy Rn')."
        )

    cmds = api.GetCommandAndQueryMetadata()
    exists = any(cmd["name"] == "GetVersion" for cmd in cmds)
    return clean_version_string(api.GetVersion()) if exists else "23.1"
