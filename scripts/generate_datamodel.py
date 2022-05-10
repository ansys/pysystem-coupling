"""
Provide a module to generate the Fluent settings tree.

Running this module generates a python module with the definition of the Fluent
settings classes. The out is placed at:

- ansys/fluent/core/solver/settings.py

Running this module requires Fluent to be installed.

Usage
-----
python <path to settingsgen.py>
"""

import io
import json
import os
import pprint
import sys
from typing import IO

from ansys.systemcoupling.core.settings import datamodel
from ansys.systemcoupling.core.settings.process_command_data import (
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

        child_names = getattr(cls, "child_names", None)
        if child_names:
            out.write(f"{istr1}child_names = \\\n")
            strout = io.StringIO()
            pprint.pprint(
                child_names, stream=strout, compact=True, width=80 - indent * 4 - 10
            )
            mn = ("\n" + istr2).join(
                strout.getvalue().strip().replace("'", '"').split("\n")
            )
            out.write(f"{istr2}{mn}\n")
            for child in child_names:
                _write_cls_helper(out, getattr(cls, child), indent + 1)

        property_names_types = getattr(cls, "property_names_types", None)
        if property_names_types:
            out.write(f"{istr1}property_names_types = \\\n")
            strout = io.StringIO()
            names_types = [
                (nm, sycnm, typ.__name__) for nm, sycnm, typ in property_names_types
            ]
            pprint.pprint(
                names_types, stream=strout, compact=True, width=80 - indent * 4 - 10
            )
            mn = ("\n" + istr2).join(
                strout.getvalue().strip().replace("'", '"').split("\n")
            )
            out.write(f"{istr2}{mn}\n")
            for prop_name, _, prop_type in names_types:
                doc = getattr(cls, prop_name).__doc__
                _write_property_helper(out, prop_name, prop_type, doc, indent + 1)

        command_names = getattr(cls, "command_names", None)
        if command_names:
            out.write(f"{istr1}command_names = \\\n")
            strout = io.StringIO()
            pprint.pprint(
                command_names, stream=strout, compact=True, width=80 - indent * 4 - 10
            )
            mn = ("\n" + istr2).join(
                strout.getvalue().strip().replace("'", '"').split("\n")
            )
            out.write(f"{istr2}{mn}\n")
            for command in command_names:
                _write_cls_helper(out, getattr(cls, command), indent + 1)

        arguments = getattr(cls, "argument_names", None)
        if arguments:
            out.write(f"{istr1}argument_names = \\\n")
            strout = io.StringIO()
            pprint.pprint(
                arguments, stream=strout, compact=True, width=80 - indent * 4 - 10
            )
            mn = ("\n" + istr2).join(
                strout.getvalue().strip().replace("'", '"').split("\n")
            )
            out.write(f"{istr2}{mn}\n")
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
    flproxy: Proxy
             Object that interfaces with the Fluent backend
    """
    hash = _gethash(obj_info)
    out.write('"""This is an auto-generated file.  DO NOT EDIT!"""\n')
    out.write("\n")
    out.write("from ansys.systemcoupling.core.settings.datamodel import *\n\n")
    out.write(f'SHASH = "{hash}"\n')
    _write_cls_helper(out, cls)


if __name__ == "__main__":

    use_test_data = len(sys.argv) > 1 and sys.argv[1] == "-t"

    dirname = os.path.dirname(__file__)

    rawcmd_file = os.path.normpath(
        os.path.join(dirname, "temp_data", "command_meta.json")
    )

    proccmd_file = os.path.normpath(
        os.path.join(dirname, "temp_data", "command_meta_proc.json")
    )

    with open(rawcmd_file, "r") as f:
        cmd_data = json.load(fp=f)

    proccmd_data = process_command_data(cmd_data)

    with open(proccmd_file, "w") as f:
        json.dump(proccmd_data, fp=f, indent=2, sort_keys=True)

    # TODO: launch syc itself to obtain settings - see how Fluent does it
    # For now, using a hard coded data set
    # NB need to add tests dir to PYTHONPATH to find dm_raw_metadata
    from dm_raw_metadata import dm_metadata

    # filepath = os.path.normpath(
    #     os.path.join(
    #         dirname,
    #         "..",
    #         "ansys",
    #         "systemcoupling",
    #         "core",
    #         "settings",
    #         "datamodel_222.py",
    #     )
    # )
    filepath = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "tests",
            "generated_testing_datamodel.py",
        )
    )
    cls = datamodel.get_cls("SystemCoupling", dm_metadata["SystemCoupling"])
    with open(filepath, "w") as f:
        write_settings_classes(f, cls, dm_metadata)
