.. _ref_user_guide:


User guide
##########
This section provides an overview of PySystemCoupling and how to use it.

Although this section describes some main System Coupling concepts, it is
not intended to be an introduction to cosimulation and the use of System Coupling.
The focus here is on guiding the use of PySystemCoupling to access System Coupling features.

.. note::
   If you are licensed to use System Coupling, you can consult the System Coupling
   product documentation for detailed product information and tutorial examples. The
   steps in the product documentation that refer to the command-line interface (CLI) are those
   that are most readily translated to the PySystemCoupling environment.

..
   This toctreemust be a top-level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   system_coupling_concepts
   syc_datamodel
   analysis_setup
   syc_solution
   syc_persistence



Launch() function
=================
The ``launch()`` function in PySystemCoupling creates an instance of
System Coupling in the background and sends commands to this service.


.. code-block:: python

   syc_session = pysystemcoupling.launch()


The ``launch()`` function returns a ``Session`` object.

Session object
==============
A ``Session`` object is the client-side access point in PySystemCoupling to a System Coupling server instance.
This object exposes an API that allows a System Coupling analysis to be set up and solved. One or more
such server sessions can be launched simultaneously from the client.

In addition to providing an API for setting up and solving coupled analyses, the``Session``
object provides access to a few basic capabilities described in the sections that follow.

Connection check
----------------
To confirm that there is a functioning connection to the System Coupling server, call the ``ping`` method
with this command:

.. code-block:: python

   syc_session.ping()


The ``ping`` method returns ``True`` if a simple call can successfully be made on System Coupling's
`gRPC` server. Otherwise, the attempt to make the call raises an exception.


Output streaming
----------------
By default, any output that the System Coupling server process prints to its standard output streams
(``stdout`` and ``stderr``) is not shown. Output is streamed to the PySystemCoupling session and
printed to its console when the following code is used to call the ``start_output()`` method:

.. code-block:: python

   syc_session.start_output()

You can turn off output streaming using this code to call the ``end_output()`` method:

.. code-block:: python

   syc_session.end_output()


Exiting
-------
When you are finished with a PySystemCoupling session, it is advisable to end it cleanly using the
``exit()`` method. Otherwise, PySystemCoupling still attempts to clean up active server sessions
when the Python environment is exited, which is naturally less reliable than a directed exit.

Once you use the following code to call the ``exit()`` method on a session object, the object
is no longer usable.

.. code-block:: python

   syc_session.exit()

   # Will raise exception!
   syc_session.ping()


However, you can reassign the ``syc_session`` variable to a new session with this code:

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
Some basic logging capabilities are accessible via the ``LOG`` object. Built on the
standard Python logging framework, this object allows you to set a log level as a severity
filter and to specify whether logging goes to a file, to the console, or to both.

.. code-block:: python

   from ansys.systemcoupling.core import LOG

   ...
   LOG.set_level("ERROR") # Log at level Error or more severe
   LOG.log_to_stdout()

