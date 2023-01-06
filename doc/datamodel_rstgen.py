"""Provide a module to generate the documentation classes for System Coupling data model
and commands tree.

Running this module generates a .rst files for the System Coupling auto-generated API classes.
The output is placed at:

- doc/source/api/core/settings/_autosummary/api

Process
-------
    - From the settings API classes recursively generate the list of parents for the current class.
    -- Populate a parents dictionary with current class file name (not class name) as key and list
       of parents file names (not class names) as value.
    - Recursively Generate the rst files for classes starting with root class.
    -- Add target reference as the file name for the given class. This is used by other classes to
       generate hyperlinks
    -- Add properties like members, undoc-memebers, show-inheritence to the autoclass directive.
    -- Generate the tables of children, commands, arguments, and parents.
    --- Get access to the respective properties and members on the class with get_attr.
    --- Use the filename of the child class to generate the hyperlink to that class.
    --- Use the __doc__ property to generate the short summary for the corresponding child
    --- Use the previously generated perents dict to populate the parents table.
Usage
-----
python <path to datamodel_rstgen.py>
"""
import importlib
import os

# PYSYC_DOC_BUILD_VERSION should contain a string such as "23_2" that determines the
# System Coupling version the API is generated for and which we are building doc for.
# This should be the only place in this script where we depend on the version.
api_path = f"ansys.systemcoupling.core.adaptor.api_{os.environ['PYSYC_DOC_BUILD_VERSION']}"
case_root = importlib.import_module(f"{api_path}.case_root")
setup_root = importlib.import_module(f"{api_path}.setup_root")
solution_root = importlib.import_module(f"{api_path}.solution_root")

from ansys.systemcoupling.core.util.name_util import to_python_name as to_snake_case

parents_dict = {}
rst_list = []


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _find_indent(line):
    count = 0
    while line and line[count] == " ":
        count += 1
    return count


def _generate_property_list_for_rst(r, data_dict={}):
    indent = " " * 4
    for prop, info in data_dict.items():
        doc, type = info
        if type.endswith("Type"):
            r.write(f"{prop} : :ref:`{type}<{to_snake_case(type)}>`\n")
        else:
            r.write(f"{prop} : `{type}`\n")
        lines = doc.split("\n")
        if len(lines) > 1:
            # Assume multi-line doc string has initial text immediately after
            # opening """. Following lines will then have a default indent bringing
            # them in line with first '"'. It is possible that some lines might have
            # a further indent. Find the minimum indent from second line onwards
            # and remove it. Ignore any empty/whitespace only lines (paragraph
            # separators).
            #
            # This falls down if all lines are meant to be indented
            # relative to first. Could be addressed by manually splitting first doc
            # line perhaps?
            inferred_indent = min(
                (_find_indent(line) for line in lines[1:] if line.strip() != ""), default=0
                )
            lines = [lines[0]] + [line[inferred_indent:] for line in lines[1:]]

        doc = indent + (f"\n{indent}".join(lines))
        r.write(f"{doc}\n\n")


def _generate_table_for_rst(r, data_dict={}):
    # Get dimensions for columns
    key_max = len(max(data_dict.keys(), key=len))
    val_max = len(max(data_dict.values(), key=len))
    col_gap = 3
    total = key_max + val_max + col_gap
    # Top border
    r.write(f'{"="*key_max}{" "*col_gap}{"="*val_max}\n\n')
    header = True
    for key, value in data_dict.items():
        if header:
            # Write header and border
            r.write(f'{key}{" "*(total-len(key)-len(value))}{value}\n\n')
            r.write(f'{"="*key_max}{" "*col_gap}{"="*val_max}\n')
            header = False
        else:
            # actual data
            r.write(f'{key}{" "*(total-len(key)-len(value))}{value}\n\n')
    # Bottom border
    r.write(f'{"="*key_max}{" "*col_gap}{"="*val_max}\n\n')


def _populate_parents_list(cls):
    if hasattr(cls, "child_names"):
        for child in cls.child_names:
            child_cls = getattr(cls, child)
            child_file = child_cls.__module__.split(".")[-1]
            if not parents_dict.get(child_file):
                parents_dict[child_file] = []
            if not cls in parents_dict[child_file]:
                parents_dict[child_file].append(cls)

    if hasattr(cls, "command_names"):
        for child in cls.command_names:
            child_cls = getattr(cls, child)
            child_file = child_cls.__module__.split(".")[-1]
            if not parents_dict.get(child_file):
                parents_dict[child_file] = []
            if not cls in parents_dict[child_file]:
                parents_dict[child_file].append(cls)

    # if hasattr(cls, "argument_names"):
    #     for child in cls.argument_names:
    #         child_cls = getattr(cls, child)
    #         child_file = child_cls.__module__.split(".")[-1]
    #         if not parents_dict.get(child_file):
    #             parents_dict[child_file] = []
    #         if not cls in parents_dict[child_file]:
    #             parents_dict[child_file].append(cls)

    if hasattr(cls, "child_object_type"):
        child_cls = getattr(cls, "child_object_type")
        child_file = child_cls.__module__.split(".")[-1]
        if not parents_dict.get(child_file):
            parents_dict[child_file] = []
        if not cls in parents_dict[child_file]:
            parents_dict[child_file].append(cls)

    if hasattr(cls, "child_names"):
        for child in cls.child_names:
            _populate_parents_list(getattr(cls, child))

    if hasattr(cls, "command_names"):
        for child in cls.command_names:
            _populate_parents_list(getattr(cls, child))

    if hasattr(cls, "argument_names"):
        for child in cls.argument_names:
            _populate_parents_list(getattr(cls, child))

    if hasattr(cls, "child_object_type"):
        _populate_parents_list(getattr(cls, "child_object_type"))


