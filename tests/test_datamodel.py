import pytest
from state import StateForTesting
from dm_meta_rawdata import dm_meta_testing_raw_data

from ansys.systemcoupling.core.settings import datamodel222

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
    return datamodel222.get_root(proxy)

def test_empty(dm):
    assert dm.get_state() == {}

def test_create_library(dm):
    dm.Library = {}
    assert dm.get_state() == {'Library':{}}

def test_create_expression(dm):
    dm.Library.Expression['bob'] = {'ExpressionName': 'expr', 'ExpressionString': '2 * x'}
    assert dm.get_state() == {'Library': {'Expression': {'bob': {'ExpressionName': 'expr', 'ExpressionString': '2 * x'}}}}
    assert dm.Library() == {'Expression': {'bob': {'ExpressionName': 'expr', 'ExpressionString': '2 * x'}}}
    assert dm.Library.Expression['bob']() == {'ExpressionName': 'expr', 'ExpressionString': '2 * x'}
    assert dm.Library.Expression['bob']() == dm.Library.Expression['bob'].get_state()

def test_modify_expression(dm):
    dm.Library.Expression['bob'] = {'ExpressionName': 'expr', 'ExpressionString': '2 * x'}
    dm.Library.Expression['bob'].ExpressionString = '3 * x'
    assert dm.Library.Expression['bob']() == {'ExpressionName': 'expr', 'ExpressionString': '3 * x'}
    assert dm.Library.Expression['bob'].ExpressionString() == '3 * x'
    #assert dm.Library.Expression['bob'].ExpressionString == '3 * x'