"""
Module for accessing and modifying hierarchy of System Coupling settings.

The only useful method is 'get_root' which returns the root object for
accessing System Coupling settings.

Child objects can be generally accessed/modified using attribute access.
Named child objects can be accessed/modified using index operator.

Primitive settings are accessed (get/set) as properties.

Calling an object will return its current value as a "state" dictionary.

Example
-------
r = flobject.get_root(proxy)
is_energy_on = r.setup.models.energy.enabled()
r.setup.models.energy.enabled = True
r.boundary_conditions.velocity_inlet['inlet'].vmag.constant = 20
"""
import collections
import hashlib
import importlib
import json
import keyword
import sys
from typing import Dict, Generic, List, NewType, Tuple, TypeVar, Union
import weakref

from ansys.systemcoupling.core.util import name_util
from ansys.systemcoupling.core.util.logging import LOG

# Type hints
RealType = NewType("real", Union[float, str])  # constant or expression
RealListType = List[RealType]
RealVectorType = Tuple[RealType, RealType, RealType]
IntListType = List[int]
StringListType = List[str]
BoolListType = List[bool]
PrimitiveStateType = Union[
    str, RealType, int, bool, RealListType, IntListType, StringListType, BoolListType
]
DictStateType = Dict[str, "StateType"]
ListStateType = List["StateType"]
StateType = Union[PrimitiveStateType, DictStateType, ListStateType]

# Special types for specific command arguments
StrFloatPairType = Tuple[str, float]
StrFloatPairListType = List[StrFloatPairType]
StrOrIntType = Union[str, int]
StrOrIntDictType = Dict[str, StrOrIntType]
StrOrIntDictListType = List[StrOrIntDictType]
StrOrIntDictListDictType = Dict[str, StrOrIntDictListType]


def to_python_name(syc_name: str) -> str:
    """Convert a native SyC name string to python variable name.

    Native names are camel case - we convert to snake case.
    """
    if not syc_name:
        return syc_name
    name = name_util.to_python_name(syc_name)
    while name in keyword.kwlist:
        name = name + "_"
    return name


class Base:
    """
    Base class for settings and command objects.

    Parameters
    ----------
    name : str
           name of the object if a child of named-object.
    parent: Base
           Object's parent.

    Attributes
    ----------
    sycproxy
    obj_name
    syc_name

    """

    _initialized = False

    def __init__(self, name: str = None, parent=None):
        self._parent = weakref.proxy(parent) if parent is not None else None
        if name is not None:
            self._name = name

    _sycproxy = None

    @classmethod
    def set_sycproxy(cls, sycproxy):
        """Set sycproxy object."""
        cls._sycproxy = sycproxy

    @property
    def sycproxy(self):
        """Proxy object.

        This is set at the root level, and accessed via parent for child
        classes.
        """
        if self._sycproxy is None:
            return self._parent.sycproxy
        return self._sycproxy

    _name = None
    syc_name = None
    _syc_pathsep = "/"

    @property
    def obj_name(self) -> str:
        """SystemCoupling name of this object.

        By default, this returns the object's static name. If the object is a
        named-object child, the object's name is returned.
        """
        if self._name is None:
            return self.syc_name
        return self._name

    @property
    def path(self) -> str:
        """Path of this object.

        Constructed from obj_name of self and path of parent.
        """
        if self._parent is None:
            return self.obj_name
        ppath = self._parent.path
        if not ppath:
            return self.obj_name
        return ppath + "/" + self.obj_name

    @property
    def syc_path(self) -> str:
        """Path of this object in native SystemCoupling form."""
        if self._parent is None:
            return "/" + self.syc_name
        ppath = self._parent.syc_path
        return ppath + self._parent._syc_pathsep + self.obj_name

    def get_attrs(self, attrs) -> DictStateType:
        return self.sycproxy.get_attrs(self.syc_path, attrs)

    def get_attr(self, attr) -> StateType:
        attrs = self.get_attrs([attr])
        if attr != "active?" and attrs.get("active?", True) is False:
            raise RuntimeError("Object is not active")
        return attrs[attr]

    def is_active(self) -> bool:
        """TODO: "active" settings are not currently identified."""
        return True


StateT = TypeVar("StateT")


