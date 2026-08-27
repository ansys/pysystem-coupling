.. _ref_syc_analysis_setup:

Analysis setup
==============

This page describes the basic workflow for setting up a coupled analysis from scratch.
It assumes that a PySystemCoupling ``Session`` object (``syc_session``) has been created.

The focus here is on the ``setup`` attribute (``syc_session.setup``) for the ``Session`` object.
This attribute defines the analysis in terms of the :ref:`data model<ref_syc_datamodel>`.

For descriptions of the ``Session`` object's ``solution`` and ``case`` attributes, see these pages:

- :ref:`ref_syc_solution`: Operations related to solving an analysis and examining the solution
- :ref:`ref_syc_persistence`: Operations for saving and resuming cases


Set up participant cases
------------------------

Any participant that is involved in a coupled analysis must set up its case to solve its part of
the coupled physics analysis. Typically, this is very similar to setting up a standalone case
for this solver. Each participant has its own way of specifying data transfers to and from
System Coupling. For example, Fluent uses fluid boundary conditions. 

While information on setting up participant cases is beyond the scope of this guide, you
can see the System Coupling documentation for examples.

Add participants
----------------

The ``add_participant`` command is used to define information about the participants involved
in the analysis.

In its most common usage, this command accepts a file containing essential data about a participant,
such as the variables it exposes and the regions on which they are available.

.. code-block:: python

    >>> setup.add_participant(input_file="fluent.scp")
    'FLUENT-1'
    >>> setup.add_participant(input_file="mapdl.scp")
    'MAPDL-2'


The name of the created ``coupling_participant`` object is returned in each case.

This code shows how you can capture the name in a variable to facilitate subsequent access
to the object:

.. code-block:: python

    fluent_part = setup.add_participant(input_file="fluent.scp")
    assert setup.coupling_participant[fluent_part].participant_type == "FLUENT"


The ``add_participant`` command not only creates a participant object but also helps
to initialize other aspects of the data model state. After the preceding code
adds Fluent and MAPDL participants, the ``analysis_control``, ``solution_control``, and
``output_control`` objects are created with reasonable default values. For more information,
see the following output from the ``print_state`` command. Ellipses (``...``) appear where
details are omitted from the output.

.. code-block:: python

    >>> setup.print_state()

    coupling_participant :
        MAPDL-2 :
            participant_type : MAPDL
            participant_display_name : MAPDL Transient
            display_name : MAPDL Transient
            dimension : 3D
            participant_analysis_type : Transient
            restarts_supported : True
            variable :
                FORC :
                    quantity_type : Force
                    ...
                INCD :
                    quantity_type : Incremental Displacement
                    ...
             region :
                FSIN_1 :
                    topology : Surface
                    input_variables :
                        0 : FORC
                    output_variables :
                        0 : INCD
                    display_name : FSIN_1_Fluid Solid Interface
            update_control :
                option : ProgramControlled
            execution_control :
                option : ProgramControlled
                ...
        FLUENT-1 :
            participant_type : FLUENT
            participant_display_name : Fluid Flow (Fluent)
            display_name : Fluid Flow (Fluent)
            dimension : 3D
            participant_analysis_type : Transient
            restarts_supported : True
            variable :
            force :
                quantity_type : Force
                ...
            displacement :
                quantity_type : Incremental Displacement
                ...
            region :
                ...
                wall_deforming :
                    topology : Surface
                    input_variables :
                        0 : displacement
                    output_variables :
                        0 : force
                    display_name : wall_deforming
                ...
            update_control :
                option : ProgramControlled
            execution_control :
                option : ProgramControlled
                ...
    analysis_control :
        analysis_type : Transient
        ...
        global_stabilization :
            option : None
    solution_control :
        duration_option : EndTime
        end_time : <None>
        time_step_size : <None>
    output_control :
        option : LastStep
        ...


Set *unset* values
------------------

In the preceding ``print_state`` output, most settings are assigned default values.
A value of ``<None>`` indicates an *unset* (missing) value.

.. note::
   For some settings in the data model, the string ``"None"`` is a legitimate value.
   For example, the default for the ``analysis_control.global_stabilization.option``
   setting is ``"None"``. Thus, to avoid ambiguity, the ``print_state`` output
   displays ``<None>`` for unset values.
   
   If queried in Python, an unset value holds the Python ``None`` object or an empty list
   (``[]``) for a setting whose value is a list.


In the preceding setup, the important unset values are those for ``solution_control`` settings.
These unset values are addressed later because they are considered to be errors in the setup.
Unless values are provided, the solution is blocked.

While some settings in the ``coupling_participant`` objects have ``<None>`` values, these
unset values are not considered to be missing values nor indicate any kind of error in the
setup. They are rather more specialized optional settings that have not been provided in
the relevant input files.

Generally, the ``coupling_participant`` state can be considered to be read-only once it has
been created. Further edits should not be necessary.

Create interfaces
-----------------

Each coupled analysis must have at least one coupling interface. Coupling interfaces must be
added to the analysis individually. When adding a coupling interface, you must specify the
participant name and the regions to be associated with each side of the coupling interface.

Interface names must be unique within the coupled analysis. When coupling interfaces are added,
they are assigned default names according to the convention ``CouplingInterface#``, where ``#``
indicates the order in which the interfaces were created. For example, if three interfaces are
created, they are named ``CouplingInterface1``, ``CouplingInterface2``, and ``CouplingInterface3``.

