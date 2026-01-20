# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from copy import deepcopy
from typing import Dict, List, Tuple

from ansys.systemcoupling.core.adaptor.impl.get_syc_version import get_syc_version
from ansys.systemcoupling.core.adaptor.impl.injected_commands import (
    get_injected_cmd_data,
)
from ansys.systemcoupling.core.util.name_util import to_python_name


def process_cmd_data(raw_data: list, category: str = None) -> dict:
    """Take the raw command and query metadata provided by System Coupling
        and manipulate it into a form that can be used by the data model
        generation functionality.

        Parameters
        ----------
        raw_data : list
            List of dict objects, each of which contains the attributes defining
            a command or query.
        category : str, optional
            Category for filtering the commands to process. The default is ``None``,
            in which case all commands are process.

    Returns
    -------
    dict
       Dictionary keyed by the System Coupling native name to a dictionary
        of relevant attributes. If the ``category`` parameter is provided,
        it is used to filter the commands that are processed.
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
                raise Exception("Argument type is missing.")
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
    """Combine the preprocessed data model and command metadata into a single structure.

    This dictionary is the final form of the *static information* that is used to
    generate the adaptor API classes.

    Parameters
    ----------
    dm_metadata : dict
        Metadata describing the data model content.
    cmd_metadata : list
        Metadata describing the commands and queries to expose.
    category : str
        The API category to extract metadata for.

    Returns
    -------
    dict
        Metadata dictionary in which the command data is rooted under the root
        ``SystemCoupling`` element.

    """
    root_type = "SystemCoupling"
    metadata = deepcopy(dm_metadata)
    cmd_meta = process_cmd_data(cmd_metadata, category=category)
    metadata[root_type]["__commands"] = cmd_meta
    metadata[root_type]["category_root"] = f"{category}_root"
    return metadata


def make_cmdonly_metadata(cmd_metadata: dict, category: str) -> Tuple[dict, str]:
    """Combine the command metadata into a single structure.

    Although this function is similar to the ``make_combined_metadata`` function, it covers
    the case where the category contains commands but no hierarchical data model content.

    Parameters
    ----------
    cmd_metadata : list
        Metadata describing the commands and queries to expose.
    category : str
        API category to extract metadata for.

    Returns
    -------
    tuple
        Tuple comprising a metadata dictionary and a *root type* to use as a key
        into the dictionary for the command data.

    """
    cmd_data = process_cmd_data(cmd_metadata, category=category)
    root_type = category.title() + "Commands"
    # root_type isn't a real SyC data model object but we fake it
    # so that we can generate the command group under a common root.
    # Note extra properties to make it work as an object - these
    # must be consistent with pre-generation code.
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
    """Get sources of metadata defining the data model from the System
    Coupling server and combine into a single structure.

    Queries are performed on the direct *native API* to System Coupling.
    System Coupling has a pre-existing query that provides the bulk of the
    metadata, but this is geared to System Coupling requirements. A second
    query is made for PySystemCoupling-specific data exposed by the server
    instance.

    A simple process is performed to merge the extended data into the main
    data.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling *native API*. For example,
        access to the commands and queries available in the System Coupling
        command-line app.
    root_type : str
        Root object type accessed in the queried metadata.
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
                        # Note that recursing occurs only
                        # as long as there is a corresponding
                        # item in the extended data.
                        merge_metadata(cdata, data_ex[c])
            if k == "__parameters":
                for p, pdata in v.items():
                    update = get_update(p, data_ex)
                    if update is not None:
                        pdata.update(update)

    merge_metadata(dm_metadata[root_type], dm_metadata_ex[root_type])
    return dm_metadata


