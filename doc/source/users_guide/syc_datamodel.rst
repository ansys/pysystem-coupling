.. _ref_syc_datamodel:

System Coupling Data Model
==========================

The System Coupling data model is a hierarchical structure, represented in the PySystemCoupling API
as nested attributes. Ultimately, the nested attributes navigate down to primitive values which are the
basic settings defining the set-up. The nested structure allows the data to be organized in a way
that fits with the underlying concepts of a System Coupling analysis.


Data Model Structure
--------------------

The following shows the main hierarchy of the "objects" in the data model. Such objects hold a collection
of primitive settings and/or further "child" objects.
The primitive settings are named values of type integer, boolean, string, etc.


- *participant*

  - *variable*

  - *region*

- analysis_control

- *coupling_interface*

  - *side*

  - *data_transfer*

- solution_control

- output_control

The italicized names represent those for which more than one instance may exist --- each instance is given a name.
In general, names may be freely chosen, but ``side`` is unusual in that exactly two instances exist, with fixed names "One" and "Two".

Non-italic names indicate objects for which only one unnamed instance may appear at that level of the hierarchy.

Accessing the Data Model
------------------------

The data model is accessed via the ``setup`` attribute of ``Session``. The objects in the data model are
attributes of ``setup``.

For example, to access the ``analysis_control`` object:

.. code:: python

   ...
   setup = syc_session.setup
   analysis_control = setup.analysis_control

As noted above, the data model objects hold basic settings of different value types.
For example, ``analysis_control`` contains a setting ``analysis_type`` of type string. This defines the
type of analysis to be performed. The valid values are "Steady" and "Transient". The following illustates
how the setting may be set and queried:

.. code:: python

    analysis_control.analysis_type = "Transient"
    print(analysis_control.analysis_type)

Named objects are accessed using syntax like Python dictionary lookups:

.. code:: python

    dt = setup.coupling_interface["Interface-1"].data_transfer["Force"]
    # target_side is either "One" or "Two"
    print(dt.target_side)



Populating the Data Model
-------------------------

The examples above assume that the data model is already populated with data, so that the
objects referenced from the hierarchy already exist. This would be the situation if modifying
an existing case, perhaps one that had been previously set up and saved and has now been
re-opened.

If a new analysis is being set up from scratch, the objects need to be created. In pricniple,
this can be done using direct, low-level, operations on the data model. This is not the
recommended approach, which is to use the higher level "commands" that are provided by the
API. See ????? for details on this.

Nevertheless, it can sometimes be useful to know how to create an object directly in the
data model, so a couple of examples will be given below.

Unnamed objects such as ``analysis_control`` can be accessed as attributes, even when
they are initially "empty". This may be confirmed using ``print_state()``:

.. code::

	>>> setup.analysis_control.print_state()

	>>>

If a setting is applied on such an object, that not only applies the specified
value but also fills the other settings with default values where possible:

.. code::

    >>> setup.analysis_control.analysis_type = "Steady"
    >>> setup.analysis_control.print_state()

    analysis_type : Steady
    optimize_if_one_way : True
    allow_simultaneous_update : False
    partitioning_algorithm : SharedAllocateMachines
    global_stabilization :
    option : None
    >>>

To create a named object instance, the ``create()`` method can be used on the
object's type attribute:

.. code::

	>>> setup.coupling_participant.create("Part1")
	>>> setup.coupling_participant["Part1"].print_state()

	participant_type : DEFAULT
	participant_display_name : Part1
	display_name : Part1
	dimension : 3D
	participant_analysis_type : <None>
	restarts_supported : False
	update_control :
	option : ProgramControlled
	execution_control :
	option : UserDefined
	working_directory : .
	executable : <None>
	additional_arguments : <None>
	parallel_fraction : 1.0
	>>>

Note that this is for illustration only. A ``coupling_participant`` requires very specific
data for it to be initialized in a useful manner. Usually, this data is derived from some external source.
The ``add_participant()`` command exists to help with this, and this is how a participant would normally
be created. This, and various other commands are available as methods on the session's ``setup``
attribute. See ???<analysis set up> and ???<API> for more details.




