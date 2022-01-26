PySystemCoupling
################

The System Coupling API exposed as a Python package.

Project Overview
----------------
Although the System Coupling product itself exposes a Python-based scripting
and command line interface, this is embedded in the product and is based
on a specific version of Python. This is not amenable to incorporation
in systems that make extensive use of the Python ecosystem.

To support the broader PyAnsys initiative, therefore, PySystemCoupling
offers a lightweight Python package that exposes an API similar to
System Coupling's built-in scripting interface.

In the current version, this library is expected to be used in a
desktop environment with System Coupling running, as a background
server, from an installation on the user's machine.

Note: the API is currently exposed more or less in the form that exists
in System Coupling itself. This means that property names, method names,
etc., generally do not conform to standard Python naming conventions.
The expectation is that in due course we will migrate PySystemCoupling
to use standard conventions in such a way that here will be a largely
predictable mapping between the exposed and internal forms of the names.

Installation
------------
Install PySystemCoupling with:

.. code::

   pip install ansys-systemcoupling-core

Alternatively, clone and install in development mode with:

.. code::

   git clone https://github.com/pyansys/pysystem-coupling.git
   cd pysystem-coupling
   pip install -e .


Documentation
-------------

TODO

Usage
-----

It is assumed that an Ansys installation is available and that it
includes System Coupling and the participant products that are
needed for the coupled analysis.

Currently, by default, System Coupling will be found via the
``AWP_ROOT222`` environment variable. The ``SystemCoupling``
directory is expected to be immediately below the directory
specified by the variable.

The System Coupling installation location may be overridden by
setting the ``SYSC_ROOT``  environment variable.

The following example shows the set up and solve of the "oscillating plate"
tutorial, using Ansys Fluent as the CFD solver.

.. code:: python

   >>> import ansys.systemcoupling.core as pysystemcoupling
   >>> syc = pysystemcoupling.launch_syc()
   >>> syc.AddParticipant(InputFile = 'mapdl.scp')
   >>> syc.AddParticipant(InputFile = 'fluent.scp')
   >>> interface = syc.CouplingInterface['interface-1']
   >>> interface.Side['One'].CouplingParticipant = 'MAPDL-1'
   >>> interface.Side['One'].RegionList = ['FSIN_1']
   >>> interface.Side['Two'].CouplingParticipant = 'FLUENT-2'
   >>> interface.Side['Two'].RegionList = ['wall_deforming']
   >>> interface.DataTransfer['transfer-1'].TargetSide = 'One'
   >>> interface.DataTransfer['transfer-1'].TargetVariable = 'FORC'
   >>> interface.DataTransfer['transfer-1'].SourceVariable = 'force'
   >>> interface.DataTransfer['transfer-2'] = {'TargetSide': 'Two',
   ...                                         'SourceVariable': 'INCD',
   ...                                         'TargetVariable': 'displacement'}
   >>> syc.SolutionControl.MaximumIterations = 3
   >>> syc.Solve()
   >>> syc.exit()

In this example, the System Coupling server was started by the ``launch_syc``
function. Alternatively, the server can be started in advance with
command line arguments ``-m cosimtest --srvport=<host:port>`` and
``pysystemcoupling.connect_to_syc(host, port)`` called instead of
``pysystemcoupling.launch_syc()`` in the above.



License
-------
``PySystemCoupling`` is licensed under the MIT license.

This module, ``ansys-systemcoupling-core`` makes no commercial claim over Ansys
whatsoever.  This tool extends the functionality of ``System Coupling`` by
adding a Python interface to the System Coupling service without changing the
core behavior or license of the original software.  The use of the
interactive System Coupling control of ``PySystemCoupling`` requires a legally licensed
local copy of Ansys.

To get a copy of Ansys, please visit `Ansys <https://www.ansys.com/>`_.
