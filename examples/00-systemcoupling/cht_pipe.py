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

This example illustrates a two way conjugate heat transfer case for
*flow in a pipe* that is used as a tutorial for System Coupling. This Fluid-Structure
interaction (FSI) is based on a steady case fluid flow in a pipe with surface data transfers.

- Ansys Mechanical APDL (MAPDL) is used to perform a structural analysis.
- Ansys Fluent is used to perform a steady fluid-flow analysis.
- System Coupling coordinates the coupled sloution involving the above products to
  solve the multiphysics problem via co-simulation.

**Problem description**

A fluid at a certain temperature flows into a pipe of known diameter and length. As it flows,
the heated wall of the pipe conducts heat to the inner wall, which in turns heats the fluid and
cools down the walls of the pipe.



The flow is smooth inside the pipe and the outer wall of the pipe is adiabatic. Fluid enters
at an initial temperature of 300K while the outside pipe of the wall is at 400K.
The setup is simulated for a few iterations to allow the examination
of the temperature field in the pipe.

"""
# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of performing imports, downloading
# the input file, and launching the required products.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import ``ansys-systemcoupling-core``, ``ansys-fluent-core``

import ansys.fluent.core as pyfluent
import ansys.mapdl.core as pymapdl

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
# Download the mesh file
fluent_msh_file = examples.download_file(
    "fluid_domain.msh", "pysystem-coupling/cht_pipe"
)

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
# Create hollow pipe
mapdl.cyl4(0, 0, rad1=r_in, rad2=r_out, depth=l)
mapdl.esize(0.002)
mapdl.vsweep(1)
print(mapdl.geometry.anum)


# %%
# Biot number prediction
def biot_number(rho=1000, mu=1e-3, cp=4180, k_f=0.6, k_s=237, L_c=r_out - r_in, U=0.1):
    Re = (rho * U * L_c) / mu
    Pr = (mu * cp) / k_f
    Nu = 0.023 * Re**0.8 * Pr**0.4
    h = Nu * k_f / L_c
    Bi = h * L_c / k_s
    return Bi


Bi = biot_number()
print("The Biot number is ", Bi)

# %%
# Creating the regions from the geometry for named selections
# Inner wall NS
mapdl.asel("S", "AREA", "", 5, 6)
mapdl.nsla("S", 1)
mapdl.cm("FSIN_1", "NODE")
mapdl.allsel()

# Outer wall NS
mapdl.asel("S", "AREA", "", 3, 4)
mapdl.cm("Outer_wall", "AREA")
mapdl.allsel()

# Outlet NS
mapdl.asel("S", "AREA", "", 2)
mapdl.cm("Outlet", "AREA")
mapdl.allsel()

# Inlet NS
mapdl.asel("S", "AREA", "", 1)
mapdl.cm("Inlet", "AREA")
mapdl.allsel()

# %%
# Boundary conditions
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
# Set up the fluid analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Read the pre-created mesh file

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
fluent.setup.boundary_conditions.velocity_inlet["inlet"].momentum.velocity = 0.1
fluent.setup.boundary_conditions.velocity_inlet["inlet"].thermal.temperature = 300
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
syc.setup.add_thermal_data_transfers(interface=interface_name)

# %%
# Time step size, end time, output controls
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
