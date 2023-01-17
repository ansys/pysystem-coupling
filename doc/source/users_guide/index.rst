.. _ref_user_guide:


User guide
##########
This guide provides a general overview of the PySystemCoupling library and its basic use.

Although this documentation provides a brief overview of the main concepts in System Coupling, it is not intended to be a comprehensive introduction to cosimulation and the use of System Coupling.
The focus is on guiding the use of PySystemCoupling client library to access System Coupling features.

.. note::
   Users who are licensed to use System Coupling can consult the product documentation for
   a detailed introduction to the product, illustrated with tutorial examples. The
   steps in the documentation that refer to the Command Line Interface (CLI) are those
   that are most readily translated to the PySystemCoupling environment.

..
   This toctreemust be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   system_coupling_concepts
   syc_datamodel
   analysis_setup
   syc_solution
   syc_persistence



Launching
=========
The ``launch()`` function in the ``ansys-systemcoupling-core`` library creates an instance of
System Coupling in the background and sends commands to that service.


.. code-block:: python

   syc_session = pysystemcoupling.launch()

The ``launch()`` function returns a ``Session`` object.


Session
=======
A ``Session`` object is the client-side access point in the library to a System Coupling server instance. ``Session`` exposes an API that allows a System Coupling analysis to be set up and solved. One or more such server sessions may be launched simultaneously from the client.

In addition to the setup and solve API, ``Session`` provides access to a few basic general facilities, described in the sections that follow.

Connection check
----------------
To confirm that there is a functioning connection to the System Coupling server, call the ``ping`` method:

.. code-block:: python

   syc_session.ping()

The ``ping`` method returns ``True`` if a simple call can successfully be made on System Coupling's `gRPC` server. Otherwise, the attempt to make the call raises an exception.


Output streaming
----------------
By default, any output that the System Coupling server process prints to its standard output streams
(``stdout`` and ``stderr``) is not shown. Output is streamed to the PySystemCoupling session and printed to its console when the ``start_output`` method is called:

.. code-block:: python

   syc_session.start_output()

You may turn off output streaming using ``end_output``:

.. code-block:: python

   syc_session.end_output()


Exiting
-------
When you finished with a PySystemCoupling session, it is advisable to end it cleanly using the
``exit`` method. Otherwise, the PySystemCoupling library still attempts to clean
up active server sessions when the Python environment is exited, which is naturally less
reliable than a directed exit.

Once you have called ``exit`` on a session object, the object is no longer usable.

.. code-block:: python

   syc_session.exit()

   # Will raise exception!
   syc_session.ping()

However, you could reassign the ``syc_session`` variable to a new session:

.. code-block:: python


   syc_session = pysystemcoupling.launch()

   # Ok
   syc_session.ping()

The ``Session`` class supports the Python `context manager protocol`. This means that
if a ``Session`` is created using a Python ``with`` statement, it is automatically
cleaned up --- that is, ``exit`` called on it --- upon leaving the scope of the ``with``.

.. code-block:: python

   with pysystemcoupling.launch() as syc_session:
      # Use syc_session
      ...
      # No need to call syc_session.exit() at the end

   # syc_session has been exited at this point



Logging
=======
Some basic logging capabilities are accessible via the ``LOG`` object. Built on the standard Python logging framework, this object allows you to set a ``level`` as a severity filter and to specify whether logging goes to a file and/or to the console.

.. code-block:: python

   from ansys.systemcoupling.core import LOG

   ...
   LOG.set_level("ERROR") # Log at level Error or more severe
   LOG.log_to_stdout()






