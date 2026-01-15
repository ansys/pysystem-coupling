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
from ansys.systemcoupling.core.adaptor.impl.static_info import (
    make_named_object_level_map,
)


def test_make_map():

    metadata = {
        "ROOT": {
            "__children": {
                "B": {"isNamed": False, "__children": {}},
                "C": {
                    "isNamed": True,
                    "__children": {
                        "D": {"isNamed": True, "__children": {}},
                        "E": {"isNamed": True, "__children": {}},
                        "F": {"isNamed": False, "__children": {}},
                    },
                },
            },
        }
    }

    level_map = make_named_object_level_map(metadata, "ROOT")

    assert level_map[0] == set(["C"])
    assert level_map[1] == set(["D", "E"])
