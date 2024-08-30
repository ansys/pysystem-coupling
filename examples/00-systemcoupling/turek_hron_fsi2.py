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

""".. _ref_turek_hron_fsi2_example:

Turek-Hron example
------------------

This example is a version of the *Turek-Hron FSI2* case that is
often used as a benchmark case for System Coupling. This two-way, fluid-structure
interaction (FSI) case is based on co-simulation of a transient oscillating
beam with surface data transfers.

- Ansys Mechanical APDL (MAPDL) is used to perform a transient structural analysis.
- Ansys Fluent is used to perform a transient fluid-flow analysis.
- System Coupling coordinates the coupled solution involving the above products to
  solve the multiphysics problem via co-simulation.

**Problem description**

An elastic beam structure is attached to a rigid rigid cylinder. The system
resides within a fluid filled channel:

.. image:: /_static/turek_hron_case.png
   :width: 400pt
   :align: center

The flow is laminar with a Reynolds number of $Re = 100$. The inlet velocity
has a parabolic profile with a maximum value of $1.5\bar{U}$, where $\bar{U}$
is the average inlet velocity. The cylinder sits at an offset of $0.05~m$ to the
incoming flow, causing an imbalance of surface forces on the elastic beam.
The beam and the surrounding fluid are simulated for a few time setps to
allow an examination of the motion of the beam as it starts vibrating due to
vortices shedded by the rigid cylinder.
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

# sphinx_gallery_thumbnail_path = '_static/turek_hron_velocity.jpeg'

import ansys.fluent.core as pyfluent
import ansys.mapdl.core as pymapdl
import matplotlib.pyplot as plt

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
#
# Download the input file
# ~~~~~~~~~~~~~~~~~~~~~~~
# This example uses one pre-created file - a Fluent mesh file that contains
# the fluids mesh and named zones.
#
fluent_msh_file = examples.download_file(
    "turek_hron_fluid.msh", "pysystem-coupling/turek-horn-benchmark"
)

# %%
# Launch products
# ~~~~~~~~~~~~~~~
# Launch instances of the Mechanical APDL, Fluent, and System Coupling
# and return *client* (session) objects that allow you to interact with
# these products via APIs exposed into the current Python environment.
# mapdl = pymapdl.launch_mapdl(version="24.2", nproc=1, start_timeout=120, override=True)
# fluent = pyfluent.launch_fluent(start_transcript=False, processor_count=4)

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
mapdl.mp("DENS", 1, 10000)  # density
mapdl.mp("EX", 1, 1400000)  # Young's modulus
mapdl.mp("NUXY", 1, 0.4)  # Poisson's ratio
mapdl.mp("GXY", 1, 500000)  # Shear modulus

# %%
# Set element types to SOLID186.
mapdl.et(1, 186)
mapdl.keyopt(1, 2, 1)

# %%
# Make geometry.
mapdl.block(0.25, 0.6, 0.19, 0.21, 0.0, 0.01)
mapdl.lsel("s", "length", vmin=0.35)
mapdl.lesize("all", ndiv=60)
mapdl.lsel("s", "tan1", "y", 1)
mapdl.lsel("a", "tan2", "y", 1)
mapdl.lesize("all", ndiv=5)
mapdl.lsel("s", "tan1", "z", 1)
mapdl.lsel("a", "tan2", "z", 1)
mapdl.lesize("all", ndiv=1)
mapdl.vsweep(1)

# %%
# Add fixed support at x=0.25
mapdl.nsel("s", "loc", "x", 0.25)
mapdl.d("all", "all")

# %%
# Add the FSI interface.
mapdl.nsel("s", "loc", "x", 0.60)
mapdl.nsel("a", "loc", "y", 0.19)
mapdl.nsel("a", "loc", "y", 0.21)
mapdl.cm("FSIN_1", "node")
mapdl.sf("FSIN_1", "FSIN", 1)

# %%
# Set up the rest of the transient analysis
mapdl.allsel()
mapdl.slashsolu()
mapdl.antype(4)  # transient analysis
mapdl.nlgeom("on")  # large deformations
mapdl.kbc(1)
mapdl.eqslv("sparse")
mapdl.trnopt(tintopt="hht")
mapdl.tintp("mosp")
mapdl.autots("on")
mapdl.nsubst(1, 1, 1, "off")
mapdl.time(20.0)
mapdl.timint("on")
mapdl.outres("all", "all")

# %%
# Set up the fluid analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Read the pre-created mesh file
fluent.file.read(file_type="mesh", file_name=fluent_msh_file)

# %%
# Define the fluid material
fluent.setup.models.viscous.model = "laminar"
fluent.setup.materials.fluid["fsi2"] = {
    "density": {"option": "constant", "value": 1000},
    "viscosity": {"option": "constant", "value": 1.0},
}
fluent.setup.cell_zone_conditions.fluid["*fluid*"].general.material = "fsi2"

# %%
# Create the parabolic inlet profile as a named expression
fluent.setup.named_expressions["u_bar"] = {  # average velocity
    "definition": "1.0 [m/s]"
}
fluent.setup.named_expressions["t_bar"] = {"definition": "1.0 [s]"}
fluent.setup.named_expressions["y_bar"] = {"definition": "1.0 [m]"}
fluent.setup.named_expressions["u_y"] = {
    "definition": "(6.0 * u_bar / 0.1681 * ( y/y_bar ) * ( 0.41 - y/y_bar )"
}

# %%
# Update the inlet field
inlet_fluid = fluent.setup.boundary_conditions.velocity_inlet["inlet"]
inlet_fluid.momentum.initial_gauge_pressure.value = 0
inlet_fluid.momentum.velocity.value = "u_y"

# %%
# First, a steady simulation is conducted to initialize the
# flow field with the parabolic inlet flow.
fluent.solution.initialization.hybrid_initialize()
fluent.solution.run_calculation.iterate(iter_count=200)

# %%
# Switch to transient mode and prepare for coupling
fluent.setup.general.solver.time = "unsteady-1st-order"

# %%
# Define dynamic meshing for deforming symmetry planes.
# Currently, dynamic_mesh is not exposed to the fluent root
# session directly. We need to use the `tui` framework to create
# dynamic zones.
fluent.tui.define.dynamic_mesh.dynamic_mesh("yes", "no", "no", "no", "no")
fluent.tui.define.dynamic_mesh.zones.create("fsi", "system-coupling")
fluent.tui.define.dynamic_mesh.zones.create(
    "symmetry_bot", "deforming", "plane", "0.", "0.", "0.", "0", "0", "1"
)
fluent.tui.define.dynamic_mesh.zones.create(
    "symmetry_top", "deforming", "plane", "0.", "0.", "0.01", "0", "0", "1"
)

# %%
# Define number of sub-steps fluent iterates for each coupling step.
# Maximum integration time and total steps are controlled by
# system coupling.
transient_controls = fluent.solution.run_calculation.transient_controls
transient_controls.max_iter_per_time_step = 20

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
    side_one_regions=["fsi"],
    side_two_participant=solid_name,
    side_two_regions=["FSIN_1"],
)

# set up 2-way FSI coupling - add force & displacement data transfers
dt_names = syc.setup.add_fsi_data_transfers(interface=interface_name)

# modify force transfer to specify the under relaxation factor
force_transfer = syc.setup.coupling_interface[interface_name].data_transfer["FORC"]
force_transfer.relaxation_factor = 0.5  # required for stabilizing the flow.

# %%
# Purely due to the scale of the mesh on the fluid side,
# it is generally better to run fluent on multiple cores and
# mapdl on a single core.

syc.setup.coupling_participant[solid_name].execution_control.parallel_fraction = 1.0
syc.setup.coupling_participant[fluid_name].execution_control.parallel_fraction = 4.0

# %%
# Time step size, end time, output controls
syc.setup.solution_control.time_step_size = "0.01 [s]"  # time step is 0.01 [s]
# To generate the results shown in the documents increase
# this parameter to 20.0 s.
syc.setup.solution_control.end_time = 5  # end time is 5.0 [s]

syc.setup.output_control.option = "StepInterval"
syc.setup.output_control.output_frequency = 50
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
# %%
# Post-process the structural results
mapdl.finish()
mapdl.post1()
mapdl.nsel("s", "loc", "x", 0.60)
mapdl.nsel("r", "loc", "y", 0.20)
tip_node = mapdl.nsel("r", "loc", "z", 0.00)[0]
tip_y_0 = mapdl.get_value("node", tip_node, "loc", "y")
tip_y = []
nsets = mapdl.post_processing.nsets
for i in range(1, nsets + 1):
    mapdl.set(i, 1)
    u_y = mapdl.get_value("node", tip_node, "u", "y")
    tip_y.append(tip_y_0 + u_y)

time_values = mapdl.post_processing.time_values
plt.plot(time_values, tip_y)
plt.xlabel("t (s)")
plt.ylabel(r"$x_{tip}$ (m)")
plt.savefig("fsi2_tip_disp.png")

###############################################################################
# .. image:: /_static/fsi2_tip_disp.png
#   :width: 500pt
#   :align: center


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

contour.surfaces_list = ["symmetry_bot"]
contour.display()

fluent.results.graphics.views.restore_view(view_name="front")
fluent.results.graphics.views.auto_scale()
fluent.results.graphics.picture.save_picture(file_name="fsi2_pressure_contour.png")

###############################################################################
# .. image:: /_static/fsi2_pressure_contour.png
#   :width: 500pt
#   :align: center


# %%
# Post-process the System Coupling results - display the charts
# showing displacement and force values during the simulation
# syc.solution.show_plot(show_convergence=False)


# %%
# Exit
# ----

syc.exit()
fluent.exit()
mapdl.exit()
