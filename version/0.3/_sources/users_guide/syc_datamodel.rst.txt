.. _ref_syc_datamodel:

System Coupling data model
==========================

The System Coupling data model is a hierarchical structure represented in the PySystemCoupling API
as nested attributes. Ultimately, the nested attributes end at primitive values, which are the
basic settings defining the setup. The nested structure allows the data to be organized in a way
that fits with the underlying concepts of a System Coupling analysis.


Data model structure
---------------------

The following image shows the hierarchy of *objects* in the System Coupling data model. These objects
hold a collection of *primitive settings* and/or additional *child objects*. The primitive settings
are named values of different value types, such as ``integer``, ``boolean``, and ``string``.

  .. code-block:: none
    :emphasize-lines: 5,9,10
    :caption: System Coupling data model structure
    
    root
      ├── participant
      │      ├── variable
      │      └── region
      ├── analysis_control
      ├── coupling_interface   
      │      ├── side
      │      └── data_transfer
      ├── solution_control   
      └── output_control   


In the image, highlighting distinguishes items representing objects at a level of the
hierarchy with only one *unnamed* instance versus multiple *named* instances:

* Highlighted items represent objects for which only one unnamed instance can exist at this level
  (*singletons*).
* Non-highlighted items represent objects for which multiple named instances can exist at this
  level. 
  
  .. note:: 
    In general, object names can be freely chosen. The exception is the ``side`` object, for which exactly
    two instances exist. These two instances have fixed names: ``One`` and ``Two``.


Access the data model
---------------------

The ``setup`` attribute of the ``Session`` object is used to access the data model. The objects in the data model are
attributes of the ``setup`` attribute. For example, this code accesses the ``analysis_control`` object:

.. code-block:: python

   ...
   setup = syc_session.setup
   analysis_control = setup.analysis_control


As noted, the data model objects hold basic settings of different value types.
For example, the ``analysis_control`` object contains an ``analysis_type`` setting having a
``string`` value type. Valid values are ``Steady`` and ``Transient``. Thus, this setting
defines the type of analysis to be performed.

This code shows how you set and query the ``analysis_type`` setting:

.. code:: python

    analysis_control.analysis_type = "Transient"
    print(analysis_control.analysis_type)


To access a named object, use a syntax like Python dictionary lookups:

.. code:: python

    dt = setup.coupling_interface["Interface-1"].data_transfer["Force"]
    # target_side is either "One" or "Two"
    print(dt.target_side)


Populate the data model
-----------------------

The preceding code examples assume that the data model is already populated with data, so that the
objects referenced from the hierarchy already exist. This would be the situation when you modify
an existing case, perhaps one that had previously been set up and saved, and you have now re-opened.

When setting up an analysis from scratch, you must create the objects. In principle,
you can do this using direct, low-level, operations on the data model, but this is not recommended.
Instead,you should use the higher-level *commands* that are provided by the
API. For more information, see :ref:`ref_syc_analysis_setup`.

Nevertheless, it can sometimes be useful to know how to create an object directly in the
data model, as shown in the following code examples.

You can access unnamed objects, such as ``analysis_control`` attributes, even when
they are initially *empty*. You can confirm this using the ``print_state()`` method:

.. code-block:: python

	>>> setup.analysis_control.print_state()

	>>>


When you apply a setting to such an object, this not only sets a value for the specified
setting but also sets the default values for other settings (where possible):

.. code-block:: python

    >>> setup.analysis_control.analysis_type = "Steady"
    >>> setup.analysis_control.print_state()

    analysis_type : Steady
    optimize_if_one_way : True
    allow_simultaneous_update : False
    partitioning_algorithm : SharedAllocateMachines
    global_stabilization :
    option : None
    >>>


To create a named object instance, use the ``create()`` method on the
object's type attribute:

.. code-block:: python

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


.. note::  
  The preceding code examples are for illustration only. A ``coupling_participant``
  object requires very specific data for it to be initialized in a useful manner. Usually,
  this data is derived from some external source. The ``add_participant()`` command,
  which is the recommended method for creating a participant, exists to help with this.
  This command and various other commands are available as methods on the session's
  ``setup`` attribute. For more information, see :ref:`ref_syc_analysis_setup` and
  :ref:`ref_setup`.
  
