.. _ref_user_guide:

==========
User Guide
==========
This guide provides a general overview of the basics and usage of the PySystemCoupling library.

Although this guide does provide a brief overview of the main concepts in System Coupling, it is
not intended to be a comprehensive introduction to cosimulation and the use of System Coupling.
The focus will be on guiding the use of PySystemCoupling client library to access System
Coupling features.

.. note::
   Users who are licensed to use System Coupling may consult the product documentation for
   a detailed introduction, illustrated with tutorial examples. The
   steps in the documentation that refer to the Command Line Interface (CLI) will be those
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
To confirm that there is a functioning connection to the System Coupling server, the ``ping`` method may be called.

.. code:: python

   syc_session.ping()

``ping`` returns ``True`` if a simple call can succesfully be made on System Coupling's `gRPC` server. Otherwise,
the attempt to make the call will raise an exception.


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

Logging
=======
Some basic logging capabilities may be accessed via the ``LOG`` object. This is built on the standard Python logging framework
and allows a `level` to be set as a severity filter, and allows logging to a file and/or to the console.

.. code:: python

   from ansys.systemcoupling.core import LOG

   ...
   LOG.set_level("ERROR") # Log at level Error or more severe
   LOG.log_to_stdout()






