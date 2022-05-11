"""
Script to generate the System Coupling settings tree.

This generates a python module with the definition of the System Coupling
data model settings classes. The module is placed at:

- ansys/systemcoupling/core/solver/settings/datamodel_222.py

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
    """
    hash = _gethash(obj_info)
    out.write('"""This is an auto-generated file.  DO NOT EDIT!"""\n')
    out.write("\n")
    out.write("from ansys.systemcoupling.core.settings.datamodel import *\n\n")
    out.write(f'SHASH = "{hash}"\n')
    _write_cls_helper(out, cls)


if __name__ == "__main__":

    dirname = os.path.dirname(__file__)

    use_test_data = len(sys.argv) > 1 and sys.argv[1] == "-t"

    if use_test_data:
        # NB need to add tests dir to sys.path to find dm_raw_metadata
        sys.path.append(os.path.normpath(os.path.join(dirname, "..", "tests")))

        from dm_raw_metadata import dm_metadata_with_cmds as dm_metadata

        filepath = os.path.normpath(
            os.path.join(
                dirname,
                "..",
                "tests",
                "generated_testing_datamodel.py",
            )
        )
    else:
        import ansys.systemcoupling.core as pysyc

        syc = pysyc.launch()
        print("helper instance of syc successfully launched. Querying metadata...")
        api = syc.native_api

        dm_metadata = api.GetMetadata()
        cmd_metadata = api.GetCommandAndQueryMetadata()
        print("...raw metadata received. Processing...")

        cmd_metadata = process_command_data(cmd_metadata)
        dm_metadata["SystemCoupling"]["__commands"] = cmd_metadata

        filepath = os.path.normpath(
            os.path.join(
                dirname,
                "..",
                "ansys",
                "systemcoupling",
                "core",
                "settings",
                "datamodel_222.py",
            )
        )

    # with open("dump_meta.json", "w") as f:
    #    json.dump(dm_metadata, fp=f, indent=2, sort_keys=True)

    cls = datamodel.get_cls("SystemCoupling", dm_metadata["SystemCoupling"])
    with open(filepath, "w") as f:
        write_settings_classes(f, cls, dm_metadata)
    print(f"Finished generating {filepath}")
