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

"""Source of adaptor API "root" classes and related functionality.

At runtime, the key function provided here is ``get_root``. This
returns a ``Container`` instance for the requested API root based
on queries to the System Coupling server. The default assumption in
normal use is that this returns a concrete class that forms
part of the PySystemCoupling package, which at some point was generated
based on metadata queried from the current version of System Coupling.

The API classes are generated at *build time* by a script that calls
another function from this module, ``get_cls``. This takes the metadata
queried from the System Coupling server and constructs the classes in memory
using Python facilities. The classes are then effectively *serialized*
by writing out their definitions based on the in-memory objects to Python
module files.

If, at runtime, it is determined that the server is a different version
from the one used to generate the API classes, the ``get_root`` function falls back
to using the ``get_cls`` method. In this case, instead of providing the *out of sync*
pre-generated classes, runtime classes that are consistent with the System Coupling
server are constructed and returned.
"""

import hashlib
import importlib
import json
from types import ModuleType
from typing import Callable

from ansys.systemcoupling.core.adaptor.impl.types import *  # noqa: F403
from ansys.systemcoupling.core.util.logging import LOG

from .syc_proxy_interface import SycProxyInterface

# Data model property types defined as primitive types/type hint names
_property_types = {
    "Integer": int,
    "Logical": bool,
    "Real": "RealType",
    "String": str,
    "Real List": "RealListType",
    "Real Triplet": "RealVectorType",
    "String List": "StringListType",
}

# Command arguments still defined as settings classes
_arg_types = {
    "ParticipantSession": ParticipantSession,
    "Integer": Integer,
    "Logical": Boolean,
    "Real": Real,
    "String": String,
    "Real List": RealList,
    "Real Triplet": RealVector,
    "String List": StringList,
    "StrFloatPairList": StrFloatPairList,
    "StrOrIntDictList": StrOrIntDictList,
    "StrOrIntDictListDict": StrOrIntDictListDict,
}


def _get_property_type(id, info):
    data_type = info.get("type", None)
    try:
        t = _property_types[data_type]
        return t if isinstance(t, str) else t.__name__
    except AttributeError:
        print(
            f"AttributeError occuured in property type = {_property_types[data_type]}."
        )
        raise
    except KeyError:
        raise RuntimeError(f"Property '{id}' type, '{data_type}' is not known.")


def _get_type(id, info):
    if id == "child_object_type":
        return Container
    data_type = info.get("type", None)

    if data_type is None:
        if "isQuery" in info:
            # looks like a *Command
            if info["isPathCommand"]:
                return PathCommand
            elif info["isInjected"]:
                return InjectedCommand
            else:
                return Command
        else:
            # assume Object or Singleton
            try:
                is_named = info["isNamed"]
            except:
                raise RuntimeError(f"Data model metadata for '{id}' is badly formed.")
            return NamedContainer if is_named else Container
    else:
        try:
            return _arg_types[data_type]
        except KeyError:
            raise RuntimeError(f"Property '{id}' type, '{data_type}', is not known.")


def get_cls(name: str, info: dict, parent=None):
    """Create a class for the object identified by ``name``.

    This is used both to construct classes during the API code
    generation phase and also at run time to generate an in-memory
    API representation in the case that the pre-generated version
    is determined to be out of date.
    """
    try:
        return _get_cls(name, info, parent)
    except Exception:
        LOG.error(
            f"Unable to construct class for '{name}' of "
            f"'{parent.syc_name if parent else None}'."
        )
        raise


def _indent_doc(indent, doc_str):
    doc = doc_str.split("\n")
    sep = f"\n{indent}"
    return indent + sep.join(doc)


