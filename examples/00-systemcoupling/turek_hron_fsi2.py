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

import os

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

mapdl_cdb_file = examples.download_file(
    "turek_hron_solid_model.cdb", "pysystem-coupling/turek-horn-benchmark"
)


# %%
# Launch products
# ~~~~~~~~~~~~~~~
# Launch instances of the Mechanical APDL, Fluent, and System Coupling
# and return *client* (session) objects that allow you to interact with
# these products via APIs exposed into the current Python environment.
# mapdl = pymapdl.launch_mapdl(version="24.2", nproc=1, start_timeout=120, override=True)
# fluent = pyfluent.launch_fluent(start_transcript=False, processor_count=4)

mapdl = pymapdl.launch_mapdl(nproc=1)
fluent = pyfluent.launch_fluent(start_transcript=False, ui_mode="gui")

syc = pysyc.launch(start_output=True)

# %%
# Setup
# -----
# The setup consists of setting up the structural analysis,
# the fluids analysis, and the coupled analysis.

# %%
# Clear cache
# ~~~~~~~~~~~
mapdl.clear()

# %%
# Enter Mechancal APDL setup
mapdl.prep7()

# %%
# Read the CDB file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.cdread(option="DB", fname=mapdl_cdb_file, ext="cdb")


# %%
# Define material properties.
mapdl.mp("DENS", 1, 10000)  # density
mapdl.mp("EX", 1, 1400000)  # Young's modulus
mapdl.mp("NUXY", 1, 0.4)  # Poisson's ratio
mapdl.mp("GXY", 1, 500000)  # Shear modulus

# %%
# Mechanical solver setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.slashsolu()
mapdl.antype(4)
mapdl.nlgeom("on")
mapdl.kbc(1)

mapdl.eqslv("sparse")
mapdl.run("rstsuppress,none")  # don't suppress anything due to presence of FSI loading
mapdl.dmpoption("emat", "no")
mapdl.dmpoption("esav", "no")

mapdl.cmwrite()  # Export components due to presence of FSI loading
mapdl.trnopt(tintopt="hht")
mapdl.tintp("mosp")  # No such option in docs
mapdl.nldiag("cont", "iter")
mapdl.scopt("NO")

mapdl.autots("on")  # User turned on automatic time stepping
mapdl.nsubst(1, 1, 1, "OFF")
mapdl.time(20.0)  # Max time set to any high value; will be controlled by syc
mapdl.timint("on")

mapdl.outres("all", "all")

# %%
# Set up the fluid analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Read the pre-created mesh file
fluent.file.read(file_type="mesh", file_name=fluent_msh_file)
fluent.mesh.check()

# %%
# Define fluids general solver settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent.setup.general.solver.type = "pressure-based"
fluent.solution.methods.high_order_term_relaxation.enable = True

# %%
# Define the fluid material
fluent.setup.models.viscous.model = "laminar"
fluent.setup.materials.fluid["water"] = {
    "density": {"option": "constant", "value": 1000},
    "viscosity": {"option": "constant", "value": 1.0},
}

fluent.setup.cell_zone_conditions.fluid["*fluid*"].general.material = "water"
fluent.setup.materials.print_state()


# %%
# Create the parabolic inlet profile as a named expression
fluent.setup.named_expressions["u_bar"] = {  # average velocity
    "definition": "1.0 [m/s]"
}
fluent.setup.named_expressions["t_bar"] = {"definition": "1.0 [s]"}
fluent.setup.named_expressions["y_bar"] = {"definition": "1.0 [m]"}
fluent.setup.named_expressions["u_y"] = {
    "definition": "(6.0 * u_bar / 0.1681 * ( y/y_bar ) * ( 0.41 - y/y_bar ) )"
}

# %%
# Update the inlet field
inlet_fluid = fluent.setup.boundary_conditions.velocity_inlet["inlet"]
inlet_fluid.momentum.initial_gauge_pressure.value = 0
inlet_fluid.momentum.velocity.value = "u_y"
fluent.setup.named_expressions.print_state()

# %%
# Setup any relevant solution controls
fluent.solution.methods.discretization_scheme = {
    "mom": "second-order-upwind",
    "pressure": "second-order",
}

# %%
# First, a steady simulation is conducted to initialize the
# flow field with the parabolic inlet flow.
fluent.solution.initialization.hybrid_initialize()
fluent.solution.run_calculation.iterate(iter_count=500)

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
    "symmetry_bot",
    "deforming",
    "plane",
    "0.",
    "0.",
    "0.00",
    "0",
    "0",
    "1",
    "no",
    "yes",
    "yes",
    "yes",
    "no",
    "yes",
    "no",
    "yes",
)
fluent.tui.define.dynamic_mesh.zones.create(
    "symmetry_top",
    "deforming",
    "plane",
    "0.",
    "0.",
    "0.01",
    "0",
    "0",
    "1",
    "no",
    "yes",
    "yes",
    "yes",
    "no",
    "yes",
    "no",
    "yes",
)

# %%
# Define number of sub-steps fluent iterates for each coupling step.
# Maximum integration time and total steps are controlled by
# system coupling.
fluent.solution.run_calculation.transient_controls.max_iter_per_time_step = 20


fluent.file.auto_save.save_data_file_every.frequency_type = "time-step"
fluent.file.auto_save.data_frequency = 10
fluent.file.auto_save.root_name = os.path.join(os.getcwd(), "turek_hron_fluid_resolved")

# %%
# Set up the coupled analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# System Coupling setup involves adding the structural and fluid
# participants, adding coupled interfaces and data transfers,
# and setting other coupled analysis properties.

# %%
# Add participants by passing session handles to System Coupling.
solid = syc.setup.add_participant(participant_session=mapdl)
fluid = syc.setup.add_participant(participant_session=fluent)

syc.setup.coupling_participant[solid].display_name = "Solid"
syc.setup.coupling_participant[fluid].display_name = "Fluid"

# %%
# Add a coupling interface and data transfers.
interface_name = syc.setup.add_interface(
    side_one_participant=fluid,
    side_one_regions=["fsi"],
    side_two_participant=solid,
    side_two_regions=["FSIN_1"],
)

# set up 2-way FSI coupling - add force & displacement data transfers
disp_transfer = syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="One",
    source_variable="INCD",
    target_variable="displacement",
)

forc_transfer = syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="Two",
    source_variable="force",
    target_variable="FORC",
)

syc.setup.coupling_interface[interface_name].data_transfer[
    forc_transfer
].relaxation_factor = 0.5

# %%
# Purely due to the scale of the mesh on the fluid side,
# it is generally better to run fluent on multiple cores and
# mapdl on a single core.

syc.setup.coupling_participant[solid].execution_control.parallel_fraction = 1.0
syc.setup.coupling_participant[fluid].execution_control.parallel_fraction = 4.0

# %%
# Time step size, end time, output controls
syc.setup.solution_control.time_step_size = "0.01 [s]"  # time step is 0.01 [s]
# To generate the results shown in the documents increase
# this parameter to 20.0 s.
syc.setup.solution_control.end_time = "5.0 [s]"  # end time is 5.0 [s]

syc.setup.output_control.option = "StepInterval"
syc.setup.output_control.output_frequency = 250
syc.setup.output_control.generate_csv_chart_output = True

print(syc.setup.get_setup_summary())

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