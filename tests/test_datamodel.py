import pytest
from state import StateForTesting
from dm_meta_rawdata import dm_meta_testing_raw_data

from ansys.systemcoupling.core.settings import datamodel222_v2


class SycProxy:
    def __init__(self):
        self.__state = StateForTesting()

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


@pytest.fixture
def dm():
    proxy = SycProxy()
    return datamodel222_v2.get_root(proxy)


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
