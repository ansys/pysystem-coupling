.. _ref_syc_solution:


Solving An Analysis
===================

As in :ref:`ref_syc_analysis_setup`, a PySystemCoupling ``Session`` object is assumed to have
been created and will be referred to as ``syc`` in the code snippets.

This section focuses on the ``solution`` section of the API (``syc.solution``), which provides
operations associated with solving an analysis and examining results data.

``solve`` command
-----------------

If an analysis has been set up and has no errors, thr ``solve`` command is all that is needed
to attempt to obtain a solution. If output streaming is not already turned on, it can be
particularly useful to do this before solving in order to track the solution's progress via
the solver transcript output.

.. code:: python

    syc.start_output()
    syc.solution.solve()





