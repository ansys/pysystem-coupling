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

from ansys.api.systemcoupling.v0 import variant_pb2

# See to_variant() for use of this
_DUMMY_KEY = "__@!%$__"


def to_variant(val, var, convert_key=None):
    """Convert Python data type to Variant data type."""
    if val is None:
        var.none_state = variant_pb2.NONE_VALUE
    elif isinstance(val, bool):
        var.bool_state = val
    elif isinstance(val, int):
        var.int64_state = val
    elif isinstance(val, float):
        var.double_state = val
    elif isinstance(val, str):
        var.string_state = val
    elif isinstance(val, list) or isinstance(val, tuple):
        if len(val) == 0:
            # We need to force the one_of type to be set
            var.variant_vector_state.item.add()
            var.variant_vector_state.item.pop()
        for item in val:
            item_var = var.variant_vector_state.item.add()
            to_variant(item, item_var, convert_key)
    elif isinstance(val, dict):
        if len(val) == 0:
            # Analogous to list case - force map type to be set
            var.variant_map_state.item[_DUMMY_KEY].none_state = variant_pb2.NONE_VALUE
            del var.variant_map_state.item[_DUMMY_KEY]
        for k, v in val.items():
            k = convert_key(k) if convert_key else k
            to_variant(v, var.variant_map_state.item[k], convert_key)


def from_variant(var, convert_key=None):
    """Convert Variant data type to Python data type."""
    what = var.WhichOneof("as")
    if what == "none_state":
        return None
    if not what.startswith("variant_"):
        return getattr(var, what)
    if what == "variant_vector_state":
        return [from_variant(val, convert_key) for val in var.variant_vector_state.item]
    elif what == "variant_map_state":
        return {
            convert_key(k) if convert_key else k: from_variant(v, convert_key)
            for k, v in var.variant_map_state.item.items()
        }
