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

This example illustrates a two way conjugate heat transfer case for *flow in a pipe* that is used as
a tutorial for System Coupling. This Fluid-Structure interaction (FSI) is based on a steady case fluid flow
in a pipe with surface data transfers.

- Ansys Mechanical APDL (MAPDL) is used to perform a structural analysis.
- Ansys Fluent is used to perform a steady fluid-flow analysis.
- System Coupling coordinates the coupled sloution involving the above prodcuts to
  solve the multiphysics problem via co-simulation.
    
**Problem description** 

A fluid at a certain temperature flows into a pipe of known diameter and length. As it flows, the heated wall
of the pipe conducts heat to the inner wall, which in turns heats the fluid and cools down the walls of the pipe.
#image

The flow is smooth inside the pipe and the outer wall of the pipe is adiabatic. Fluid enters at an initial 
temperature of 300K while the outside pipe of the wall is at some higher temperature. The setup is simulated for 
a few iterations to allow the examination of the temperature field in the pipe.

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
import ansys.systemcoupling.core as pysyc

#===

# launch Fluent session and read in mesh file
pipe_fluid_session = pyfluent.launch_fluent(start_transcript=False)
pipe_fluid_mesh_file = "pipe_fluid.msh.h5"
pipe_fluid_session.file.read(file_type="mesh", file_name=pipe_fluid_mesh_file)

# turn on energy model
pipe_fluid_session.setup.models.energy.enabled = True

# add water material
pipe_fluid_session.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

# set up cell zone conditions
pipe_fluid_session.setup.cell_zone_conditions.fluid["fluid"].material = "water-liquid"

# set up boundary conditions
pipe_fluid_session.setup.boundary_conditions.velocity_inlet["inlet"].momentum.velocity = 0.1
pipe_fluid_session.setup.boundary_conditions.wall["wall"].thermal.thermal_bc = "via System Coupling"

# set up solver settings - 1 fluent iteration per 1 coupling iteration
pipe_fluid_session.solution.run_calculation.iter_count = 1

#===

# launch another Fluent session and read in mesh file
pipe_solid_session = pyfluent.launch_fluent(start_transcript=False)
pipe_solid_mesh_file = "pipe_solid.msh.h5"
pipe_solid_session.file.read(file_type="mesh", file_name=pipe_solid_mesh_file)

# turn on energy model
pipe_solid_session.setup.models.energy.enabled = True

# add copper material
pipe_solid_session.setup.materials.database.copy_by_name(type="solid", name="copper")

# set up cell zone conditions
pipe_solid_session.setup.cell_zone_conditions.solid["solid"].material = "copper"

# set up boundary conditions
pipe_solid_session.setup.boundary_conditions.wall["outer_wall"].thermal.thermal_bc = "Temperature"
pipe_solid_session.setup.boundary_conditions.wall["outer_wall"].thermal.t.value = 350

pipe_solid_session.setup.boundary_conditions.wall["inner_wall"].thermal.thermal_bc = "via System Coupling"

pipe_solid_session.setup.boundary_conditions.wall["insulated1"].thermal.thermal_bc = "Heat Flux"
pipe_solid_session.setup.boundary_conditions.wall["insulated1"].thermal.q.value = 0

pipe_solid_session.setup.boundary_conditions.wall["insulated2"].thermal.thermal_bc = "Heat Flux"
pipe_solid_session.setup.boundary_conditions.wall["insulated2"].thermal.q.value = 0

# set up solver settings - 1 fluent iteration per 1 coupling iteration
pipe_solid_session.solution.run_calculation.iter_count = 1

import numpy as np


rho_water = 998.2          
mu_water  = 1.002e-3       
k_water   = 0.6            
Pr_water  = 7.0            

rho_al    = 2700           
k_al      = 237            
cp_al     = 900            


# Flow and Geometry

u         = 0.5            # velocity [m/s]
L         = 0.5            # pipe length [m]
D         = 0.1            # inner diameter [m] → characteristic length for fluid
t_wall    = 0.12           # wall thickness [m] → characteristic length for solid conduction


# Functions

def getReynoldsNumber(rho, u, D, mu):
    return rho * u * D / mu

def getPrandtlNumber(mu, cp, k):
    return mu * cp / k

def getNusseltNumber(Re, Pr, L_over_D):
    
    if Re < 2300:
        Nu = 3.66  # laminar, fully developed
    elif Re < 10000:
        Nu = 0.023 * Re**0.8 * Pr**0.4  # transitional approximation
    else:
        Nu = 0.023 * Re**0.8 * Pr**0.4  # fully turbulent
    return Nu

def getConvectionCoefficient(Nu, k_fluid, D):
    return Nu * k_fluid / D

def getBiotNumber(h, k_solid, t_wall):
    return h * t_wall / k_solid


Re = getReynoldsNumber(rho_water, u, D, mu_water)
Pr = Pr_water  # directly used
L_over_D = L / D

Nu = getNusseltNumber(Re, Pr, L_over_D)
h  = getConvectionCoefficient(Nu, k_water, D)
Bi = getBiotNumber(h, k_al, t_wall)


print(f"{'Parameter':<25} {'Value':<15} {'Unit'}")
print("-" * 50)
print(f"{'Reynolds Number (Re)':<25} {Re:<15.2f}")
print(f"{'Prandtl Number (Pr)':<25} {Pr:<15.1f}")
print(f"{'Nusselt Number (Nu)':<25} {Nu:<15.2f}")
print(f"{'Convection coeff (h)':<25} {h:<15.1f} W/m²·K")
print(f"{'Biot Number (Bi)':<25} {Bi:<15.6f}")
print("-" * 50)
print(f"The Biot number is {Bi:.6f}")


if Bi < 0.1:
    print("→ Bi < 0.1 → Lumped capacitance valid (uniform wall temperature)")
elif Bi > 10:
    print("→ Bi > 10 → Significant temperature gradient in wall")
else:
    print("→ 0.1 < Bi < 10 → Moderate internal resistance")
#===

# launch System Coupling session
syc = pysyc.launch()
syc.start_output()

# add two Fluent sessions above as participants
fluid_name = syc.setup.add_participant(participant_session = pipe_fluid_session)
solid_name = syc.setup.add_participant(participant_session = pipe_solid_session)
syc.setup.coupling_participant[fluid_name].display_name = "Fluid"
syc.setup.coupling_participant[solid_name].display_name = "Solid"

# add a coupling interface
interface = syc.setup.add_interface(
  side_one_participant = fluid_name, side_one_regions = ["wall"],
  side_two_participant = solid_name, side_two_regions = ["inner_wall"])

# set up 2-way coupling - add temperature and heat flow data transfers
syc.setup.add_thermal_data_transfers(interface = interface)

# set up coupled analysis settings
# it should take about 80 iterations to converge
syc.setup.solution_control.maximum_iterations = 100

#===

# solve the coupled analysis
syc.solution.solve()

#===

# clean up at the end
syc.end_output()
pipe_fluid_session.exit()
pipe_solid_session.exit()
syc.exit()