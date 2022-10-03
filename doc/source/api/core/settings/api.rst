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

The API implementation is built on a number of generic objects, which will be briefly described below.

Top-level Objects
-----------------

The commands and settings API is accessible via the top-level attributes of the ``Session`` class,
``case``, ``setup``, and ``solution``. Details of the concrete API accessed from these root attributes
are given in the :ref:`ref_api_details` section below.

.. code-block::

  >>> import ansys.systemcoupling.core as pysystemcoupling
  >>> analysis = pysystemcoupling.launch()
  >>> setup = analysis.setup

These top-level attributes are all instances of the ``Container`` type.


Settings Object Types
---------------------

In essence, the datamodel settings that define a System Coupling analysis comprise
a collection of primitive property values - values of types such as ``Integer``,
``Real``, ``String`` or ``Boolean``. In order to provide a structure to the settings,
they are organized as groups of properties in *container* objects.

There are two types of container objects: ``Container`` and ``NamedContainer``.

A ``Container`` object represents a grouping of primitive settings, accessible as
property attributes. It may also contain further statically defined container objects as *child objects*
which are accessible as attributes. For example, ``setup.output_control.results``
refers to the ``results`` child of ``output_control`` child of the ``setup`` object. The
names of the child objects can be accessed with the ``child_names``
attribute of a ``Container`` object. A settings property of ``output_control``, for example
``option``, would be accessed as ``setup.output_control.option``. This particular setting
would be a string value.

A ``NamedContainer`` is a container holding dynamically created named objects of
its specified child type (accessible via ``child_object_type`` attribute).
A specific named object can be accessed using the ``[]`` index operator, so that
``NamedContaier`` behaves somewhat like a Python dictionary. For example,
``setup.coupling_interface['intf-1']`` refers to the
``coupling_interface`` object with name ``intf-1``. The current list of named
object children can be accessed with the ``get_object_names()`` function of the
container class. In practice, the named object instances are ``Container``
objects. Thus, in the example just given, ``setup.coupling_interface['intf-1']``
is a ``Container``.


Setting and Modifying State
---------------------------

The state of any container object can be accessed by "calling" it and
this will return the state of its properties and any children as a nested dictionary.

The state of a container can be modified by assigning the corresponding attribute
in its parent object. This assignment could be done at any level. The assigned
state value should be a dictionary.

Individual settings may be queried and assigned as properties on their container objects.

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
not specified and is optional, its default value is used. Arguments are also settings objects
and can be either primitive type or container type.

*Note*: the implementation of the settings classes is sufficiently flexible to
allow commands to be exposed at any level of the container hierarchy. This is
not exploited in the current API but there is scope to do so in future extensions of
the API. For example, where a command currently takes a reference to a datamodel object as
an argument, the explicit argument could be avoided by allowing the command to be
called on the relevant object.

.. _ref_api_details:

Settings API Content
--------------------
:ref:`Case and persistence commands<case_root>`

:ref:`Analysis setup commands and datamodel<setup_root>`

:ref:`Solution commands<solution_root>`