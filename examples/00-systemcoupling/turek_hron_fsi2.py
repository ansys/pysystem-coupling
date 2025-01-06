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

""".. _ref_turek_hron_fsi2_example:

Turek-Hron FSI2 Benchmark Example
---------------------------------

This example is a version of the *Turek-Hron FSI2* case that is
often used as a benchmark case for System Coupling. This two-way, fluid-structure
interaction (FSI) case is based on co-simulation of a transient oscillating
beam with surface data transfers.

- Ansys Mechanical APDL (MAPDL) is used to perform a transient structural analysis.
- Ansys Fluent is used to perform a transient fluid-flow analysis.
- System Coupling coordinates the coupled solution involving the above products to
  solve the multiphysics problem via co-simulation.

**Problem description**

An elastic beam structure is attached to a rigid cylinder. The system
resides within a fluid filled channel:

.. image:: /_static/turek_hron_case.png
   :width: 400pt
   :align: center

The flow is laminar with a Reynolds number of :math:`Re = 100`. The inlet velocity
has a parabolic profile with a maximum value of :math:`1.5 \cdot \\bar{U}`, where :math:`\\bar{U}`
is the average inlet velocity. The cylinder sits at an offset of :math:`0.05~m` to the
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

mapdl_cdb_file = examples.download_file(
    "turek_hron_solid_model.cdb", "pysystem-coupling/turek-horn-benchmark"
)


# %%
# Launch products
# ~~~~~~~~~~~~~~~
# Launch instances of the Mechanical APDL, Fluent, and System Coupling
# and return *client* (session) objects that allow you to interact with
# these products via APIs exposed into the current Python environment.

mapdl = pymapdl.launch_mapdl()
fluent = pyfluent.launch_fluent()

syc = pysyc.launch(start_output=True)


# %%
# Setup Mechanical APDL, Fluent, and System Coupling analyses
# -----------------------------------------------------------
# The setup consists of setting up the structural analysis,
# the fluids analysis, and the coupled analysis.

# %%
# Define constants
# ~~~~~~~~~~~~~~~~
CYLINDER_DIA = 0.1  # Diameter of the cylinder
RE = 100  # Reynolds number
U_BAR = 1  # Average velocity
FLUID_DENS = 1000  # Fluid density
SOLID_DENS = 10000  # Solid density
NU = 0.4  # Poisson's ratio
G = 500000  # Shear modulus
E = 2 * G * (1 + NU)  # Youngs modulus

# %%
# Clear cache
# ~~~~~~~~~~~
mapdl.clear()

# %%
# Enter Mechancal APDL setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.prep7()

# %%
# Read the CDB file
# ~~~~~~~~~~~~~~~~~~
mapdl.cdread(option="DB", fname=mapdl_cdb_file)


# %%
# Define material properties.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.mp("DENS", 1, SOLID_DENS)  # density
mapdl.mp("EX", 1, E)  # Young's modulus
mapdl.mp("NUXY", 1, NU)  # Poisson's ratio
mapdl.mp("GXY", 1, G)  # Shear modulus

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
fluent.file.read_mesh(file_name=fluent_msh_file)
fluent.mesh.check()

# %%
# Define fluids general solver settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent.setup.general.solver.type = "pressure-based"
fluent.solution.methods.high_order_term_relaxation.enable = True

# %%
# Define the fluid and update the material properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

viscosity = (FLUID_DENS * U_BAR * CYLINDER_DIA) / RE

fluent.setup.models.viscous.model = "laminar"
fluent.setup.materials.fluid["water"] = {
    "density": {"option": "constant", "value": FLUID_DENS},
    "viscosity": {"option": "constant", "value": viscosity},
}

fluent.setup.cell_zone_conditions.fluid["*fluid*"].general.material = "water"
fluent.setup.materials.print_state()


# %%
# Create the parabolic inlet profile as a named expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent.setup.named_expressions["u_bar"] = {  # average velocity
    "definition": f"{U_BAR} [m/s]"
}
fluent.setup.named_expressions["t_bar"] = {"definition": "1.0 [s]"}
fluent.setup.named_expressions["y_bar"] = {"definition": "1.0 [m]"}
fluent.setup.named_expressions["u_y"] = {
    "definition": f"(6 * u_bar / ( ( 4.1 * {CYLINDER_DIA} ) ** 2 )) \
* ( y/y_bar + 0.2 ) * ( 0.21 - y/y_bar )"
}

# %%
# Update the inlet field
# ~~~~~~~~~~~~~~~~~~~~~~
inlet_fluid = fluent.setup.boundary_conditions.velocity_inlet["inlet"]
inlet_fluid.momentum.initial_gauge_pressure.value = 0
inlet_fluid.momentum.velocity.value = "u_y"
fluent.setup.named_expressions.print_state()

# %%
# Setup any relevant solution controls
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent.solution.methods.discretization_scheme = {
    "mom": "second-order-upwind",
    "pressure": "second-order",
}

# %%
# Initialize the flow field & run a steady simulation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# First, a steady simulation is conducted to initialize the
# flow field with the parabolic inlet flow.
fluent.solution.initialization.hybrid_initialize()
fluent.solution.run_calculation.iterate(iter_count=500)

# %%
# Switch to transient mode and prepare for coupling
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent.setup.general.solver.time = "unsteady-1st-order"

# %%
# Define dynamic meshing
# ~~~~~~~~~~~~~~~~~~~~~~
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
# Results and output controls
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define number of sub-steps fluent iterates for each coupling step.
# Maximum integration time and total steps are controlled by
# system coupling.
fluent.solution.run_calculation.transient_controls.max_iter_per_time_step = 20


fluent.file.auto_save.save_data_file_every.frequency_type = "time-step"
fluent.file.auto_save.data_frequency = 10
fluent.file.auto_save.root_name = "turek_hron_fluid_resolved"

# %%
# Set up the coupled analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# System Coupling setup involves adding the structural and fluid
# participants, adding coupled interfaces and data transfers,
# and setting other coupled analysis properties.

# %%
# Add participants
# ~~~~~~~~~~~~~~~~
# Add participants by passing session handles to System Coupling.
fluid = syc.setup.add_participant(participant_session=fluent)
solid = syc.setup.add_participant(participant_session=mapdl)

# %%
# Setup the interface and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add a coupling interface and data transfers.
interface_name = syc.setup.add_interface(
    side_one_participant=fluid,
    side_one_regions=["fsi"],
    side_two_participant=solid,
    side_two_regions=["FSIN_1"],
)


# set up 2-way FSI coupling - add force & displacement data transfers
data_transfer = syc.setup.add_fsi_data_transfers(interface=interface_name)
force_transfer = syc.setup.coupling_interface[interface_name].data_transfer["FORC"]
force_transfer.relaxation_factor = 0.5


# %%
# Time step size, end time, output controls
syc.setup.solution_control.time_step_size = "0.01 [s]"  # time step is 0.01 [s]

# To generate similar results shown in this example documentation, increase an end_time
# parameter to 15 [s].
syc.setup.solution_control.end_time = "0.1 [s]"  # end time

syc.setup.output_control.option = "StepInterval"
syc.setup.output_control.output_frequency = 250
# print(syc.setup.get_setup_summary())

# %%
# Solve the coupled system
# ------------------------
syc.solution.solve()


# %%
# Postprocessing
# ---------------

# %%
# Postprocess the structural results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.finish()
mapdl.post1()
mapdl.nsel("s", "loc", "x", 0.45)  # select the right side of the beam
mapdl.nsel("r", "loc", "y", 0.00)  # select the top of the beam
tip_node = mapdl.nsel("r", "loc", "z", 0.005)[0]  # select the tip node
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
plt.savefig("turek_horn_fsi2_tip_disp.png")
# If you want to see the in-line plot, comment following line.
plt.close()  # close the plot to avoid showing it in the docs.

###############################################################################
# .. image:: /_static/turek_horn_fsi2_tip_disp.png
#   :width: 500pt
#   :align: center


# %%
# Postprocess the fluids results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
fluent.results.graphics.picture.save_picture(
    file_name="turek_horn_fsi2_pressure_contour.png"
)

###############################################################################
# .. image:: /_static/turek_horn_fsi2_pressure_contour.png
#   :width: 500pt
#   :align: center


# %%
# Exit
# ----

syc.exit()
fluent.exit()
mapdl.exit()

# %%
# Note
# ----
# The results shown in this example are for illustrative purposes only.
# To get similar results, you may need to run the simulation with an end_time equal to 15[s].
# Refer to the section time step size, end time, output controls section to update the end time.

# The results shown below are at end_time as 15 [s] and it took approx. 2 hrs based on
# the compute resource used.Please note that the runtime may vary depending on the
# compute resources used.

# Velocity field at 15 [sec]

###############################################################################
# .. image:: /_static/turek_hron_velocity_field_at_15_sec.png
#   :width: 500pt
#   :align: center


# Pressure field at 15 [sec]

###############################################################################
# .. image:: /_static/turek_hron_pressure_field_at_15_sec.png
#   :width: 500pt
#   :align: center

# %%
# References
# ----------
#
# [1]. Turek, S., & Hron, J. (2006). Proposal for numerical benchmarking of fluid-structure
# interaction between an elastic object and laminar incompressible flow (pp. 371-385).
# Springer Berlin Heidelberg.
