# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

cmd_metadata = [
    {
        "args": [
            ("ObjectPath", {"Type": "<class 'str'>"}),
            ("ParameterName", {"Type": "<class 'str'>"}),
        ],
        "defaults": (None,),
        "essentialArgNames": ["ObjectPath"],
        "isQuery": False,
        "name": "PrintExpressionVariables",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "PrintSetup",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "ClearState",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("CouplingIteration", {"Type": "<class 'int'>"}),
            ("CouplingStep", {"Type": "<class 'int'>"}),
            (
                "FilePath",
                {
                    "AllowUnicode": True,
                    "Type": "<class "
                    "'kernel.util.FileUtilities.ReadableUnicodeDirectory'>",
                },
            ),
        ],
        "defaults": (".", None, None),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "Open",
        "optionalArgNames": ["CouplingStep", "CouplingIteration"],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            (
                "FilePath",
                {
                    "AllowUnicode": True,
                    "Type": "<class "
                    "'kernel.util.FileUtilities.WritableUnicodeDirectory'>",
                },
            ),
        ],
        "defaults": (".",),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "Save",
        "optionalArgNames": [],
        "retType": "<class 'bool'>",
    },
    {
        "args": [
            (
                "ParticipantNames",
                {"Type": "<class " "'kernel.commands.ListTypes.StrList'>"},
            )
        ],
        "defaults": (None,),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "StartParticipants",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "Initialize",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "Shutdown",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "Solve",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [("Count", {"Type": "<class 'int'>"})],
        "defaults": (1,),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "Step",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("SideOneParticipant", {"Type": "<class 'str'>"}),
            (
                "SideOneRegions",
                {"Type": "<class " "'kernel.commands.ListTypes.StrList'>"},
            ),
            ("SideTwoParticipant", {"Type": "<class 'str'>"}),
            (
                "SideTwoRegions",
                {"Type": "<class " "'kernel.commands.ListTypes.StrList'>"},
            ),
        ],
        "defaults": (),
        "essentialArgNames": [
            "SideOneParticipant",
            "SideOneRegions",
            "SideTwoParticipant",
            "SideTwoRegions",
        ],
        "isQuery": False,
        "name": "AddInterface",
        "optionalArgNames": [],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            ("SideOneParticipant", {"Type": "<class 'str'>"}),
            (
                "SideOneRegions",
                {"Type": "<class " "'kernel.commands.ListTypes.StrList'>"},
            ),
            ("SideTwoParticipant", {"Type": "<class 'str'>"}),
            (
                "SideTwoRegions",
                {"Type": "<class " "'kernel.commands.ListTypes.StrList'>"},
            ),
        ],
        "defaults": (),
        "essentialArgNames": [
            "SideOneParticipant",
            "SideOneRegions",
            "SideTwoParticipant",
            "SideTwoRegions",
        ],
        "isQuery": False,
        "name": "AddInterfaceByDisplayNames",
        "optionalArgNames": [],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            ("Interface", {"Type": "<class 'str'>"}),
            ("SideOneVariable", {"Type": "<class 'str'>"}),
            ("SideTwoVariable", {"Type": "<class 'str'>"}),
            ("SourceVariable", {"Type": "<class 'str'>"}),
            ("TargetSide", {"Type": "<class 'str'>"}),
            ("TargetVariable", {"Type": "<class 'str'>"}),
            ("Value", {"Type": "<class 'str'>"}),
            ("ValueX", {"Type": "<class 'str'>"}),
            ("ValueY", {"Type": "<class 'str'>"}),
            ("ValueZ", {"Type": "<class 'str'>"}),
        ],
        "defaults": (None, None, None, None, None, None, None, None),
        "essentialArgNames": ["Interface", "TargetSide"],
        "isQuery": False,
        "name": "AddDataTransfer",
        "optionalArgNames": [
            "TargetVariable",
            "Value",
            "ValueX",
            "ValueY",
            "ValueZ",
            "SideOneVariable",
            "SideTwoVariable",
        ],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            ("Interface", {"Type": "<class 'str'>"}),
            ("SideOneVariable", {"Type": "<class 'str'>"}),
            ("SideTwoVariable", {"Type": "<class 'str'>"}),
            ("SourceVariable", {"Type": "<class 'str'>"}),
            ("TargetSide", {"Type": "<class 'str'>"}),
            ("TargetVariable", {"Type": "<class 'str'>"}),
            ("Value", {"Type": "<class 'str'>"}),
            ("ValueX", {"Type": "<class 'str'>"}),
            ("ValueY", {"Type": "<class 'str'>"}),
            ("ValueZ", {"Type": "<class 'str'>"}),
        ],
        "defaults": (None, None, None, None, None, None, None, None),
        "essentialArgNames": ["Interface", "TargetSide"],
        "isQuery": False,
        "name": "AddDataTransferByDisplayNames",
        "optionalArgNames": [
            "TargetVariable",
            "Value",
            "ValueX",
            "ValueY",
            "ValueZ",
            "SideOneVariable",
            "SideTwoVariable",
        ],
        "retType": "<class 'str'>",
    },
    {
        "args": [("ParticipantName", {"Type": "<class 'str'>"})],
        "defaults": (),
        "essentialArgNames": ["ParticipantName"],
        "isQuery": False,
        "name": "GetRegionNamesForParticipant",
        "optionalArgNames": [],
        "retType": "<class 'dict'>",
    },
    {
        "args": [("ParentReferenceFrame", {"Type": "<class 'str'>"})],
        "defaults": (None,),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "AddReferenceFrame",
        "optionalArgNames": [],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            ("Angle", {"Type": "<class 'object'>"}),
            ("Axis", {"Type": "<class 'str'>"}),
            ("ReferenceFrame", {"Type": "<class 'str'>"}),
            ("TransformationType", {"Type": "<class 'str'>"}),
            ("Vector", {"Type": "<class 'list'>"}),
        ],
        "defaults": (None, None, None),
        "essentialArgNames": ["ReferenceFrame", "TransformationType"],
        "isQuery": False,
        "name": "AddTransformation",
        "optionalArgNames": ["Axis", "Vector"],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            ("ReferenceFrame", {"Type": "<class 'str'>"}),
            ("TransformationName", {"Type": "<class 'str'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ReferenceFrame", "TransformationName"],
        "isQuery": False,
        "name": "DeleteTransformation",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [("ParticipantName", {"Type": "<class 'str'>"})],
        "defaults": (),
        "essentialArgNames": ["ParticipantName"],
        "isQuery": False,
        "name": "GetExecutionCommand",
        "optionalArgNames": [],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            ("FileName", {"Type": "<class 'str'>"}),
            ("ParticipantName", {"Type": "<class 'str'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ParticipantName", "FileName"],
        "isQuery": False,
        "name": "GenerateInputFile",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("AlgorithmName", {"Type": "<class 'str'>"}),
            (
                "MachineList",
                {"Type": "<class " "'kernel.commands.ListTypes.DictList'>"},
            ),
            (
                "NamesAndFractions",
                {"Type": "<class " "'kernel.commands.ListTypes.TupleList'>"},
            ),
        ],
        "defaults": (None, None, None),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "PartitionParticipants",
        "optionalArgNames": ["NamesAndFractions", "MachineList"],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "OpenResultsInEnSight",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("Binary", {"Type": "<class 'bool'>"}),
            ("FileName", {"Type": "<class 'str'>"}),
        ],
        "defaults": (True,),
        "essentialArgNames": ["FileName"],
        "isQuery": False,
        "name": "WriteEnSight",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "CreateRestartPoint",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("AdditionalArguments", {"Type": "<class 'str'>"}),
            (
                "Executable",
                {
                    "AllowUnicode": False,
                    "Type": "<class " "'kernel.util.FileUtilities.ValidFileName'>",
                },
            ),
            (
                "InputFile",
                {
                    "AllowUnicode": False,
                    "Type": "<class " "'kernel.util.FileUtilities.ReadableFileName'>",
                },
            ),
            ("ParticipantType", {"Type": "<class 'str'>"}),
            (
                "WorkingDirectory",
                {
                    "AllowUnicode": False,
                    "Type": "<class " "'kernel.util.FileUtilities.ValidDirectoryName'>",
                },
            ),
        ],
        "defaults": (None, None, None, None, None),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "AddParticipant",
        "optionalArgNames": [
            "InputFile",
            "Executable",
            "AdditionalArguments",
            "WorkingDirectory",
        ],
        "retType": "<class 'str'>",
    },
    {
        "args": [
            (
                "FilePath",
                {
                    "AllowUnicode": False,
                    "Type": "<class " "'kernel.util.FileUtilities.ReadableFileName'>",
                },
            )
        ],
        "defaults": (),
        "essentialArgNames": ["FilePath"],
        "isQuery": False,
        "name": "ImportSystemCouplingInputFile",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("OverwriteExisting", {"Type": "<class 'bool'>"}),
            ("SnapshotName", {"Type": "<class 'str'>"}),
        ],
        "defaults": (False,),
        "essentialArgNames": ["SnapshotName"],
        "isQuery": False,
        "name": "SaveSnapshot",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [("SnapshotName", {"Type": "<class 'str'>"})],
        "defaults": (None,),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "OpenSnapshot",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [("SnapshotName", {"Type": "<class 'str'>"})],
        "defaults": (),
        "essentialArgNames": ["SnapshotName"],
        "isQuery": False,
        "name": "DeleteSnapshot",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "PrintSnapshots",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "WriteCsvChartFiles",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            (
                "FileName",
                {
                    "AllowUnicode": False,
                    "Type": "<class " "'kernel.util.FileUtilities.ReadableFileName'>",
                },
            )
        ],
        "defaults": (),
        "essentialArgNames": ["FileName"],
        "isQuery": False,
        "name": "ReadScriptFile",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [("CommandString", {"Type": "<class 'str'>"})],
        "defaults": (),
        "essentialArgNames": ["CommandString"],
        "isQuery": False,
        "name": "ExecuteCommandString",
        "optionalArgNames": [],
        "retType": "<class 'object'>",
    },
    {
        "args": [("ObjectPath", {"Type": "<class 'str'>"})],
        "defaults": (),
        "essentialArgNames": ["ObjectPath"],
        "isQuery": False,
        "name": "DeleteObject",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("ObjectPath", {"Type": "<class 'str'>"}),
            ("State", {"Type": "<class 'dict'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ObjectPath", "State"],
        "isQuery": False,
        "name": "SetState",
        "optionalArgNames": [],
        "retType": "<class 'bool'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "GetErrors",
        "optionalArgNames": [],
        "retType": "<class 'list'>",
    },
    {
        "args": [
            (
                "ExpressionName",
                {
                    "Type": "<class "
                    "'kernel.util.ValidPythonSymbol.ValidPythonSymbol'>"
                },
            ),
            ("ExpressionString", {"Type": "<class 'str'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ExpressionName", "ExpressionString"],
        "isQuery": False,
        "name": "CreateNamedExpression",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            (
                "ExpressionName",
                {
                    "Type": "<class "
                    "'kernel.util.ValidPythonSymbol.ValidPythonSymbol'>"
                },
            ),
            ("ExpressionString", {"Type": "<class 'str'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ExpressionName", "ExpressionString"],
        "isQuery": False,
        "name": "AddNamedExpression",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            (
                "Function",
                {
                    "Type": "<class "
                    "'kernel.util.ValidPythonSymbol.ValidPythonSymbol'>"
                },
            ),
            (
                "FunctionName",
                {
                    "Type": "<class "
                    "'kernel.util.ValidPythonSymbol.ValidPythonSymbol'>"
                },
            ),
            ("Module", {"Type": "<class 'str'>"}),
        ],
        "defaults": (None,),
        "essentialArgNames": ["Module", "Function"],
        "isQuery": False,
        "name": "AddExpressionFunction",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": False,
        "name": "ReloadExpressionFunctionModules",
        "optionalArgNames": [],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            (
                "ObjectPath",
                {"Type": "<class " "'kernel.datamodel.ObjectPath.ObjectPath'>"},
            )
        ],
        "defaults": (),
        "essentialArgNames": ["ObjectPath"],
        "isQuery": True,
        "name": "GetChildren",
        "optionalArgNames": [],
        "retType": "<class 'list'>",
    },
    {
        "args": [
            (
                "ObjectPath",
                {"Type": "<class " "'kernel.datamodel.ObjectPath.ObjectPath'>"},
            )
        ],
        "defaults": (),
        "essentialArgNames": ["ObjectPath"],
        "isQuery": True,
        "name": "GetChildNames",
        "optionalArgNames": [],
        "retType": "<class 'list'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": True,
        "name": "DatamodelRoot",
        "optionalArgNames": [],
        "retType": "<class 'kernel.datamodel.ObjectPath.ObjectPath'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": True,
        "name": "GetCommandAndQueryNames",
        "optionalArgNames": [],
        "retType": "<class 'list'>",
    },
    {
        "args": [
            ("ExplicitSettingsOnly", {"Type": "<class 'bool'>"}),
            ("FileMode", {"Type": "<class 'str'>"}),
            ("FilePath", {"Type": "<class 'str'>"}),
            ("ObjectPath", {"Type": "<class 'str'>"}),
        ],
        "defaults": (None, None, "w", False),
        "essentialArgNames": [],
        "isQuery": True,
        "name": "PrintState",
        "optionalArgNames": ["FilePath", "FileMode", "ExplicitSettingsOnly"],
        "retType": "<class 'NoneType'>",
    },
    {
        "args": [
            ("Name", {"Type": "<class 'object'>"}),
            ("ObjectPath", {"Type": "<class 'str'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ObjectPath", "Name"],
        "isQuery": True,
        "name": "GetParameter",
        "optionalArgNames": [],
        "retType": "<class 'object'>",
    },
    {
        "args": [
            ("Name", {"Type": "<class 'str'>"}),
            ("ObjectPath", {"Type": "<class 'str'>"}),
        ],
        "defaults": (),
        "essentialArgNames": ["ObjectPath", "Name"],
        "isQuery": True,
        "name": "GetParameterOptions",
        "optionalArgNames": [],
        "retType": "<class 'tuple'>",
    },
    {
        "args": [("ObjectPath", {"Type": "<class 'str'>"})],
        "defaults": (),
        "essentialArgNames": ["ObjectPath"],
        "isQuery": True,
        "name": "GetState",
        "optionalArgNames": [],
        "retType": "<class 'dict'>",
    },
    {
        "args": [],
        "defaults": (),
        "essentialArgNames": [],
        "isQuery": True,
        "name": "GetErrorsXML",
        "optionalArgNames": [],
        "retType": "<class 'object'>",
    },
]
