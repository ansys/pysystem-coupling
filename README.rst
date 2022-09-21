PySystemCoupling
================
|pyansys| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/

.. |GH-CI| image:: https://github.com/pyansys/pysystem-coupling/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/pyansys/pysystem-coupling/actions/workflows/ci_cd.yml

.. |codecov| image:: https://codecov.io/gh/pysystem-coupling/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pysystem-coupling

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black

--------
The PySystemCoupling project provides Pythonic access to Ansys System
Coupling. Although the System Coupling product itself exposes a
Python-based scripting and command line interface, this is embedded in
the product and is based on a specific version of Python. PySystemCoupling,
in contrast, enables seamless use of System Coupling within the Python
ecosystem, providing:

* Ability to launch System Coupling using a local Ansys installation.
* Access to APIs to set up and solve coupled analyses.
* Full access to the System Coupling data model via a convenient and Pythonic interface.

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


Documentation and Issues
------------------------

TODO

Usage
-----

It is assumed that an Ansys installation is available, and that it
includes System Coupling and the participant products needed for the coupled analysis.

The System Coupling installation will be found by examining via the following environment variables
in the given order:

* ``SYSC_ROOT``
* ``AWP_ROOT``
* ``AWP_ROOT231``

Note that if a variable is set but is found not to refer to a valid installation, PySystemCoupling
will fail at that point rather than attempting to use the next variable.

In a standard user installation, the expectation is that only ``AWP_ROOT231`` would be set.

The System Coupling API is exposed to PySystemCoupling in two basic forms:

* A documented interface based on concrete Python classes, following `Pythonic` conventions.
* A dynamic, undocumented (in PySystemCoupling), interface that replicates the `native` System Coupling API.

Both forms are strongly related to each other. A key difference in the Pythonic API is that naming is adjusted, in a generally predictable manner,
to follow Python conventions. Users who are already familiar with System Coupling should find it easy to adjust to this form, which is the recommended
API, but the native form is made available as a convenience, particularly to user who might be transitioning existing scripts.
It should be noted that, while most commands should work as expected via the native API, no guarantees can be given because of the nature of how it is exposed.

The following example shows the set up and solve of the "oscillating plate" tutorial in the Pythonic API, using Ansys Fluent as the CFD solver.

.. code:: python

   import ansys.systemcoupling.core as pysystemcoupling

   syc = pysystemcoupling.launch()
   setup = syc.setup
   setup.add_participant(input_file="mapdl.scp")
   setup.add_participant(input_file="fluent.scp")

   ## Create interfaces and data transfers by specifying participant regions

   interface_name = "interface-1"
   interface = setup.coupling_interface.create(interface_name)
   interface.side["One"].coupling_participant = "MAPDL-1"
   interface.side["One"].region_list = ["FSIN_1"]
   interface.side["Two"].coupling_participant = "FLUENT-2"
   interface.side["Two"].region_list = ["wall_deforming"]

   # Use commands to add data transfers
   force_transfer_name = setup.add_data_transfer(
      interface=interface_name,
      target_side="One",
      side_one_variable="FORC",
      side_two_variable="force",
   )

   disp_transfer_name = setup.add_data_transfer(
      interface=interface_name,
      target_side="Two",
      side_one_variable="INCD",
      side_two_variable="displacement",
   )

   # Change analysis duration and step size
   setup.solution_control.time_step_size = "0.1 [s]"
   setup.solution_control.end_time = "1.0 [s]"

   # Set output control settings
   setup.output_control.option = "StepInterval"
   setup.output_control.output_frequency = 2

   # Start streaming standard output from server
   syc.start_output()

   # Solve
   solution = syc.solution
   solution.solve()

Note that the API is divided into a number of "areas". These are represented as "root" attributes from which
an appropriate group of commands may be accessed. The above example shows ``setup`` and ``solution``. ``setup`` is the largest part of the
API, and is where one finds all of the commands related to populating the settings that define a coupled analysis. It also provides
direct access to the hierarchical data model, as illustrated in the example. ``solution`` is home to ``solve`` and a few other related
operations. There is also a ``case`` attribute available (not illustrated), for case file and persistence related commands.

In this example, the System Coupling server was started by the ``launch`` function. Alternatively, the server can be started in advance with
command line arguments ``-m cosimgui --grpcport=<host:port>`` and ``pysystemcoupling.connect(host, port)`` called instead of
``pysystemcoupling.launch()`` in the above.

The following shows the use of the native form of the API. This involves setting up the same analysis as above; it is less complete but
should be sufficient to illustrate the differences and connections between the API forms.


.. code:: python

   import ansys.systemcoupling.core as pysystemcoupling
   syc = pysystemcoupling.launch()
   native_api = syc._native_api

   native_api.AddParticipant(InputFile = 'mapdl.scp')
   native_api.AddParticipant(InputFile = 'fluent.scp')

   interface = native_api.CouplingInterface['interface-1']
   interface.Side['One'].CouplingParticipant = 'MAPDL-1'
   ...

   native_api.SolutionControl.TimeStepSize = "0.1 [s]"
   ...
   syc.start_output()
   native_api.Solve()

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
