""".. _ref_oscillating_plate_example:

Oscillating Plate tutorial case
-------------------------------

This example is a version of the `Oscillating Plate` case, which is
often used as an introductory tutorial case for System Coupling. It
is a two-way fluid-structural interaction (FSI) case, based on transient
oscillating plate co-simulation with 2D data transfers.

In this version, MAPDL performs a transient-structural analysis and
Fluent performs a transient fluid-flow analysis, while System Coupling
coordinates the simultaneous execution of the solvers and the data
transfers between their coupled surface regions.

Problem description
~~~~~~~~~~~~~~~~~~~

This tutorial uses an example of an oscillating plate within a
fluid-filled cavity. A thin plate is anchored to the bottom of
a closed cavity filled with fluid (air), as shown in the image below.

There is no friction between the plate and the side of the cavity. An
initial pressure of 100 Pa is applied to one side of the thin plate
for 0.5 s to distort it. Once this pressure is released, the plate
oscillates back and forth to regain its equilibrium, and the
surrounding air damps this oscillation. The plate and surrounding
air are simulated for a few oscillations to allow an examination of the
motion of the plate as it is damped.

.. image:: /_static/img_oscplate_case.png
   :width: 400pt
   :align: center

"""

# sphinx_gallery_thumbnail_path = '_static/oscplate_displacement.png'

# %%
# Example Setup
# -------------
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the PySystemCoupling package and other required imports, and download
# the input files for this example.

