"""Define commands that are not exposed as part of the 'setup' API.
Some of these are exposed in a different way (i.e. not via autogeneration) on
non-setup parts of the API. Some are excluded for now but might be included
later. Some are used in the internal implementation of the setup API and are
effectively exposed there but not via the auto-generated route (e.g.
SetState and GetState).
"""

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
_solution_list = [
    "DoResultsExist",
    "DoesEnSightExist",
    "GetRestarts",
    "IsAnalysisInitialized",
    "OpenResultsInEnSight",
    "PartitionParticipants",
    "Shutdown",
    "Solve",
    "StartParticipants",
    "Step",
    "WriteEnSight",
]

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
