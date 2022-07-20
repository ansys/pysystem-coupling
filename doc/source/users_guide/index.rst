.. _ref_user_guide:

==========
User Guide
==========
This guide provides information regarding using Ansys PySystemCoupling and its
constituent modules and components.


..
   This toctreemust be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   launching_ansys_system_coupling
   analysis_setup


PySystemCoupling Basic Overview
===============================
Analysis objects are the main entry point when using the PySystemCoupling library. Each such object
is associated with a System Coupling server session and provides access to an API that allows a
System Coupling analysis to be set up and solved. One or more such analyses/System Coupling server
sessions may be launched simultaneously from the client. For example:

.. code:: python

   syc_analysis = pysystemcoupling.launch()
