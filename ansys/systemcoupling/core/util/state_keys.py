import copy


def adapt_native_named_object_keys(state):
    """Transforms a System Coupling native-style nested state dict
    to an equivalent client-side format.

    In System Coupling each named object instance has a "<type>:<name>"
    key in the state dict, so the structure is:

    `"<type>:<name>" => {<state>}`

    On the client side, the structure is:

    `"<type>" => {"<name>" => {<state>}}`

    This function leaves the source state unaltered and returns a completely
    new dict in the required format. See `adapt_native_named_object_keys_in_place`
    for an alternative that modifies the structure in place.
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
    """Modifies in place a provided System Coupling native-style nested state dict
    to its equivalent client-side format.

    See `adapt_native_named_object_keys` for details.
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


def adapt_client_named_object_keys(state, level_type_map):
    """Transforms a System Coupling client-style nested state dict
    to an equivalent native format.

    This is the opposite of the transformation that
    `adapt_native_named_object_keys` performs. Unlike that function,
    the present function cannot reliably do its job purely based on
    the input state dictionary. This is because it is not possible
    to distinguish between what might be instances of a named object
    within the dict from what might equally be unnamed object entries.
    Some data model metadata is therefore required. This is provided
    by the `level_type_map` parameter.

    `level_type_map` is a dict from integer nest level (0-based) to
    sets of named object types at that level. Note that the level is
    the _datamodel_ level. This means it does not include the extra
    levels introduced by the client-side format, but is more closely
    aligned with the target native format.
    """

    def do_adapt(s, level=0):
        state_out = {}
        named_types = level_type_map.get(level, set())
        for id, sub_state in s.items():
            if id in named_types:
                for name, named_obj_state in sub_state.items():
                    state_out[f"{id}:{name}"] = do_adapt(named_obj_state, level + 1)
            elif isinstance(sub_state, dict):
                state_out[id] = do_adapt(sub_state, level + 1)
            else:
                state_out[id] = copy.copy(sub_state)
        return state_out

    return do_adapt(state)
