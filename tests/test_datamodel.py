from dm_meta_rawdata import dm_meta_testing_raw_data
import pytest
from state import StateForTesting

from ansys.systemcoupling.core.settings import datamodel_222 as datamodel


class SycProxy:
    def __init__(self):
        self.__state = StateForTesting()
        self.clear_last_cmd()

    def clear_last_cmd(self):
        self.last_cmd_path = None
        self.last_cmd_name = None
        self.last_cmd_args = None

    def get_static_info(self):
        return dm_meta_testing_raw_data

    def set_state(self, path, state):
        self.__state.set_state(path, state)

    def get_state(self, path):
        return self.__state.get_state(path)

    def delete(self, path):
        self.__state.delete_object(path)

    def create(self, path, name):
        self.__state.create(path, name)

    def get_object_names(self, path):
        state = self.__state.get_state(path)
        return list(state.keys())

    def execute_cmd(self, *args, **kwargs):
        self.last_cmd_path = args[0]
        self.last_cmd_name = args[1]
        self.last_cmd_args = dict(**kwargs)
        return None


@pytest.fixture
def dm():
    proxy = SycProxy()
    return datamodel.get_root(proxy)


def test_empty(dm):
    assert dm.get_state() == {}


def test_create_library(dm):
    dm.library = {}
    assert dm.get_state() == {"library": {}}


def test_create_expression(dm):
    dm.library.expression["bob"] = {
        "expression_name": "expr",
        "expression_string": "2 * x",
    }
    assert dm.get_state() == {
        "library": {
            "expression": {
                "bob": {"expression_name": "expr", "expression_string": "2 * x"}
            }
        }
    }
    assert dm.library() == {
        "expression": {"bob": {"expression_name": "expr", "expression_string": "2 * x"}}
    }
    assert dm.library.expression["bob"]() == {
        "expression_name": "expr",
        "expression_string": "2 * x",
    }
    assert dm.library.expression["bob"]() == dm.library.expression["bob"].get_state()


def test_modify_expression(dm):
    dm.library.expression["bob"] = {
        "expression_name": "expr",
        "expression_string": "2 * x",
    }
    dm.library.expression["bob"].expression_string = "3 * x"
    assert dm.library.expression["bob"]() == {
        "expression_name": "expr",
        "expression_string": "3 * x",
    }
    assert dm.library.expression["bob"].expression_string == "3 * x"


def test_set_nested_state_get_by_path(dm):
    dm.set_state(
        {
            "library": {
                "expression": {
                    "bob": {"expression_name": "expr", "expression_string": "2 * x"}
                }
            }
        }
    )
    assert dm.library.expression["bob"].expression_string == "2 * x"


def test_syc_path(dm):
    dm.library.expression["bob"] = {}
    assert dm.library.expression["bob"]() == {}
    assert (
        dm.library.expression["bob"].syc_path
        == "/SystemCoupling/Library/Expression:bob"
    )


def test_invoke_solve(dm):
    dm.sycproxy.clear_last_cmd()
    dm.solve()
    assert dm.sycproxy.last_cmd_name == "Solve"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling"
    assert dm.sycproxy.last_cmd_args == {}


def test_invoke_get_parameter_options(dm):
    dm.sycproxy.clear_last_cmd()
    dm.get_parameter_options(name="dummy")
    assert dm.sycproxy.last_cmd_name == "GetParameterOptions"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling"
    assert dm.sycproxy.last_cmd_args == {
        "ObjectPath": "/SystemCoupling",
        "Name": "dummy",
    }


def test_solution_control_state(dm):
    # Not really testing anything new here but sanity
    # check in prep for path-based command
    dm.solution_control.duration_option = "EndTime"
    assert dm.solution_control.duration_option == "EndTime"


def test_invoke_get_parameter_options_on_path(dm):
    dm.sycproxy.clear_last_cmd()
    dm.solution_control.duration_option = "EndTime"
    dm.solution_control.get_parameter_options(name="duration_option")
    assert dm.sycproxy.last_cmd_name == "GetParameterOptions"
    assert dm.sycproxy.last_cmd_path == "SystemCoupling/SolutionControl"
    # TODO: Name is problematic as we should be transforming this to SyC name!
    assert dm.sycproxy.last_cmd_args == {
        "ObjectPath": "/SystemCoupling/SolutionControl",
        "Name": "duration_option",
    }
