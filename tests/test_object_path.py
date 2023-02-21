import pytest

from ansys.systemcoupling.core.native_api.object_path import ObjectPath
from ansys.systemcoupling.core.util.pathstr import to_typepath
from state import StateForTesting


@pytest.fixture
def rules():
    children = "children"
    params = "params"
    named = "named"
    data = {
        "/ROOT": {children: ["A", "B", "C"], params: [], named: False},
        "/ROOT/A": {children: ["A1"], params: ["a01", "a02"], named: False},
        "/ROOT/A/A1": {children: ["A2"], params: ["a11"], named: True},
        "/ROOT/A/A1/A2": {children: [], params: ["a21", "a22", "a23"], named: False},
        "/ROOT/B": {children: ["B1"], params: [], named: False},
        "/ROOT/B/B1": {children: [], params: ["b11"], named: False},
        "/ROOT/C": {children: ["C1"], params: ["c01"], named: False},
        "/ROOT/C/C1": {children: [], params: ["c11", "c12"], named: True},
    }
    return _Rules(data)


@pytest.fixture
def api():
    return _CommandApi()


@pytest.fixture
def root(api, rules):
    return ObjectPath("/ROOT", api, rules)


def test_root(root):
    assert str(root) == "/ROOT"
    assert set(root.child_types()) == set(["A", "B", "C"])


def test_named(root):
    path = root.A.A1["bob"]
    assert path == "/ROOT/A/A1:bob"
    assert path.get_name() == "bob"


def test_set_and_get_state(root):
    path = root.A.A1["bob"]
    assert path.GetState() == {}
    state = {"a11": 99}
    path.SetState(State=state)
    assert path.GetState() == state


def test_get_param_value(root):
    path = root.A.A1["bob"]
    path.SetState(State={"a11": 99})
    assert path.a11 == 99


def test_set_and_get_param(root):
    path = root.A.A1["bob"]
    assert path.GetState() == {}
    path.a11 = 100
    assert path.a11 == 100
    assert path.GetState() == {"a11": 100}


class _Rules:
    def __init__(self, data):
        self._rules = data

    def parameter_names(self, path):
        path = to_typepath(path)
        if path not in self._rules:
            return set()
        return set(self._rules[path]["params"])

    def child_types(self, path):
        path = to_typepath(path)
        if path not in self._rules:
            return set()
        return set(self._rules[path]["children"])

    def is_parameter_path(self, path):
        parent, _, last = path.rpartition("/")
        parent = to_typepath(parent)
        return parent in self._rules and last in self._rules[parent]["params"]

    def is_object_path(self, path):
        return to_typepath(path) in self._rules

    def is_named_object_path(self, path):
        objrules = self._rules.get(to_typepath(path), {})
        return objrules and objrules["named"]

    def get_objpath_command_and_query_names(self):
        return ["Fun1", "SetState", "GetState", "GetParameter"]

    def is_objpath_command_or_query(self, name):
        return name in self.get_objpath_command_and_query_names()


class _CommandApi:
    def __init__(self):
        self.__state = StateForTesting()

    def execute_command(self, name, *args, **kwargs):
        cmd = self._get_command(name)
        return cmd(*args, **kwargs)

    def _get_command(self, name):
        def Fun1(ObjectPath, Param1, Param2):
            pass

        def SetState(ObjectPath, State):
            self.__state.set_state(ObjectPath, State)

        def GetState(ObjectPath):
            return self.__state.get_state(ObjectPath)

        def GetParameter(ObjectPath, Name):
            return self.__state.get_parameter(ObjectPath, Name)

        if name == "Fun1":
            return Fun1

        if name == "SetState":
            return SetState

        if name == "GetParameter":
            return GetParameter

        if name == "GetState":
            return GetState

        return None
