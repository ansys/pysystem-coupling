.. _getting_started:

===============
Getting Started
===============
To run PySystemCoupling, you must have a local copy of Ansys System Coupling.
Although Ansys System Coupling itself does not need a license to enable it,
licenses will be needed for all Ansys produces involved in your coupled analysis.

PySystemCoupling supports Ansys System Coupling versions 2023 R1 or newer.

Visit `Ansys <https://www.ansys.com/>`_ for more information on
getting a licensed copy of Ansys products.

************
Installation
************

Python Module
~~~~~~~~~~~~~
The ``ansys-systemcoupling-core`` package currently supports Python 3.7 through
Python 3.10 on Windows and Linux. (**THIS NEEDS TO BE VERFIIED!**)

(**NB - Not yet, until released**) Install the latest release from `PyPi
<https://pypi.org/project/ansys-systemcoupling-core/>`_ with:

.. code::

   pip install ansys-systemcoupling-core

Alternatively, install the latest from `PySystemCoupling GitHub
<https://github.com/pyansys/pysystem-coupling/issues>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pysystem-coupling.git


For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pysystem-coupling.git
   cd pysystem-coupling
   pip install -e .

*************************
Launching System Coupling
*************************

You can launch System Coupling from Python using the ``launch`` function:

.. code:: python

  import ansys.systemcoupling.core as pysystemcoupling
  syc = pysystemcoupling.launch()
  syc.ping() # TODO: replace with health check

System Coupling is now active and ready to be used as a service. For details of
using the PySystemCoupling interface, see :ref:`ref_user_guide`.
