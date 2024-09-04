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

""".. _ref_heating_tank_fmu_example:

Heating tank with a Functional Mock-up Unit (FMU)
-------------------------------------------------

This demo illustrates a transient coupled simulation of convection
heating of a fluid in a cylindrical tank. Fluent is used to prepare
the thermal analysis while heat flow in source is controlled via an FMU,
by taking the temperature from a sensor as an input.

- Ansys Fluent is used to perform the transient fluid-thermal analysis.
- FMU is used to control the heat flow at the bottom of the tank.
- System Coupling coordinates the simultaneous execution of the solvers for
  these Ansys products and the data transfers between their coupled surface regions.

**Problem description**

Heating tank with FMU:

.. image:: /_static/heating_tank_fmu.png
   :width: 400pt
   :align: center

The thermostat receives a temperature from the Fluent sensor
and outputs a heat-rate. The FMU has three parameters that
can be set:

    - Target temperature [K]
    - Maximum heat output [W]
    - Heat scale factor [W/K].

Two coupling interfaces :

    - sensor-FMU coupling interface
    - heat source- FMU coupling interface

Two data transfers :

    - temperature
    - heat flow

"""

# Tags: FMU, Fluent, transient

# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of performing imports, downloading
# the input file, and launching the required products.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the ``ansys-systemcoupling-core`` package and other required packages.

# sphinx_gallery_thumbnail_path = '_static/heating_tank_fmu.png'

import ansys.fluent.core as pyfluent

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download input files
# ~~~~~~~~~~~~~~~~~~~~
# Download the case file for Fluent and the FMU file.

fmu_file = examples.download_file(
    "thermostat.fmu", "pysystem-coupling/heating_tank_fmu/FMU"
)

fluent_cas_file = examples.download_file(
    "fluent.cas.h5", "pysystem-coupling/heating_tank_fmu/Fluent"
)


# %%
# Launch products
# ~~~~~~~~~~~~~~~
# Launch a remote Fluent and System Coupling instances and
# return *client* objects that allows you to interact with
# these products via an API exposed into the current Python
# environment.
#
# .. note::
#    Fluent version greater than 24.1 is required.
#    To specify Fluent version explicitly when launching Fluent,
#    use ``product_version`` argument to the ``launch_fluent``
#    function, for example ``pyfluent.launch_fluent(product_version="24.2.0")``
fluent = pyfluent.launch_fluent(start_transcript=False)
syc = pysystemcoupling.launch(start_output=True)

# %%
# Setup
# -----
# The setup consists of setting up the the fluids analysis
# and the coupled analysis.

# %%
# Set up the fluid analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Read the pre-created case file.
fluent.file.read(file_type="case", file_name=fluent_cas_file)

# %%
# Set up the coupled analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# System Coupling setup involves adding the fluid and FMU
# participants, adding coupled interfaces and data transfers,
# and setting other coupled analysis properties.

# %%
# Add participants
fluid_name = syc.setup.add_participant(participant_session=fluent)
fmu_name = syc.setup.add_participant(input_file=fmu_file)

# %%
# Set FMU settings

fmu_participant = syc.setup.coupling_participant[fmu_name]

# Change the "maximum heat output" settings
max_heat_output_param = fmu_participant.fmu_parameter["Real_2"]
max_heat_output_param.real_value = 10.0
max_heat_output_param.display_name = "Maximum_Heat_Output"

# Change the "target temperature" settings
target_temperature_param = fmu_participant.fmu_parameter["Real_3"]
target_temperature_param.real_value = 350
target_temperature_param.display_name = "Target_Temperature"

# Change the "heat scale factor" settings
heat_scale_factor_param = fmu_participant.fmu_parameter["Real_4"]
heat_scale_factor_param.real_value = 2.0
heat_scale_factor_param.display_name = "Heat_Scale_Factor"

# %%
# Add a coupling interface and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a coupling interface for Fluent sensor region -> FMU
sensor_interface_name = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["sensor"],
    side_two_participant=fmu_name,
)

# Add the temperature data transfer
temperature_transfer_name = syc.setup.add_data_transfer(
    interface=sensor_interface_name,
    target_side="Two",
    source_variable="temperature",
    target_variable="Real_0",
)

# Add a coupling interface for FMU -> Fluent heat source region
heat_source_interface_name = syc.setup.add_interface(
    side_one_participant=fmu_name,
    side_two_participant=fluid_name,
    side_two_regions=["heat_source"],
)

# Add the heat flow data transfer
heatflow_transfer_name = syc.setup.add_data_transfer(
    interface=heat_source_interface_name,
    target_side="Two",
    source_variable="Real_1",
    target_variable="heatflow",
)

# %%
# Other controls

# Set time step size
syc.setup.solution_control.time_step_size = "0.5 [s]"

# Set the simulation end time
syc.setup.solution_control.end_time = "40.0 [s]"

# Set minimum and maximum iterations per time step
syc.setup.solution_control.minimum_iterations = 1
syc.setup.solution_control.maximum_iterations = 5

# Turn on chart output
syc.setup.output_control.generate_csv_chart_output = True

# %%
# Solution
# --------
syc.solution.solve()

# %%
# Post-processing
# ---------------
# Print the chart displaying sensor temperature over time
syc.solution.show_plot(
    interface_name=sensor_interface_name,
    show_convergence=False,
)

# %%
# Exit
# ----

syc.exit()
