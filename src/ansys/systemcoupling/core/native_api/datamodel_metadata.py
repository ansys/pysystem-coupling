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

from ansys.systemcoupling.core.util.assertion import assert_
from ansys.systemcoupling.core.util.pathstr import to_typelist


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
        assert_(category != Node.Parameter)
        super().__init__(id, category, parent)
        self.children = []

    def child(self, id):
        for c in self.children:
            if c.id == id:
                return c
        return None


class Parameter(Node):
    def __init__(self, name, data_type, parent):
        assert_(parent is not None)
        super().__init__(name, Node.Parameter, parent)
        self.data_type = data_type
        self.options = None


class Metadata:
    def __init__(self, root_node):
        self.__root = root_node

    def root_type(self):
        return self.__root.id

    def parameter_names(self, path):
        node = self._find_node(path)
        return [c.id for c in node.children if c.category == Node.Parameter]

    def child_types(self, path):
        node = self._find_node(path)
        return [
            c.id for c in node.children if c.category in (Node.Singleton, Node.Object)
        ]

    def is_parameter_path(self, path: str) -> bool:
        parent, _, last = path.rpartition("/")
        try:
            parent_node = self._find_node(parent)
            for c in parent_node.children:
                if c.category == Node.Parameter and c.id == last:
                    return True
            return False
        except:
            return False

    def is_object_path(self, path: str) -> bool:
        try:
            node = self._find_node(path)
            return node.category in (Node.Singleton, Node.Object)
        except:
            return False

    def is_named_object_path(self, path: str) -> bool:
        try:
            node = self._find_node(path)
            return node.category == Node.Object
        except:
            return False

    def _find_node(self, path: str) -> Node:
        types = to_typelist(path)
        node = self.__root
        if types[0] != node.id:
            raise RuntimeError(
                f"Invalid root type '{types[0]}' in path '{path}' (expected '{node.id}')."
            )
        last_t = None
        try:
            for t in types[1:]:
                last_t = t
                node = node.child(t)
            return node
        except KeyError as e:
            extra = (
                f" Type '{last_t}' unknown or at incorrect position." if last_t else ""
            )
            raise RuntimeError(f"Invalid data model path: {path}." + extra)


def _visit_metadata(raw_data, parent_node, write_option_values):
    for name, p_data in sorted(
        raw_data["__parameters"].items(), key=lambda item: item[1]["ordinal"]
    ):
        node = Parameter(name, p_data["type"], parent_node)
        options = p_data.get("staticOptions", None)
        if write_option_values and options:
            node.options = p_data["staticOptions"]
    for obj_type, c_data in sorted(
        raw_data["__children"].items(), key=lambda item: item[1]["ordinal"]
    ):
        node = Container(
            obj_type, Node.Object if c_data["isNamed"] else Node.Singleton, parent_node
        )
        _visit_metadata(c_data, node, write_option_values)


def build(raw_data):
    root = Container("SystemCoupling", Node.Singleton)
    _visit_metadata(raw_data[root.id], root, write_option_values=True)
    return Metadata(root)
