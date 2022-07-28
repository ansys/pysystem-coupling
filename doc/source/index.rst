PySystemCoupling Documentation |version|
========================================

.. toctree::
   :hidden:
   :maxdepth: 2

   getting_started/index
   users_guide/index
   api/index
   contributing

NOTE
----

The PySystemCoupling documentation is under development and none of the content should be relied on.

Its current state reflects work on the following aspects:

* Setting out of the approximate structure intended in the final documentation.
* Development of infrastructure for automatic API generation.

The content itself is incomplete and possibly incorrect in places.


Introduction
------------
The Ansys portfolio of simulation software facilitates the creation of multidisciplinary physics analyses — 
not only within the context of a single product, but also through the use of Ansys `System Coupling`. 

System Coupling can integrate multiple individual analyses, enabling you to leverage different physics 
solvers and/or static external data sources in a single multiphpysics simulation. When two or more analyses
are coupled, an examination of their combined results can capture more complex interactions than an 
examination of those results in isolation, producing more accurate results and yielding an optimal solution.

What is PySystemCoupling?
-------------------------

PySystemCoupling is part of the `PyAnsys <https://docs.pyansys.com>`_ ecosystem that
lets you use Ansys System Coupling within or alongside any other Python environment,
whether it is in conjunction with other Ansys Python libraries and packages or
with other external Python products.

...etc etc ... see PyFluent and others for guidance on content here ...


License
-------
PySystemCoupling is licensed under the MIT license.

This module makes no commercial claim over Ansys whatsoever. PySystemCoupling extends
the functionality of Ansys System Coupling by adding an additional Python interface to
Ansys System Coupling without changing the core behavior or license of the original
software. The use of the interactive control of PySystemCoupling requires a legally
licensed local copy of Ansys System Coupling. For more information about Ansys System Coupling,
visit the Ansys System Coupling page on the Ansys website.

Project Index
-------------

* :ref:`genindex`