This code shows how you use the ``add_interface`` command to add an interface to the analysis:

.. code:: python

    interface_name = setup.add_interface(
        side_one_participant="MAPDL-2",
        side_one_regions=["FSIN_1"],
        side_two_participant="FLUENT-1",
        side_two_regions=["wall_deforming"]
    )

The ``add_interface`` command returns the name of the interface created. This name
is saved in a variable for later use.

Add data transfers
------------------

Each interface must contain at least one data transfer specification in the form of a
named ``data_transfer`` object. When adding a data transfer, you must specify the
interface on which the transfer is to be added, the target side for the transfer,
and the variables to be associated with each side of the interface.

The following code shows how you use the ``add_data_transfer`` command to add a data transfer
to an interface. The interface name is the value that is returned by the ``add_interface``
command.

.. code:: python

    force_transfer_name = setup.add_data_transfer(
        interface=interface_name,
        target_side="One",
        target_variable="FORC",
        source_variable="force"
    )

    displacement_transfer_name = setup.add_data_transfer(
        interface=interface_name,
        target_side="Two",
        source_variable="INCD",
        target_variable="displacement"
    )

This code shows how you can examine the state of the resulting interface:

.. code-block:: python

    >>> setup.coupling_interface[interface_name].print_state()

    display_name : Interface-1
    side :
        Two :
            coupling_participant : FLUENT-1
            region_list :
                0 : wall_deforming
            reference_frame : GlobalReferenceFrame
            instancing : None
        One :
            coupling_participant : MAPDL-2
            region_list :
                0 : FSIN_1
            reference_frame : GlobalReferenceFrame
            instancing : None
    data_transfer :
        FORC :
            display_name : Force
            suppress : False
            target_side : One
            option : UsingVariable
            source_variable : force
            target_variable : FORC
            ramping_option : None
            relaxation_factor : 1.0
            convergence_target : 0.01
            mapping_type : Conservative
        displacement :
            display_name : displacement
            suppress : False
            target_side : Two
            option : UsingVariable
            source_variable : INCD
            target_variable : displacement
            ramping_option : None
            relaxation_factor : 1.0
            convergence_target : 0.01
            mapping_type : ProfilePreserving
            unmapped_value_option : Nearest Value
    mapping_control :
        stop_if_poor_intersection : True
        poor_intersection_threshold : 0.5
        face_alignment : ProgramControlled
        absolute_gap_tolerance : 0.0 [m]
        relative_gap_tolerance : 1.0


Check for errors and finalize settings
--------------------------------------

The setup is essentially complete at this point. However, as mentioned earlier,
some unset settings remain. If you were to try to solve the analysis at this
point, it would fail immediately with a raised exception because of the unset values.

To query for any errors in the setup, call the ``get_status_messages`` command. This
command also returns any current warnings, informational messages, and any active settings
that are at *Alpha* or *Beta* level.

As shown in the following code, the return value of the ``get_status_messages`` command
is a list of dictionaries, where each dictionary provides the details of a message. You
can use the ``level`` field in a message dictionary to filter the message list:

.. code-block:: python


    >>> from pprint import pprint
    >>> pprint([msg for msg in setup.get_status_messages() if msg["level"] == "Error"])
    [{'level': 'Error',
    'message': 'TimeStepSize not defined for Transient analysis',
    'path': 'solution_control'},
    {'level': 'Error',
    'message': 'EndTime not defined for Transient analysis',
    'path': 'solution_control'}]

.. note::

    The ``'path'`` field in a message dictionary indicates the location in the data model
    to which the message pertains. In the preceding output, this points to the ``solution_control``
    object, but the specific settings causing the error are indicated in the message itself.
    However, the setting names referenced in the message (such as ``'TimeStepSize'`` and
    ``'EndTime'``) are in the form that is used in System Coupling's native API. This reflects the
    way that ``get_status_messages`` is exposed into PySystemCoupling, which
    does not allow for reliable automatic translation to PySystemCoupling naming. You should
    be able to infer the PySystemCoupling names relatively easily by assuming a conversion
    from *camel case* to *snake case*.

The following code addresses the ``'TimeStepSize'`` and ``'EndTime'`` errors by assigning values to
``end_time`` and ``time_step_size`` in the ``solution_control`` object. These settings define,
respectively, the duration of the transient coupled analysis and the time interval between
each coupling step.

.. code:: python

    setup.solution_control.time_step_size = "0.1 [s]"
    setup.solution_control.end_time = "1.0 [s]"


Perform additional steps
------------------------

By performing the preceding steps, you have created a minimal workflow for a basic analysis
setup. With this setup, you can attempt to solve the case. For more information, see
:ref:`ref_syc_solution`.

At this time, you might want to save the case or take a snapshot. For more information,
see :ref:`ref_syc_persistence`.

Although a complete setup has been defined, you could apply many optional settings.
For example, you might want to control the frequency with which solution data is saved or
apply advanced settings to control the solution algorithm.

In addition, you can create other data model object types to introduce more advanced
features, such as expressions and reference frames, to the analysis. While advanced
features are beyond the scope of this guide, the data model and its contents are fully
documented in :ref:`ref_index_api`. Additional guidance is available in the
System Coupling documentation.
