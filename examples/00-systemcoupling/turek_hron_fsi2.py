# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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
The beam and the surrounding fluid are simulated for a few time steps to
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
import numpy as np

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
#
# Download the input files
# ~~~~~~~~~~~~~~~~~~~~~~~~
# This example uses two pre-created files - a Fluent mesh file that contains
# the fluid mesh and named zones, and a MAPDL CDB file containing the
# structural mesh.
#
fluent_msh_file = examples.download_file(
    "fluent-fsi2.msh.h5", "pysystem-coupling/turek-horn-benchmark"
)

mapdl_cdb_file = examples.download_file(
    "turek_hron_benchmark_solid.cdb", "pysystem-coupling/turek-horn-benchmark"
)

drag_data_file = examples.download_file(
    "drag_data.csv", "pysystem-coupling/turek-horn-benchmark"
)

lift_data_file = examples.download_file(
    "lift_data.csv", "pysystem-coupling/turek-horn-benchmark"
)

# %%
# Launch products
# ~~~~~~~~~~~~~~~
# Launch instances of the Mechanical APDL, Fluent, and System Coupling
# and return *client* (session) objects that allow you to interact with
# these products via APIs exposed into the current Python environment.

mapdl = pymapdl.launch_mapdl()
fluent = pyfluent.launch_fluent(processor_count=8)
syc = pysyc.launch(start_output=True, nprocs=10, sycnprocs=2)

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
U_BAR = 1.0  # Average velocity
FLUID_DENS = 1000  # Fluid density
SOLID_DENS = 10000  # Solid density
NU = 0.4  # Poisson's ratio
E = 1.4e6  # Young's modulus
viscosity = 1  # Kinematic viscosity

# %%
# Clear cache
# ~~~~~~~~~~~
mapdl.clear()

# %%
# Enter Mechanical APDL setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.prep7()

# %%
# Read the CDB file
# ~~~~~~~~~~~~~~~~~
mapdl.cdread(option="DB", fname=mapdl_cdb_file)

# %%
# Define material properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.mp("DENS", 1, SOLID_DENS)  # density
mapdl.mp("EX", 1, E)  # Young's modulus
mapdl.mp("NUXY", 1, NU)  # Poisson's ratio

# %%
# Mechanical solver setup
# ~~~~~~~~~~~~~~~~~~~~~~~
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
mapdl.tintp(0.1)  # Numerical damping for HHT time integration
mapdl.nldiag("cont", "iter")
mapdl.scopt("NO")

mapdl.autots("on")  # Automatic time stepping
mapdl.nsubst(1, 1, 1, "OFF")
mapdl.time(35.0)  # Max time; controlled by System Coupling
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
# Define the fluid and update the material properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fluent.setup.models.viscous.model = "laminar"
fluent.setup.materials.fluid["fsi_fluid"] = {
    "density": {"option": "constant", "value": FLUID_DENS},
    "viscosity": {"option": "constant", "value": viscosity},
}

fluent.setup.cell_zone_conditions.fluid["*fluid*"].general.material = "fsi_fluid"
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
    "definition": "1.5*u_bar*(4*(y/y_bar)*(0.41 - y/y_bar)/(0.41^2))"
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent.setup.general.solver.time = "unsteady-2nd-order"

