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

""".. _ref_parametric_sweep_example:

Parametric sweep
----------------

This example is based on a steady fluid-structure interaction (FSI) case
where fluid is flowing over a flexible plate. It shows how to use PySystemCoupling
with other PyAnsys libraries.

The case is run a number of times, with varying Young's modulus value of the
structure. The goal is to extract the maximum plate deflection from each solution
to examine how it respondes to the changing Young's modulus value.

- Ansys Mechanical APDL (MAPDL) is used to perform a steady structural analysis.
- Ansys Fluent is used to perform a steady fluid-flow analysis.
- System Coupling coordinates the coupled solution involving the above products to
  solve the multiphysics problem via co-simulation.

.. image:: /_static/param_sweep_flow.png
   :width: 400pt
   :align: center

"""
# %%
# Import modules, download files, launch products
# -----------------------------------------------
# Setting up this example consists of performing imports, downloading
# the input file, and launching the required products.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import ``ansys-systemcoupling-core``, ``ansys-fluent-core`` and
# ``ansys-mapdl-core`` and other required packages.

# sphinx_gallery_thumbnail_path = '_static/param_sweep_flow.png'

import time

import ansys.fluent.core as pyfluent
import ansys.mapdl.core as pymapdl
import matplotlib.pyplot as plt
import numpy as np

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

# %%
# Download the input file
# ~~~~~~~~~~~~~~~~~~~~~~~
# This example uses one pre-created file - a Fluent input file that
# contains the fluids setup.
#
fluent_cas_file = examples.download_file(
    "case.cas.h5", "pysystem-coupling/parametric_sweep_vel/Fluent"
)

#
#
# Launch instances of Fluent and System Coupling
# and return *client* (session) objects that allow you to interact with
# these products via APIs exposed into the current Python environment.
# Note that instance(s) of Mechanical APDL will be launched
# later in the script.
fluent = pyfluent.launch_fluent(start_transcript=False)
syc = pysyc.launch(start_output=False)

# %%
# Define functions
# ~~~~~~~~~~~~~~~~
# This example is broken into functions that define the main steps that
# must be performed. It makes particular sense to do this for the main task of
# running a coupled analysis because this task must be repeated for multiple
# values of a single input parameter. This is encapsulated in the
# `get_max_displacement` function. In turn, this function is broken into
# further functions that represent its main steps. Also, the function `plot()`
# is defined to plot the final results.


def setup_fluid(fluent):
    """
    Set up the fluid analysis.
    """
    print("Reading Fluent case file...")
    inlet_velocity = 10.0
    fluent.file.read(file_type="case", file_name=fluent_cas_file)
    inlet = fluent.setup.boundary_conditions.velocity_inlet["wall_inlet"]
    inlet.momentum.velocity = inlet_velocity
    print(f"Inlet velocity is set to {inlet_velocity} [m/s]")


def setup_structure(mapdl, youngs_modulus):
    """
    Set up the structural analysis.
    """
    print(f"Setting up MAPDL case")
    mapdl.clear()
    mapdl.prep7()
    # define material properties
    mapdl.mp("DENS", 1, 2550)
    mapdl.mp("ALPX", 1, 1.2e-05)
    mapdl.mp("EX", 1, youngs_modulus)
    print(f"Young's modulus is set to {youngs_modulus} [Pa]")
    mapdl.mp("NUXY", 1, 0.35)
    # set element types to SOLID186
    mapdl.et(1, 186)
    mapdl.keyopt(1, 2, 1)
    # make geometry
    mapdl.block(10.00, 10.06, 0.0, 1.0, 0.0, 0.4)
    mapdl.vsweep(1)
    # add fixed support at y=0
    mapdl.nsel("S", "LOC", "Y", 0)
    mapdl.d("all", "all")
    # add FSI interface
    mapdl.nsel("S", "LOC", "X", 9.99, 10.01)
    mapdl.nsel("A", "LOC", "Y", 0.99, 1.01)
    mapdl.nsel("A", "LOC", "X", 10.05, 10.07)
    mapdl.cm("FSIN_1", "NODE")
    mapdl.sf("FSIN_1", "FSIN", 1)
    mapdl.allsel()
    mapdl.run("/SOLU")
    # set analysis type to steady
    mapdl.antype(0)


def solve_coupled_analysis(syc, fluent, mapdl):
    """
    Set up and solve the coupled analysis.
    """
    print("Setting up the coupled analysis...")
    syc.case.clear_state()
    fluent_name = syc.setup.add_participant(participant_session=fluent)
    mapdl_name = syc.setup.add_participant(participant_session=mapdl)
    fsi_name = syc.setup.add_interface(
        side_one_participant=fluent_name,
        side_one_regions=["wall_deforming"],
        side_two_participant=mapdl_name,
        side_two_regions=["FSIN_1"],
    )
    syc.setup.add_fsi_data_transfers(interface=fsi_name, use_force_density=True)
    syc.setup.solution_control.maximum_iterations = 10
    print("Solving the coupled analysis. This may take a while....")
    syc.solution.solve()
    print("...finished solving coupled analysis.")


def extract_max_displacement(mapdl):
    """
    Post-process mapdl session to extract maximum displacmement.
    """
    print("Extracting max displacement value...")
    mapdl.finish()
    d = mapdl.result.nodal_displacement(0)[1]
    value = max([val[0] for val in d])
    print(f"Max displacement value = {value}")
    return value


def get_max_displacement(fluent, mapdl, syc, youngs_modulus):
    """
    Set up and solve the bending plate FSI problem
    and to extract the maximum plate displacement.
    """
    setup_fluid(fluent)
    setup_structure(mapdl, youngs_modulus)
    solve_coupled_analysis(syc, fluent, mapdl)
    return extract_max_displacement(mapdl)


def plot(x, y):
    """
    Plot Young's modulus on x-axis vs. max displacement on y-axis.
    """
    fig, ax = plt.subplots()
    ax.plot(x, y, "-o")
    ax.set(
        xlabel="Young's modulus [Pa]",
        ylabel="Max Displacement [m]",
        title="Plate max displacement vs. Young's modulus",
    )
    ax.grid()
    plt.savefig("plot")
    plt.show()


# %%
# Run analyses
# ~~~~~~~~~~~~
# Use the `get_max_displacement()` function sequentially, with input
# velocity values provided by an initialized `x` array. The results
# of the calls to the `get_max_displacement()` function are used to
# fill in the corresponding values of the `y` array. Finally, call
# the `plot()` function to generate a plot from the arrays.

x = np.array([2e6, 3e6, 4e6, 5e6, 6e6])
y = np.array([0.0] * len(x))

for index, youngs_modulus in enumerate(x):
    mapdl = pymapdl.launch_mapdl()
    y[index] = get_max_displacement(fluent, mapdl, syc, youngs_modulus)
    mapdl.exit()
    print("Waiting for 1 second until next design point...")
    time.sleep(1)

plot(x, y)

# %%
# Exit
# ----
syc.exit()
fluent.exit()
