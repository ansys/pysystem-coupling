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

fluent_cas_file = examples.download_file(
    "fluent.cas.h5", "pysystem-coupling/heating_tank_fmu/Fluent"
)


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

fluent_session = pyfluent.launch_fluent(start_transcript=False)
fluent_v241 = pyfluent.utils.fluent_version.FluentVersion.v241
assert fluent_session.get_fluent_version() >= fluent_v241

fluent_session.file.read(file_type="case", file_name=fluent_cas_file)

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

# %%
# Post-process the results
# ----------------------------

# %%
# Set some graphics preferences
fluent_session.tui.display.set.lights.lights_on("yes")
fluent_session.tui.preferences.graphics.graphics_effects.grid_plane_enabled("no")
fluent_session.tui.preferences.graphics.graphics_effects.reflections_enabled("no")
fluent_session.tui.preferences.graphics.graphics_effects.simple_shadows_enabled("no")


# %%
# Method to save png images
def save_png(fluent_session, png_name):
    fluent_session.results.graphics.picture.driver_options.hardcopy_format = "png"
    fluent_session.results.graphics.picture.use_window_resolution = False
    fluent_session.results.graphics.picture.x_resolution = 1920
    fluent_session.results.graphics.picture.y_resolution = 1080
    fluent_session.tui.display.save_picture(png_name)


# %%
# Create a plane
normal_plane = "zx"
position = 0.0
plane_name = "plane" + "-" + normal_plane + "-" + str(position)
fluent_session.results.surfaces.plane_surface.create(plane_name)
fluent_session.results.surfaces.plane_surface[plane_name].method = (
    normal_plane + "-plane"
)
fluent_session.results.surfaces.plane_surface[plane_name].y = position

# %%
# Create a mutli-plane
normal_multiplane = "xy"
mutliplane_list = []
number_of_planes = 8
height = 0.14
step = height / (number_of_planes + 2)
for i in range(0, number_of_planes):
    multiplane_name = "plane" + "-" + normal_multiplane + "-" + str(i)
    fluent_session.results.surfaces.plane_surface.create(multiplane_name)
    fluent_session.results.surfaces.plane_surface[multiplane_name].method = (
        normal_multiplane + "-plane"
    )
    fluent_session.results.surfaces.plane_surface[multiplane_name].z = (
        float(i) * step + step
    )
    mutliplane_list.append(multiplane_name)


# %%
# Method to create a contour
def contour(fluent_session, surface_list, surface_name, field, color):
    contour_name = "contour-" + field + "-" + surface_name
    fluent_session.results.graphics.contour.create(contour_name)
    fluent_session.results.graphics.contours.render_mesh = True
    fluent_session.results.graphics.contour[contour_name] = {
        "name": contour_name,
        "field": field,
        "filled": True,
        "boundary_values": True,
        "contour_lines": False,
        "node_values": True,
        "surfaces_list": surface_list,
        "range_option": {
            "option": "auto-range-on",
            "auto_range_on": {"global_range": True},
        },
        "coloring": {"option": "smooth", "smooth": False},
        "color_map": {
            "visible": True,
            "size": 100,
            "color": color,
            "log_scale": False,
            "format": "%0.4g",
            "user_skip": 20,
            "show_all": True,
            "position": 1,
            "font_name": "Helvetica",
            "font_automatic": True,
            "font_size": 0.032,
            "length": 0.54,
            "width": 6.0,
        },
        "display_state_name": "None",
    }
    fluent_session.results.graphics.contour[contour_name].display()
    scene(fluent_session, contour_name)


