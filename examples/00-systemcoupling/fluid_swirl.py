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

""".. _ref_fluid_swirl_example:

Fluid swirl
-----------

This example illustrates a one-way data transfer from a SCDT file to
Fluent, using System Coupling. Fluent solves a simple steady fluid
flow problem, where the flow is affected by the momentum sources
defined in the SCDT file.

**Problem description**

Fluid flow problem consists of the water flowing through the pipe.

.. image:: /_static/fluid_swirl_setup.png
   :width: 400pt
   :align: center

The SCDT file will be generated that consists of a cloud of points
overlapping the fluid domain. At each point, the force density value
is defined, with force acting along the flow cross-section, always in a
counter-clockwise direction (if looking from the inlet to the outlet).

System Coupling is used to map the data from the cloud of points defined
in the SCDT file onto Fluent mesh. The force values are then transferred
into Fluent and Fluent solves the resulting fluid flow problem, where
the fluid is influenced by the provided forces. As a result, the
swirl is induced in the fluid flow.

"""

# Tags: SCDT, Fluent, steady

# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of performing imports, downloading
# the input file, and launching the required products.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the ``ansys-systemcoupling-core`` package and other required packages.

# sphinx_gallery_thumbnail_path = '_static/fluid_swirl_point_cloud.png'

import math

import ansys.fluent.core as pyfluent

import ansys.systemcoupling.core as pysystemcoupling
from ansys.systemcoupling.core import examples

# %%
#
# Download input files
# ~~~~~~~~~~~~~~~~~~~~
# Download the case file for Fluent and the FMU file.

fluent_cas_file = examples.download_file(
    "water_pipe_flow.cas.h5", "pysystem-coupling/fluid-swirl"
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
fluent = pyfluent.launch_fluent(start_transcript=True, processor_count=4)
syc = pysystemcoupling.launch(start_output=False)

# %%
# Setup
# -----
# The setup consists of setting up the the fluids analysis,
# generating the SCDT file, and setting up the coupled analysis.

# %%
# Set up the fluid analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Read the pre-created case file.
fluent.file.read(file_type="case", file_name=fluent_cas_file)

# %%
# Generate the SCDT file
# ~~~~~~~~~~~~~~~~~~~~~~
# The following script generates a simple comma-separated file
# with points defined along the fluid domain. Six columns of data
# will be written: x, y, z coordinate values, followed by
# x-, y-, and z-components of the force density field.
# The number of points can be adjusted by `naxial`, `ncirc`,
# and `nrad` parameter values.
# The magnitude of the force (defined in N/m^3) can be adjusted
# by `force_mag` parameter value.


def create_source_file(file_name):
    force_mag = 5.0
    naxial = 33
    ncirc = 10
    nrad = 20
    radius = 0.025
    with open(file_name, "w") as f:
        for xi in range(naxial):
            x = (1.0 - 0.0) * xi / (naxial - 1)
            for ti in range(ncirc):
                theta = 2.0 * math.pi * ti / ncirc
                for ri in range(nrad):
                    r = radius * (ri + 1) / nrad
                    z = r * math.cos(theta)
                    y = r * math.sin(theta)
                    fx = 0.0
                    fy = force_mag * math.sin(theta + 0.5 * math.pi)
                    fz = force_mag * math.cos(theta + 0.5 * math.pi)
                    f.write(f"{x}, {y}, {z}, {fx}, {fy}, {fz}\n")


src_file_base_name = "source"
src_file_name = f"{src_file_base_name}.scdt"
create_source_file(src_file_name)

###############################################################################
# .. image:: /_static/fluid_swirl_point_cloud.png
#   :width: 500pt
#   :align: center

# %%
# Set up the coupled analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# System Coupling setup involves adding the SCDT file and
# Fluent solver session as participants, adding coupled
# interfaces and data transfers, and setting other coupled
# analysis properties.

# %%
# Add participants
source_name = syc.setup.add_participant(input_file=src_file_name)
fluid_name = syc.setup.add_participant(participant_session=fluent)


# %%
# Add a coupling interface and data transfers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a coupling interface for SCDT file -> Fluent
interface_name = syc.setup.add_interface(
    side_one_participant=source_name,
    side_one_regions=[src_file_base_name],
    side_two_participant=fluid_name,
    side_two_regions=["tube_solid"],
)

# Add force data transfer.
# Use System Coupling expression to combine force field
# components in the SCDT file into a vector.
# System Coupling will automatically convert force density
# values on the source (defined in [N/m^3]) to force
# values on the target (defined in [N]).
syc.setup.add_data_transfer(
    interface=interface_name,
    target_side="Two",
    target_variable="lorentz-force",
    value="vector(Variable1 * 1.0 [N], Variable2 * 1.0 [N], Variable3 * 1.0 [N])",
)

# %%
# Solution
# --------
syc.solution.solve()

# %%
# Post-processing
# ---------------
# Generate an image with fluid flow streamlines using PyFluent post-processing.
# Note how the force values defined in the SCDT file induce the swirl in
# the fluid flow.
if fluent.results.graphics.picture.use_window_resolution.is_active():
    fluent.results.graphics.picture.use_window_resolution = False

fluent.results.graphics.picture.x_resolution = 1920
fluent.results.graphics.picture.y_resolution = 1440

fluent.results.graphics.pathline["pathline"] = {}
pathline = fluent.results.graphics.pathline["pathline"]
pathline.field = "velocity-magnitude"
pathline.release_from_surfaces = ["in"]
pathline.display()

fluent.results.graphics.views.restore_view(view_name="isometric")
fluent.results.graphics.views.auto_scale()
fluent.results.graphics.picture.save_picture(file_name="fluid_swirl_pathline.png")

###############################################################################
# .. image:: /_static/fluid_swirl_pathline.png
#   :width: 500pt
#   :align: center

# %%
# Exit
# ----

fluent.exit()
syc.exit()