def _get_cls(name, info, parent):
    if parent is None:
        pname = info.get("category_root", "root")
    elif "pysyc_name" in info:
        # Python name provided - for the case where there is a preferred
        # alternative to the default generated name.
        pname = info["pysyc_name"]
    else:
        pname = to_python_name(name)
    base = _get_type(name, info)
    dct = {"syc_name": name}
    if base == InjectedCommand:
        dct["cmd_name"] = pname
    helpinfo = info.get("help")
    if helpinfo:
        dct["__doc__"] = helpinfo
    else:
        if parent is None:
            dct["__doc__"] = "'root' object"
        else:
            # Assume commands always have helpinfo, so must be an object here.
            dct["__doc__"] = f"'{pname}' child."

    cls = type(pname, (base,), dct)

    children = info.get("__children")
    parameters = info.get("__parameters")
    if base == NamedContainer:
        children = parameters = None

    def unique_name(base_name, existing_names):
        # TODO: this was new in Fluent; related to flattening changes, but
        # it is not entirely clear when we would see non-unique children and
        # whether this is really needed.
        candidate_name = base_name
        i = 0
        while candidate_name in existing_names:
            i += 1
            candidate_name = f"{base_name}_{i}"
        return candidate_name

    if children:
        child_keys = sorted(children.keys(), key=lambda c: children[c]["ordinal"])
        cls.child_names = []
        for cname in child_keys:
            cinfo = children[cname]
            ccls = get_cls(cname, cinfo, cls)
            ccls.__name__ = unique_name(ccls.__name__, cls.child_names)
            # pylint: disable=no-member
            cls.child_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)

    if parameters:
        prop_keys = sorted(parameters.keys(), key=lambda p: parameters[p]["ordinal"])
        cls.property_names_types = []
        for prname in prop_keys:
            sycname = prname
            prinfo = parameters[sycname]
            prname = prinfo.get("py_sycname") or to_python_name(prname)
            prtype = _get_property_type(prname, prinfo)
            docstr_default = f"'{prname}' property of '{parent.__name__}' object"
            docstr = prinfo.get("help", docstr_default)
            setattr(
                cls,
                prname,
                property(
                    # NB: the prname defaults are needed to force capture.
                    #     For information, see StackOverflow Q 2295290.
                    fget=lambda slf, prname=prname: slf.get_property_state(prname),
                    fset=lambda slf, val, prname=prname: slf.set_property_state(
                        prname, val
                    ),
                    doc=docstr,
                ),
            )
            cls.property_names_types.append((prname, sycname, prtype))

    commands = info.get("__commands")
    if commands:
        cls.command_names = []
        for cname, cinfo in commands.items():
            ccls = get_cls(cname, cinfo, cls)
            ccls.__name__ = unique_name(ccls.__name__, cls.command_names)
            # pylint: disable=no-member
            cls.command_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)
        cls.command_names.sort()

    arguments = info.get("args")
    if arguments:
        doc = cls.__doc__
        doc += "\n\n"
        doc += "Parameters\n"
        doc += "----------\n"
        cls.argument_names = []
        # essential arg names are native SyC names
        essential_args = info.get("essentialArgs", [])
        for aname, ainfo in arguments:
            if aname == "ObjectPath":
                continue
            ccls = get_cls(aname, ainfo, cls)
            th = ccls._state_type
            th = th.__name__ if hasattr(th, "__name__") else str(th)
            optional_sfx = "" if aname in essential_args else ", optional"
            arg_indent = "    "
            doc += f"{ccls.__name__} : {th}{optional_sfx}\n"
            doc += f"{_indent_doc(arg_indent, ccls.__doc__)}\n"
            ccls.__name__ = unique_name(ccls.__name__, cls.argument_names)
            # pylint: disable=no-member
            cls.argument_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)
        cls.__doc__ = doc
        cls.essential_arguments = [
            to_python_name(a) for a in info.get("essentialArgs", [])
        ]

    # object_type = info.get('object-type')
    object_type = Container if base == NamedContainer else None
    if object_type:
        cls.child_object_type = get_cls("child_object_type", info, cls)

    return cls


def get_hash(obj_info):
    """Get hash for the metadata dictionary that is used in class generation."""
    dhash = hashlib.sha256()
    dhash.update(json.dumps(obj_info, sort_keys=True).encode())
    return dhash.hexdigest()


def get_root(
    sycproxy: SycProxyInterface,
    category: str = "setup",
    version: str = None,
    generated_module: ModuleType = None,
    report_whether_dynamic_classes_created: Callable[[bool], None] = lambda _: None,
) -> Container:
    """Get a root API adaptor object for the requested category.

    Parameters
    ----------
    sycproxy: SycProxyInterface
            Object that interfaces with the System Coupling backend.
    category: str, optional
            Category of the API that this root refers to. The default
            is ``"setup"``.
    version: str, optional
            Version of the API that this root refers to. The default is ``None``.
    generated_module: module, optional
            Alternative pre-generated module to use instead in place of the
            default one. The default is ``None``. This parameter exists to
            support unit testing.
    report_whether_dynamic_classes_created: callable, optional
            Whether to report if dynamic classes were created. The default is
            ``True``. If ``False``, the pre-existing module is used. The former
            happens if the static information provided by the proxy
            does not match the hash of the pre-existing module. (This parameter
            exists to support unit testing.)

    Returns
    -------
    Root ``Container`` object.
    """
    obj_info, root_type = sycproxy.get_static_info(category)
    try:
        if generated_module is None:
            api_ver = f"api_{version}" if version else "api"
            generated_module = importlib.import_module(
                f"ansys.systemcoupling.core.adaptor.{api_ver}.{category}_root"
            )

        info_hash = get_hash(obj_info)
        if generated_module.SHASH == info_hash:
            LOG.debug("Using pre-generated datamodel classes.")
        else:
            LOG.warning(
                "Mismatch exists between generated file and server object "
                "information. Dynamically created settings classes will "
                "be used."
            )
            raise RuntimeError("Mismatch exists in hash values.")
        cls = getattr(generated_module, f"{category}_root")
        report_whether_dynamic_classes_created(False)
    except Exception:
        cls = get_cls(root_type, obj_info[root_type])
        report_whether_dynamic_classes_created(True)
    # pylint: disable=no-member
    cls.set_sycproxy(sycproxy)
    return cls()