def get_cmd_metadata(api) -> list:
    """Get command metadata from System Coupling and adapt it to the
    form needed for the client implementation.

    System Coupling currently splits this data across two separate
    queries. One is the purely native System Coupling data, which
    provides the core information. The other is information
    specific to how the commands should be exposed into
    pySystemCoupling. This function blends the data into a single
    structure that is compatible with the ``datamodel`` class
    generation code.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling *native API* .

    Returns
    -------
    list
        list of dictionary objects where each object contains
        the details of a command to be exposed.

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
    """Get command metadata from System Coupling and adapt it to the
    form needed for the client implementation.

    The metadata that this function gets includes locally defined *commands*
    that are injected into the API.

    This function is essentially an extension of the ``get_cmd_metadata``
    function that inserts *injected command data* into the queried data.

    Parameters
    ----------
    api : NativeApi
        Object providing access to the System Coupling *native API*.
    """

    def fix_up_doc(cmd_metadata):
        version = get_syc_version(api)
        if version not in ("24.2", "25.1"):
            return cmd_metadata

        command_to_fix = None
        if version == "24.2":
            command_to_fix = "add_participant"
        elif version == "25.1":
            command_to_fix = "update_participant"

        # There are bugs in doc text queried from 24.2 and 25.1 SyC.
        # The "*" need to be escaped to avoid issues in Sphinx. This
        # can be a surgical fix because these versions are frozen now.
        for cmd in cmd_metadata:
            if cmd["pyname"] == command_to_fix:
                add_part_cmd = cmd
                for arg_name, arg_info in add_part_cmd["args"]:
                    if arg_name == "InputFile":
                        arg_info["doc"] = arg_info["doc"].replace("*", r"\*")
        return cmd_metadata

    def find_item_by_name(items: List[Dict], name: str) -> dict:
        for item in items:
            if item["name"] == name:
                return item
        raise RuntimeError(f"Did not find dict element of list with 'name' == {name}")

    def merge_data(target: list, source: list) -> None:
        target_names = set(d["name"] for d in target)
        source_names = set(d["name"] for d in source)
        new_names = source_names - target_names
        common_names = source_names & target_names

        # Injected commands can either be completely new commands injected into
        # the set of available commands, or can be "overrides" that replace the
        # SyC command that would have been generated. Occasionally, we still
        # want to generate the command that is being replaced so that we can
        # call it internally. This is identified by a "pysyc_internal_name"
        # field. In this case we split the command data into an injected command
        # and a "normal" command but with the internal name as the pysyc name
        # for the latter.

        special_injected_commands = [
            name
            for name in common_names
            if "pysyc_internal_name" in find_item_by_name(source, name)
        ]

        for name in special_injected_commands:
            src_item = find_item_by_name(source, name)
            tgt_item = find_item_by_name(target, name)

            # Target item becomes a "normally" exposed SyC command except that
            # it is "internal" on the PySyC side - only intended for internal
            # PySyC use.  It will be given a special internal name rather than
            # the one derived from its SyC name. It will also have its doc
            # info removed.

            # - Take a copy of tgt before we remove doc.
            tgt_copy = deepcopy(tgt_item)
            if "doc" in tgt_item:
                tgt_item["doc"] = "For internal use only."

            for arg in tgt_item.get("args", []):
                _, arg_info = arg
                if "doc" in arg_info:
                    arg_info["doc"] = "..."

            # - Name for PySyC exposure is the "pysyc_internal_name" from the source item
            tgt_item["pyname"] = src_item["pysyc_internal_name"]

            # Source item becomes a normal injected command. It is processed like the
            # items in the common_names later but has special treatment for its
            # doc and arguments. That is done here, so it will be removed from
            # common_names and added to new_names.
            for k, v in tgt_copy.items():
                if k in ("essentialArgNames", "optionalArgNames", "args"):
                    src_item[k] = src_item.get(f"{k}_extra", []) + v
                elif k == "doc":
                    prefix = src_item.get(f"{k}_prefix", "")
                    if prefix:
                        prefix += "\n\n"
                    suffix = src_item.get(f"{k}_suffix", "")
                    if suffix:
                        suffix = "\n" + suffix
                    src_item[k] = prefix + v + suffix
                else:
                    src_item[k] = v

            src_item["name"] = src_item["pyname"]

            common_names.remove(name)
            new_names.add(src_item["name"])

        for src_item in source:
            name = src_item["name"]
            if name in new_names:
                target.append(src_item)
            elif name in common_names:
                tgt_item = find_item_by_name(target, name)

                # Single-level merge of source item dictionary into
                # target item dictionary. If any aspect of the arguments
                # is different, then they must be fully redefined. (This
                # should suffice for now.)
                for k, v in src_item.items():
                    tgt_item[k] = v

    cmd_metadata = get_cmd_metadata(api)
    injected_data = get_injected_cmd_data()
    merge_data(cmd_metadata, injected_data)
    cmd_metadata = fix_up_doc(cmd_metadata)
    return cmd_metadata


def make_named_object_level_map(dm_metadata, root_type) -> dict[int, str]:
    level_map = {}

    def visit_children(metadata, level):
        for k, v in metadata["__children"].items():
            if v["isNamed"]:
                level_map.setdefault(level, set()).add(k)
            visit_children(v, level + 1)

    visit_children(dm_metadata[root_type], 0)

    return level_map
