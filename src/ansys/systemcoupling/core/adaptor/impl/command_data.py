from ansys.systemcoupling.core.util.name_util import to_python_name


def process(raw_data: list, category: str = None) -> dict:
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
