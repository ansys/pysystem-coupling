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

""".. _ref_cht_pipe_example:

Conjugate Heat Transfer- Pipe Flow
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
the heated outer wall of the pipe conducts heat to the inner wall, which in turn heats the
fluid and cools down the walls of the pipe.

.. image:: /_static/pipe_schematic.png
   :width: 400pt
   :align: center

The flow is smooth inside the pipe and the outer wall of the pipe is adiabatic. Fluid enters
at an initial temperature of 300K while the outer wall of the pipe is at 350K.


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

# sphinx_gallery_thumbnail_path = '_static/title_image.png'

import ansys.fluent.core as pyfluent
import ansys.mapdl.core as pymapdl

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
# Download the Fluent mesh file.
fluent_msh_file = examples.download_file(
    "fluid_domain.msh", "pysystem-coupling/cht_pipe"
)

# %%
# Launch MAPDL to create the solid domain.
# ----------------------------------------

# Launch MAPDL.
mapdl = pymapdl.launch_mapdl()
mapdl.clear()
mapdl.prep7()

# %%
# Set material properties of the pipe.
mapdl.mp("EX", 1, 69e9)
mapdl.mp("NUXY", 1, 0.33)
mapdl.mp("DENS", 1, 2700)
mapdl.mp("ALPX", 1, 23.6e-6)
mapdl.mp("KXX", 1, 237)
mapdl.mp("C", 1, 900)

# %%
# Set element type to SOLID279.
mapdl.et(1, 279)
mapdl.keyopt(1, 2, 1)
print(mapdl)


# %%
# Set the pipe inner and outer diameter and length.
d_in = 0.025
d_out = 0.035
l = 0.2

# %%
# Create a simple hollow pipe
mapdl.cyl4(0, 0, rad1=d_in, rad2=d_out, depth=l)
mapdl.esize(0.002)
mapdl.vsweep(1)

###############################################################################
# .. image:: /_static/pipe_elements.png
#   :width: 700pt
#   :align: center

# %%
# Creating the regions from the geometry for named selections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Creating a named selection for Inner wall.
mapdl.asel("S", "AREA", "", 5, 6)
mapdl.nsla("S", 1)
mapdl.cm("FSIN_1", "NODE")
mapdl.allsel()

# Creating a named selection for Outer wall.
mapdl.asel("S", "AREA", "", 3, 4)
mapdl.cm("Outer_wall", "AREA")
mapdl.allsel()

# Creating a named selection for Outlet.
mapdl.asel("S", "AREA", "", 2)
mapdl.cm("Outlet", "AREA")
mapdl.allsel()

# Creating a named selection for Inlet.
mapdl.asel("S", "AREA", "", 1)
mapdl.cm("Inlet", "AREA")
mapdl.allsel()

# %%
# Set the boundary conditions for the structure. Temperature is in degrees Celsius.
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
# Setup the rest of the analysis.
mapdl.run("/SOLU")
mapdl.antype(0)


# %%
# Set up the fluid analysis and read the pre-created mesh file
# ------------------------------------------------------------

fluent = pyfluent.launch_fluent(start_transcript=False)
fluent.file.read(file_type="mesh", file_name=fluent_msh_file)

# %%
# Define the fluid solver settings.
fluent.setup.models.energy.enabled = True

# %%
# Add the material.
fluent.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

fluent.setup.cell_zone_conditions.fluid["fff_fluiddomain"].material = "water-liquid"

# %%
# Define boundary conditions.
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
# ---------------------------
# System Coupling setup involves adding the structural and fluid
# participants, adding coupled interfaces and data transfers,
# and setting other coupled analysis settings.
syc = pysyc.launch(start_output=True)

# %%
# Add participants by passing session handles to System Coupling.
fluid_name = syc.setup.add_participant(participant_session=fluent)
solid_name = syc.setup.add_participant(participant_session=mapdl)

syc.setup.coupling_participant[fluid_name].display_name = "Fluid"
syc.setup.coupling_participant[solid_name].display_name = "Solid"

# %%
# Add coupling interface.
interface_name = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["inner_wall"],
    side_two_participant=solid_name,
    side_two_regions=["FSIN_1"],
)

# %%
# Set up 2-way thermal FSI coupling.

# Temperature from solid to fluid
temp_transfer = syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="One",
    source_variable="TEMP",
    target_variable="temperature",
)

# Heat flux from fluid to solid
hf_transfer = syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="Two",
    source_variable="heatflow",
    target_variable="HFLW",
)

# %%
# Define constants and calculate Biot number
# ------------------------------------------

L_c = (d_out - d_in) / 2  # Characteristic length of the pipe (thickness)
U = 0.1
fluid_rho = 998.3  # Density of fluid
mu_fluid = 0.001  # Dynamic viscosity of fluid
cp_fluid = 4182  # Specific heat capacity of fluid
k_fluid = 0.6  # Thermal conductivity of fluid
k_solid = 237  # Thermal conductivity of solid


def nusselt_number(Re, Pr, d_in, L):
    # From: Bergman, T. L., Lavine, A. S., Incropera, F. P., & DeWitt, D. P. (2017).
    # Fundamentals of Heat and Mass transfer (8th ed.). Wiley.
    if Re >= 6000:
        Nu = 0.023 * Re**0.8 * Pr**(1/3)
        method = "Colburn"
    else:
        Nu = 3.66 + (0.068 * (Re * Pr * d_in / L)) / (
            1 + 0.04 * (Re * Pr * d_in / L) ** (2 / 3)
        )
        method = "Hausen"

    return Nu, method

def compute_thermo_numbers(rho, mu, cp, k_fluid, k_solid, velocity, d_in, L, L_c):
    Pr = cp * mu / k_fluid
    Re = rho * velocity * d_in / mu

    #Nusselt number
    Nu, correlation= nusselt_number(Re, Pr, d_in, L)

    #Convective heat transfer coefficient
    h= Nu * k_fluid / d_in

    #Biot number
    Bi= h * L_c / k_solid

    return Re, Pr, h, Bi, correlation

Re, Nu, h, Bi, corr= compute_thermo_numbers(fluid_rho, mu_fluid, cp_fluid, k_fluid, k_solid,
                                             U, d_in, l, L_c)

print(f"Reynolds number = {Re}")
print(f"Nusselt number = {Nu}")
print(f"Heat transfer coefficient h = {h} W/(m^2·K)")
print(f"Biot number = {Bi}")
print(f"Nusselt correlation used = {corr}")
# %%
# Apply stabilization if Biot number exceeds 10.
if Bi > 10:
    syc.setup.analysis_control.global_stabilization.option = "Quasi-Newton"

syc.setup.solution_control.time_step_size = "0.1 [s]"  # time step is 0.1 [s]
syc.setup.solution_control.end_time = 10  # end time is 10.0 [s]

syc.setup.output_control.option = "EveryStep"
syc.setup.output_control.generate_csv_chart_output = True

# %%
# Solution
# --------
syc.solution.solve()

# %%
# Post processing
# ---------------
# Post process the fluid results in Fluent.
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

###############################################################################
# .. image:: /_static/cht_temp_contour.png
#   :width: 800pt
#   :align: center

# %%
# Post-process the system coupling results - display the charts showing the convergence plot.
syc.solution.show_plot(show_convergence=True)

# %%
# Exit
# ----
syc.exit()
fluent.exit()
mapdl.exit()
