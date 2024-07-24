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
# Import ``ansys-systemcoupling-core``, ``ansys-fluent-core`` and
# ``ansys-mapdl-core`` and other required packages.

# sphinx_gallery_thumbnail_path = '_static/oscplate_displacement.png'

import ansys.fluent.core as pyfluent
import ansys.mapdl.core as pymapdl

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
#
# Download input file
# ~~~~~~~~~~~~~~~~~~~
# This example uses one pre-created file - a Fluent input file that contains
# the fluids setup.
#
fluent_cas_file = examples.download_file(
    "plate.cas.gz", "pysystem-coupling/oscillating_plate/Fluent"
)

# %%
# Launch and connect to System Coupling
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Launch a remote System Coupling instance and return a *client* object
# (a ``Session`` object) that allows you to interact with System Coupling
# via an API exposed into the current Python environment.
syc = pysyc.launch()


# %%
# Launch and connect to Fluent
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use the created ``fluent`` session object to read the case file.
fluent = pyfluent.launch_fluent(start_transcript=True)
fluent.file.read(file_type="case", file_name=fluent_cas_file)

# %%
# Launch and connect to MAPDL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use the ``mapdl`` session object to set up the structural side of the FSI
# case.
mapdl = pymapdl.launch_mapdl()
mapdl.prep7()

# %%
# Define material properties.
mapdl.mp("DENS", 1, 2550)  # density
mapdl.mp("ALPX", 1, 1.2e-05)  # thermal expansion coefficient
mapdl.mp("EX", 1, 2500000)  # Young's modulus
mapdl.mp("NUXY", 1, 0.35)  # Poisson's ratio

# %%
# Set element types to SOLID186.
mapdl.et(1, 186)
mapdl.keyopt(1, 2, 1)

# %%
# Make geometry.
mapdl.block(10.00, 10.06, 0.0, 1.0, 0.0, 0.4)
mapdl.vsweep(1)

# %%
# Add fixed support at y=0.
mapdl.run("NSEL,S,LOC,Y,0")
mapdl.d("all", "all")

# %%
# Add the FSI interface.
mapdl.run("NSEL,S,LOC,X,9.99,10.01")
mapdl.run("NSEL,A,LOC,Y,0.99,1.01")
mapdl.run("NSEL,A,LOC,X,10.05,10.07")
mapdl.cm("FSIN_1", "NODE")
mapdl.sf("FSIN_1", "FSIN", 1)

mapdl.allsel()

mapdl.run("/SOLU")

# %%
# Set analysis type to steady.
mapdl.antype(4)

mapdl.nlgeom("ON")  # large deformations
mapdl.kbc(1)
mapdl.trnopt("full", "", "", "", "", "hht")
mapdl.tintp(0.1)
mapdl.autots("off")
mapdl.run("nsub,1,1,1")
mapdl.run("time,10.0")
mapdl.timint("on")

# %%
# Create the coupled analysis
# ---------------------------
# Creating the analysis consists of accessing the ``setup`` API,
# adding the participants, creating and verifying both interfaces and
# data transfers, querying for setup errors, and modifying settings.
#
# Access the ``setup`` API
# ~~~~~~~~~~~~~~~~~~~~~~~~
setup = syc.setup

syc.setup.activate_hidden.beta_features = True
syc.setup.activate_hidden.alpha_features = True
syc.setup.activate_hidden.lenient_validation = True

# %%
# Add participants
# ~~~~~~~~~~~~~~~~
# Add the ``fluent`` and ``mapdl`` sessions as participants in the
# analysis.
fluid_name = syc.setup.add_participant(participant_session=fluent)
solid_name = syc.setup.add_participant(participant_session=mapdl)

syc.setup.coupling_participant[fluid_name].display_name = "Fluid"
syc.setup.coupling_participant[solid_name].display_name = "Solid"

# add a coupling interface
interface_name = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["wall_deforming"],
    side_two_participant=solid_name,
    side_two_regions=["FSIN_1"],
)

# set up 2-way FSI coupling - add force & displacement data transfers
dt_names = syc.setup.add_fsi_data_transfers(interface=interface_name)

# modify force transfer to apply constant initial loading for the first 0.5 [s]
force_transfer = syc.setup.coupling_interface[interface_name].data_transfer["FORC"]
force_transfer.option = "UsingExpression"
force_transfer.value = "vector(5.0 [N], 0.0 [N], 0.0 [N]) if Time < 0.5 [s] else force"

syc.setup.solution_control.time_step_size = 0.1
syc.setup.solution_control.end_time = (
    3.0  # shorten the run a bit, full run is 10 seconds
)

syc.setup.output_control.option = "EveryStep"

print(f"SyC server info: {syc._native_api.GetServerInfo()}")

# solve the coupled analysis
syc.solution.solve()

mapdl.finish()

# post-process structural results
mapdl.post1()

"""
mapdl.result.animate_nodal_displacement(
    rnum = 0,
    loop=True,
    add_text=False,
    displacement_factor=1.0,
    show_edges=True,
    cpos="xy")
"""

# post-process fluid results
# ...

# exit
syc.exit()
fluent.exit()
mapdl.exit()
