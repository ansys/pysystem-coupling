# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""".. _ref_oscillating_plate_example:

Oscillating plate
-----------------

This example is a version of the *Oscillating Plate* case that is
often used as a tutorial for System Coupling. This two-way, fluid-structural
interaction (FSI) case is based on co-simulation of a transient oscillating
plate with 2D data transfers.

- Ansys Mechanical APDL (MAPDL) is used to perform a transient structural analysis.
- Ansys Fluent is used to perform a transient fluid-flow analysis.
- System Coupling coordinates the simultaneous execution of the solvers for
  these Ansys products and the data transfers between their coupled surface regions.

**Problem description**

An oscillating plate resides within a fluid-filled cavity. A thin plate is
anchored to the bottom of a closed cavity filled with fluid (air):

.. image:: /_static/img_oscplate_case.png
   :width: 400pt
   :align: center

There is no friction between the plate and the side of the cavity. An
initial pressure of 100 Pa is applied to one side of the thin plate
for 0.5 seconds to distort it. Once this pressure is released, the plate
oscillates back and forth to regain its equilibrium, and the
surrounding air damps this oscillation. The plate and surrounding
air are simulated for a few oscillations to allow an examination of the
motion of the plate as it is damped.

"""

# %%
# Set up example
# --------------
# Setting up this example consists of performing imports, downloading
# input files, preparing the directory structure, and launching System Coupling.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the ``ansys-systemcoupling-core`` package and other required packages.

# sphinx_gallery_thumbnail_path = '_static/oscplate_displacement.png'
import os
from pprint import pprint

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download input files
# ~~~~~~~~~~~~~~~~~~~~
# Clear the downloads target directory (which is to be used as the
# working directory). Download the SCP files for Fluent and MAPDL, which
# provide solver-specifc information to System Coupling and the respective
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
# Prepare expected directory structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The target download directory is used as the working directory.
# The SCP files are defined such that there is expected to be a Fluent
# subdirectory in which Fluent runs and an MAPDL subdirectory in
# which MAPDL runs. These directories should contain their respective
# case and input files.

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
# Launch a remote System Coupling instance and return a *client* object
# (a ``Session`` object) that allows you to interact with System Coupling
# via an API exposed into the current Python environment.

syc = pysystemcoupling.launch(working_dir=working_dir)

# %%
# Create analysis
# ---------------
# Creating the analysis consists of accessing the ``setup`` API,
# loading participants, creating and verifying both interfaces and
# data transfers, querying for setup errors, and modifying settings.
#
# Access the ``setup`` API
# ~~~~~~~~~~~~~~~~~~~~~~~~
setup = syc.setup


# %%
# Load participants
# ~~~~~~~~~~~~~~~~~
# Use ``add_participant`` to create ``coupling_participant`` objects
# representing the Fluent and MAPDL participants, based on the data
# in the `scp` files that were previously exported by the respective
# products.
mapdl_part_name = setup.add_participant(input_file="mapdl.scp")
fluent_part_name = setup.add_participant(input_file="fluent.scp")

# %%
# Verify ``coupling_participant`` objects exist:
setup.coupling_participant.keys()

# %%
# Create interfaces and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create interfaces and data transfers by specifying participant regions.
# This consists of calling the appropriate commands to create an interface
# and both force and displacement data transfers.

interface_name = setup.add_interface(
    side_one_participant=mapdl_part_name,
    side_one_regions=["FSIN_1"],
    side_two_participant=fluent_part_name,
    side_two_regions=["wall_deforming"],
)

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
# Verify creation of interfaces and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Confirm the coupling interface exists.
setup.coupling_interface.keys()

# %%
# Examine the coupling interface state. Note that
# ``data_transfer`` child objects exist for ``"displacement"``
# and ``"FORC"``.
setup.coupling_interface[interface_name].print_state()


# %%
# Query for setup errors
# ~~~~~~~~~~~~~~~~~~~~~~
# A coupled analysis setup cannot be solved if errors
# exist. Errors are indicated by messages with
# the ``level`` field set to ``Error``. Here, there are
# two missing settings that must be corrected.
# There is also an ``Information`` level message that
# advises that, once the current setup is solved, it is
# not possible to restart it from any point except the
# last step.

pprint(setup.get_status_messages())

# %%
#   .. note::
#      In the current release of PySystemCoupling, the ``get_status_messages``
#      class provides messages generated by System Coupling using its native
#      terminology. This means that any identifiers for settings that are
#      mentioned in messages are in System Coupling's usual *camel case* format.
#
#      In most cases, it should be obvious how to translate to the
#      *snake case* format for the corresponding PySystemCoupling setting.
#      For example, the ``EndTime`` setting in System Coupling's
#      ``OutputControl`` object corresponds to the ``output_control.end_time``
#      setting in PySystemCoupling.

# %%
# Modify settings
# ~~~~~~~~~~~~~~~
# View contents of the ``solution_control`` object. Notice that
# the ``time_step_size`` and ``end_time`` settings are unset,
# consistent with what was shown in the status messages.
# Values shown in the ``print_state`` output as ``<None>``
# have Python values of ``None``.
setup.solution_control.print_state()


# %%
# Change the ``time_step_size`` setting.
setup.solution_control.time_step_size = "0.1 [s]"

# %%
# Verify the ``time_step_size`` setting.
setup.solution_control.time_step_size

# %%
# Change the ``end_time`` setting.
setup.solution_control.end_time = "1.0 [s]"

# %%
# View the ``output_control`` object.
setup.output_control.print_state()

# %%
# View the valid values for the ``option`` setting.
setup.output_control.get_property_options("option")

# %%
# Set the ``option`` setting.
setup.output_control.option = "StepInterval"

# %%
# Change the ``output_frequency`` frequency setting.
setup.output_control.output_frequency = 2

# %%
# View the ``output_control`` object again:
setup.output_control.print_state()

# %%
# Review setup
# ------------
# Verify that there are no longer any setup errors.
pprint(setup.get_status_messages())


# %%
# Use the ``get_setup_summary`` class to return a string showing a summary of
# the coupled analysis setup. This summary is also shown in the
# transcript output when the solve is started, but it can
# be useful to review this before starting the solve.
print(setup.get_setup_summary())


# %%
# Run solution
# ------------
# The System Coupling server's ``stdout`` and ``stderr`` output is not shown
# in PySystemCoupling by default. To see it, turn output streaming on.
syc.start_output()
# %%
# Access the ``solve`` command via the ``solution`` API.
solution = syc.solution
solution.solve()

# %%
# Extend analysis end time
# ------------------------
# Extend the analysis end time for a restarted run.
# Access the ``case`` attribute for file handling and persistence.
# Use this attribute to completely clear the current case and reload
# from the case saved during the solve.
case = syc.case
case.clear_state()
case.open()


# %%
# Extend analysis
# ~~~~~~~~~~~~~~~
#
# View the ``solution_control`` object, change the ``end-time`` setting,
# and verify the setting change.
# This code extends the analysis to 1.5 seconds.
setup.solution_control.print_state()
setup.solution_control.end_time = "1.5 [s]"
setup.solution_control.print_state()

# %%
# Change additional settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Examine ``"Force"`` data transfer.
force_transfer = setup.coupling_interface[interface_name].data_transfer[
    force_transfer_name
]
force_transfer.print_state()

# %%
# Change a setting in the ``"Force"`` data transfer and increase the
# minimum iterations value in the ``solutions_control`` object from its default
# value of 1 to 2.
force_transfer.convergence_target = 0.001

setup.solution_control.minimum_iterations = 2

# %%
# Review setup
# ~~~~~~~~~~~~
# To review the setup again, use the ``get_setup_summary`` class to return a string
# showing a summary.
print(setup.get_setup_summary())

# %%
# Restart solution
# ----------------
# To restart the solution, access the ``solve`` command via the ``solution`` API.
solution.solve()

# %%
# Stop streaming output and shut down the server instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Stop streaming output from the server and shut down the server instance.
syc.end_output()
syc.exit()

# %%
# .. note::
#    This ``syc`` object is now *defunct*. Any attempt to
#    use it to perform a further action yields an error. To do
#    more in the current Python session, you must create a new ``syc`` instance
#    using ``syc = pysystemcoupling.launch()``.
