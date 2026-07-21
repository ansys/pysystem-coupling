.. _ref_syc_solution:


Solving an analysis
===================

As in :ref:`ref_syc_analysis_setup`, a PySystemCoupling ``Session`` object is assumed to have
been created and is referred to as ``syc_session`` in the code snippets.

This section focuses on the ``solution`` part of the API (``syc_session.solution``), which provides
operations associated with solving an analysis and examining results data.

The ``solve`` command
----------------------

If you have set up an analysis and it has no errors, you may attempt to solve it by calling ``solve``.

.. tip::
    Before beginning the solve, you can enable output streaming to use the solver transcript output to track the solution's progress.

.. code-block:: python

    syc_session.start_output()
    syc_session.solution.solve()

Currently, all commands in the PySystemCoupling API (including ``solve``) are executed synchronously. This is a reflection of how the underlying operations currently work in System Coupling.

Because ``solve`` tends to be a long-running operation, it can be useful to execute it
asynchronously in the Python environment. This is not supported explicitly, because
in the current version of the API, there is no protection against trying to make calls
concurrently. However, you can call ``solve`` asynchronously by "manual" coding using Python
threads:

.. code-block:: python

    import threading

    ...

    solve_thread = threading.Thread(target=syc_session.solution.solve)

    solve_thread.start()

    # Do other things in the Python environment
    ...

    # wait for solve to finish
    solve_thread.join()

The majority of the session's API should be avoided while the thread is active.
An exception is that it is possible to interrupt or force the end of a solve.

Interrupting and aborting a solve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can interrupt or force the end of a solve using the ``solution.interrupt()`` and ``solution.abort()`` calls. These are unusual PySystemCoupling calls in that they *must* be called in a different thread from the one in which ``solve`` is executing.

Both calls have the effect of stopping the solve that is in progress. The key difference
is that ``interrupt`` allows you to resume the solve (by calling ``solve`` again).

Low-level solution control
^^^^^^^^^^^^^^^^^^^^^^^^^^

Commands are available for more advanced scenarios offering lower-level control over the
solution process --- specifically ``initialize``, ``step``, ``create_restart_point``
and ``shutdown``. Roughly speaking, these perform the individual actions that are usually
encapsulated in a simple ``solve`` call, allowing custom code to be executed between these
actions.

Such advanced usage is not within the scope of this guide.


Postprocessing support
----------------------

You can examine the results for the individual participants in the analysis by using their respective postprocessing applications. For details, see the relevant product documentation.

For System Coupling-specific results, data can be written in EnSight format. This allows you to use Ansys EnSight for visualization, animation, and postprocessing. PySystemCoupling also supports the writing of some convergence diagnostics in CSV format.

Generating EnSight data
^^^^^^^^^^^^^^^^^^^^^^^

When a solution is available, you can specify that EnSight files are written on demand:

.. code:: python

    solution.write_ensight(file_name="EnSightResults")

Alternatively, you can use the ``output_control`` settings to specify the automatic generation of EnSight data at certain points during the solution:

.. code:: python

    setup.output_control.results.option = "StepInterval"
    setup.output_control.results.output_frequency = 2

Using EnSight to postprocess output data is not covered in this guide. For more information, see the relevant System Coupling and EnSight product documentation.

Convergence diagnostic data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a solution is available, you can specify that CSV-formatted convergence data is written on demand:

.. code:: python

    solution.write_csv_chart_files()

This creates one file per coupling interface, where the file is named ``<interface name>.csv``. Each file contains the interface's convergence and transfer data for each iteration.

Alternatively, you can use the ``output_control`` settings to turn on automatic writing of these files:

.. code:: python

    setup.output_control.generate_csv_chart_output = True












