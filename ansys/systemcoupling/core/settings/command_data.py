from ansys.systemcoupling.core.util.name_util import to_python_name


def process(raw_data, category=None):
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
    "<class 'kernel.commands.ListTypes.DictList'>": "StrOrIntDictList",
    "<class 'kernel.commands.ListTypes.TupleList'>": "StrFloatPairList",
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


###
# Define commands that are not exposed as part of the 'setup' API.
# Some of these are exposed in a different way (i.e. not via autogeneration) on
# non-setup parts of the API. Some are excluded for now but might be included
# later. Some are used in the internal implementation of the setup API and are
# effectively exposed there but not via the auto-generated route (e.g.
# SetState and GetState).
###

# These are GUI-only commands in SyC
# We may want to expose them later in pySyC
_special_data_transfer_list = [
    "AddAerodampingDataTransfers",
    "AddFSIDataTransfers",
    "AddThermalDataTransfers",
    "GetAddDataTransferGroupCommands",
    "GetModeShapeVariables",
    "GetThermalDataTransferOptions",
]

# State and metadata commands/queries
# These are (or might be) used in impl but don't
# need exposing explicitly.
_state_meta_list = [
    "DatamodelRoot",
    "DeleteObject",
    "GetChildNames",
    "GetChildNamesStr",
    "GetChildren",
    "GetChildrenStr",
    "GetCommandAndQueryMetadata",
    "GetCommandAndQueryNames",
    "GetExplicitState",
    "GetMetadata",
    "GetParameter",
    "GetParameterOptions",
    "GetState",
    "GetStateWithOptions",
    "SetState",
]

# Related to case persistence
_case_list = [
    "GetSnapshots",
    "Open",
    "OpenSnapshot",
    "Save",
    "SaveSnapshot",
]


#
# Solution and postprocessing related
# Some exposed via other APIs
#
_exposed_solution_list = [
    "GetRestarts",
    "OpenResultsInEnSight",
    "PartitionParticipants",
    "Shutdown",
    "Solve",
    "StartParticipants",
    "Step",
    "WriteEnSight",
]

_other_solution_list = [
    "DoResultsExist",
    "DoesEnSightExist",
    "IsAnalysisInitialized",
    "OpenResultsInEnSight",
]

_solution_list = _exposed_solution_list + _other_solution_list

# Miscellaneous other exclusions
_misc_list = [
    "CreateNamedExpression",
    "ExecPythonString",
    "ExecuteCommandString",
    "GetErrorsXML",
    "GetOutOfSyncModules",
    "PrintExpressionVariables",
    "PrintSetup",
    "PrintSnapshots",
    "PrintState",
    "ReadScriptFile",
    "StartJournalFile",
    "StopLastJournalFile",
    "ValidateModuleSynchronization",
]

excluded_list = (
    _misc_list
    + _solution_list
    + _case_list
    + _special_data_transfer_list
    + _state_meta_list
)
