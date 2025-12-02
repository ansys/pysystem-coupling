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

""".. _ref_CHT_pipe_example:

Conjugate Heat transfer- Pipe flow
-----------------------------------

Conjugate heat transfer (CHT) simulations often exhibit numerical sensitivity at the fluid-solid
interface. This example demonstrates how users can appropriately select interface conditions
and stabilization schemes for a typical pipe-flow configuration. It highlights best practices
for setting up a robust CHT workflow in System Coupling, including managing temperature and
heat-flux exchange, controlling relaxation, ensuring consistent mesh-to-mesh interpolation.

- Ansys Fluent is used to model the thermal fluid flow in the pipe.
- Ansys Mechanical APDL (MAPDL) is used to model thermal transfer in the pipe wall.
- System Coupling coordinates the coupled solution to the conjugate heat transfer problem,
  including numerical stabilization if needed.

**Problem description**

A fluid at a certain temperature flows into a pipe of known diameter and length. As it flows,
the heated outer wall of the pipe conducts heat to the inner wall, which in turns heats the
fluid and cools down the walls of the pipe.

The flow is smooth inside the pipe and the outer wall of the pipe is adiabatic. Fluid enters
at an initial temperature of 300K while the outside pipe of the wall is at 350K.


"""
# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of performing imports, downloading
# the input file, and launching the required products.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import ``ansys-systemcoupling-core``, ``ansys-fluent-core``, ``ansys-mapdl-core``

import ansys.fluent.core as pyfluent
import ansys.mapdl.core as pymapdl

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
# Download the mesh file
fluent_msh_file = examples.download_file(
    "fluid_domain.msh", "pysystem-coupling/cht_pipe"
)

# %%
# Launch MAPDL
mapdl = pymapdl.launch_mapdl()
mapdl.clear()
mapdl.prep7()

# %%
# Define material properties
mapdl.mp("EX", 1, 69e9)
mapdl.mp("NUXY", 1, 0.33)
mapdl.mp("DENS", 1, 2700)
mapdl.mp("ALPX", 1, 23.6e-6)
mapdl.mp("KXX", 1, 237)
mapdl.mp("C", 1, 900)

# %%
# Set element type to SOLID279
mapdl.et(1, 279)
mapdl.keyopt(1, 2, 1)
print(mapdl)


# %%
# Parameter of the pipe
r_in = 0.025
r_out = 0.035
l = 0.2

# %%
# Create a simple hollow pipe
mapdl.cyl4(0, 0, rad1=r_in, rad2=r_out, depth=l)
mapdl.esize(0.002)
mapdl.vsweep(1)


# %%
# Creating the regions from the geometry for named selections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Inner wall Named Selection
mapdl.asel("S", "AREA", "", 5, 6)
mapdl.nsla("S", 1)
mapdl.cm("FSIN_1", "NODE")
mapdl.allsel()

# Outer wall Named Selection
mapdl.asel("S", "AREA", "", 3, 4)
mapdl.cm("Outer_wall", "AREA")
mapdl.allsel()

# Outlet Named Selection
mapdl.asel("S", "AREA", "", 2)
mapdl.cm("Outlet", "AREA")
mapdl.allsel()

# Inlet Named Selection
mapdl.asel("S", "AREA", "", 1)
mapdl.cm("Inlet", "AREA")
mapdl.allsel()

# %%
# Boundary conditions in degrees Celsius
mapdl.cmsel("S", "Outer_wall")
mapdl.d("Outer_wall", "TEMP", 77)
mapdl.allsel()

mapdl.cmsel("S", "Inlet")
mapdl.sf("ALL", "HFLUX", 0)
mapdl.allsel()

mapdl.cmsel("S", "Outlet")
mapdl.sf("ALL", "HFLUX", 0)
mapdl.allsel()

mapdl.cmsel("S", "FSIN_1")
mapdl.sf("FSIN_1", "FSIN", 1)
mapdl.allsel()

# %%
# Setup the rest of the analysis
mapdl.run("/SOLU")
mapdl.antype(0)


# %%
# Set up the fluid analysis and read the pre-created mesh file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fluent = pyfluent.launch_fluent(start_transcript=False)
fluent.file.read(file_type="mesh", file_name=fluent_msh_file)

# %%
# Define the fluid solver settings
fluent.setup.models.energy.enabled = True

# %%
# Add the material
fluent.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

fluent.setup.cell_zone_conditions.fluid["fff_fluiddomain"].material = "water-liquid"

# %%
# Define boundary conditions
fluent.setup.boundary_conditions.velocity_inlet["inlet"].momentum.velocity = (
    0.1  # units: m/s
)
fluent.setup.boundary_conditions.velocity_inlet["inlet"].thermal.temperature = (
    300  # Units: Kelvin
)
fluent.setup.boundary_conditions.wall["inner_wall"].thermal.thermal_bc = (
    "via System Coupling"
)

fluent.solution.run_calculation.iter_count = 20

