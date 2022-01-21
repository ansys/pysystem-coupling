class Node:
    Singleton = 0
    Object = 1
    ParameterHolder = 2
    Parameter = 3

    def __init__(self, id, category, parent=None):
        self.id = id
        self.category = category
        self.parent = parent
        if parent:
            parent.children.append(self)

class Container(Node):
    def __init__(self, id, category, parent=None):
        assert category != Node.Parameter
        super().__init__(id, category, parent)
        self.children = []

class Parameter(Node):
    def __init__(self, name, data_type, parent):
        assert parent is not None
        super().__init__(name, Node.Parameter, parent)
        self.data_type = data_type
        self.options = None

class Metadata:
    def __init__(self, root_node):
        self.__root = root_node
        
    def parameter_names(self, path):
        node = self._find_node(path)
        return [c.id for c in node.children if c.category == Node.Parameter]
     
    def child_types(self, path):
        node = self._find_node(path)
        return [c.id for c in node.children if c.category in (Node.Singleton, Node.Object)]
        
    def is_parameter_path(self, path):
        parent, _, last = path.rpartition('/')
        try:
            parent_node = self._find_node(parent)
            for c in parent_node.children:
                if c.category == Node.Parameter and c.id == last:
                    return True
            return False
        except:
            return False
        
    def is_object_path(self, path):
        try:
            node = self._find_node(path)
            return node.category in (Node.Singleton, Node.Object)
        except:
            return False
        
    def is_named_object_path(self, path):
        try:
            node = self._find_node(path)
            return node.category == Node.Object
        except:
            return False

    def _find_node(self, path):
        types = _to_typelist(path)
        node = self.__root
        last_t = None
        try:
            for t in types:
                last_t = t
                node = node.children[t]
            return node
        except KeyError as e:
            extra = f' Type \'{last_t}\' unknown or at incorrect position.') if last_t else ''
            raise RuntimeError(f'Invalid data model path: {path}.' + extra)

def _to_typelist(path):
    if ':' not in path:
        return path.split('/')
    return [c.split(':')[0] for c in path.split('/')]
       
def _to_typepath(path):
    if ':' not in path:
        return path
    return '/'.join(c.split(':')[0] for c in path.split('/'))


def _visit_metadata(raw_data, parent_node, write_option_values):
    for name, p_data in sorted(raw_data['__parameters'].items(), 
                       key=lambda item: item[1]['ordinal']):
        node = Parameter(name, p_data['type'], parent_node)
        options = p_data.get('staticOptions', None)
        if write_option_values and options:
            node.options = p_data['staticOptions']
    for obj_type, c_data in sorted(raw_data['__children'].items(), 
                                 key=lambda item: item[1]['ordinal']):
        node = Container(obj_type, 
                         Node.Object if c_data['isNamed'] else Node.Singleton,
                         parent_node)
        _visit_metadata(c_data, node, write_option_values)

def build(raw_data):
    root = Container('SystemCoupling', Node.Singleton)
    meta_tree = _visit_metadata(raw_data[root.id], root, write_option_values=True)
    return Metadata(meta_tree)
    
