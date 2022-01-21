import pytest

from ansys.systemcoupling.core import object_path

@pytest.fixture
def rules():
    children = 'children'
    params = 'params'
    named = 'named'
    data = {
        '/ROOT': { children: ['A', 'B', 'C'], params: [], named: False },
        '/ROOT/A': { children: ['A1'], params: ['a01', 'a02'], named: False },
        '/ROOT/A/A1': { children: ['A2'], params: ['a11'], named: True },
        '/ROOT/A/A1/A2': { children: [], params: ['a21', 'a22', 'a23'], named: False },
        '/ROOT/B': { children: ['B1'], params: [], named: False },
        '/ROOT/B/B1': { children: [], params: ['b11'], named: False },
        '/ROOT/C': { children: ['C1'], params: ['c01'], named: False },
        '/ROOT/C/C1': { children: [], params: ['c11', 'c12'], named: True }
    }
    return _Rules(data)

@pytest.fixture
def api():
    return _CommandApi()

@pytest.fixture
def root(api, rules):
    return ObjectPath('/ROOT', api, rules)


ObjectPath = object_path.ObjectPath

def test_root(root):
    print(type(root))
    assert str(root) == '/ROOT'
    assert set(root.child_types()) == set(['A', 'B', 'C'])

def test_named(root):
    path = root.A.A1['bob']
    assert path == '/ROOT/A/A1:bob'
    assert path.GetName() == 'bob'

def test_set_and_get_state(root):
    path = root.A.A1['bob']
    assert path.GetState() == {}
    state = {'a11': 99}
    path.SetState(State=state)
    assert path.GetState() == state
    
def test_get_param_value(root):
    path = root.A.A1['bob']
    path.SetState(State={'a11': 99})
    assert path.a11 == 99
    
def test_set_and_get_param(root):
    path = root.A.A1['bob']
    assert path.GetState() == {}
    path.a11 = 100
    assert path.a11 == 100
    assert path.GetState() == {'a11': 100}
    
class _Rules:

    def __init__(self, data):
        self._rules = data

    def parameter_names(self, path):
        path = _toTypePath(path)
        if path not in self._rules:
            return set()
        return set(self._rules[path]['params'])
        
    def child_types(self, path):
        path = _toTypePath(path)
        if path not in self._rules:
            return set()
        return set(self._rules[path]['children'])

    def is_parameter_path(self, path):
        parent, _, last = path.rpartition('/')
        parent = _toTypePath(parent)
        return parent in self._rules and last in self._rules[parent]['params']

    def is_object_path(self, path):
        return _toTypePath(path) in self._rules

    def is_named_object_path(self, path):
        objrules = self._rules.get(_toTypePath(path), {})
        return objrules and objrules['named']

    def get_object_path_command_and_query_names(self):
        return ['Fun1', 'SetState', 'GetState', 'GetParameter']

    def is_object_path_command_or_query(self, name):
        return name in self.get_object_path_command_and_query_names()
            

class _CommandApi:

    def __init__(self):
        self.__state = {}
    
    def execute_command(self, name, *args, **kwargs):
        cmd = self._get_command(name)
        return cmd(*args, **kwargs)
    
    def _get_command(self, name):

        def Fun1(ObjectPath, Param1, Param2):
            pass

        def SetState(ObjectPath, State):
            comps = ObjectPath.split('/')
            if comps and comps[0] == '':
                comps = comps[1:]
            if not comps:
                raise Exception('Path is empty')

            comps, last = comps[:-1], comps[-1]

            s = self.__state
            missed = False
            for comp in comps:
                if comp in s:
                    s = s[comp]
                else:
                    s[comp] = {}
                    s = s[comp]
                    #missed = True
                    #break
            if missed:
                raise Exception(f"Path '{ObjectPath}' does not exist in state")

            s[last] = State
            
        
        def GetState(ObjectPath):
            comps = ObjectPath.split('/')
            if comps and comps[0] == '':
                comps = comps[1:]

            s = self.__state
            found_some = False
            for comp in comps:
                if comp in s:
                    found_some = True
                    s = s[comp]
                else:
                    return {}
            
            return s if found_some else {}

        def GetParameter(ObjectPath, Name):
            s = GetState(ObjectPath)
            return s.get(Name, None)
        
        if name == 'Fun1':
            return Fun1

        if name == 'SetState':
            return SetState

        if name == 'GetParameter':
            return GetParameter
        
        if name == 'GetState':
            return GetState
        
        return None

def _toTypePath(path):
    if ':' not in path:
        return path
    return '/'.join(c.split(':')[0] for c in path.split('/'))

                    
