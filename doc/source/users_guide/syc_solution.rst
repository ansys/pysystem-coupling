.. _ref_syc_solution:


Solving An Analysis
===================

As in :ref:`ref_syc_analysis_setup`, a PySystemCoupling ``Session`` object is assumed to have
been created and is referred to as ``syc_session`` in the code snippets.

This section focuses on the ``solution`` part of the API (``syc_session.solution``), which provides
operations associated with solving an analysis and examining results data.

``solve`` command
-----------------

If an analysis has been set up and has no errors, a solution may be attempted simply by
calling ``solve``. If output streaming is not already turned on, it can be
particularly useful to do this before solving to track the solution's progress via
the solver transcript output.

.. code:: python

    syc_session.start_output()
    syc_session.solution.solve()

Currently, all commands in the PySystemCoupling API are executed synchronously, including ``solve``.
This is a reflection of how the underlying operations currently work in System Coupling.

Sometimes, because ``solve`` tends to be a long running operation, it can be useful to run it
asynchronously in the Python environment. This is not supported explicitly because
in the current version of the API, there is no protection against trying to make calls
concurrently. However, ``solve`` can be called asynchronously by "manual" coding, using Python
threads:

.. code:: python

    import threading
    ...

    solve_thread = threading.Thread(target = syc_session.solution.solve)

    solve_thread.start()

    # Do other thing in the Python environment
    ...

    # wait for solve to finish
    solve_thread.join()

The majority of the session's API should be avoided while the thread is active.
An exception is that it is possible to interrupt or force the end of a solve.

Interrupting and aborting a solve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can interrupt or force the end of a solve using the ``solution.interrupt()`` and ``solution.abort()``
calls. These are unusual PySystemCoupling calls in that they *must* be called in a different thread from the one
in which ``solve`` is executing.

Both calls have the effect of stopping the solve that is in progress. The key difference
is that ``interrupt`` supports the resumption of the solve (by calling ``solve`` again).

Low-level solution control
^^^^^^^^^^^^^^^^^^^^^^^^^^

Commands are available for more advanced scenarios offering lower level control over the
solution process, specifically ``initialize``, ``step``, ``create_restart_point``
and ``shutdown``. Roughly speaking, these provide the capability to perform the
individual actions that are usually encapsulated in a simple ``solve`` call, allowing
custom code to be executed between these actions.

Such advanced usage is not considered further in this User Guide.


Postprocessing support
----------------------

The results for the individual participants in the analysis can be
examined using their respective postprocessing applications. Consult the relevant
documentation for details.

For System Coupling-specific results, data can be written in EnSight format, so that
EnSight can be used for visualization, animation, and postprocessing. PySystemCoupling
also supports the writing of some convergence diagnostics in CSV format.

Generating EnSight data
^^^^^^^^^^^^^^^^^^^^^^^

When a solution is available, EnSight files can be written on demand:

.. code:: python

    solution.write_ensight(file_name="EnSightResults")

Alternatively, the ``output_control`` settings in the set-up data can be used
to specify the automatic generation of EnSight data at certain points during the
solution:

.. code:: python

    setup.output_control.results.option = "StepInterval"
    setup.output_control.results.output_frequency = 2

The use of EnSight for postprocessing the output data is not covered in this
User Guide. See the comprehensive System Coupling documentation and relevant
EnSight documentation for more information.

Convergence diagnostic data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a solution is available, CSV-formatted convergence data can be written on demand:

.. code:: python

    solution.write_csv_chart_files()

This creates one file per coupling interface, where the file is named *<interface name>.csv*. Each file
contains the interface's convergence and transfer data for each iteration.

Alternatively, the ``output_control`` settings in the set-up data can be used to turn on
automatic writing of these files:

.. code:: python

    setup.output_control.generate_csv_chart_output = True












