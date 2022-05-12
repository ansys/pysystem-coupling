from .excluded_commands_tmp import _case_list, excluded_list


def process(raw_data, category=None, apply_exclusions=True):
    """Takes the raw command and query metadata provided by System Coupling
    and manipulates it into a form that can be used by the datamodel
    generation functionality.

    Returns a dictionary keyed by System Coupling native name to a dict
    of relevant attributes. Only commands to be included on the 'setup'
    API are included.

    Note:
    This is a hacky stop-gap. In the longer term it might make more sense
    for the SyC process itself to do more to define the pySystemCoupling
    command exposure. This cannot necessarily be easily automated client side
    as it requires a certain amount of judgement.

    Parameters
    ----------
    raw_data : list
        List of dict objects, each of which contains the attributes defining
        a command or query.
    category : str
        If not None, used to filter the category of commands to process.
    apply_exclusions : bool
        If False (default is True), do not respect the exclusion list when
        processing commands. Specify False only for test purposes.
    """

    def filter(name):
        if category is None:
            return not apply_exclusions or name not in excluded_list
        elif category == "case":
            return name in _case_list
        else:
            raise Exception(f"unhandled category {category}")

    cmds_out = {}
    for cmd_info in raw_data:
        name = cmd_info["name"]
        if not filter(name):
            continue

        essential_args = cmd_info["essentialArgNames"]
        args_out = []
        is_path_cmd = False
        for arg, arg_info in cmd_info["args"]:
            if arg == "ObjectPath":
                is_path_cmd = True
                continue

            arg_info_out = {}
            arg_type = arg_info.get("Type")
            if not arg_type:
                arg_type = arg_info.get("type")
            if not arg_type:
                raise Exception("Missing argument type")
            arg_info_out["type"] = _process_arg_type(arg_type)
            args_out.append((arg, arg_info_out))

        cmds_out[name] = {
            "args": args_out,
            "isPathCommand": is_path_cmd,
            "isQuery": cmd_info["isQuery"],
            "essentialArgs": essential_args,
        }

    return cmds_out


# XXX TODO this is somewhat temporary in its current form
# Some work may be needed to handled possible argument types
_type_map = {
    # 1. These can all be treated as str for now:
    "<class 'kernel.util.FileUtilities.ValidDirectoryName'>": "String",
    "<class 'kernel.util.FileUtilities.WritableUnicodeDirectory'>": "String",
    "<class 'kernel.util.FileUtilities.ReadableUnicodeDirectory'>": "String",
    "<class 'kernel.util.FileUtilities.ReadableFileName'>": "String",
    "<class 'kernel.util.FileUtilities.WritableUnicodeFileName'>": "String",
    "<class 'kernel.util.FileUtilities.ValidFileName'>": "String",
    "<class 'kernel.util.ValidPythonSymbol.ValidPythonSymbol'>": "String",
    # 2. DictList and TupleList not in exposed commands
    # "<class 'kernel.commands.ListTypes.DictList'>": None,
    # "<class 'kernel.commands.ListTypes.TupleList'>": None,
    # 3. ObjectPath is always 'hidden'
    "<class 'kernel.datamodel.ObjectPath.ObjectPath'>": "String",
    # 4. Only used in AddTransformation for "Angle"
    #   XXX TODO Get away with Real for now
    "<class 'object'>": "Real",
    # 5. dict is not used in any exposed command
    # "<class 'dict'>": None,
    # 6. Only instance is a real list (XXX TODO)
    "<class 'list'>": "Real List",
    # 7. StrList - straightforward StringList
    "<class 'kernel.commands.ListTypes.StrList'>": "String List",
    # 8. Straightforward:
    "<class 'str'>": "String",
    "<class 'bool'>": "Logical",
    "<class 'int'>": "Integer",
}

_target_types = set(_type_map.values())


def _process_arg_type(arg_type):
    if arg_type in _target_types:
        return arg_type
    return _type_map[arg_type]