class SettingsBase(Base, Generic[StateT]):
    """
    Base class for settings objects.

    Methods
    -------
    get_state()
        Return the current state of the object

    set_state(state)
        Set the state of the object
    """

    @classmethod
    def to_syc_keys(cls, value: StateT) -> StateT:
        """Convert value to have keys with native System Coupling names.

        This is overridden in Group and NamedObject classes.
        """
        return value

    @classmethod
    def to_python_keys(cls, value: StateT) -> StateT:
        """Convert value to have keys with python names.

        This is overridden in Group and NamedObject classes.
        """
        return value

    @classmethod
    def to_syc_name(cls, name: str) -> str:
        """Convert Python name native System Coupling identifier.

        This is overridden in Group and NamedObject classes.
        """
        return name

    @classmethod
    def to_python_name(cls, name: str) -> str:
        """Convert native System Coupling identifier to Python name.

        This is overridden in Group and NamedObject classes.
        """
        return name

    def __call__(self) -> StateT:
        """Alias for self.get_state."""
        return self.get_state()

    def get_state(self) -> StateT:
        """Get the state of this object."""
        return self.to_python_keys(self.sycproxy.get_state(self.syc_path))

    def set_state(self, state: StateT):
        """Set the state of this object."""
        return self.sycproxy.set_state(self.syc_path, self.to_syc_keys(state))

    def set_property_state(self, prop, value):
        self.set_state({prop: value})

    def get_property_state(self, prop):
        return self.sycproxy.get_state(self.syc_path + "/" + self.to_syc_name(prop))

    @staticmethod
    def _print_state_helper(state, out=sys.stdout, indent=0, indent_factor=2):
        if isinstance(state, dict):
            out.write("\n")
            for key, value in state.items():
                if value is not None:
                    out.write(f'{indent*indent_factor*" "}{key} : ')
                    SettingsBase._print_state_helper(
                        value, out, indent + 1, indent_factor
                    )
        elif isinstance(state, list):
            out.write("\n")
            for index, value in enumerate(state):
                out.write(f'{indent*indent_factor*" "}{index} : ')
                SettingsBase._print_state_helper(value, out, indent + 1, indent_factor)
        else:
            out.write(f"{state}\n")

    def print_state(self, out=sys.stdout, indent_factor=2):
        """Print the state of this object."""
        self._print_state_helper(self.get_state(), out, indent_factor=indent_factor)


class Integer(SettingsBase[int]):
    """An Integer object represents an integer value setting."""

    _state_type = int


class Real(SettingsBase[RealType]):
    """A Real object represents a real value setting.

    Some Real objects also accept string arguments representing expression
    values.
    """

    _state_type = RealType


class String(SettingsBase[str]):
    """A String object represents a string value setting."""

    _state_type = str


class Filename(SettingsBase[str]):
    """A Filename object represents a file name."""

    _state_type = str


class Boolean(SettingsBase[bool]):
    """A Boolean object represents a boolean value setting."""

    _state_type = bool


class RealList(SettingsBase[RealListType]):
    """A RealList object represents a real list setting."""

    _state_type = RealListType


class IntegerList(SettingsBase[IntListType]):
    """An Integer object represents a integer list setting."""

    _state_type = IntListType


class RealVector(SettingsBase[RealVectorType]):
    """An object to represent a 3D vector.

    A RealVector object represents a real vector setting consisting of
    3 real values.
    """

    _state_type = RealVectorType


class StringList(SettingsBase[StringListType]):
    """A StringList object represents a string list setting."""

    _state_type = StringListType


class BooleanList(SettingsBase[BoolListType]):
    """A BooleanList object represents a boolean list setting."""

    _state_type = BoolListType


class StrFloatPairList(SettingsBase[StrFloatPairListType]):
    """A StrFloatPairList object represents a list of string-float pairs."""

    _state_type = StrFloatPairListType


class StrOrIntDictList(SettingsBase[StrOrIntDictListType]):
    """A StrOrIntDictList object represents a list of simple dictionary values
    with string keys and string or int values."""

    _state_type = StrOrIntDictListType


class StrOrIntDictListDict(SettingsBase[StrOrIntDictListDictType]):
    """A StrOrIntDictListDict object represents a dictionary of string keys to
    StrOrIntDictList values."""

    _state_type = StrOrIntDictListDictType


