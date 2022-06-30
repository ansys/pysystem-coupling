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
import os
import pprint
import sys
from typing import IO

import black

# Allows us to run pysystemcoupling from source without setting PYTHONPATH
_dirname = os.path.dirname(__file__)
sys.path.append(os.path.normpath(os.path.join(_dirname, "..")))

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import LOG
from ansys.systemcoupling.core.settings import datamodel
from ansys.systemcoupling.core.settings.command_data import (
    process as process_command_data,
)
from ansys.systemcoupling.core.syc_proxy_adapter import get_cmd_metadata

hash_dict = {}
files_dict = {}


def _gethash(obj_info):
    return datamodel._gethash(obj_info)


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _gather_hashes(name, info, cls, is_named_child=False):

    # print(name)
    # For named objects we visit the info twice - once for the
    # parent container, and once for the contained child. The latter
    # is what contains the object structure
    keep_info = None
    if info.get("isNamed") and not is_named_child:
        # This is the container
        keep_info = info
        info = {}

    children = info.get("__children")
    if children:
        children_hash = []
        for cname, cinfo in children.items():
            for child in getattr(cls, "child_names", None):
                child_cls = getattr(cls, child)
                if cname == child_cls.syc_name:
                    children_hash.append(_gather_hashes(cname, cinfo, child_cls))
                    break
    else:
        children_hash = None

    parameters = info.get("__parameters")
    if parameters:
        parameters_hash = []
        for pname, pinfo in parameters.items():
            parameters_hash.append(_gather_hashes(pname, pinfo, None))
    else:
        parameters_hash = None

    commands = info.get("__commands")
    if commands:
        commands_hash = []
        for cname, cinfo in commands.items():
            for command in getattr(cls, "command_names", None):
                command_cls = getattr(cls, command)
                if cname == command_cls.syc_name:
                    commands_hash.append(_gather_hashes(cname, cinfo, command_cls))
                    break
    else:
        commands_hash = None

    arguments = info.get("args")
    if arguments:
        arguments_hash = []
        for aname, ainfo in arguments:
            for argument in getattr(cls, "argument_names", None):
                argument_cls = getattr(cls, argument)
                if aname == argument_cls.syc_name:
                    arguments_hash.append(_gather_hashes(aname, ainfo, argument_cls))
                    break
    else:
        arguments_hash = None

    if keep_info:
        info = keep_info

    if info.get("isNamed") and not is_named_child:
        is_named_child = True
        object_hash = _gather_hashes(
            "child-object-type",
            info,
            getattr(cls, "child_object_type", None),
            is_named_child,
        )
    else:
        object_hash = None

    cls_tuple = (
        name,
        info.get("type"),
        info.get("help"),
        children_hash,
        parameters_hash,
        commands_hash,
        arguments_hash,
        object_hash,
    )
    hash = _gethash(cls_tuple)
    if not hash_dict.get(hash):
        hash_dict[hash] = (
            cls,
            children_hash,
            parameters_hash,
            commands_hash,
            arguments_hash,
            object_hash,
        )
    return hash


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


def _write_list_attr(out, attr_name, items):
    indent = 1
    istr1 = _get_indent_str(indent)
    istr2 = _get_indent_str(indent + 1)
    out.write(f"{istr1}{attr_name} = \\\n")
    strout = io.StringIO()
    pprint.pprint(items, stream=strout, compact=True, width=80 - indent * 4 - 10)
    mn = ("\n" + istr2).join(strout.getvalue().strip().replace("'", '"').split("\n"))
    out.write(f"{istr2}{mn}\n")


