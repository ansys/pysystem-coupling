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
    - Density [kg/m\ :sup:`3`\ ] and specific heat [W/kgK] of the fluid
      (by default, set to the properties of water)
    - Convection heat transfer coefficient between the fluid and its
      surroundings [W/m\ :sup:`2`\ K]
    - Temperature of the tank's surroundings [K].

The thermostat receives a temperature from the tank sensor and outputs
a heat-rate. The FMU has three parameters that can be set:

    - Target temperature [K]
    - Maximum heat output [W]
    - Heat scale factor [W/K].

Two coupling interfaces :

    - sensor coupling interface
    - heat source coupling interface

Two data transfers :

    - temperature
    - heat flow

"""

# Tags: FMU, transient

# %%
# Set up example
# --------------
# Setting up this example consists of performing imports, downloading
# input files, and launching System Coupling.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the ``ansys-systemcoupling-core`` package and other required packages.

# sphinx_gallery_thumbnail_path = '_static/heating_tank_fmu.png'

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download input files
# ~~~~~~~~~~~~~~~~~~~~
# Clear the downloads target directory (which is to be used as the
# working directory). Download the FMU files, which define the
# participant-specific setup information.

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
syc = pysystemcoupling.launch()

# %%
# Create analysis
# ---------------
# Creating the analysis consists of accessing the ``setup`` API,
# loading participants, creating and verifying both interfaces and
# data transfers, querying for setup errors, and modifying settings.
#
# Access the ``setup`` API
# ~~~~~~~~~~~~~~~~~~~~~~~~
setup = syc.setup


# %%
# Add participants
# ~~~~~~~~~~~~~~~~~
# Use ``add_participant`` to create ``coupling_participant`` objects
# representing the FMU participants, based on the previously defined
# setup information.
heater_part_name = setup.add_participant(input_file=fmu_file_heater)
tank_part_name = setup.add_participant(input_file=fmu_file_tank)


# %%
# FMU settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Change FMU parameters by accessing ``fmu_parameter``

# Change the "maximum heat output" settings
setup.coupling_participant[heater_part_name].fmu_parameter["Real_2"].real_value = 10.0

# %%
# Change the "target temperature" settings
setup.coupling_participant[heater_part_name].fmu_parameter["Real_3"].real_value = 350.0

# %%
# Change the "heat scale factor" settings
setup.coupling_participant[heater_part_name].fmu_parameter["Real_4"].real_value = 2.0

# %%
# Create interfaces and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create interfaces and data transfers by specifying participant variables
# to map to one another. This consists of calling the appropriate commands
# to create an interface and both temperature and heat flow data transfers.

# Create a coupling interface for tank <-> heater (sensor, heat source)
interface = setup.add_interface(
    side_one_participant=tank_part_name, side_two_participant=heater_part_name
)

# Create data transfer for "temperature"
temperatureDataTransfer = setup.add_data_transfer(
    interface=interface,
    target_side="Two",
    source_variable="Real_0",
    target_variable="Real_0",
)

# Create data transfer for "heatflow"
heatFlowDataTransfer = setup.add_data_transfer(
    interface=interface,
    target_side="One",
    source_variable="Real_1",
    target_variable="Real_1",
)

# %%
# Change the ``time_step_size`` setting.
setup.solution_control.time_step_size = "1 [s]"

# %%
# Change the ``end_time`` setting.
setup.solution_control.end_time = "50 [s]"

# %%
# Change the ``minimum_iterations`` and ``maximum_iterations`` settings.
setup.solution_control.minimum_iterations = 1
setup.solution_control.maximum_iterations = 5

# %%
# Set the ``option`` setting.
setup.output_control.option = "StepInterval"

# %%
# Change the ``output_frequency`` frequency setting.
setup.output_control.output_frequency = 2

# %%
# Change the ``generate_csv_chart_output`` setting to record the temperature
# and heat rate values over time in a ``.csv`` file. This step is necessary
# to chart the data after solving.
setup.output_control.generate_csv_chart_output = True

# %%
# Run solution
# ------------
# The System Coupling server's ``stdout`` and ``stderr`` output is not shown
# in PySystemCoupling by default. To see it, turn output streaming on.
syc.start_output()

# %%
# Access the ``solve`` command via the ``solution`` API.
solution = syc.solution
solution.solve()

# %%
# Plot graphs of temperature and heat rate over time using System Coupling's
# charting command.
syc.solution.show_plot(interface_name=interface, show_convergence=False)

# %%
# Terminate the system coupling session with ``exit``.
syc.exit()
