.. _ref_syc_persistence:

Analysis Persistence
====================

The ``case`` attribute of ``Session`` provides access to commands relating to persistence and overall state
of an analysis case:

* Opening and saving a case
* Saving a `snapshot` of a case
* Clearing/resetting the entire state

In the code snippets below, the ``case`` variable is assumed to have been assigned as follows:

.. code:: python

    case = syc.case


Saving and opening a case
-------------------------

Files defining the state of an analysis case are always saved and loaded from a `SyC/` subdirectory and, by default, this will
exist in the working directory.

.. code:: python

    # Open a case from sub-directory SyC of current working directory:
    case.open()
    ...

    # Open a case from sub-directory SyC of specified directory
    case.open(file_path="cht_cases/case1")

Opening a case will restore the analysis settings at the time of saving, and
will load results data if it exists.

Similarly for saving the current state of a case:

.. code:: python

    # Save a case to sub-directory SyC of current working directory:
    case.save()
    ...

    # Save a case to sub-directory SyC of specified directory
    case.save(file_path="cht_cases/case1")

When saving a case, the `SyC` directory will be created if it does not already exist.
Settings data is saved in a file called `settings.h5`.

Note that if a case is opened with a specified ``file_path`` and subsequently saved
without specifying a path, it will be written to a `SyC` subdirectory of the `current
working directory`; it will not be rewritten to the directory from which it was opened.

If the case has been
successfully solved, one or more `restart` files --- files with names of the form
*Restart_step<n>* or *Restart_iter<n>* --- will exist, depending on whether the analysis
is a transient or steady cases. The restart files allow the
results to be loaded at any point partway through the analysis for which a restart
file exists. For example, if results were saved at the end of step 2, then the ``coupling_step``
option may be provided to ``open``:

.. code:: python

    # Open at step 2
    case.open(coupling_step=2)

The frequency with which restart files are written during a solution is controlled by
the setting ``setup.output_control.option``.

.. note::
    Opening a case at a restart point that is not the final step/iteration will result
    in *later* restart files being deleted. Typically, the reason for opening at an
    earlier point is to re-run the analysis from that point. If it is important to
    save all of the results, the :ref:`ref_snapshots` facility may be used.

The results data itself is stored in the `Results` subdirectory of `SyC`.

.. _ref_snapshots:

Case snapshots
--------------
Snapshot capabilities allow you to capture the current state of a coupled
analysis as a whole and then later restore the analysis to that state.

Snapshots give you the ability to save and return to a specific point in a coupled analysis.

A snapshot captures the current state of the coupled analysis as a whole (rather than just of the data model).
It includes all the files and directories contained in System Coupling's working directory that are necessary
to restore the coupled analysis to its current state --- specifically, the `SyC` subdirectory and the coupling
working directories of all loaded coupling participants.

The snapshot facility relies on the `SyC` directory and the participants' working directories being
subdirectories of the System Coupling working directory.

Snapshots are saved in a subdirectory `SyCSnapshots` that exists in the working directory alongside
the `SyC` directory. Each snapshot is saved as a `zip` file. A snapshot named `Initial.zip` is
created automatically when a solve is started (if it does not already exist); otherwise,
snapshots are managed on demand using the API commands as discussed below.

The basic operations supported are:

* saving a snapshot
* loading a snapshot
* deleting a snapshot
* querying available snapshots

.. code:: python

    # solve the current case
    solution.solve()
    ...

    # Save the solution as a snapshot
    case.save_snapshot(snapshot_name='Solution1')

    # Restore the the Initial snapshot from before solve
    case.open_snapshot(snapshot_name='Initial')
    # Make some changes and solve again
    ...
    solution.solve()
    # Save this solution to a snapshot
    case.save_snapshot(snapshot_name='Solution2')

    # Query snapshots..
    case.get_snapshots()
    # Returns a dict, snapshot name=>file name
    #
    # { 'Initial': 'Initial.zip',
    #   'Solution1': 'Solution1.zip',
    #   'Solution2': 'Solution2.zip' }
    #

    # Delete Solution1
    case.delete_snapshot(snapshot_name='Solution1')

Clearing current state
----------------------

Occasionally, it might be useful to be able to clear the entire state of settings and
results that are loaded in the current System Coupling session.

This can be achieved by calling the ``clear_state`` command:

.. code:: python

    case.clear_state()

Another option to achieve a similar outcome in the PySystemCoupling environment
would be exit the current session and create a new one.

.. code:: python

    syc_session.exit()
    syc_session = pysystemcoupling.launch()