class Group(SettingsBase[DictStateType]):
    """A Group container object.

    A Group object is a container similar to a C++ struct object. Child objects
    can be accessed via attribute access.

    Attributes
    ----------
    child_names: list[str]
                 Names of the child objects
    command_names: list[str]
                   Names of the commands
    """

    _state_type = DictStateType

    def __init__(self, name: str = None, parent=None):
        super().__init__(name, parent)
        for child in self.child_names:
            cls = getattr(self.__class__, child)
            setattr(self, child, cls(None, self))
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            setattr(self, cmd, cls(None, self))
        self._initialized = True

    @classmethod
    def to_syc_keys(cls, value):
        """Convert value to have keys with System Coupling names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                if k in cls.child_names:
                    ccls = getattr(cls, k)
                    ret[ccls.syc_name] = ccls.to_syc_keys(v)
                else:
                    ret[cls.to_syc_name(k)] = v
            return ret
        else:
            return value

    @classmethod
    def _syc_to_py_childmap(cls):
        if not hasattr(cls, "__s2p_childmap"):
            cls.__s2p_childmap = {}
            for pyname in cls.child_names:
                ccls = getattr(cls, pyname)
                cls.__s2p_childmap[ccls.syc_name] = pyname
        return cls.__s2p_childmap

    @classmethod
    def _syc_to_py_propertymap(cls):
        if not hasattr(cls, "__s2p_propertymap"):
            cls.__s2p_propertymap = {
                sycname: pyname for pyname, sycname, _ in cls.property_names_types
            }
        return cls.__s2p_propertymap

    @classmethod
    def to_python_keys(cls, value):
        """Convert value to have keys with python names."""
        if isinstance(value, collections.abc.Mapping):

            cmap = cls._syc_to_py_childmap()
            pmap = cls._syc_to_py_propertymap()

            ret = {}
            for k, v in value.items():
                pyname = cmap.get(k, None)
                if pyname:
                    ret[pyname] = getattr(cls, pyname).to_python_keys(v)
                else:
                    pyname = pmap.get(k, None)
                    if pyname:
                        # property => no need to procss v further
                        ret[pyname] = v
            return ret
        else:
            return value

    @classmethod
    def to_syc_name(cls, name: str) -> str:
        """Convert Python property name to native System Coupling name.

        This is overridden in Group and NamedObject classes.
        """
        for prop, sycprop, _ in cls.property_names_types:
            if prop == name:
                return sycprop
        raise RuntimeError(f"Key '{name}' is invalid")

    @classmethod
    def to_python_name(cls, name: str) -> str:
        """Convert native System Coupling property name to Python name.

        This is overridden in Group and NamedObject classes.
        """
        return cls._syc_to_py_propertymap()[name]

    child_names = []
    command_names = []
    property_names_types = []

    def get_active_child_names(self):
        """Names of children that are currently active."""
        ret = []
        for child in self.child_names:
            if getattr(self, child).is_active():
                ret.append(child)
        return ret

    def get_active_command_names(self):
        """Names of commands that are currently active."""
        ret = []
        for command in self.command_names:
            if getattr(self, command).is_active():
                ret.append(command)
        return ret

    def get_property_options(self, name: str) -> StringList:
        """Returns the currently available options for the specified property name.

        This function is applicable as follows:

        - May only be called for `String` and `StringList` properties; an
          exception will be thrown otherwise.

        - Should only be called for properties that are known currently to be
          active in the data model. This requirement is not yet enforced or validated
          but, if it is violated, the content of any value returned is unspecified.

        - Should only be called for properties that are known to be constrained
          to a certain list of allowed values. An empty list is returned in other
          cases.
        """
        syc_prop_name, prop_type = self._get_property_name_type(name, self.path)
        if prop_type not in ("String", "StringList"):
            raise RuntimeError(
                f"Options are not available for non-string type '{name}'."
            )
        return self.sycproxy.get_property_options(self.syc_path, syc_prop_name)

    def __getattribute__(self, name):
        if name in super().__getattribute__("child_names"):
            if not self.is_active():
                raise RuntimeError(f"'{self.path}' is currently not active")
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value):
        if not self._initialized or name[0] == "_":
            super().__setattr__(name, value)
        elif any(name == n for n, _, __ in self.property_names_types):
            super().__setattr__(name, value)
        else:
            attr = getattr(self, name)
            attr.set_state(value)

    @classmethod
    def _get_property_name_type(cls, name, path):
        for pname, syc_name, prop_type in cls.property_names_types:
            if pname == name:
                return (syc_name, prop_type)
        raise RuntimeError(f"'{name}' does not exist in '{path}'.")


ChildTypeT = TypeVar("ChildTypeT")


class NamedObject(SettingsBase[DictStateType], Generic[ChildTypeT]):
    """A NamedObject container.

    A NamedObject is a container object, similar to a Python dict object.
    Generally, many such objects can be created with different names.

    Attributes
    ----------
    command_names: list[str]
                   Names of the commands
    """

    _syc_pathsep = ":"

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name: str = None, parent=None):
        super().__init__(name, parent)
        self._objects = {}
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            setattr(self, cmd, cls(None, self))

    @classmethod
    def to_syc_keys(cls, value):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_syc_keys(v)
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_python_keys(v)
            return ret
        else:
            return value

    command_names = []

    def _create_child_object(self, cname: str):
        ret = self._objects.get(cname)
        if not ret:
            # pylint: disable=no-member
            cls = self.__class__.child_object_type
            ret = self._objects[cname] = cls(cname, self)
        return ret

    def _update_objects(self):
        names = self.get_object_names()
        for name in list(self._objects.keys()):
            if name not in names:
                del self._objects[name]
        for name in names:
            if name not in self._objects:
                self._create_child_object(name)

    def __delitem__(self, name: str):
        self.sycproxy.delete(self.syc_path, name)
        if name in self._objects:
            del self._objects[name]

    def __contains__(self, name: str):
        return name in self.get_object_names()

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        self._update_objects()
        return iter(self._objects)

    def keys(self):
        """Object names."""
        self._update_objects()
        return self._objects.keys()

    def values(self):
        """Object values."""
        self._update_objects()
        return self._objects.values()

    def items(self):
        """Items."""
        self._update_objects()
        return self._objects.items()

    def create(self, name: str):
        """Create a named object with given name.

        Parameters
        ----------
        name: str
              Name of new object

        Returns
        -------
        The object that has been created
        """
        self.sycproxy.create_named_object(self.syc_path, name)
        return self._create_child_object(name)

    def get_object_names(self):
        """Object names."""
        return self.sycproxy.get_object_names(self.syc_path)

    def __getitem__(self, name: str) -> ChildTypeT:
        if name not in self.get_object_names():
            raise KeyError(name)
        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            self.sycproxy.create_named_object(self.syc_path, name)
        child = self._objects.get(name)
        if not child:
            child = self._create_child_object(name)
        child.set_state(value)


class Command(Base):
    """Command object."""

    _is_path_cmd = False

    def __call__(self, **kwds):
        """Call a command with the specified keyword arguments."""
        newkwds = {}
        if self._is_path_cmd:
            newkwds["ObjectPath"] = self._parent.syc_path

        try:
            missing_args = set(self.essential_arguments)
            if self._is_path_cmd:
                missing_args.discard("object_path")
        except AttributeError:
            missing_args = set()

        for k, v in kwds.items():
            if k in self.argument_names:
                ccls = getattr(self, k)
                newkwds[ccls.syc_name] = ccls.to_syc_keys(v)
                missing_args.discard(k)
            else:
                raise RuntimeError("Argument '" + str(k) + "' is invalid")

        if missing_args:
            raise RuntimeError(
                "At least one essential argument has not been provided.\n"
                f"(Missing: {list(missing_args)})."
            )

        return self.sycproxy.execute_cmd(self._parent.path, self.obj_name, **newkwds)


class PathCommand(Command):
    """Path-based command object."""

    _is_path_cmd = True


_param_types = {
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


def _get_param_type(id, info):
    data_type = info.get("type", None)
    try:
        return _param_types[data_type].__name__
    except KeyError:
        raise RuntimeError(f"Property '{id}' type, '{data_type}', not known.")


def _get_type(id, info):
    if id == "child_object_type":
        return Group
    data_type = info.get("type", None)

    if data_type is None:
        if "isQuery" in info:
            # looks like a Command
            return PathCommand if info["isPathCommand"] else Command
        else:
            # assume Object or Singleton
            try:
                is_named = info["isNamed"]
            except:
                raise RuntimeError(f"Data model metadata for '{id}' is badly formed.")
            return NamedObject if is_named else Group
    else:
        try:
            return _param_types[data_type]
        except KeyError:
            raise RuntimeError(f"Property '{id}' type, '{data_type}', not known.")


def get_cls(name, info, parent=None):
    """Create a class for the object identified by "path"."""
    try:
        return _get_cls(name, info, parent)
    except Exception:
        LOG.error(
            f"Unable to construct class for '{name}' of "
            f"'{parent.syc_name if parent else None}'"
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
    if base == NamedObject:
        children = parameters = None

    def unique_name(base_name, existing_names):
        # TODO: this was new in Fluent; related to flattening changes, but
        # it is not entirely clear when we would see non-unique children and
        # whether this is really needed
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
            prname = to_python_name(prname)
            prinfo = parameters[sycname]
            prtype = _get_param_type(prname, prinfo)
            docstr = f"'{prname}' property of '{parent.__name__}' object"
            setattr(
                cls,
                prname,
                property(
                    # NB: the prname defaults are needed to force capture
                    #     StackOverflow Q 2295290 for details!
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

    arguments = info.get("args")
    if arguments:
        doc = cls.__doc__
        doc += "\n\n"
        doc += "Parameters\n"
        doc += "----------\n"
        cls.argument_names = []
        for aname, ainfo in arguments:
            if aname == "ObjectPath":
                continue
            ccls = get_cls(aname, ainfo, cls)
            th = ccls._state_type
            th = th.__name__ if hasattr(th, "__name__") else str(th)
            arg_indent = "    "
            doc += f"{arg_indent}{ccls.__name__} : {th}\n"
            doc += f"{_indent_doc(arg_indent * 2, ccls.__doc__)}\n"
            ccls.__name__ = unique_name(ccls.__name__, cls.argument_names)
            # pylint: disable=no-member
            cls.argument_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)
        cls.__doc__ = doc
        cls.essential_arguments = [
            to_python_name(a) for a in info.get("essentialArgs", [])
        ]

    # object_type = info.get('object-type')
    object_type = Group if base == NamedObject else None
    if object_type:
        cls.child_object_type = get_cls("child_object_type", info, cls)

    return cls


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(json.dumps(obj_info, sort_keys=True).encode())
    return dhash.hexdigest()


def get_root(
    sycproxy,
    category="setup",
    generated_module=None,
    report_whether_dynamic_classes_created=lambda _: None,
) -> Group:
    """
    Get the root settings object.

    Parameters
    ----------
    sycproxy: Proxy
            Object that interfaces with the System Coupling backend
    category: str
            Category of data that this 'root' refers to.
    generated_module: module
            Provide an alternative pre-generated module to be be used
            instead of the one that is otherwise used by default.
    report_whether_dynamic_classes_created: callable
            Callback that will be called with a bool parameter to report whether
            dynamic classes were created (True) or whether the pre-existing module could
            be used (False). The former will happen if the static info provided by the proxy
            does not match the hash of the pre-existing module.
    Returns
    -------
    root object
    """
    obj_info, root_type = sycproxy.get_static_info(category)
    try:
        if generated_module is None:
            ver = "v231"  # TODO parametrise
            generated_module = importlib.import_module(
                f"ansys.systemcoupling.core.settings.{ver}.{category}_root"
            )

        info_hash = _gethash(obj_info)
        if generated_module.SHASH == info_hash:
            LOG.debug("Using pre-generated datamodel classes.")
        else:
            LOG.warning(
                "Mismatch between generated file and server object "
                "info. Dynamically created settings classes will "
                "be used."
            )
            raise RuntimeError("Mismatch in hash values")
        cls = getattr(generated_module, f"{category}_root")
        report_whether_dynamic_classes_created(False)
    except Exception:
        cls = get_cls(root_type, obj_info[root_type])
        report_whether_dynamic_classes_created(True)
    # pylint: disable=no-member
    cls.set_sycproxy(sycproxy)
    return cls()