# %%
# Define dynamic meshing
# ~~~~~~~~~~~~~~~~~~~~~~
# Define dynamic meshing for the FSI interface and symmetry planes.
# Currently, dynamic_mesh is not exposed to the fluent root
# session directly. We need to use the ``tui`` framework to create
# dynamic zones.
fluent.tui.define.dynamic_mesh.dynamic_mesh("yes", "no", "no", "no", "no")
fluent.tui.define.dynamic_mesh.zones.create("fsi", "system-coupling")
fluent.tui.define.dynamic_mesh.zones.create(
    "back",
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
    "front",
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
for zone in ["cylinder", "outlet", "inlet", "channel"]:
    fluent.tui.define.dynamic_mesh.zones.create(zone, "stationary")

# %%
# Results and output controls
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define number of sub-steps fluent iterates for each coupling step.
# Maximum integration time and total steps are controlled by
# system coupling.
fluent.solution.run_calculation.transient_controls.max_iter_per_time_step = 50

fluent.file.auto_save.save_data_file_every.frequency_type = "time-step"
fluent.file.auto_save.data_frequency = 20
fluent.file.auto_save.root_name = "turek_hron_fluid_resolved"
fluent.setup.materials.print_state()
fluent.setup.cell_zone_conditions.print_state()

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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
# Drag and lift report definitions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create drag report along x
fluent.settings.solution.report_definitions.drag.create(name="drag_force")
fluent.settings.solution.report_definitions.drag["drag_force"].zones = [
    "cylinder",
    "fsi",
]
fluent.settings.solution.report_definitions.drag["drag_force"].force_vector = [1, 0, 0]
fluent.settings.solution.report_definitions.drag["drag_force"].report_output_type = (
    "Drag Force"
)

# Create lift report along y
fluent.settings.solution.report_definitions.lift.create(name="lift_force")
fluent.settings.solution.report_definitions.lift["lift_force"].zones = [
    "cylinder",
    "fsi",
]
fluent.settings.solution.report_definitions.lift["lift_force"].force_vector = [0, 1, 0]
fluent.settings.solution.report_definitions.lift["lift_force"].report_output_type = (
    "Lift Force"
)

# Create monitor plots for lift and drag
fluent.settings.solution.monitor.report_plots.create(name="drag_force")
fluent.settings.solution.monitor.report_plots["drag_force"].report_defs = "drag_force"

fluent.settings.solution.monitor.report_plots.create(name="lift_force")
fluent.settings.solution.monitor.report_plots["lift_force"].report_defs = "lift_force"

# Create output files for drag and lift
fluent.settings.solution.monitor.report_files.create(name="drag_force")
fluent.settings.solution.monitor.report_files["drag_force"] = {
    "file_name": "drag_force.out",
    "report_defs": ["drag_force"],
}

fluent.settings.solution.monitor.report_files.create(name="lift_force")
fluent.settings.solution.monitor.report_files["lift_force"] = {
    "file_name": "lift_force.out",
    "report_defs": ["lift_force"],
}

# %%
# Time step size, end time, output controls
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
syc.setup.solution_control.time_step_size = "0.01 [s]"

# To generate similar results shown in this example documentation, increase
# end_time to 35 [s].
syc.setup.solution_control.end_time = "0.1 [s]"

syc.setup.output_control.option = "StepInterval"
syc.setup.output_control.output_frequency = 100

# %%
# Solve the coupled system
# ------------------------
syc.solution.solve()

# %%
# Postprocessing
# --------------

# %%
# Postprocess the structural results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mapdl.finish()
mapdl.post1()

# Select tip node and store it
mapdl.nsel("s", "loc", "x", 0.6)
mapdl.nsel("r", "loc", "y", 0.2)
mapdl.nsel("r", "loc", "z", 0.005)
tip_node = mapdl.get_value("node", 0, "num", "max")
tip_y_0 = mapdl.get_value("node", tip_node, "loc", "y")
mapdl.nsel("all")  # restore all nodes before looping

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
plt.close()  # close the plot to avoid showing it in the docs.

###############################################################################
# .. image:: /_static/turek_horn_fsi2_tip_disp.png
#   :width: 500pt
#   :align: center

# %%
# Postprocess the fluids results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# use_window_resolution option not active inside containers or Ansys Lab environment

if fluent.results.graphics.picture.use_window_resolution.is_active():
    fluent.results.graphics.picture.use_window_resolution = False

fluent.results.graphics.picture.x_resolution = 1920
fluent.results.graphics.picture.y_resolution = 1440

fluent.results.graphics.contour["contour_static_pressure"] = {}
contour = fluent.results.graphics.contour["contour_static_pressure"]

contour.colorings.banded = True
contour.field = "pressure"
contour.filled = True

contour.surfaces_list = ["back"]
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
# Plot drag and lift forces vs paper data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The simulation results are compared against the reference data from
# Turek & Hron (2006). A time offset is applied to align the periodic
# oscillations between the simulation and the paper data.

DT = 0.01  # simulation time step (s)
DEPTH = 0.01  # mesh z-depth (m), converts Fluent N -> N/m
TIME_OFFSET = 25.35  # shift paper data left in time until curves align

drag = np.loadtxt("drag_force.out", delimiter=None, skiprows=4)
lift = np.loadtxt("lift_force.out", delimiter=None, skiprows=4)

x_drag = drag[:, 0] * DT
y_drag = drag[:, 1] / DEPTH

x_lift = lift[:, 0] * DT
y_lift = lift[:, 1] / DEPTH

drag_paper = np.loadtxt(drag_data_file, delimiter=",", skiprows=0)
lift_paper = np.loadtxt(lift_data_file, delimiter=",", skiprows=0)

x_drag_paper = drag_paper[:, 0] - TIME_OFFSET
y_drag_paper = drag_paper[:, 1]

x_lift_paper = lift_paper[:, 0] - TIME_OFFSET
y_lift_paper = lift_paper[:, 1]

plt.figure(1, figsize=(8, 5))
plt.plot(x_drag, y_drag, color="steelblue", lw=1.2, label="Drag force - Simulation")
plt.plot(
    x_drag_paper,
    y_drag_paper,
    color="darkorange",
    lw=1.2,
    linestyle="dashed",
    label="Drag force - Paper (time offset applied)",
)
plt.xlabel("Time (s)")
plt.ylabel("Drag force (N/m)")
plt.title("Drag Force vs Time")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("drag_final.png", dpi=150)
plt.close()  # close the plot to avoid showing it in the docs.

###############################################################################
# .. image:: /_static/drag_final.png
#   :width: 500pt
#   :align: center

plt.figure(2, figsize=(8, 5))
plt.plot(x_lift, y_lift, color="steelblue", lw=1.2, label="Lift force - Simulation")
plt.plot(
    x_lift_paper,
    y_lift_paper,
    color="darkorange",
    lw=1.2,
    linestyle="dashed",
    label="Lift force - Paper (time offset applied)",
)
plt.xlabel("Time (s)")
plt.ylabel("Lift force (N/m)")
plt.title("Lift Force vs Time")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("lift_final.png", dpi=150)
plt.close()  # close the plot to avoid showing it in the docs.

###############################################################################
# .. image:: /_static/lift_final.png
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
# To get similar results, you may need to run the simulation with an end_time
# equal to 35 [s]. Refer to the time step size, end time, output controls
# section to update the end time.
#
# The results shown below are at end_time = 35 [s] and took approximately
# 5 hrs based on the compute resources used. Runtime may vary depending on
# the compute resources available.

# Velocity field at 35 [sec]

###############################################################################
# .. image:: /_static/turek_hron_velocity_field_at_15_sec.png
#   :width: 500pt
#   :align: center

# Pressure field at 35 [sec]

###############################################################################
# .. image:: /_static/turek_hron_pressure_field_at_15_sec.png
#   :width: 500pt
#   :align: center

# %%
# References
# ----------
#
# [1]. Turek, S., & Hron, J. (2006). Proposal for numerical benchmarking of
# fluid-structure interaction between an elastic object and laminar
# incompressible flow (pp. 371-385). Springer Berlin Heidelberg.
