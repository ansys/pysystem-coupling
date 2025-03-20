PySystemCoupling
================

|pyansys| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/

.. |GH-CI| image:: https://github.com/ansys/pysystem-coupling/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/ansys/pysystem-coupling/actions/workflows/ci.yml

.. |codecov| image:: https://codecov.io/gh/pysystem-coupling/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pysystem-coupling

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black

Overview
--------
PySystemCoupling provides Pythonic access to Ansys System
Coupling. Although this Ansys product exposes its own
Python-based scripting and command line interface, it is embedded
and based on a specific version of Python. In contrast,
PySystemCoupling enables seamless use of System Coupling within the Python
ecosystem, providing additional capabilities, including:

* Ability to launch System Coupling using a local Ansys installation
* Access to APIs to set up and solve coupled analyses
* Full access to the System Coupling data model via a convenient and Pythonic interface

Installation
------------
Install PySystemCoupling with this command:

.. code::

   pip install ansys-systemcoupling-core


Alternatively, clone and install PySystemCoupling in *development mode*
with this code:

.. code::

   git clone https://github.com/ansys/pysystem-coupling.git
   cd pysystem-coupling
   python -m pip install --upgrade pip
   pip install -e .
   pip install .[classesgen]
   python scripts\generate_datamodel.py


Documentation and Issues
------------------------

For more information, see the `Documentation <https://systemcoupling.docs.pyansys.com>`_ page.

Use the `PySystemCoupling Issues <https://github.com/ansys/pysystem-coupling/issues>`_ page to
post bug reports, questions and feature requests.

Usage
-----

It is assumed that an Ansys installation is available and that this installation
includes System Coupling and the participant products needed for the coupled analysis.

The System Coupling installation is found by examining the following environment variables
in this order:

* ``SYSC_ROOT``
* ``AWP_ROOT``
* ``AWP_ROOT251``

If a variable is set but does not refer to a valid installation, PySystemCoupling
fails at that point, rather than attempting to use the next variable.

In a standard user installation, the expectation is that only ``AWP_ROOT251`` is set.

(It is also possible to provide a different version number as an argument to the ``launch()``
function. This will affect which ``AWP_ROOT<version>`` environment variable is examined.)

   **WARNING**

   There is an issue with the 25 R1 release of Ansys System Coupling that prevents it from
   working in the gRPC server mode on which PySystemCoupling depends. A small patch
   is available that may be applied to some of the Python files in the System Coupling
   installation. This is provided in the ``patches/`` directory of this repository and will
   allow System Coupling to work with the current release of PySystemCoupling.

   Otherwise, PySystemCoupling should be used with an earlier release of System Coupling by
   setting the environment variable ``AWP_ROOT`` or specifying the version number as an
   argument to the ``launch()`` function.


The System Coupling API is exposed to PySystemCoupling in two forms:

* A documented interface based on concrete Python classes, following Pythonic conventions
* A dynamic interface, undocumented in PySystemCoupling, that replicates the native System Coupling API

Both forms are strongly related to each other. A key difference in the Pythonic API is that naming
is adjusted, in a generally predictable manner, to follow Python conventions. If you are already
familiar with System Coupling, adjusting to this form, which is the recommended API, should be easy.
However, if you are transitioning existing scripts, the native System Coupling API is made available
as a convenience.

   **Note**

   While most commands should work as expected via the native System Coupling API,
   no guarantees can be given because of the nature of how it is exposed.

This example shows how to set up and solve an oscillating plate example in the Pythonic API.
It uses Ansys Fluent as the CFD solver.

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


The Pythonic API partitions commands via three high-level *root* attributes of the
``Session`` class: ``setup``, ``solution``, and ``case``. The preceding example
uses both the ``setup`` and ``solution`` attributes.

* The ``setup`` attribute is the largest part of the API. It is where you find all
  commands related to populating the settings that define a coupled analysis. This
  attribute also provides direct access to the hierarchical data model.
* The ``solution`` attribute is home to commands related to solving an analysis and
  examining the solution.
* The ``case`` attribute, which is not used in the preceding example, provides all
  commands related to case file management and persistence.

While the preceding example uses the ``pysystemcoupling.launch()`` method to start the
System Coupling server, alternatively, the server can be started in advance by calling
command line arguments ``-m cosimgui --grpcport=<host:port>`` and
``pysystemcoupling.connect(host, port)``.

This next example shows how to set up the same analysis using the native System Coupling
API. While the code here is less complete than the code shown previously, it should
sufficiently illustrate the differences and connections between the two API forms.

.. code:: python

   import ansys.systemcoupling.core as pysystemcoupling

   syc = pysystemcoupling.launch()
   native_api = syc._native_api

   native_api.AddParticipant(InputFile="mapdl.scp")
   native_api.AddParticipant(InputFile="fluent.scp")

   interface = native_api.CouplingInterface["interface-1"]
   interface.Side["One"].CouplingParticipant = "MAPDL-1"
   ...

   native_api.SolutionControl.TimeStepSize = "0.1 [s]"
   ...
   syc.start_output()
   native_api.Solve()


License
-------
PySystemCoupling is licensed under the MIT license.

The ``ansys-systemcoupling-core`` package makes no commercial claim over Ansys
whatsoever.  It extends the functionality of Ansys System Coupling by
adding a Python interface to the System Coupling service without changing the
core behavior or license of the original software. Interactively controlling
System Coupling via PySystemCoupling requires a local copy of System Coupling
and licenses for all Ansys products involved in your coupled analysis.

To get a copy of Ansys, visit `Ansys <https://www.ansys.com/>`_.
