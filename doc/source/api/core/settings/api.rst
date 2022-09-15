.. _ref_api:

Commands and Settings API
=========================

Introduction
------------

A System Coupling analysis is defined in terms of a hierarchical data model of settings. An API is
exposed that provides direct access to the data model as well as to commands that assist in
various aspects of setting up and solving an analysis.

The API is defined in terms of a number of generic objects which will be described.

**TODO** This has been adapted/cut down from Fluent docs. Needs more customising for SyC differences
as well as expansion in places.

**Q** Should we draw attention to similarities with Fluent, or should we change implementation object names to make them more distinct.

Top-level Objects
-----------------

The commands and settings API is accessible via the top-level attributes of the ``Analysis`` class,
``case``, ``setup``, and ``solution``.

.. code-block::

  >>> import ansys.systemcoupling.core as pysystemcoupling
  >>> analysis = pysystemcoupling.launch()
  >>> setup = analysis.setup

Types of Settings Objects
-------------------------

A settings object can be one of the primitive types like ``Integer``, ``Real``,
``String`` and ``Boolean`` or a container object.

There are two types of container objects: ``Group`` and ``NamedObject``.

A ``Group`` object is a static container with pre-defined child objects which
can be accessed via attribute access. For example, ``setup.output_control.results``
refers to the ``results`` child of ``output_control`` child of the ``setup`` object. The
names of the child objects of a group can be accessed with the ``child_names``
attribute of a ``Group`` object.

A ``NamedObject`` is a container holding dynamically created named objects of
its specified child type (accessible via ``child_object_type`` attribute)
similar to a dictionary. A specific named object can be accessed using the
index operator. For example,
``setup.coupling_interface['intf-1']`` refers to the
``coupling_interface`` object with name ``intf-1``. The current list of named
object children can be accessed with the ``get_object_names()`` function of the
container class.


Setting and Modifying State
---------------------------

The state of any object can be accessed by "calling" it. For container objects,
this will return the state of the children as a dictionary.

To modify the state of any object, you could assign the corresponding attribute
in its parent object. This assignment could be done at any level. For ``Group``
and ``NamedObject`` type objects, the state value will be a dictionary.

The state of an object can also be accessed via the ``get_state`` method, and
modified via the ``set_state`` method.

The current state can also be printed in a simple text format with the
``print_state`` method. For example, the following


Commands
--------

Commands are methods of settings objects that are used to modify the state of
the application. For example, ... The ``command_names`` attribute of a settings object
provides the names of its commands.

If needed, commands can be passed keyword arguments, and the list of valid
arguments can be accessed using the ``arguments`` attribute.  If an argument is
not specified, its default value is used. Arguments are also settings objects
and can be either primitive type or container type.

Additional Metadata
-------------------

**Unused in System Coupling.**

Active Objects and Commands
---------------------------

** Unimplemented in System Coupling **

Objects and commands can be active or inactive based on the application state.
application. The ``is_active()`` method returns ``True`` if an object or command
is active at a particular time. ``get_active_child_names`` returns the list of
active children. ``get_active_command_names`` returns the list of active
commands.

Settings Objects Root
---------------------
:ref:`Case and persistence commands<case_root>`

:ref:`Analysis setup commands and datamodel<setup_root>`

:ref:`Solution commands<solution_root>`