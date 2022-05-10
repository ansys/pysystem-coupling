from cmd_raw_metadata2 import cmd_metadata
from dm_raw_metadata import dm_metadata
import pytest
from state import StateForTesting

from ansys.systemcoupling.core.analysis import SycAnalysis


class _MockCommandExecutor:
    def __init__(self):
        self.__state = StateForTesting(native_state_format=True)

    def GetMetadata(self):
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
    analysis = SycAnalysis(cmd_exec)
    return analysis.native_api


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
