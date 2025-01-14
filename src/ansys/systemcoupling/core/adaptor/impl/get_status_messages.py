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

"""Local implementation of the System Coupling ``GetErrors`` command, to be injected
into the ``setup`` hierarchy.
"""

from .types import Container, NamedContainer


def get_status_messages(rpc, setup_root_obj: Container, **kwargs):
    def get_field(msg, field_name):
        field = msg.get(field_name)
        if field is None:
            field = ""
        else:
            field = field.strip()
        return field

    def process(msg):
        path = _map_path(
            setup_root_obj, get_field(msg, "entity"), get_field(msg, "property")
        )
        level = get_field(msg, "level")
        message = get_field(msg, "text")
        return {"path": path, "level": level, "message": message}

    return [process(msg) for msg in rpc.GetErrors()]


def _make_attribute_path(container_path, property_name):
    path = ""
    for type, name in container_path:
        if path != "":
            path += "."
        path += type
        if name:
            path += f'["{name}"]'
    if property_name:
        path += f".{property_name}"
    return path


def _map_path(setup_root, initial_path, extra_path):
    if not initial_path:
        return None

    # The path data is in a strange legacy format. There are two parts that
    # need joining. The result may be a path to an object or a path to a
    # property.
    if not extra_path:
        full_path = initial_path
    else:
        full_path = initial_path + "/" + extra_path

    path_components = full_path.split("/")
    if path_components[0] == "":
        path_components = path_components[1:]
    if path_components[0] == "SystemCoupling":
        path_components = path_components[1:]

    # Drilling down the path components uses the settings
    # classes as a source of metadata.
    local_path = []
    local_property = None
    curr = setup_root
    for comp in path_components:
        if ":" in comp:
            type, _, name = comp.partition(":")
        else:
            type, name = comp, ""

        if isinstance(curr, Container) or isinstance(curr, NamedContainer):
            if isinstance(curr, NamedContainer):
                curr = curr.child_object_type
            child_map = curr._syc_to_py_childmap()
            if type in child_map:
                local_path.append((child_map[type], name))
                continue
        else:
            # Assume a property, so "type" is a property name
            # if there is a valid path and the location is the last
            # component.
            if len(local_path) == len(path_components) - 1:
                pmap = curr._syc_to_py_propertymap()
                local_property = pmap.get(type, None)
                if local_property:
                    # Done
                    break

    npath = len(path_components)
    nlocal = len(local_path)
    if (local_property and nlocal + 1 == npath) or (
        local_property is None and nlocal == npath
    ):
        return _make_attribute_path(local_path, local_property)

    # If you arrive here, the path was invalid.
    return None