import os
from pprint import pprint
import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download the input files for this example
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Clear the downloads target directory (which we are going to use as our
# working directory). Download the "SCP" files for Fluent and MAPDL, which
# provide solver-specifc  information to System Coupling, and the respective
# solver input files for each solver run.
#

examples.delete_downloads()

mapdl_scp_file = examples.download_file(
    "mapdl.scp", "pysystem-coupling/oscillating_plate"
)

fluent_scp_file = examples.download_file(
    "fluent.scp", "pysystem-coupling/oscillating_plate"
)

mapdl_dat_file = examples.download_file(
    "mapdl.dat", "pysystem-coupling/oscillating_plate/MAPDL"
)

fluent_cas_file = examples.download_file(
    "plate.cas.gz", "pysystem-coupling/oscillating_plate/Fluent"
)

# %%
#
# Prepare the expected directory structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# We will use the target download directory as our working directory.
# The SCP files are defined such that there is expected to be a Fluent
# sub-directory in which Fluent runs, and an MAPDL sub-directory in
# which MAPDL runs. These directories should contain their respective
# input/case files.

working_dir = os.path.dirname(mapdl_scp_file)

fluent_working_dir = os.path.join(working_dir, "Fluent")
os.mkdir(fluent_working_dir)
mapdl_working_dir = os.path.join(working_dir, "MAPDL")
os.mkdir(mapdl_working_dir)

os.rename(fluent_cas_file, os.path.join(fluent_working_dir, "plate.cas.gz"))
os.rename(mapdl_dat_file, os.path.join(mapdl_working_dir, "mapdl.dat"))

# %%
#
# Launch System Coupling
# ~~~~~~~~~~~~~~~~~~~~~~
# Launch a remote System Coupling instance and return a "client" object
# (a ``Session`` object) that allows us to interact with System Coupling
# via an API exposed into the current Python environment.

syc = pysystemcoupling.launch(working_dir=working_dir)

# %%
# Create analysis
# ~~~~~~~~~~~~~~~
#
# Access the `setup` API:
setup = syc.setup


# %%
# Load participants
# ^^^^^^^^^^^^^^^^^
# Use ``add_participant`` to create ``coupling_participant`` objects
# representing the Fluent and MAPDL participants, based on the data
# in the `scp` files that were previously exported by the respective
# products.
setup.add_participant(input_file="mapdl.scp")
setup.add_participant(input_file="fluent.scp")

# %%
# Verify that the ``coupling_participant`` objects now exist:
setup.coupling_participant.keys()

# %%
# Create interfaces and data transfers by specifying participant regions
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# `Note`: instead of direct datamodel assignment, we could have used
# the command ``setup.add_interface(...)``. This would have been
# closer to the original tutorial and is usually the recommended
# approach. However, the following provides
# an illustration of creating a datamodel object directly via the
# PySystemCoupling API.

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

# %%
# Verify creation of interface and data transfers
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Coupling interface exists:
setup.coupling_interface.keys()

# %%
# Coupling interface state. Note the "FORC" and "displacement"
# ``data_transfer`` child objects:
setup.coupling_interface[interface_name].print_state()


# %%
# Query for any current setup errors
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# A coupled analysis setup cannot be solved if there
# are any errors. Errors are indicated by messages with
# ``level`` field set to ``Error``. Here, it is seen that
# there are two missing settings that need to be corrected.
# There is also an ``Information`` level message that
# advises that, once the current setup is solved, it will
# not be possible to restart it from any point except the
# last step.

pprint(setup.get_status_messages())

# %%
#   .. note::
#      In the current release of PySystemCoupling, ``get_status_messages``
#      provides messages generated by System Coupling using its native
#      terminology. This means that any settings identifiers that are
#      mentioned in messages will be in System Coupling's usual `camel case` format.
#
#      In most cases, it should be obvious how to translate to the
#      corresponding PySystemCoupling setting. For example ``EndTime``
#      in System Coupling's ``OutputControl`` object corresponds to the
#      PySystemCoupling ``output_control.end_time`` setting.

# %%
# Modify settings
# ^^^^^^^^^^^^^^^
#
# View contents of `solution_control`. Notice that
# ``time_step_size`` and ``end_time`` are unset,
# consistent with what was shown in the status messages.
# Values shown in the ``print_state`` output as ``<None>``
# actually have Python values of ``None``.
setup.solution_control.print_state()


# %%
# Change `time_step_size` setting:
setup.solution_control.time_step_size = "0.1 [s]"

# %%
# Verify setting:
setup.solution_control.time_step_size

# %%
# Change `end_time`:
setup.solution_control.end_time = "1.0 [s]"

# %%
# View `output_control`:
setup.output_control.print_state()

# %%
# Set `option` in `output_control`. First, see valid options:
setup.output_control.get_property_options("option")

# %%
# Set output option:
setup.output_control.option = "StepInterval"

# %%
# View `output_control` again:
setup.output_control.print_state()

# Change `output_frequency`:
setup.output_control.output_frequency = 2

# %%
# Review setup
# ~~~~~~~~~~~~
#
# Verify that there are no longer any setup errors:
pprint(setup.get_status_messages())


# %%
# ``get_setup_summary`` returns a string showing a summary of
# the coupled analysis setup. This will also be shown in the
# transcript output when the solve is started, but it can
# be useful to review this before starting the solve.
print(setup.get_setup_summary())


# %%
# Run solution
# ------------
#
# Access `solve` via the `solution` API.
solution = syc.solution
solution.solve()

# %%
# Extend analysis end time for a restarted run
# --------------------------------------------
#
# Access the `case` API for file handling and persistence.
# Use this to completely clear the current case and reload
# from the case saved during the solve.
case = syc.case
case.clear_state()
case.open()


# %%
# Extend analysis
# ~~~~~~~~~~~~~~~
#
# View `solution_control`, change `end-time` and verify setting.
# The analysis is extended to 1.5 seconds.
setup.solution_control.print_state()
setup.solution_control.end_time = "1.5 [s]"
setup.solution_control.print_state()

# %%
# Additional settings changes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Examine "Force" data transfer.
force_transfer = setup.coupling_interface[interface_name].data_transfer[
    force_transfer_name
]
force_transfer.print_state()

# %%
# Change `convergence_target` and `ramping_option` of "Force" data
# transfer, and set minimum iterations value.
force_transfer.convergence_target = 0.001
force_transfer.ramping_option = "Linear"

setup.solution_control.minimum_iterations = 2

# %%
# Review setup
# ~~~~~~~~~~~~
print(setup.get_setup_summary())

# %%
# Restart solution
# ----------------
solution.solve()

# %%
# Stop streaming output from server and shut down this server instance:
syc.end_output()
syc.exit()

# %%
# .. note::
#    This `syc` object is now "defunct" and any attempt to
#    use it to perform any further actions will yield an error. To do
#    more in the current Python session, create a new syc instance
#    using ``syc = pysystemcoupling.launch()`` again.)
