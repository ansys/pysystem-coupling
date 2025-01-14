# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
often used as a tutorial for System Coupling. This two-way, fluid-structure
interaction (FSI) case is based on co-simulation of a transient oscillating
plate with surface data transfers.

- Ansys Mechanical APDL (MAPDL) is used to perform a transient structural analysis.
- Ansys Fluent is used to perform a transient fluid-flow analysis.
- System Coupling coordinates the coupled solution involving the above products to
  solve the multiphysics problem via co-simulation.

**Problem description**

An oscillating plate resides within a fluid-filled cavity. A thin plate is
anchored to the bottom of a closed cavity filled with fluid (air):

.. image:: /_static/img_oscplate_case.png
   :width: 400pt
   :align: center

There is no friction between the plate and the side of the cavity. An
initial constant force in x-direction is applied to one side of the thin plate
for the first 0.5 seconds to distort it. Once this pressure is released, the plate
oscillates back and forth to regain its equilibrium, and the
surrounding air damps this oscillation. The plate and surrounding
air are simulated for a few oscillations to allow an examination of the
motion of the plate as it is damped.

"""
# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of performing imports, downloading
# the input file, and launching the required products.
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
# Download the input file
# ~~~~~~~~~~~~~~~~~~~~~~~
# This example uses one pre-created file - a Fluent input file that contains
# the fluids setup.
#
fluent_cas_file = examples.download_file(
    "oscillating_plate.cas.h5", "pysystem-coupling/oscillating_plate"
)

# %%
# Launch products
# ~~~~~~~~~~~~~~~
# Launch instances of the Mechanical APDL, Fluent, and System Coupling
# and return *client* (session) objects that allow you to interact with
# these products via APIs exposed into the current Python environment.
mapdl = pymapdl.launch_mapdl()
fluent = pyfluent.launch_fluent(start_transcript=False)
syc = pysyc.launch(start_output=True)

# %%
# Setup
# -----
# The setup consists of setting up the structural analysis,
# the fluids analysis, and the coupled analysis.

# %%
# Set up the structural analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Enter Mechancal APDL setup
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
mapdl.nsel("S", "LOC", "X", 9.99, 10.01)
mapdl.nsel("A", "LOC", "Y", 0.99, 1.01)
mapdl.nsel("A", "LOC", "X", 10.05, 10.07)
mapdl.cm("FSIN_1", "NODE")
mapdl.sf("FSIN_1", "FSIN", 1)

# %%
# Set up the rest of the transient analysis
mapdl.allsel()
mapdl.run("/SOLU")
mapdl.antype(4)  # transient analysis
mapdl.nlgeom("ON")  # large deformations
mapdl.kbc(1)
mapdl.trnopt("full", "", "", "", "", "hht")
mapdl.tintp(0.1)
mapdl.autots("off")
mapdl.run("nsub,1,1,1")
mapdl.run("time,10.0")
mapdl.timint("on")

# %%
# Set up the fluid analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Read the pre-created case file
fluent.file.read(file_type="case", file_name=fluent_cas_file)


# %%
# Set up the coupled analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# System Coupling setup involves adding the structural and fluid
# participants, adding coupled interfaces and data transfers,
# and setting other coupled analysis properties.

# %%
# Add participants by passing session handles to System Coupling.
solid_name = syc.setup.add_participant(participant_session=mapdl)
fluid_name = syc.setup.add_participant(participant_session=fluent)

syc.setup.coupling_participant[solid_name].display_name = "Solid"
syc.setup.coupling_participant[fluid_name].display_name = "Fluid"

# %%
# Add a coupling interface and data transfers.
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

# %%
# Time step size, end time, output controls
syc.setup.solution_control.time_step_size = "0.1 [s]"  # time step is 0.1 [s]
syc.setup.solution_control.end_time = 10  # end time is 10.0 [s]

syc.setup.output_control.option = "EveryStep"
syc.setup.output_control.generate_csv_chart_output = True

# %%
# Solution
# --------
syc.solution.solve()


# %%
# Post-processing
# ---------------

# %%
# Post-process the structural results
mapdl.finish()
mapdl.post1()
node_ids, node_coords = mapdl.result.nodal_displacement(0)
max_dx = max([value[0] for value in node_coords])
print(f"There are {len(node_ids)} nodes. Maximum x-displacement is {max_dx}")

# %%
# Post-process the fluids results

# use_window_resolution option not active inside containers or Ansys Lab environment
if fluent.results.graphics.picture.use_window_resolution.is_active():
    fluent.results.graphics.picture.use_window_resolution = False

fluent.results.graphics.picture.x_resolution = 1920
fluent.results.graphics.picture.y_resolution = 1440

fluent.results.graphics.contour["contour_static_pressure"] = {}
contour = fluent.results.graphics.contour["contour_static_pressure"]

contour.coloring.option = "banded"
contour.field = "pressure"
contour.filled = True

contour.surfaces_list = ["symmetry1", "wall_deforming"]
contour.display()

fluent.results.graphics.views.restore_view(view_name="front")
fluent.results.graphics.views.auto_scale()
fluent.results.graphics.picture.save_picture(file_name="oscplate_pressure_contour.png")

###############################################################################
# .. image:: /_static/oscplate_pressure_contour.png
#   :width: 500pt
#   :align: center


# %%
# Post-process the System Coupling results - display the charts
# showing displacement and force values during the simulation
syc.solution.show_plot(show_convergence=False)


# %%
# Exit
# ----

syc.exit()
fluent.exit()
mapdl.exit()
