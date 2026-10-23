PySystemCoupling documentation |version|
########################################

.. toctree::
   :hidden:
   :maxdepth: 2

   getting_started/index
   users_guide/index
   examples/index
   api/index
   contributing

What is Ansys System Coupling?
==============================
The Ansys portfolio of simulation software facilitates the creation of multidisciplinary physics analyses,
not only within the context of a single product but also through the use of Ansys System Coupling.

System Coupling is software for solving multiphysics problems by connecting independent physics
solvers and coordinating the exchange of the solution data. This enables accurate capturing of the
complex interactions between physical models, typically simulated in separate solvers.

System Coupling connects to several existing Ansys physics solvers, including Ansys CFX,
Ansys Forte, Ansys MAPDL, and Ansys Electronics Desktop. Examples of problems that can be solved
by System Coupling include Fluid-Structure Interaction (FSI), Conjugate Heat Transfer (CHT), and Joule
Heating.

System Coupling capabilities include the ability to:

* Solve steady and transient coupled analyses
* Couple surface and volume regions
* Couple any scalar or vector, real or complex fields

What is PySystemCoupling?
=========================
PySystemCoupling is part of the `PyAnsys <https://docs.pyansys.com>`_ ecosystem. It lets you
use System Coupling within or alongside any Python environment, whether in conjunction
with other Ansys Python libraries and packages or with other external Python products.

PySystemCoupling implements a client-server architecture. Internally, it uses
`Google remote procedure call` (`gRPC`) interfaces to launch or connect
with a running System Coupling process as a server. However, you only need to interact
with the Python interface.

You can use PySystemCoupling to programmatically create, interact with, and control a
System Coupling session to create your own customized workspace. In addition, you can
use PySystemCoupling to enhance your productivity with highly configurable,
customized scripts.

License
-------
PySystemCoupling is licensed under the MIT license.

The ``ansys-systemcoupling-core`` package makes no commercial claim over Ansys
whatsoever.  It extends the functionality of Ansys System Coupling by
adding a Python interface to the System Coupling service without changing the
core behavior or license of the original software. Interactively controlling
System Coupling via PySystemCoupling requires a legally licensed
local copy of System Coupling.

.. TODO Add the appropriate link when available.

For more information about System Coupling,
visit the Ansys System Coupling page on the Ansys website.

Project index
==============

* :ref:`genindex`
