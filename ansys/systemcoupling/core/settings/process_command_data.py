from .excluded_commands_tmp import excluded_list


def process(raw_data):
    """Takes the raw command and query metadata provided by System Coupling
    and manipulates it into a form that can be used by the datamodel
    generation functionality.

    Returns a dictionary keyed by System Coupling native name to a dict
    of relevant attributes. Only commands to be included on the 'setup'
    API are included.

    Note:
    This is probably a stop-gap. In the longer term it might make more sense
    for the SyC process itself to do more to define the pySystemCoupling
    command exposure. This cannot necessarily be easily automated client side
    as it requires a certain amount of judgement.

    Parameters
    ----------
    raw_data : list
        List of dict objects, each of which contains the attributes defining
        a command or query.
    """

    cmds_out = {}
    for cmd_info in raw_data:
        name = cmd_info["name"]
        if name in excluded_list:
            continue

        args_out = {}
        for arg, arg_info in cmd_info["args"].items():
            # if arg == "ObjectPath":
            #    continue

            args_out[arg] = {}
            arg_type = arg_info.get("Type")
            if arg_type:
                args_out[arg]["type"] = _process_arg_type(arg_type)

        cmds_out[name] = {"args": args_out, "isQuery": cmd_info["isQuery"]}

    return cmds_out


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


def _process_arg_type(arg_type):
    return _type_map[arg_type]
