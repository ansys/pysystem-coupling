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
from ansys.systemcoupling.core.util.pathstr import join_path_strs


class ObjectPath(str):
    """Provides a simple utility class for attribute-based access to children of data model
    objects and values.

    For example:

    ``Root.CouplingInterface["intf-1"].Side["One"].CouplingParticipant = "MAPDL-1"``
    """

    def __new__(cls, path, api, rules):
        inst = str.__new__(cls, path)

        inst.__setattr("_api", api)
        inst.__setattr("_rules", rules)
        inst.__setattr("_parameter_names", None)
        inst.__setattr("_child_types", None)
        inst.__setattr("_is_object_path", None)
        inst.__setattr(
            "_get_param_value",
            lambda path, name: api.execute_command(
                "GetParameter", ObjectPath=path, Name=name
            ),
        )

        return inst

    def parameter_names(self):
        if self._parameter_names is None:
            self.__setattr("_parameter_names", self._rules.parameter_names(self))
        return self._parameter_names

    def child_types(self):
        if self._child_types is None:
            self.__setattr("_child_types", self._rules.child_types(self))
        return self._child_types

    def param_path(self, name):
        return join_path_strs(self, name)

    def obj_path(self, name):
        return self + ":" + name

    def __getitem__(self, name):
        if isinstance(name, (int, slice)):
            return super(ObjectPath, self).__getitem__(name)
        else:
            return self.make_path(self.obj_path(name))

    def is_param_path(self):
        return self._rules.is_parameter_path(self)

    def is_object_path(self):
        if self._is_object_path is None:
            self.__setattr("_is_object_path", self._rules.is_object_path(self))
        return self._is_object_path

    def get_name(self):
        left, sep, right = self.rpartition("/")
        assert_(":" in right)
        type, sep, name = right.partition(":")
        return name

    def __setattr__(self, name, value):
        self.SetState(State={name: value})

    def __setitem__(self, name, value):
        self.make_path(self.obj_path(name)).SetState(State=value)

    def __setattr(self, name, value):
        # used during init only - not to be confused with __setattr__
        return super(ObjectPath, self).__setattr__(name, value)

    def __getattr__(self, name):
        if self.is_object_path():
            if name in self.parameter_names():
                return self._get_param_value(self, name)
            elif name in self.child_types():
                obj = self.make_path(self.param_path(name))
                self.__setattr(name, obj)
                return obj
        if self._rules.is_objpath_command_or_query(name):
            return lambda **kwds: self._api.execute_command(
                name, ObjectPath=self, **kwds
            )
        raise AttributeError(name)

    def make_path(self, path_str):
        return ObjectPath(path_str, self._api, self._rules)
