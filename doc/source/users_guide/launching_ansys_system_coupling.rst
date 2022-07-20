Launching Ansys System Coupling Locally
=======================================
System Coupling can be started from python in gRPC mode using
:func:`launch() <ansys.systemcoupling.core>`.
This starts System Coupling in the background and sends commands to that service.

.. code:: python

    import ansys.systemcoupling.core as pysystemcoupling
    syc_analysis = pysystemcoupling.launch()

System Coupling is now active and you can send commands to it as a Python class.
