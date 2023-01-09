.. _ref_user_guide:

==========
User Guide
==========
This guide provides a general overview of the PySystemCoupling library and its basic use.

Although this guide does provide a brief overview of the main concepts in System Coupling, it is
not intended to be a comprehensive introduction to cosimulation and the use of System Coupling.
The focus is on guiding the use of PySystemCoupling client library to access System
Coupling features.

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


.. code:: python

   syc_session = pysystemcoupling.launch()

The ``launch()`` function returns a ``Session`` object.


Session
=======
A ``Session`` object is
the client-side access point in the library to a System Coupling server instance.
``Session`` exposes an API that allows a System Coupling analysis to be set up and solved. One or more such server
sessions may be launched simultaneously from the client.

In addition to the set up and solve API, ``Session`` provides access to a few basic general facilities, described below.

Connection Check
----------------
To confirm that there is a functioning connection to the System Coupling server, call the ``ping`` method.

.. code:: python

   syc_session.ping()

``ping`` returns ``True`` if a simple call can successfully be made on System Coupling's `gRPC` server. Otherwise,
the attempt to make the call raises an exception.


Output Streaming
----------------
By default, any output that the System Coupling server process prints to its standard output streams
(``stdout`` and ``stderr``) is not shown. Such output is streamed to the PySystemCoupling session and
printed on its console if the ``start_output`` method is called:

.. code:: python

   syc_session.start_output()

Output may be turned off again using ``end_output``:

.. code:: python

   syc_session.end_output()


Exiting
-------
When finished with a PySystemCoupling session, it is advisable to end it cleanly using the
``exit`` method. If this is not done, the PySystemCoupling library still attempts to clean
up active server sessions when the Python environment is exited, but this is naturally less
reliable than a directed exit.

Once ``exit`` has been called on a session object, it is no longer usable.

.. code:: python

   syc_session.exit()

   # Will raise exception!
   syc_session.ping()

However, the ``syc_session`` variable could be reassigned to a new session:

.. code:: python

   syc_session = pysystemcoupling.launch()

   # Ok
   syc_session.ping()

The ``Session`` class supports the Python `context manager protocol`. This means that
if a ``Session`` is created using a Python ``with`` statement, it is automatically
cleaned up --- that is, ``exit`` called on it --- on leaving the scope of the ``with``.

.. code:: python

   with pysystemcoupling.launch() as syc_session:
      # Use syc_session
      ...
      # No need to call syc_session.exit() at the end

   # syc_session has been exited at this point



Logging
=======
Some basic logging capabilities are accessible via the ``LOG`` object. This is built on the standard Python logging framework
and allows you to set a `level` as a severity filter, and to specify whether logging goes to a file and/or to the console.

.. code:: python

   from ansys.systemcoupling.core import LOG

   ...
   LOG.set_level("ERROR") # Log at level Error or more severe
   LOG.log_to_stdout()






