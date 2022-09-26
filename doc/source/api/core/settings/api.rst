.. _ref_api:

Commands and Settings API
=========================

Introduction
------------

A System Coupling analysis is defined in terms of a hierarchical data model of settings. An API is
exposed that provides direct access to the data model as well as to commands that assist in
various aspects of setting up and solving an analysis.

Although it is possible to set up an analysis by directly assigning the relevant
data model objects and settings, the expected - and more convenient - approach is to use the
various commands that are provided to set up the main objects. Direct data model assignment
should then be used for fine adjustments to the setup.

The API implementation is built on a number of generic objects, which will be described. Note that while
it is anticpated that the API as it is used in practice will remain stable, the details of the underlying
generic implementation classes should not be relied on to any great extent.



Top-level Objects
-----------------

The commands and settings API is accessible via the top-level attributes of the ``Session`` class,
``case``, ``setup``, and ``solution``.

.. code-block::

  >>> import ansys.systemcoupling.core as pysystemcoupling
  >>> analysis = pysystemcoupling.launch()
  >>> setup = analysis.setup

These top-level attributes are all instances of the ``Container`` type.


Types of Settings Objects
-------------------------

A settings object can be one of the primitive types like ``Integer``, ``Real``,
``String`` and ``Boolean`` or a `container` object.

There are two types of container objects: ``Container`` and ``NamedContainer``.

A ``Container`` object is a static object with pre-defined child objects which
can be accessed via attribute access. For example, ``setup.output_control.results``
refers to the ``results`` child of ``output_control`` child of the ``setup`` object. The
names of the child objects of a group can be accessed with the ``child_names``
attribute of a ``Container`` object.

A ``NamedContainer`` is a container holding dynamically created named objects of
its specified child type (accessible via ``child_object_type`` attribute)
similar to a dictionary. A specific named object can be accessed using the
index operator. For example,
``setup.coupling_interface['intf-1']`` refers to the
``coupling_interface`` object with name ``intf-1``. The current list of named
object children can be accessed with the ``get_object_names()`` function of the
container class. In practice, the named object instances are ``Container``
objects. Thus, in the example just given, ``setup.coupling_interface['intf-1']``
is a ``Container``.


Setting and Modifying State
---------------------------

The state of any container object can be accessed by "calling" it and
this will return the state of the children as a dictionary.

The state of a container can be modified by assigning the corresponding attribute
in its parent object. This assignment could be done at any level. The assigned
state value should be a dictionary.

Individual settings may be queries and assigned as properties on their container objects.

The state of a container can also be accessed via the ``get_state`` method, and
modified via the ``set_state`` method.

The current state can be printed in a simple text format with the
``print_state`` method.


Commands
--------

Commands are methods of settings objects that are used to modify the state of
the application. For example, ... The ``command_names`` attribute of a settings object
provides the names of its commands.

If needed, commands can be passed keyword arguments, and the list of valid
arguments can be accessed using the ``arguments`` attribute.  If an argument is
not specified, its default value is used. Arguments are also settings objects
and can be either primitive type or container type.

Note: while the implementation of the settings classes is sufficiently flexible to
allow commands to be exposed at any level of the container hierarchy,

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