def _populate_rst_from_settings(rst_dir, cls):
    istr1 = _get_indent_str(1)
    cls_name = cls.__name__
    file_name = cls.__module__.split(".")[-1]
    rstpath = os.path.normpath(os.path.join(rst_dir, file_name + ".rst"))

    has_properties = (
        hasattr(cls, "property_names_types") and len(cls.property_names_types) > 0
    )
    has_children = hasattr(cls, "child_names") and len(cls.child_names) > 0
    has_commands = hasattr(cls, "command_names") and len(cls.command_names) > 0
    has_arguments = hasattr(cls, "argument_names") and len(cls.argument_names) > 0
    has_named_object = hasattr(cls, "child_object_type")
    with open(rstpath, "w") as r:
        # Populate initial rst
        r.write(":orphan:\n\n")
        r.write(f".. _{file_name}:\n\n")
        title = cls_name
        # Possibly need something like this, but generalised?
        # if title == "case_root":
        #    title = "Case and Persistence Commands"
        r.write(f"{title}\n")
        r.write(f'{"="*(len(title))}\n\n')
        r.write(
            f".. currentmodule:: {api_path}.{file_name}\n\n"
        )
        r.write(f".. autoclass:: {cls_name}\n")
        r.write(f"{istr1}:show-inheritance:\n")
        r.write(f"{istr1}:undoc-members:\n")

        if has_properties:
            r.write(f".. rubric:: Properties\n\n")
            data_dict = {}
            for prop, _, ptype in cls.property_names_types:
                prop_attr = getattr(cls, prop)
                data_dict[prop] = (prop_attr.__doc__, ptype)
            _generate_property_list_for_rst(r, data_dict)

        if has_children:
            r.write(f".. rubric:: Children\n\n")
            data_dict = {}
            data_dict["Child"] = "Summary"
            for child in cls.child_names:
                child_cls = getattr(cls, child)
                ref_string = f":ref:`{child} <{child_cls.__module__.split('.')[-1]}>`"
                data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

        if has_commands:
            r.write(f".. rubric:: Commands\n\n")
            data_dict = {}
            data_dict["Command"] = "Summary"
            for child in cls.command_names:
                child_cls = getattr(cls, child)
                ref_string = f":ref:`{child} <{child_cls.__module__.split('.')[-1]}>`"
                data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

        if False and has_arguments:
            r.write(f".. rubric:: Arguments\n\n")
            data_dict = {}
            data_dict["Argument"] = "Summary"
            for child in cls.argument_names:
                child_cls = getattr(cls, child)
                ref_string = f":ref:`{child} <{child_cls.__module__.split('.')[-1]}>`"
                data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

        if has_named_object:
            child_cls = getattr(cls, "child_object_type")
            ref_string = (
                f":ref:`{child_cls.__name__} <{child_cls.__module__.split('.')[-1]}>`"
            )
            data_dict = {}
            data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            r.write(f".. rubric:: Named object type\n\n")
            r.write(f"{ref_string}\n\n\n")

        if parents_dict.get(file_name):
            r.write(f".. rubric:: Included in:\n\n")
            data_dict = {}
            data_dict["Parent"] = "Summary"
            for parent in parents_dict.get(file_name):
                parent_file = parent.__module__.split(".")[-1]
                ref_string = f":ref:`{parent.__name__} <{parent_file}>`"
                data_dict[ref_string] = parent.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

    if not rstpath in rst_list:
        rst_list.append(rstpath)
        if has_children:
            for child in cls.child_names:
                _populate_rst_from_settings(rst_dir, getattr(cls, child))

        if has_commands:
            for child in cls.command_names:
                _populate_rst_from_settings(rst_dir, getattr(cls, child))

        # if has_arguments:
        #    for child in cls.argument_names:
        #        _populate_rst_from_settings(rst_dir, getattr(cls, child))

        if has_named_object:
            _populate_rst_from_settings(rst_dir, getattr(cls, "child_object_type"))


if __name__ == "__main__":
    print("Generating rst files for settings API classes")
    dirname = os.path.dirname(__file__)
    rst_dir = os.path.normpath(
        os.path.join(
            dirname,
            "source",
            "api",
            "core",
            "settings",
            "_autosummary",
            "api",
        )
    )
    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    for root in (
        case_root.case_root,
        setup_root.setup_root,
        solution_root.solution_root,
    ):
        _populate_parents_list(root)
        _populate_rst_from_settings(rst_dir, root)
        parents_dict = {}
        rst_list = []
