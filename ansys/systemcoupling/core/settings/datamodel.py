"""
Module for accessing and modifying hierarchy of Fluent settings.

The only useful method is 'get_root' which returns the root object for
accessing Fluent settings.

Child objects can be generally accessed/modified using attribute access.
Named child objects can be accessed/modified using index operator.

Calling an object will return its current value.

Example
-------
r = flobject.get_root(proxy)
is_energy_on = r.setup.models.energy.enabled()
r.setup.models.energy.enabled = True
r.boundary_conditions.velocity_inlet['inlet'].vmag.constant = 20
"""
import collections
import hashlib
import keyword
import logging as LOG
import pickle
import sys
from typing import Dict, Generic, List, NewType, Tuple, TypeVar, Union
import weakref

from ansys.systemcoupling.core.settings import name_util

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


def to_python_name(syc_name: str) -> str:
    """Convert a scheme string to python variable name.

    The function does this by replacing symbols with _. `?`s are  ignored.
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
        return self.sycproxy.get_attrs(self.path, attrs)

    def get_attr(self, attr) -> StateType:
        attrs = self.get_attrs([attr])
        if attr != "active?" and attrs.get("active?", True) is False:
            raise RuntimeError("Object is not active")
        return attrs[attr]

    def is_active(self) -> bool:
        return True
        # return self.get_attr('active?')


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
        print(f"calling get_state...")
        print(f"proxy state = {self.sycproxy.get_state(self.path)}")
        print(
            f"python converted state = {self.to_python_keys(self.sycproxy.get_state(self.path))}"
        )
        return self.to_python_keys(self.sycproxy.get_state(self.path))

    def set_state(self, state: StateT):
        """Set the state of this object."""
        return self.sycproxy.set_state(self.path, self.to_syc_keys(state))

    def set_property_state(self, prop, value):
        self.set_state({prop: value})
        # self.sycproxy.set_state(self.path + '/' + prop, value)

    def get_property_state(self, prop):
        return self.sycproxy.get_state(self.path + "/" + self.to_syc_name(prop))

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


class NamedObject(SettingsBase[DictStateType]):
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

    def rename(self, new: str, old: str):
        """
        Rename a named object.

        Parameters:
        ----------
        new: str
             New name
        old: str
             Old name
        """
        self.sycproxy.rename(self.path, new, old)
        if old in self._objects:
            del self._objects[old]
        self._create_child_object(new)

    def __delitem__(self, name: str):
        self.sycproxy.delete(self.path, name)
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
        self.sycproxy.create(self.path, name)
        return self._create_child_object(name)

    def get_object_names(self):
        """Object names."""
        return self.sycproxy.get_object_names(self.path)

    def __getitem__(self, name: str):
        if name not in self.get_object_names():
            raise KeyError(name)
        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            self.sycproxy.create(self.path, name)
        child = self._objects.get(name)
        if not child:
            child = self._create_child_object(name)
        child.set_state(value)


class Command(Base):
    """Command object."""

    is_path_cmd = False

    def __call__(self, **kwds):
        """Call a command with the specified keyword arguments."""
        newkwds = {}
        if self.is_path_cmd:
            newkwds["ObjectPath"] = self._parent.syc_path

        for k, v in kwds.items():
            if k in self.argument_names:
                ccls = getattr(self, k)
                newkwds[ccls.syc_name] = ccls.to_syc_keys(v)
            else:
                raise RuntimeError("Argument '" + str(k) + "' is invalid")
        return self.sycproxy.execute_cmd(self._parent.path, self.obj_name, **newkwds)


class PathCommand(Command):
    """Path-based command object."""

    is_path_cmd = True


_param_types = {
    "Integer": Integer,
    "Logical": Boolean,
    "Real": Real,
    "String": String,
    "Real List": RealList,
    "Real Triplet": RealList,
    "String List": StringList,
}


def _get_type(id, info):
    if id == "child_object_type":
        return Group
    data_type = info.get("type", None)

    if data_type is None:
        if "isQuery" in info:
            # looks like a Command
            return PathCommand if "ObjectPath" in info["args"] else Command
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
        if name == "":
            pname = "root"
        else:
            pname = to_python_name(name)
        # obj_type = info['type']
        # base = _baseTypes.get(obj_type)
        base = _get_type(name, info)
        dct = {"syc_name": name}
        helpinfo = info.get("help")
        if helpinfo:
            dct["__doc__"] = helpinfo
        else:
            if parent is None:
                dct["__doc__"] = "root object"
            else:
                if False:  # obj_type == 'command':
                    dct["__doc__"] = f"'{pname}' command of '{parent.__name__}' object"
                else:
                    dct["__doc__"] = f"'{pname}' child of '{parent.__name__}' object"
        cls = type(pname, (base,), dct)

        children = info.get("__children")
        parameters = info.get("__parameters")
        if base == NamedObject:
            children = parameters = None

        if children:
            child_keys = sorted(children.keys(), key=lambda c: children[c]["ordinal"])
            cls.child_names = []
            for cname in child_keys:
                cinfo = children[cname]
                ccls = get_cls(cname, cinfo, cls)
                # pylint: disable=no-member
                cls.child_names.append(ccls.__name__)
                setattr(cls, ccls.__name__, ccls)

        if parameters:
            prop_keys = sorted(
                parameters.keys(), key=lambda p: parameters[p]["ordinal"]
            )
            cls.property_names_types = []
            for prname in prop_keys:
                sycname = prname
                prname = to_python_name(prname)
                prinfo = parameters[sycname]
                prtype = _get_type(prname, prinfo)
                docstr = f"'{prname}' property of '{parent.__name__}' object"
                setattr(
                    cls,
                    prname,
                    property(
                        fget=lambda slf: slf.get_property_state(prname),
                        fset=lambda slf, val: slf.set_property_state(prname, val),
                        doc=docstr,
                    ),
                )
                # ccls = get_cls(cname, cinfo, cls)
                # pylint: disable=no-member
                cls.property_names_types.append((prname, sycname, prtype))
                # cls.child_names.append(ccls.__name__)
                # setattr(cls, ccls.__name__, ccls)

        commands = info.get("__commands")
        if commands:
            cls.command_names = []
            for cname, cinfo in commands.items():
                ccls = get_cls(cname, cinfo, cls)
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
            for aname, ainfo in arguments.items():
                if aname == "ObjectPath":
                    continue
                ccls = get_cls(aname, ainfo, cls)
                th = ccls._state_type
                th = th.__name__ if hasattr(th, "__name__") else str(th)
                doc += f"    {ccls.__name__} : {th}\n"
                doc += f"        {ccls.__doc__}\n"
                # pylint: disable=no-member
                cls.argument_names.append(ccls.__name__)
                setattr(cls, ccls.__name__, ccls)
            cls.__doc__ = doc
        # object_type = info.get('object-type')
        object_type = Group if base == NamedObject else None
        if object_type:
            cls.child_object_type = get_cls("child_object_type", info, cls)
    except Exception:
        print(
            f"Unable to construct class for '{name}' of "
            f"'{parent.syc_name if parent else None}'"
        )
        raise
    return cls


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def get_root(sycproxy) -> Group:
    """
    Get the root settings object.

    Parameters
    ----------
    sycproxy: Proxy
             Object that interfaces with the System Coupling backend

    Returns
    -------
    root object
    """
    obj_info = sycproxy.get_static_info()
    try:
        from ansys.systemcoupling.core.settings import datamodel_222 as dm

        if dm.SHASH != _gethash(obj_info):
            LOG.warning(
                "Mismatch between generated file and server object "
                "info. Dynamically created settings classes will "
                "be used."
            )
            raise RuntimeError("Mismatch in hash values")
        cls = dm.root
    except Exception:
        cls = get_cls("SystemCoupling", obj_info["SystemCoupling"])
    # pylint: disable=no-member
    cls.set_sycproxy(sycproxy)
    return cls()
