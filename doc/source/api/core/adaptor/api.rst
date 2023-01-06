.. _ref_api:

.. currentmodule:: ansys.systemcoupling.core.session

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


Relationship with "Native" System Coupling API
----------------------------------------------

The API exposed in PySystemCoupling is mainly an `adaptation` of the API that exists
natively in Ansys System Coupling.

Users who are already familiar with System Coupling, or who wish to consult the System
Coupling documentation for more in-depth advice on some aspect of the system, should
find it easy to translate to the API as exposed in PySystemCoupling.

The key differences are as follows:

* Whereas naming of commands and data model elements follows `camel case` conventions
  in System Coupling,
  their equivalents in PySystemCoupling follow the `snake case` convention, which is
  the generally preferred Pythonic naming convention. Thus, the command ``AddParticipant``
  in System Coupling becomes ``add_participant`` in PySystemCoupling, and the data model
  object ``CouplingInterface`` becomes ``coupling_interface``.

* Commands and queries in System Coupling are all exposed in its Python environment as top-level
  global names. In PySystemCoupling, commands are exposed as callable objects that are accessible
  as attributes of one of the `root` attributes, :meth:`case<Session.case>`,
  :meth:`case<Session.setup>` and :meth:`case<Session.solution>`,
  of the :class:`Session<Session>` class.

* In System Coupling, the setup data model is in practice manipulated (and queried) in one of the following
  ways:

  * Using high level commands to create and initialize the main objects in the data model -
    for example, commands such as ``AddParticipant`` to add a new coupling participant, and
    ``AddDataTransfer`` to add a new data transfer object.

  * Accessing individual settings using a `path like` syntax, starting at a `root`
    returned by the ``DatamodelRoot`` command. For example::

      # Get the root object
      root = DatamodelRoot()

      # Path-like attribute access to navigate to setting of interest and assign to it
      root.CouplingInterface[
        "interface-1"
      ].DataTransfer["Force"].Value = "force*scaleFactor"

      # Similarly, path-like attribute access to query setting value
      print(root.ExecutionControl.Option)

* In PySystemCoupling, the setup data model may be manipulated in essentially the same way.
  As noted above, the setup commands are exposed from the
  :meth:`setup<Session.setup>` attribute of
  :class:`Session<Session>`, and this attribute also
  plays the role of ``DatamodelRoot()`` as an entry point to accessing
  individual settings via a similar path-like syntax::

    # Given a Session object, get the setup root
    setup = session.setup

    # Assign a setting using "path" syntax
    setup.coupling_interface[
      "interface-1"
    ].data_transfer["Force"].value = "force*scaleFactor"

    # Query a setting
    print(root.execution_control.option)

Directly Accessing the Native API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For users who want to try to perform a very quick translation from an existing
System Coupling script into the PySystemCoupling environment, or have a
specific need to access a feature not currently exposed in PySystemCoupling,
a `back door`, more direct, access to the native form of the API is offered by the
:ref:`_native_api<ref_native_api_property>` attribute of the :class:`Session<Session>` class.
An existing script will still need
some adjustment as the calls have to be via the ``_native_api`` attribute rather
than as global commands as in a System Coupling script.

For example, in a System Coupling script::

  AddParticipant(InputFile="FLUENT/fluent.scp")

The equivalent, using the `native API` in PySystemCoupling, would be::

  # Given a Session object, get the native api
  api = session._native_api

  api.AddParticipant(InputFile="FLUENT/fluent.scp")

It is recommended that this API should not be used as a matter of course, but it may
be useful in specific and limited circumstances.




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

In essence, the data model settings that define a System Coupling analysis comprise
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
arguments can be accessed using the ``arguments`` attribute. If an argument is
not specified and is optional, its default value is used. Arguments are also settings objects
and can be either primitive type or container type.

*Note*: the implementation of the settings classes is sufficiently flexible to
allow commands to be exposed at any level of the container hierarchy. This is
not exploited in the current API but there is scope to do so in future extensions of
the API. For example, where a command currently takes a reference to a data model object as
an argument, the explicit argument could be avoided by allowing the command to be
called on the relevant object.

.. _ref_api_details:

Settings API Content
--------------------
:ref:`Case and persistence commands<case_root>`

:ref:`Analysis setup commands and data model<setup_root>`

:ref:`Solution commands<solution_root>`

.. toctree::
   :maxdepth: 4
   :hidden:

   case
   setup
   solution