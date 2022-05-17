"""
Script to generate the System Coupling settings tree.

This generates a python module with the definition of the System Coupling
generated API classes. The modules are placed at:

- ansys/systemcoupling/core/solver/settings/case_231.py
- ansys/systemcoupling/core/solver/settings/setup_231.py
- ...

pysystemcoupling itself is run in a 'basic' mode to query for the input
metadata on which the generated module is based. To make pysystemcoupling
available in the current environment, there are two main options:

(i)  install a pysystemcoupling package
(ii) run directly from the source. In this case, the dependencies of
     pysystemcoupling must be installed.

This script may also be run in a mode that generates testing data.
In this case run with the -t argument. Input is taken from the
dm_raw_metadata module in tests/ and is written to
generated_testing_datamodel.py in the same directory.



Usage
-----
python <path to generate_datamodel.py> [-t]
"""

from copy import deepcopy
import io

# import json
import os
import pprint
import sys
from typing import IO

# Allows us to run pysystemcoupling from source without setting PYTHONPATH
_dirname = os.path.dirname(__file__)
sys.path.append(os.path.normpath(os.path.join(_dirname, "..")))
print(sys.path[-1])


from ansys.systemcoupling.core.settings import datamodel
from ansys.systemcoupling.core.settings.command_data import (
    process as process_command_data,
)


def _gethash(obj_info):
    return datamodel._gethash(obj_info)


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _write_property_helper(out, pname, ptype_str, doc_str, indent=0):
    istr = _get_indent_str(indent)
    istr1 = _get_indent_str(indent + 1)
    out.write("\n")
    out.write(f"{istr}@property\n")
    out.write(f"{istr}def {pname}(self) -> {ptype_str}:\n")
    out.write(f'{istr1}"""{doc_str}"""\n')
    out.write(f'{istr1}return self.get_property_state("{pname}")\n')
    out.write("\n")
    out.write(f"{istr}@{pname}.setter\n")
    out.write(f"{istr}def {pname}(self, value: {ptype_str}):\n")
    out.write(f'{istr1}self.set_property_state("{pname}", value)\n')


def _write_cls_helper(out, cls, indent=0):
    try:
        istr = _get_indent_str(indent)
        istr1 = _get_indent_str(indent + 1)
        istr2 = _get_indent_str(indent + 2)
        out.write("\n")
        out.write(
            f"{istr}class {cls.__name__}"
            f'({", ".join(c.__name__ for c in cls.__bases__)}):\n'
        )

        doc = ("\n" + istr1).join(cls.__doc__.split("\n"))
        out.write(f'{istr1}"""\n')
        out.write(f"{istr1}{doc}")
        out.write(f'\n{istr1}"""\n\n')
        out.write(f'{istr1}syc_name = "{cls.syc_name}"\n')

        def write_list_attr(attr_name, items):
            out.write(f"{istr1}{attr_name} = \\\n")
            strout = io.StringIO()
            pprint.pprint(
                items, stream=strout, compact=True, width=80 - indent * 4 - 10
            )
            mn = ("\n" + istr2).join(
                strout.getvalue().strip().replace("'", '"').split("\n")
            )
            out.write(f"{istr2}{mn}\n")

        child_names = getattr(cls, "child_names", None)
        if child_names:
            write_list_attr("child_names", child_names)
            for child in child_names:
                _write_cls_helper(out, getattr(cls, child), indent + 1)

        property_names_types = getattr(cls, "property_names_types", None)
        if property_names_types:
            names_types = [
                (nm, sycnm, typ.__name__) for nm, sycnm, typ in property_names_types
            ]
            write_list_attr("property_names_types", names_types)
            for prop_name, _, prop_type in names_types:
                doc = getattr(cls, prop_name).__doc__
                _write_property_helper(out, prop_name, prop_type, doc, indent + 1)

        command_names = getattr(cls, "command_names", None)
        if command_names:
            write_list_attr("command_names", command_names)
            for command in command_names:
                _write_cls_helper(out, getattr(cls, command), indent + 1)

        arguments = getattr(cls, "argument_names", None)
        if arguments:
            write_list_attr("argument_names", arguments)

            essential_args = getattr(cls, "essential_arguments", [])
            write_list_attr("essential_arguments", essential_args)

            for argument in arguments:
                _write_cls_helper(out, getattr(cls, argument), indent + 1)
        child_object_type = getattr(cls, "child_object_type", None)
        if child_object_type:
            _write_cls_helper(out, child_object_type, indent + 1)
    except Exception:
        raise


def write_settings_classes(out: IO, cls, obj_info):
    """
    Write the settings classes in 'out' stream.

    Parameters
    ----------
    out:     Stream
    """
    hash = _gethash(obj_info)
    out.write('"""This is an auto-generated file.  DO NOT EDIT!"""\n')
    out.write("\n")
    out.write("from ansys.systemcoupling.core.settings.datamodel import *\n\n")
    out.write(f'SHASH = "{hash}"\n')
    _write_cls_helper(out, cls)


def write_classes_to_file(filepath, obj_info, root_type="SystemCoupling"):
    cls = datamodel.get_cls(root_type, obj_info[root_type])
    with open(filepath, "w") as f:
        write_settings_classes(f, cls, obj_info)
    print(f"Finished generating {filepath}")


def _make_combined_metadata(dm_metadata, cmd_metadata, is_test_data=False):
    metadata = deepcopy(dm_metadata)
    cmd_meta = deepcopy(
        process_command_data(cmd_metadata, apply_exclusions=not is_test_data)
    )
    metadata["SystemCoupling"]["__commands"] = cmd_meta
    return metadata


def _generate_test_classes(dirname):
    # NB need to add tests dir to sys.path to find dm_raw_metadata
    sys.path.append(os.path.normpath(os.path.join(dirname, "..", "tests")))

    from dm_raw_metadata import cmd_metadata, dm_metadata

    dm_metadata = _make_combined_metadata(dm_metadata, cmd_metadata, is_test_data=True)

    filepath = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "tests",
            "generated_testing_datamodel.py",
        )
    )
    write_classes_to_file(filepath, dm_metadata)


def _generate_real_classes(dirname):
    import ansys.systemcoupling.core as pysyc

    syc = pysyc.launch()
    print("helper instance of syc successfully launched. Querying metadata...")
    api = syc.native_api

    dm_metadata = api.GetMetadata()
    cmd_metadata_orig = api.GetCommandAndQueryMetadata()
    print("...raw metadata received. Processing...")

    dm_metadata = _make_combined_metadata(dm_metadata, cmd_metadata_orig)

    filedir = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "ansys",
            "systemcoupling",
            "core",
            "settings",
            "v231",
        )
    )

    filepath = os.path.join(filedir, "setup.py")
    write_classes_to_file(filepath, dm_metadata)

    for category in ("case", "solution"):
        cat_cmd_metadata = process_command_data(cmd_metadata_orig, category=category)
        root_type = category.title() + "Commands"
        cat_metadata = {
            root_type: {
                "__commands": cat_cmd_metadata,
                "isEntity": False,
                "isNamed": False,
                "ordinal": 0,
            }
        }
        filepath = os.path.join(filedir, f"{category}.py")
        write_classes_to_file(filepath, cat_metadata, root_type=root_type)


if __name__ == "__main__":

    dirname = os.path.dirname(__file__)

    use_test_data = len(sys.argv) > 1 and sys.argv[1] == "-t"
    if use_test_data:
        _generate_test_classes(dirname)
    else:
        _generate_real_classes(dirname)
