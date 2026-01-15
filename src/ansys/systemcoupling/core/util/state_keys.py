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

import copy
from typing import Any, Dict, Set


def adapt_native_named_object_keys(state):
    """Transform a System Coupling native-style nested state dictionary
    to an equivalent client-side format.

    In System Coupling, each named object instance has a "<type>:<name>"
    key in the state dictionary. Thus, the structure is:

    `"<type>:<name>" => {<state>}`

    On the client side, the structure is:

    `"<type>" => {"<name>" => {<state>}}`

    This function leaves the source state unaltered and returns a completely
    new dictionary in the required format. For an alternative that modifies
    the structure in place, see the ``adapt_native_named_object_keys_in_place``
    function.
    """
    state_mod = {}
    for k, v in state.items():
        if isinstance(v, dict):
            if ":" in k:
                t, _, n = k.partition(":")
                state_mod.setdefault(t, {})[n] = adapt_native_named_object_keys(v)
            else:
                state_mod[k] = adapt_native_named_object_keys(v)
        else:
            # in practice, copy only applies to list-valued settings
            state_mod[k] = copy.copy(v)
    return state_mod


def adapt_native_named_object_keys_in_place(state):
    """Modify in place a provided System Coupling native-style nested state dictionary
    to its equivalent client-side format.

    For more information, see the ``adapt_native_named_object_keys`` function.
    """
    to_delete = []
    for k in list(state.keys()):
        v = state[k]
        if isinstance(v, dict):
            adapt_native_named_object_keys_in_place(v)
            if ":" in k:
                t, _, n = k.partition(":")
                state.setdefault(t, {})[n] = v
                to_delete.append(k)
    for k in to_delete:
        del state[k]


def adapt_client_named_object_keys(
    state: Dict[str, Any], level_type_map: Dict[int, Set[str]], start_level: int = 0
) -> Dict[str, Any]:
    """Transform a System Coupling client-style nested state dictionary
    to an equivalent native format.

    This is the opposite of the transformation that the
    `adapt_native_named_object_keys` function performs. Unlike that
    function, this function cannot reliably do its job based only on
    the input state dictionary. This is because it is not possible
    to distinguish between what might be instances of a named object
    within the dictionary and what might be unnamed object entries.
    Some data model metadata is therefore required. This is provided
    by the ``level_type_map`` parameter.

    Parameters
    ----------
    state: dict
        The nested state dictionary to transform to the native format.
    level_type_map: dict
        Dictionary from the integer nest level (0-based) to sets of
        named object types at this level. Note that the level is
        the data model level. This means it does not include the extra
        levels introduced by the client-side format but more closely
        aligns with the target native format.
    start_level: int, optional
        If state is a sub-state of a larger state, and the level_type_map
        is for the larger state, then this parameter can be used to
        provide a starting level for the transformation.
    """

    def do_adapt(s, level=0):
        state_out = {}
        named_types = level_type_map.get(level, set())
        for id, sub_state in s.items():
            if not isinstance(sub_state, dict):
                state_out[id] = copy.copy(sub_state)
            elif id in named_types:
                for name, named_obj_state in sub_state.items():
                    state_out[f"{id}:{name}"] = do_adapt(named_obj_state, level + 1)
            else:
                state_out[id] = do_adapt(sub_state, level + 1)
        return state_out

    return do_adapt(state, level=start_level)
