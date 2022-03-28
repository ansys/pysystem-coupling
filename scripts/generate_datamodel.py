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

import hashlib
#import imp
import io
import os
import pickle
import pprint
from typing import IO
from ansys.systemcoupling.core.settings import datamodel

def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()

def _get_indent_str(indent):
    return f"{' '*indent*4}"

def _write_property_helper(out, pname, ptype_str, doc_str, indent=0):
    istr = _get_indent_str(indent)
    istr1 = _get_indent_str(indent+1)
    out.write("\n")
    out.write(f"{istr}@property\n")
    out.write(f"{istr}def {pname}(self) -> {ptype_str}:\n")
    out.write(f'{istr1}"""{doc_str}"""\n')
    out.write(f"{istr1}return self.get_property_state('{pname}')\n")
    out.write("\n")
    out.write(f"{istr}@{pname}.setter\n")
    out.write(f"{istr}def {pname}(self, value: {ptype_str}):\n")
    out.write(f"{istr1}self.set_property_state('{pname}', value)\n")

def _write_cls_helper(out, cls, indent = 0):
    try:
        istr = _get_indent_str(indent)
        istr1 = _get_indent_str(indent+1)
        istr2 = _get_indent_str(indent+2)
        out.write('\n')
        out.write(f'{istr}class {cls.__name__}'
                   f'({", ".join(c.__name__ for c in cls.__bases__)}):\n')

        doc = ('\n' + istr1).join(cls.__doc__.split('\n'))
        out.write(f'{istr1}"""\n')
        out.write(f'{istr1}{doc}')
        out.write(f'\n{istr1}"""\n')
        out.write(f'{istr1}syc_name = "{cls.syc_name}"\n')

        child_names = getattr(cls, 'child_names', None)
        if child_names:
            out.write(f'{istr1}child_names = \\\n')
            strout = io.StringIO()
            pprint.pprint(child_names, stream=strout, compact=True,
                    width=80-indent*4-10)
            #out.write(f'{istr1}child_names_set = set({cls.__name__}.child_names)')
            mn = ('\n' + istr2).join(strout.getvalue().strip().split('\n'))
            out.write(f'{istr2}{mn}\n')
            for child in child_names:
                _write_cls_helper(out, getattr(cls, child), indent+1)
            

        property_names_types = getattr(cls, 'property_names_types', None)
        if property_names_types:
            out.write(f'{istr1}property_names_types = \\\n')
            strout = io.StringIO()
            names_types = [(nm, sycn, typ.__name__) 
                           for nm, sycn, typ in property_names_types]
            pprint.pprint(names_types, stream=strout, compact=True,
                    width=80-indent*4-10)
            mn = ('\n' + istr2).join(strout.getvalue().strip().split('\n'))
            out.write(f'{istr2}{mn}\n')
            for prop_name, _, prop_type in names_types:
                doc = getattr(cls, prop_name).__doc__
                _write_property_helper(out, prop_name, prop_type, doc, indent+1)

        command_names = getattr(cls, 'command_names', None)
        if command_names:
            out.write(f'{istr1}command_names = \\\n')
            strout = io.StringIO()
            pprint.pprint(command_names, stream=strout, compact=True,
                    width=80-indent*4-10)
            mn = ('\n' + istr2).join(strout.getvalue().strip().split('\n'))
            out.write(f'{istr2}{mn}\n')
            for command in command_names:
                _write_cls_helper(out, getattr(cls, command), indent+1)

        arguments = getattr(cls, 'argument_names', None)
        if arguments:
            out.write(f'{istr1}argument_names = \\\n')
            strout = io.StringIO()
            pprint.pprint(arguments, stream=strout, compact=True,
                    width=80-indent*4-10)
            mn = ('\n' + istr2).join(strout.getvalue().strip().split('\n'))
            out.write(f'{istr2}{mn}\n')
            for argument in arguments:
                _write_cls_helper(out, getattr(cls, argument), indent+1)
        child_object_type = getattr(cls, 'child_object_type', None)
        if child_object_type:
            _write_cls_helper(out, child_object_type, indent+1)
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
    out.write('from ansys.systemcoupling.core.settings.datamodel import *\n\n')
    out.write(f'SHASH = "{hash}"\n')
    _write_cls_helper(out, cls)

if __name__ == '__main__':
    #from ansys.fluent.core.launcher.launcher import launch_fluent
    from dm_meta_rawdata import dm_meta_testing_raw_data
    dirname = os.path.dirname(__file__)
    filepath = os.path.normpath(
            os.path.join(dirname, "..", "ansys", "systemcoupling", "core",
                "settings", "datamodel222_v2.py")
            )
    #session = launch_fluent()
    #sinfo = session.get_settings_service().get_static_info()
    cls = datamodel.get_cls('SystemCoupling', dm_meta_testing_raw_data['SystemCoupling']);
    with open(filepath, 'w') as f:
        write_settings_classes(f, cls, dm_meta_testing_raw_data)