# %%
# Set up the coupled analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# System Coupling setup involves adding the structural and fluid
# participants, adding coupled interfaces and data transfers,
# and setting other coupled analysis properties.
syc = pysyc.launch(start_output=True)

# %%
# Add participants by passing session handles to System Coupling.
fluid_name = syc.setup.add_participant(participant_session=fluent)
solid_name = syc.setup.add_participant(participant_session=mapdl)

syc.setup.coupling_participant[fluid_name].display_name = "Fluid"
syc.setup.coupling_participant[solid_name].display_name = "Solid"

# %%
# Add coupling face and data transfers
interface_name = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["inner_wall"],
    side_two_participant=solid_name,
    side_two_regions=["FSIN_1"],
)

# %%
# Set up 2-way thermal FSI coupling
# ----Temp from solid to fluid----
temp_transfer = syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="One",
    source_variable="TEMP",
    target_variable="temperature",
)

# ----Heat flux from fluid to solid----
hf_transfer = syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="Two",
    source_variable="heatflow",
    target_variable="HFLW",
)

# %%
# Calculating biot number (querying the properties from fluent will be included in a future
# release of fluent)
# solid_props = fluent.settings.setup.materials.database.get_database_material_properties(
# name="aluminum")
# fluid_props = fluent.settings.setup.materials.database.get_database_material_properties(
# name="water-liquid")
# fluid_rho = fluid_props["density"]["compressible-liquid"][1]  # Density of fluid
# mu_fluid = fluid_props["viscosity"]["constant"]  # Viscosity of fluid
# cp_fluid = fluid_props["specific-heat"]["constant"]  # Specific heat capacity of fluid
# k_fluid = fluid_props["thermal-conductivity"]["constant"]  # Thermal conductivity of fluid
# k_solid = solid_props["thermal-conductivity"]["constant"]# Thermal conductivity of solid


L_c = r_out - r_in  # Characteristic length of the pipe (thickness)
U = 0.1
fluid_rho = 998.3
mu_fluid = 0.001
cp_fluid = 4182
k_fluid = 0.6
k_solid = 1.2


def compute_thermo_numbers(rho, mu, cp, k_fluid, k_solid, velocity, L_c, n=0.4):
    """Compute Reynolds, Nusselt, h, and Biot numbers."""

    def reynolds_number(rho, mu, velocity, D_h):
        """Reynolds number."""
        return (rho * velocity * D_h) / mu

    def nusselt_number(Re, Pr, n):
        """Dittus–Boelter Nusselt number."""
        return 0.023 * (Re**0.8) * (Pr**n)

    def biot_number(h, L_c, k_solid):
        """Biot number."""
        return h * L_c / k_solid

    Pr = (cp * mu) / k_fluid
    Re = reynolds_number(rho, mu, velocity, L_c)
    Nu = nusselt_number(Re, Pr, n)
    h = Nu * k_fluid / L_c
    Bi = biot_number(h, L_c, k_solid)

    return Re, Nu, h, Bi


Re, Nu, h, Bi = compute_thermo_numbers(
    fluid_rho, mu_fluid, cp_fluid, k_fluid, k_solid, U, L_c
)

print("Reynolds Number =", Re)
print("Nusselt Number =", Nu)
print("heat transfer coefficient =", h)
print("Biot Number =", Bi)

# %%
# Apply stabilization if Biot number exceeds 10
if Bi > 10:
    syc.setup.analysis_control.global_stabilization.option = "Quasi-Newton"

syc.setup.solution_control.time_step_size = "0.1 [s]"  # time step is 0.1 [s]
syc.setup.solution_control.end_time = 10  # end time is 10.0 [s]

syc.setup.solution_control.maximum_iterations = 100

# %%
# Solution
# --------
syc.solution.solve()

# %%
# Exit
# ----
syc.end_output()
syc.exit()

# %%
# Post processing
# ~~~~~~~~~~~~~~~
# Post process the fluid results in fluent
if fluent.settings.results.graphics.picture.use_window_resolution.is_active():
    fluent.settings.results.graphics.picture.use_window_resolution = False

fluent.settings.results.graphics.picture.x_resolution = 1920
fluent.settings.results.graphics.picture.y_resolution = 1440

fluent.settings.results.surfaces.plane_surface.create(name="mid_plane")
fluent.settings.results.surfaces.plane_surface["mid_plane"].method = "zx-plane"

fluent.settings.results.graphics.contour.create(name="contour_temperature")
fluent.settings.results.graphics.contour["contour_temperature"] = {
    "field": "temperature",
    "surfaces_list": ["mid_plane"],
}
fluent.settings.results.graphics.contour.display(object_name="contour_temperature")

fluent.settings.results.graphics.views.restore_view(view_name="top")
fluent.settings.results.graphics.views.auto_scale()
fluent.settings.results.graphics.picture.save_picture(file_name="cht_temp_contour.png")

# %%
# Temperature distribution in the fluid domain
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. image:: /_static/cht_temp_contour.png
#   :width: 800px
#   :align: center
#   :alt: Temperature contour after coupled CHT simulation
