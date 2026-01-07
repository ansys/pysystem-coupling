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

import pytest

from ansys.systemcoupling.core.session import Session
from cmd_raw_metadata import cmd_metadata
from dm_raw_metadata import dm_metadata
from state import StateForTesting


class _MockCommandExecutor:
    def __init__(self):
        self.__state = StateForTesting(native_state_format=True)

    def GetMetadata(self, json_ret=None):
        return dm_metadata

    def GetCommandAndQueryMetadata(self):
        return cmd_metadata

    def SetState(self, ObjectPath, State):
        self.__state.set_state(ObjectPath, State)

    def GetState(self, ObjectPath):
        return self.__state.get_state(ObjectPath)

    def GetParameter(self, ObjectPath, Name):
        return self.__state.get_parameter(ObjectPath, Name)

    def GetCommandAndQueryNames(self):
        return [item["name"] for item in cmd_metadata]

    def execute_command(self, name, **kwargs):
        f = getattr(self, name)
        return f(**kwargs)

    def __getattr__(self, name):
        raise AttributeError(f"Command '{name}' has no mock implementation.")


@pytest.fixture
def api():
    cmd_exec = _MockCommandExecutor()
    session = Session(cmd_exec)
    return session._native_api


def test_create_object(api):
    api.Library.Expression["expr1"] = {
        "ExpressionName": "bob",
        "ExpressionString": "2 * x",
    }
    assert api.Library.GetState() == {
        "Expression:expr1": {"ExpressionName": "bob", "ExpressionString": "2 * x"}
    }


def test_top_level_obj_path_cmd(api):
    assert api.GetState() == {}


def test_top_level_non_obj_path_cmd(api):
    cmds = api.GetCommandAndQueryNames()
    # We're not bothered about checking the list in detail
    assert "GetState" in cmds
    assert len(cmds) > 15
