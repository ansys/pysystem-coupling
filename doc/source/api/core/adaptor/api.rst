.. _ref_api:

.. currentmodule:: ansys.systemcoupling.core.session

Commands and settings API
=========================

A System Coupling analysis is defined in terms of a hierarchical data model of settings.
An API is exposed that provides direct access to the data model and commands that assist
in setting up and solving an analysis.

Although it is possible to set up an analysis by directly assigning the relevant
data model objects and settings, the expected and more convenient approach is to
use the commands provided to set up the main objects. You then use direct
data model assignment to fine tune the setup.

The API implementation is built on a number of generic objects. Subsequent
sections provide brief descriptions of these objects.

Relationship with the "native" System Coupling API
--------------------------------------------------

The API exposed in PySystemCoupling is mainly an *adaptation* of the API that exists
natively in Ansys System Coupling.

If you are already familiar with System Coupling, or you want to consult the System
Coupling documentation for more in-depth advice on some aspect of the system,
you should find it easy to translate to the API that is exposed in PySystemCoupling.

The key differences are as follows:

* While names of commands and data model elements follow *camel case* conventions
  in System Coupling, the names of commands and data models in PySystemCoupling follow
  *snake case* convention, which is the preferred Pythonic naming convention.
  Thus, the ``AddParticipant`` command in System Coupling becomes the ``add_participant``
  command in PySystemCoupling. Similarly, the ``CouplingInterface`` data model object
  in System Coupling becomes the ``coupling_interface`` data model object in
  PySystemCoupling.

* Commands and queries in System Coupling are all exposed in its Python environment as top-level
  global names. Commands in PySystemCoupling are exposed as callable objects that are accessible
  as attributes of one of the *root* attributes of the :class:`Session<Session>` class:
  :meth:`case<Session.case>`, :meth:`case<Session.setup>`, and :meth:`case<Session.solution>`.
  
* In System Coupling, you manipulate and query the setup data model in one of these ways:

  * Use high level commands to create and initialize the main objects in the data model.
    For example, use the ``AddParticipant`` command to add a new coupling participant and
    the ``AddDataTransfer`` command to add a new data transfer object.

  * Access individual settings using a *path-like* syntax, starting at a *root*
    object returned by the ``DatamodelRoot`` command. For example::

      # Get the root object
      root = DatamodelRoot()

      # Path-like attribute access to navigate to a setting and assign a value to it
      root.CouplingInterface[
        "interface-1"
      ].DataTransfer["Force"].Value = "force*scaleFactor"

      # Similarly, path-like attribute access to query setting value
      print(root.ExecutionControl.Option)

* In PySystemCoupling, you manipulate and query the setup data model in essentially
  the same way. Setup commands are exposed from the :meth:`setup<Session.setup>` attribute
  of the :class:`Session<Session>` object. This attribute also plays the role of ``DatamodelRoot()``
  in the preceding code. It serves as an entry point to accessing individual settings
  via a similar path-like syntax::

    # Given a Session object, get the setup root
    setup = session.setup

    # Assign a setting using "path" syntax
    setup.coupling_interface[
      "interface-1"
    ].data_transfer["Force"].value = "force*scaleFactor"

    # Query a setting
    print(root.execution_control.option)

Direct access to the native System Coupling API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to try to quickly translate an existing System Coupling script
to the PySystemCoupling environment, or you need to access a feature
not currently exposed in PySystemCoupling, you can use the
:ref:`_native_api<ref_native_api_property>` attribute of the
:class:`Session<Session>` class offers as a *back door* for directly accessing
the native System Coupling API. However, you must still make some adjustments
to the existing System Coupling script because calls must be via the
``_native_api`` attribute rather than via global commands.

For example, here is a command in a System Coupling script::

  AddParticipant(InputFile="FLUENT/fluent.scp")

When using the `native API` in PySystemCoupling, the equivalent would be::

  # Given a Session object, get the native api
  api = session._native_api

  api.AddParticipant(InputFile="FLUENT/fluent.scp")

You should not use the ``_native_api`` attribute generally, but you
might find using it necessary in specific and limited circumstances.


Top-level objects
-----------------

The commands and settings API is accessible via the top-level attributes of
the ``Session`` class: ``case``, ``setup``, and ``solution``. These top-level
attributes are all instances of the ``Container`` type. For links to commands
for these root attributes, see :ref:`ref_api_details`.

.. code-block::

  >>> import ansys.systemcoupling.core as pysystemcoupling
  >>> analysis = pysystemcoupling.launch()
  >>> setup = analysis.setup


Container object types
----------------------

In essence, the data model settings that define a System Coupling analysis consist
of a collection of primitive property values, such as ``Integer``, ``Real``,
``String``, and ``Boolean``. To provide a structure to the settings,
they are organized as groups of properties in *container* objects.

There are two types of container objects: ``Container`` and ``NamedContainer``.

A ``Container`` object represents a grouping of primitive settings, accessible as
property attributes. A ``Container`` object can also contain statically defined
*child objects*, which are accessible as attributes. For example, ``setup.output_control.results``
refers to the ``results`` child of the ``output_control`` child of the ``setup`` object.
The names of child objects can be accessed with the ``child_names``
attribute of the ``Container`` object. For example, the ``option`` setting of the
``output_control`` object is accessed as ``setup.output_control.option``. This particular setting
is a string value.

A ``NamedContainer`` object is a container holding dynamically created named objects of
its specified child type, which is accessible via ``child_object_type`` attribute.
Because a specific named object can be accessed using the ``[]`` index operator, a
``NamedContaier`` object behaves somewhat like a Python dictionary. For example,
``setup.coupling_interface['intf-1']`` refers to the
``coupling_interface`` object with name ``intf-1``. You can use the ``get_object_names()``
method in the container class. In practice, the named object instances are ``Container``
objects. Thus, in the example just given, ``setup.coupling_interface['intf-1']``
is a ``Container`` object.

Container states
----------------

You access the state of any container object by calling it. The call returns
the state of its properties and any children as a nested dictionary.

You modify the state of a container by assigning the corresponding attribute
in its parent object. This assignment can be done at any level. The assigned
state value should be a dictionary.

You query and assign individual settings as properties on their container objects.

You use the ``get_state`` method to get the state of a container and the ``set_state``
method to modify the state of the container.

You use the ``print_state`` method to print the current state of the container in
a simple text format.

Commands
--------

Commands are methods of settings objects that you use to modify the state of
the app. The ``command_names`` attribute of a settings object
provides the names of its commands.

You can pass commands as keyword arguments if needed. You use the ``arguments``
attribute to access the list of valid arguments. If an argument is
not specified and is optional, its default value is used. Arguments are also settings objects
and can be either a primitive type or container type.

.. note::
  The implementation of the ``settings`` classes is sufficiently flexible to
  allow commands to be exposed at any level of the container hierarchy. This is
  not exploited in the current API, but there is scope to do so in future extensions of
  the API. For example, where a command currently takes a reference to a data model object as
  an argument, allowing the command to be called on the relevant object could avoid
  the explicit argument.

.. _ref_api_details:

Settings API content
--------------------

For information on commands related to settings, see:

* :ref:`Case and persistence commands <case_root>`
* :ref:`Analysis setup commands and data model <setup_root>`
* :ref:`Solution commands <solution_root>`

.. toctree::
   :maxdepth: 4
   :hidden:

   case
   setup
   solution