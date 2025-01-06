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

from typing import Iterable, List


def to_typelist(path: str) -> List[str]:
    """Return types in path (meaning discarding names) as a list."""
    if "/" not in path:
        return []
    if ":" not in path:
        return path.split("/")[1:]
    return [c.split(":")[0] for c in path.split("/")][1:]


def to_typepath(path: str) -> str:
    """Return path as a type path (meaning a path of types)."""
    if ":" not in path:
        return path
    return "/".join(c.split(":")[0] for c in path.split("/"))


def join_path_strs(*path_strs: Iterable[str]) -> str:
    """Join a list of strings as a path string.

    .. note::
       A leading empty path component is required for a
       leading path separator (``/``) in the returned value.
    """
    return "/".join(path_strs)
