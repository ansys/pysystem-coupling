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

""".. _ref_heating_tank_fmu_fmu_example:

FMU-FMU cosimulation of a heating tank & heater
-------------------------------------------------

This demo illustrates a transient coupled simulation of convection
heating of a fluid in a cylindrical tank. The heat source and heating
tank are controlled via two FMUs that share temperature and heat flow
data with one another.

- One FMU is used to model the fluid in the tank.
- Another FMU is used to model the controlled heat source at the bottom
  of the tank.
- System Coupling coordinates the simultaneous execution of the solvers
  and the data transfers between them.

**Problem description**

The tank is modelled as a uniform-temperature fluid heated by a
thermostat and experiencing convective cooling at its top. The
temperature of the fluid is available as an output, modelling a sensor
in the tank. The FMU has six parameters that can be set:

    - Height and base radius of the cylindrical tank [m]
    - Density [kg m\ :sup:`-3`\ ] and specific heat [W kg\ :sup:`-1`\ K\ :sup:`-1`\] of the fluid
      (by default, set to the properties of water)
    - Convection heat transfer coefficient between the fluid and its
      surroundings [W m\ :sup:`-2`\ K\ :sup:`-1`\]
    - Temperature of the tank's surroundings [K].

The thermostat receives a temperature from the tank sensor and outputs
a heat-rate. The FMU uses PID (proprtional-integral-derivative) control
to determine the heat output and has five parameters that can be set:

    - Target temperature [K]
    - Maximum heat output [W]
    - Heat scale proportional factor [W/K]
    - Heat scale integral factor [W K\ :sup:`-1`\ s\ :sup:`-1`\]
    - Heat scale derivative factor [W s K\ :sup:`-1`\]

One coupling interface between the FMUs with two data transfers :

    - temperature
    - heat flow

"""

# Tags: FMU, transient

# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of importing required modules,
# downloading the input files, and launching the required products.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import ``ansys-systemcoupling-core``.

# sphinx_gallery_thumbnail_path = '_static/fmu_fmu.png'

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download the input files
# ~~~~~~~~~~~~~~~~~~~~~~~~
# This example requires the two FMU files to be downloaded.
#

examples.delete_downloads()
fmu_file_heater = examples.download_file(
    "thermostat.fmu", "pysystem-coupling/heating_tank_fmu/FMU"
)
fmu_file_tank = examples.download_file(
    "heatingTank.fmu", "pysystem-coupling/heating_tank_fmu_fmu/FMU"
)


# %%
# Launch System Coupling
# ~~~~~~~~~~~~~~~~~~~~~~
# Launch a remote System Coupling instance and return a *client* object
# (a ``Session`` object) that allows you to interact with System Coupling
# via an API exposed into the current Python environment.
syc = pysystemcoupling.launch(start_output=True)

# %%
# Set up the coupled analysis
# ---------------------------
# System Coupling setup involves adding the two FMU participants,
# adding coupled interfaces and data transfers,
# and setting other coupled analysis properties.
#

# %%
# Add participants by passing session handles to System Coupling.
heater_part_name = syc.setup.add_participant(input_file=fmu_file_heater)
tank_part_name = syc.setup.add_participant(input_file=fmu_file_tank)


# %%
# Set FMU settings
# ~~~~~~~~~~~~~~~~

# Access the heater participant object
heater_participant = syc.setup.coupling_participant[heater_part_name]

# Change the "maximum heat output" settings
max_heat_output_param = heater_participant.fmu_parameter["Real_2"]
max_heat_output_param.real_value = 1000

# Change the "target temperature" settings
target_temperature_param = heater_participant.fmu_parameter["Real_3"]
target_temperature_param.real_value = 350

# Change the "heat scale proportional factor" settings
heat_p_factor_param = heater_participant.fmu_parameter["Real_4"]
heat_p_factor_param.real_value = 400

# Change the "heat scale integral factor" settings
heat_i_factor_param = heater_participant.fmu_parameter["Real_5"]
heat_i_factor_param.real_value = 0

# Change the "heat scale derivative factor" settings
heat_d_factor_param = heater_participant.fmu_parameter["Real_6"]
heat_d_factor_param.real_value = 0

# Access the heating tank participant object
tank_participant = syc.setup.coupling_participant[tank_part_name]

# Change the "tank height" settings
tank_height_param = tank_participant.fmu_parameter["Real_2"]
tank_height_param.real_value = 0.14

# Change the "tank radius" settings
tank_radius_param = tank_participant.fmu_parameter["Real_3"]
tank_radius_param.real_value = 0.05

# Change the "fluid density" settings
fluid_density_param = tank_participant.fmu_parameter["Real_4"]
fluid_density_param.real_value = 998.2

# Change the "fluid heat capacity" settings
fluid_heat_capacity_param = tank_participant.fmu_parameter["Real_5"]
fluid_heat_capacity_param.real_value = 4182

# Change the "convection heat transfer coefficient" settings
convection_coeff_param = tank_participant.fmu_parameter["Real_6"]
convection_coeff_param.real_value = 10

# Change the "surrounding temperature" settings
surrounding_temp = tank_participant.fmu_parameter["Real_7"]
surrounding_temp.real_value = 295

# %%
# Add a coupling interface and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a coupling interface for tank <-> heater (sensor, heat source)
fmu_interface_name = syc.setup.add_interface(
    side_one_participant=tank_part_name, side_two_participant=heater_part_name
)

# Add the temperature data transfer
temperature_transfer_name = syc.setup.add_data_transfer(
    interface=fmu_interface_name,
    target_side="Two",
    source_variable="Real_0",
    target_variable="Real_0",
)

# Add the heat flow data transfer
heatflow_transfer_name = syc.setup.add_data_transfer(
    interface=fmu_interface_name,
    target_side="One",
    source_variable="Real_1",
    target_variable="Real_1",
)

# %%
# Other controls

# Set time step size
syc.setup.solution_control.time_step_size = "4 [s]"

# Set the simulation end time
syc.setup.solution_control.end_time = "400 [s]"

# Set minimum and maximum number of iterations to 1
# to emulate explicit update.
syc.setup.solution_control.minimum_iterations = 1
syc.setup.solution_control.maximum_iterations = 1

# Turn on chart output. This step is necessary
# to chart the data after solving.
syc.setup.output_control.generate_csv_chart_output = True

# %%
# Solution
# --------
syc.solution.solve()

# %%
# Post-processing
# ---------------
# Plot graphs of temperature and heat rate over time using System Coupling's
# charting command.
syc.solution.show_plot(interface_name=fmu_interface_name, show_convergence=False)

# %%
# Exit
# ----
syc.exit()
