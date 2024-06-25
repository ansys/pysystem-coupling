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
# Set up example
# --------------
# Setting up this example consists of performing imports, downloading
# input files, and launching System Coupling.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the ``ansys-systemcoupling-core`` package and other required packages.

# sphinx_gallery_thumbnail_path = '_static/heating_tank_fmu.png'

import shutil

import ansys.fluent.core as pyfluent

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download input files
# ~~~~~~~~~~~~~~~~~~~~
# Clear the downloads target directory (which is to be used as the
# working directory). Download the case file for Fluent and the FMU file, which
# define the participant-specific setup information.

examples.delete_downloads()
fmu_file = examples.download_file(
    "thermostat.fmu", "pysystem-coupling/heating_tank_fmu/FMU"
)

fmu_file = "thermostat.fmu"

fluent_cas_file = examples.download_file(
    "fluent.cas.h5", "pysystem-coupling/heating_tank_fmu/Fluent"
)

shutil.copy(fluent_cas_file, "fluent.cas.h5")


# %%
# Launch Fluent
# ~~~~~~~~~~~~~~~~~~~~~~
# Launch a remote Fluent instance and return a *client* object
# (a ``Session`` object) that allows you to interact with Fluent
# via an API exposed into the current Python environment.
# Read in the Fluent case file.
#
# .. note::
#    Fluent version greater than 24.1 is required.
#    To specify Fluent version explicitly when launching Fluent,
#    use ``product_version`` argument to the ``launch_fluent``
#    function, e.g. ``pyfluent.launch_fluent(product_version="24.2.0")``

custom_config = {"fluent_image": "ghcr.io/ansys/pyfluent:v24.2.0"}
print("Launching Fluent Container")
fluent_session = pyfluent.launch_fluent(
    start_transcript=False, container_dict=custom_config
)
fluent_v241 = pyfluent.utils.fluent_version.FluentVersion.v241
assert fluent_session.get_fluent_version() >= fluent_v241
print("Reading Fluent case file")
fluent_session.file.read(file_type="case", file_name=fluent_cas_file)

# %%
# Launch System Coupling
# ~~~~~~~~~~~~~~~~~~~~~~
# Launch a remote System Coupling instance and return a *client* object
# (a ``Session`` object) that allows you to interact with System Coupling
# via an API exposed into the current Python environment.
print("Launching System Coupling Container")
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
# representing the Fluent and FMU participants, based on the setup
# information that was previously defined in the respective
# products.
fluent_part_name = setup.add_participant(participant_session=fluent_session)
fmu_part_name = setup.add_participant(input_file=fmu_file)


# %%
# FMU settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Change FMU parameters by accessing ``fmu_parameter``

# Change the "maximum heat output" settings
setup.coupling_participant[fmu_part_name].fmu_parameter["Real_2"].real_value = 10.0
setup.coupling_participant[fmu_part_name].fmu_parameter[
    "Real_2"
].display_name = "Maximum Heat Output"
# %%
# Change the "target temperature" settings
setup.coupling_participant[fmu_part_name].fmu_parameter["Real_3"].real_value = 350
setup.coupling_participant[fmu_part_name].fmu_parameter[
    "Real_3"
].display_name = "Target_Temperature"

# %%
# Change the "heat scale factor" settings
setup.coupling_participant[fmu_part_name].fmu_parameter["Real_4"].real_value = 2.0
setup.coupling_participant[fmu_part_name].fmu_parameter[
    "Real_4"
].display_name = "Heat_Scale_Factor"

# %%
# Create interfaces and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create interfaces and data transfers by specifying participant regions.
# This consists of calling the appropriate commands to create an interface
# and both force and displacement data transfers.

# Create a coupling interface for Fluent -> FMU (sensor to FMU)
sensor_interface = setup.add_interface(
    side_one_participant=fluent_part_name,
    side_one_regions=["sensor"],
    side_two_participant=fmu_part_name,
)

# Create a coupling interface for FMU -> Fluent (FMU to heat source)
heatSourceInterface = setup.add_interface(
    side_one_participant=fmu_part_name,
    side_two_participant=fluent_part_name,
    side_two_regions=["heat_source"],
)

# Create data transfer for "temperature"
temperatureDataTransfer = setup.add_data_transfer(
    interface=sensor_interface,
    target_side="Two",
    source_variable="temperature",
    target_variable="Real_0",
)

# Create data transfer for "heatflow"
heatFlowDataTransfer = setup.add_data_transfer(
    interface=heatSourceInterface,
    target_side="Two",
    source_variable="Real_1",
    target_variable="heatflow",
)

# %%
# Change the ``time_step_size`` setting.
setup.solution_control.time_step_size = "0.5 [s]"

# %%
# Change the ``end_time`` setting.
setup.solution_control.end_time = "40.0 [s]"

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
# Terminate the system coupling session with ``exit``.
syc.exit()
