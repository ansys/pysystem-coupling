# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

import pytest

from ansys.systemcoupling.core.util.pathstr import (
    join_path_strs,
    to_typelist,
    to_typepath,
)


@pytest.mark.parametrize(
    "path, expected",
    [("/a", "/a"), ("/a/b:b1", "/a/b"), ("/a:a1", "/a"), ("/", "/"), ("", "")],
)
def test_to_typepath(path, expected):
    assert to_typepath(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [("/a", ["a"]), ("/a/b:b1", ["a", "b"]), ("/a:a1", ["a"]), ("/", [""]), ("", [])],
)
def test_to_typelist(path, expected):
    assert to_typelist(path) == expected


@pytest.mark.parametrize(
    "strs, expected",
    [
        (("a",), "a"),
        (("/a", "b"), "/a/b"),
        (("a", "b"), "a/b"),
        (("/a", "b", "c"), "/a/b/c"),
    ],
)
def test_join_path_strs(strs, expected):
    assert join_path_strs(*strs) == expected