# %%
# Method to create a vector
def vector(fluent_session, surfaces_list, surface_name, field):
    vector_name = "vectors-" + field + "-" + surface_name
    fluent_session.results.graphics.vector.create(vector_name)
    fluent_session.results.graphics.vector[vector_name].style = "arrow"
    fluent_session.results.graphics.vector[vector_name].scale.scale_f = 0.6
    fluent_session.results.graphics.vector[vector_name].field = field
    fluent_session.results.graphics.vector[vector_name].surfaces_list = surfaces_list
    fluent_session.results.graphics.vector[vector_name] = {
        "color_map": {
            "visible": True,
            "size": 100,
            "color": "field-temperature",
            "log_scale": False,
            "format": "%0.4g",
            "user_skip": 20,
            "show_all": True,
            "position": 1,
            "font_name": "Helvetica",
            "font_automatic": True,
            "font_size": 0.032,
            "length": 0.54,
            "width": 6.0,
        }
    }
    fluent_session.results.graphics.vector[vector_name].display()
    scene(fluent_session, vector_name)


# %%
# Method to define the outline of an object
def outline(fluent_session):
    fluent_session.results.graphics.mesh.create("outline")
    fluent_session.results.graphics.mesh["outline"].coloring.option = "manual"
    fluent_session.results.graphics.mesh["outline"].surfaces_list = [
        "wall",
        "heat_source",
        "top",
        "sensor",
    ]
    fluent_session.results.graphics.mesh["outline"].coloring.manual.faces = "light gray"


# %%
# Method to create a scene
def scene(fluent_session, object_name):
    scene_name = "scene-" + object_name
    fluent_session.results.scene.create(scene_name)
    fluent_session.results.scene[scene_name] = {}
    fluent_session.results.scene[scene_name].graphics_objects["outline"] = {}
    fluent_session.results.scene[scene_name].graphics_objects[
        "outline"
    ].transparency = 90
    fluent_session.results.scene[scene_name].graphics_objects[object_name] = {}
    fluent_session.results.scene[scene_name].display()
    fluent_session.results.graphics.views.restore_view(view_name="top")
    fluent_session.results.graphics.views.camera.orbit(right=140, up=20)
    fluent_session.results.graphics.views.camera.zoom(factor=1.1)
    save_png(fluent_session, scene_name)


# %%
# Create the outline of the object
outline(fluent_session)

# %%
# Create contours and vectors
contour(
    fluent_session,
    surface_list=["plane-zx-0.0"],
    surface_name="plane-zx-0.0",
    field="total-temperature",
    color="field-temperature",
)
contour(
    fluent_session,
    surface_list=["plane-zx-0.0"],
    surface_name="plane-zx-0.0",
    field="velocity-magnitude",
    color="field-velocity",
)
contour(
    fluent_session,
    surface_list=mutliplane_list,
    surface_name="multiplane-xy",
    field="total-temperature",
    color="field-temperature",
)
contour(
    fluent_session,
    surface_list=mutliplane_list,
    surface_name="multiplane-xy",
    field="velocity-magnitude",
    color="field-velocity",
)
vector(
    fluent_session,
    surfaces_list=["plane-zx-0.0"],
    surface_name="plane-zx-0.0",
    field="total-temperature",
)

# %%
# Results
# ------------
# Total temperature on zx plane at y = 0
#
# .. image:: /_static/images/heating_tank_fmu/scene-contour-total-temperature-plane-zx-0.png
#   :width: 500pt
#   :align: center
#
# Velocity magnitude on zx plane at y = 0
#
# .. image:: /_static/images/heating_tank_fmu/scene-contour-velocity-magnitude-plane-zx-0.png
#   :width: 500pt
#   :align: center
#
# Total temperature on multi-xy plane
#
# .. image:: /_static/images/heating_tank_fmu/scene-contour-total-temperature-multiplane-xy.png
#   :width: 500pt
#   :align: center
#
# Velocity magnitude on multi-xy plane
#
# .. image:: /_static/images/heating_tank_fmu/scene-contour-velocity-magnitude-multiplane-xy.png
#   :width: 500pt
#   :align: center
#
# Total temperature on velocity vectors on zx plane at y = 0
#
# .. image:: /_static/images/heating_tank_fmu/scene-vectors-total-temperature-plane-zx-0.png
#   :width: 500pt
#   :align: center