def _write_flat_class_files(parent_dir, root_classname, root_hash):
    istr = _get_indent_str(0)
    istr1 = _get_indent_str(1)
    istr2 = _get_indent_str(2)
    files = []
    # generate files
    for key, (
        cls,
        children_hash,
        parameters_hash,
        commands_hash,
        arguments_hash,
        object_hash,
    ) in hash_dict.items():
        if cls is None:
            # parameter - doesn't get its own class
            continue
        cls_name = file_name = cls.__name__
        if cls_name == "child_object_type":
            # Get the first parent for this class.
            for (
                cls1,
                children_hash1,
                parameters_hash1,
                commands_hash1,
                arguments_hash1,
                object_hash1,
            ) in hash_dict.values():
                if key == object_hash1:
                    cls.__name__ = file_name = cls1.__name__ + "_child"
                    break
        i = 0
        base_file_name = file_name
        while file_name in files:
            i += 1
            file_name = f"{base_file_name}_{i}"
        files.append(file_name)
        files_dict[key] = file_name

        file_name += ".py"
        filepath = os.path.normpath(os.path.join(parent_dir, file_name))
        with open(filepath, "w") as f:
            f.write(f"name: {cls_name}")

    # populate files
    for key, (
        cls,
        children_hash,
        parameters_hash,
        commands_hash,
        arguments_hash,
        object_hash,
    ) in hash_dict.items():
        if cls is None:
            # parameter
            continue
        file_name = files_dict.get(key)
        cls_name = cls.__name__
        filepath = os.path.normpath(os.path.join(parent_dir, file_name + ".py"))
        with open(filepath, "w") as f:
            if file_name.endswith("root"):
                print(f"writing  {file_name}  (cls_name = {cls_name}")
            # disclaimer to py file
            f.write("#\n")
            f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
            f.write("#\n")
            f.write("\n")
            if cls_name == root_classname:
                print("writing hash for", file_name)
                f.write(f"SHASH = {root_hash}\n\n")

            # write imports to py file
            f.write("from ansys.systemcoupling.core.settings.datamodel import *\n\n")
            if children_hash:
                for child in children_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(f"from .{files_dict.get(child)} import {pchild_name}\n")

            if commands_hash:
                for child in commands_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(f"from .{files_dict.get(child)} import {pchild_name}\n")

            if arguments_hash:
                for child in arguments_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(f"from .{files_dict.get(child)} import {pchild_name}\n")

            if object_hash:
                pchild_name = hash_dict.get(object_hash)[0].__name__
                f.write(f"from .{files_dict.get(object_hash)} import {pchild_name}\n\n")

            # class name
            bases_gen = (
                f"{c.__name__}[{hash_dict.get(object_hash)[0].__name__}]"
                if object_hash
                else c.__name__
                for c in cls.__bases__
            )
            f.write(f"{istr}class {cls_name}" f'({", ".join(bases_gen)}):\n')

            doc = cls.__doc__
            # Custom doc for child object type
            if cls.syc_name == "child-object-type":
                doc = f"'child_object_type' of {file_name[: file_name.find('_child')]}."

            doc = ("\n" + istr1).join(doc.split("\n"))
            f.write(f'{istr1}"""\n')
            f.write(f"{istr1}{doc}")
            f.write(f'\n{istr1}"""\n\n')
            f.write(f'{istr1}syc_name = "{cls.syc_name}"\n\n')

            # write children objects
            child_names = getattr(cls, "child_names", None)
            if child_names:
                f.write(f"{istr1}child_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(child_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for child in child_names:
                    f.write(f"{istr1}{child}: {child} = {child}\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{child} child of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            property_names_types = getattr(cls, "property_names_types", None)
            if property_names_types:
                names_types = [
                    (nm, sycnm, typ) for nm, sycnm, typ in property_names_types
                ]
                _write_list_attr(f, "property_names_types", names_types)
                for prop_name, _, prop_type in names_types:
                    doc = getattr(cls, prop_name).__doc__
                    _write_property_helper(f, prop_name, prop_type, doc, 1)

            # write command objects
            command_names = getattr(cls, "command_names", None)
            if command_names:
                f.write(f"{istr1}command_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(command_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for command in command_names:
                    f.write(f"{istr1}{command}: {command} = {command}\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{command} command of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            # write arguments
            arguments = getattr(cls, "argument_names", None)
            if arguments:
                f.write(f"{istr1}argument_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(arguments, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for argument in arguments:
                    f.write(f"{istr1}{argument}: {argument} = {argument}\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{argument} argument of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            # write object type
            child_object_type = getattr(cls, "child_object_type", None)
            if child_object_type:
                f.write(f"{istr1}child_object_type: {pchild_name} = {pchild_name}\n")
                f.write(f'{istr1}"""\n')
                f.write(f"{istr1}child_object_type of {cls_name}.")
                f.write(f'\n{istr1}"""\n')


def _write_init_file(parent_dir, sinfo):
    hash = _gethash(sinfo)
    filepath = os.path.normpath(os.path.join(parent_dir, "__init__.py"))
    with open(filepath, "w") as f:
        f.write("#\n")
        f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
        f.write("#\n")
        f.write("\n")
        f.write(f'"""A package providing the System Coupling API in Python."""')
        f.write("\n")
        f.write("from ansys.systemcoupling.core.settings.datamodel import *\n\n")
        f.write(f'SHASH = "{hash}"\n')
        f.write(f"from .{root_class_path} import root")


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
            names_types = [(nm, sycnm, typ) for nm, sycnm, typ in property_names_types]
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

    parent_dir = os.path.dirname(filepath)
    parent_dir = os.path.join(parent_dir, "tmp_flat")

    hash_dict.clear()
    files_dict.clear()

    # Disable for now
    # _gather_hashes("", obj_info[root_type], cls)
    # _write_flat_class_files(parent_dir, cls.__name__, _gethash(obj_info[root_type]))
    # _write_init_file(parent_dir, obj_info)

    with io.StringIO() as out:
        write_settings_classes(out, cls, obj_info)
        content = out.getvalue()

    # Experimental: run black on generated classes

    # Prior to this change, every time the files were regenerated
    # the previous black changes applied on commit were lost so
    # the differences appeared greater than they were.
    # The two options to deal with this are to disable black on
    # the generated classes (like on the proto files) or apply
    # black formatting as part of the generation process, as here.

    # The rationale for adopting this approach is that these files
    # are more likely to be read as part of the source than are
    # proto files so there is some value in ensuring consistent
    # formatting.

    # we usually have log level as DEBUG here, but black generates a lot of output
    old_level = LOG.current_level
    LOG.set_level("WARNING")
    content = black.format_file_contents(
        content, fast=False, mode=black.Mode(preview=True)
    )
    LOG.set_level(old_level)

    with open(filepath, "w") as f:
        f.write(content)
    print(f"Finished generating {filepath}")


def _make_combined_metadata(dm_metadata, cmd_metadata, category):
    metadata = deepcopy(dm_metadata)
    cmd_meta = deepcopy(process_command_data(cmd_metadata, category=category))
    metadata["SystemCoupling"]["__commands"] = cmd_meta
    metadata["SystemCoupling"]["category_root"] = f"{category}_root"
    return metadata


def _generate_test_classes(dirname):
    # NB need to add tests dir to sys.path to find dm_raw_metadata
    sys.path.append(os.path.normpath(os.path.join(dirname, "..", "tests")))

    from dm_raw_metadata import cmd_metadata, dm_metadata

    dm_metadata = _make_combined_metadata(dm_metadata, cmd_metadata, category="setup")

    filepath = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "tests",
            "generated_data",
            "testing_datamodel.py",
        )
    )
    write_classes_to_file(filepath, dm_metadata)


def _generate_real_classes(dirname):

    LOG.log_to_stdout()
    LOG.set_level("DEBUG")
    syc = pysyc.launch()
    LOG.debug("Helper instance of syc successfully launched.")
    LOG.debug("Initialise 'native' API...")
    api = syc.native_api

    LOG.debug("Querying datamodel metadata...")
    dm_metadata = api.GetMetadata(json_ret=True)
    LOG.debug("Querying command metadata")
    cmd_metadata_orig = get_cmd_metadata(api)
    LOG.debug("Command metadata received. Processing...")

    dm_metadata = _make_combined_metadata(
        dm_metadata, cmd_metadata_orig, category="setup"
    )

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

    LOG.debug("Creating 'setup' classes.")
    filepath = os.path.join(filedir, "setup.py")
    write_classes_to_file(filepath, dm_metadata)

    for category in ("case", "solution"):
        LOG.debug(f"Processing '{category}' command data...")
        cat_cmd_metadata = process_command_data(cmd_metadata_orig, category=category)
        root_type = category.title() + "Commands"
        cat_metadata = {
            root_type: {
                "__commands": cat_cmd_metadata,
                "isEntity": False,
                "isNamed": False,
                "ordinal": 0,
                "category_root": f"{category}_root",
            }
        }
        LOG.debug(f"Creating '{category}' classes...")
        filepath = os.path.join(filedir, f"{category}.py")
        write_classes_to_file(filepath, cat_metadata, root_type=root_type)
    LOG.debug("All done.")


if __name__ == "__main__":

    if "SYSC_ROOT" not in os.environ:
        print(
            "*******************\nSYSC_ROOT is not set. Continuing, but this "
            "may not be correct.\n*******************"
        )

    dirname = os.path.dirname(__file__)

    use_test_data = len(sys.argv) > 1 and sys.argv[1] == "-t"
    if use_test_data:
        _generate_test_classes(dirname)
    else:
        _generate_real_classes(dirname)
