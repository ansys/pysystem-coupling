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

from abc import ABC, abstractmethod


class SycProxyInterface(ABC):  # pragma: no cover
    """Provides an abstract base class defining the interface for the SystemCoupling
    *proxy* object that the ``datamodel` module depends on.

    While Python doesn't strictly need this class, it is a
    significant testing seam and is useful to make explicit the
    interface depended on.
    """

    @abstractmethod
    def get_static_info(self, category):
        pass

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def set_state(self, path, state):
        pass

    @abstractmethod
    def get_state(self, path):
        pass

    @abstractmethod
    def get_property_state(self, path, name):
        pass

    @abstractmethod
    def delete(self, path):
        pass

    @abstractmethod
    def create_named_object(self, path, name):
        pass

    @abstractmethod
    def get_object_names(self, path):
        pass

    @abstractmethod
    def get_property_options(self, path, name):
        pass

    @abstractmethod
    def execute_cmd(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute_injected_cmd(self, *args, **kwargs):
        pass
