.. _ref_syc_datamodel:

System Coupling Data Model
==========================

Data Model Structure
--------------------

The following shows the main hierarchy of the "objects" in the data model.

participant
	variable
	region
analysis_control
coupling_interface
	side
	data_transfer
solution_control
output_control

The italicized names represent those for which more than one instance may exist --- each instance is given a name. (Side is unusual in that exactly two instances exist, with fixed names “One” and “Two”.)
The non-italic names

Accessing the Data Model
------------------------

The data model is accessed via the setup attribute of ``Session``. The objects in the data model are
attributes of setup.

.. code:: python

   ...
   setup = syc_session.setup
   analysis_control = setup.analysis_control

Such objects hold a collection of primitive settings, named values of type integer, boolean, string, etc.
These are also accessed