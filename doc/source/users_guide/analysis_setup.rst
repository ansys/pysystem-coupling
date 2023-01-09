.. _ref_syc_analysis_setup:


Setting Up An Analysis
======================

This section outlines the basic workflow for setting up a coupled analysis from scratch.
It assumes that a PySystemCoupling ``Session`` object (``syc_session``) has been created.

This section focuses on the ``setup`` section of the API (``syc_session.setup``), which is concerned with
defining the analysis in terms of the :ref:`data model<ref_syc_datamodel>`.

For the other main areas of the API, See :ref:`ref_syc_persistence` for guidance on saving and resuming
cases, and :ref:`ref_syc_solution` for solution-related operations.


Participant case set-up
-----------------------

Any participant that is involved in a coupled analysis must set up its case to solve its part of
the coupled physics analysis. Typically, this is very similar to setting up a standalone case
for that solver. Each participant has its own way of specifying the data transfers
to and from System Coupling - for example, as fluid boundary conditions in Fluent. Such details
are beyond the scope of this guide. See the System Coupling documentation for examples that
include details of setting up the participants' cases.


Add participants
----------------

Use the ``add_participant`` command to define the information about the participants involved
in the analysis.

In its most common usage form, this command accepts a file containing essential data about a participant,
such as the variables it exposes and the regions on which they are available.

.. code::

    >>> setup.add_participant(input_file="fluent.scp")
    'FLUENT-1'
    >>> setup.add_participant(input_file="mapdl.scp")
    'MAPDL-2'

Note that the name of the created ``coupling_participant`` object is returned in each case. This
may be captured in a variable to facilitate subsequent access to the object:

.. code:: python

    fluent_part = setup.add_participant(input_file="fluent.scp")
    assert setup.coupling_participant[fluent_part].participant_type == "FLUENT"

The ``add_participant`` commands not only create the participant object in question but
also help to initialise some other aspects of the data model state. After adding the `Fluent`
and `MAPDL` participants as described, the ``analysis_control``, ``solution_control`` and
``output_control`` objects exist, having been created with reasonable defaults. See the
output from ``print_state`` below. (Note that some details have been omitted from the output
shown, as indicated by ``...``.)

.. code::

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

Missing/unset values
^^^^^^^^^^^^^^^^^^^^

In the preceding ``print_state`` output, it can be seen that most settings have been defaulted
to some value. `<None>` is used in this output to indicate "unset" values. In some
settings in the data model, "None" is a legitimate string value, so the `<None>`
form is used in the ``print_state`` output for unset values to avoid
ambiguity. For example, the default value of
``analysis_control.global_stabilization.option`` is the string ``"None"``, which is one
of the valid options for this setting.

If queried in Python, an `unset` setting holds
the Python ``None`` object or, if a list-valued setting, the empty list, ``[]``.

The important missing values in the set-up in its current state are those in ``solution_control``.
This is addressed later as these missing values are considered to be errors in the set up,
and its solution is blocked unless the values are provided.

There are some other settings in the scope of the ``coupling_participant`` objects
that are indicated as "unset" (that is, `<None>`) in the ``print_state`` output). However,
these are not considered to be missing values nor to indicate any
kind of error in the set up, but rather are more specialized optional settings that have not
been provided in the relevant input files. Generally, ``coupling_participant`` state can be
considered to be "read-only" once it has been created, and further edits should not be necessary.

Create interfaces
-----------------

Each coupled analysis must have at least one coupling interface. Coupling interfaces must be added to
the analysis individually. When adding a coupling interface, you must specify the participant name
and the regions to be associated with each side of the coupling interface.

Interface names must be unique within the coupled analysis. When coupling interfaces are added,
they are assigned default names according to the convention "CouplingInterface#", where "#"
indicates the order in which the interfaces were created. For example, if three interfaces are
created, they are named "CouplingInterface1", "CouplingInterface2", and "CouplingInterface3".

To add an interface to the analysis, use the ``add_interface`` command:

.. code:: python

    interface_name = setup.add_interface(
        side_one_participant="MAPDL-2",
        side_one_regions=["FSIN_1"],
        side_two_participant="FLUENT-1",
        side_two_regions=["wall_deforming"]
    )

``add_interface`` returns the name of the interface created. Note that the name
has been saved in a variable for later use.

Create data transfers
^^^^^^^^^^^^^^^^^^^^^

Each interface must contain at least one data transfer specification, in the form of a named ``data_transfer``
object.

When adding a data transfer, you must specify the interface on which the transfer is to be added, the target
side for the transfer, and the variables to be associated with each side of the interface.

To add a data transfer to an interface, use the ``add_data_transfer`` command. In the following, the interface
name is the value that was returned by ``add_interface``:

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

The resultant interface state can now be examined:

.. code::

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


Checking for errors and final settings
--------------------------------------

The setup is essentially complete at this point. However, as mentioned earlier, there
remain some missing settings. If you were to try to solve the analysis at this
point, it would fail immediately with a raised exception because of the unset values.

Call ``get_status_messages`` to query for any errors in the setup. This also returns
any current warning and informational messages (as well as any active settings that are
at "Alpha" or "Beta" level).

The return value of ``get_status_messages`` is a list of dictionaries where each
dictionary provides details of a message. One of the dictionary fields is the "level"
and this can be used to filter the message list:

.. code::

    >>> from pprint import pprint
    >>> pprint([msg for msg in setup.get_status_messages() if msg["level"] == "Error"])
    [{'level': 'Error',
    'message': 'TimeStepSize not defined for Transient analysis',
    'path': 'solution_control'},
    {'level': 'Error',
    'message': 'EndTime not defined for Transient analysis',
    'path': 'solution_control'}]

.. note::

    The "path" field of the message dictionary indicates the location in the data model
    to which the message pertains. In the preceding output, this points to the ``solution_control``
    object, but the specific settings in error are indicated in the message itself. However,
    note that setting names referenced in the "message" text ("TimeStepSize" and "EndTime")
    are in the form that is used in System Coupling's native API. This reflects the
    current way that ``get_status_messages`` is exposed into PySystemCoupling. This
    does not allow for reliable automatic translation to PySystemCoupling naming. Users should,
    however, be able to infer the PySystemCoupling names relatively easily by assuming
    a conversion from "camel case" to "snake case" of such identifiers.

To address the errors, values need to be assigned to ``end_time`` and ``time_step_size``.
These define, respectively, the duration of the transient coupled analysis and the time
interval between each coupling step.

.. code:: python

    setup.solution_control.time_step_size = "0.1 [s]"
    setup.solution_control.end_time = "1.0 [s]"


Next steps/Additional set up
----------------------------

A minimal workflow for a basic analysis setup has been outlined. With this setup,
the case is ready to be solved. See :ref:`ref_syc_solution` for details. It might also be a good point to
save the case or to take a "snapshot". See :ref:`ref_syc_persistence` for details.

Although a complete setup has been defined, there are many optional settings that could be
applied - for example, to control the frequency with which solution data is saved, or
to apply advanced settings to control the solution algorithm.

In addition, there are various further data model object types that can be created to
introduce more sophisticated features to the analysis, such as expressions and
reference frames. Such features are beyond the scope of this User Guide but the data
model content is fully documented in :ref:`ref_index_api` and further guidance is available in the
System Coupling documentation.






