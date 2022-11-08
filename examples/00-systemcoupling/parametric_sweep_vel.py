""".. _parametric_sweep_example:

Parametric sweep example
========================

This example is based on a steady FSI case, where the fluid is flowing over a flexible plate.

The case is run a number of times, with varying fluid inlet velocity. The goal is to extract
the maximum plate deflection from each solution and to examine how it responds to the
changing velocity value.

It illustrates the use of PySystemCoupling in conjunction with some other PyAnsys tools.

.. image:: /_static/param_sweep_flow.png
   :width: 400pt
   :align: center

.. image:: /_static/param_sweep_result.png
   :width: 400pt
   :align: center

"""

# sphinx_gallery_thumbnail_path = '_static/param_sweep_flow.png'

# %%
# Perform required imports
# ------------------------
# In addition to the PySystemCoupling package, we also need to import PyFluent
# and PyDPF for this example. In addition, facilities from `matplotlib` and
# `numpy` are used to produce a simple plot of our results.

import os

import matplotlib.pyplot as plt
import numpy as np

import ansys.dpf.core as pydpf
import ansys.fluent.core as pyfluent
import ansys.systemcoupling.core as pysyc

from ansys.systemcoupling.core import examples


# %%
# Define functions
# ----------------
# This example is broken into functions that define the main steps that
# need to be performed. It makes particular sense to do this for the
# main task of running a coupled analysis as that needs to be repeated
# for multiple values of a single input parameter. This is encapsulated
# in ``get_max_displacement``. In turn, this is broken into further
# functions that represent its main steps. We also define a function that prepares our
# working directory (``setup_working_directory``) and one that plots the final
# results (``plot``).
#
# ``setup_working_directory``
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up the working directory with downloaded
# data files for this example. The Mapdl files will be placed in a
# sub-directory Mapdl of the working directory and the Fluent files
# in a sub-directory Fluent.
#
# The function returns the path of the working directory for later use.

def setup_working_directory():
    examples.delete_downloads()

    mapdl_scp_file = examples.download_file(
        "mapdl.scp", "pysystem-coupling/parametric_sweep_vel/Mapdl"
    )

    fluent_scp_file = examples.download_file(
        "fluent.scp", "pysystem-coupling/parametric_sweep_vel/Fluent"
    )

    mapdl_dat_file = examples.download_file(
        "ds.dat", "pysystem-coupling/parametric_sweep_vel/Mapdl"
    )

    fluent_cas_file = examples.download_file(
        "case.cas.h5", "pysystem-coupling/parametric_sweep_vel/Fluent"
    )

    working_dir = os.path.dirname(mapdl_scp_file)

    fluent_working_dir = os.path.join(working_dir, "Fluent")
    os.mkdir(fluent_working_dir)
    mapdl_working_dir = os.path.join(working_dir, "Mapdl")
    os.mkdir(mapdl_working_dir)

    os.rename(fluent_cas_file, os.path.join(fluent_working_dir, "case.cas.h5"))
    os.rename(mapdl_dat_file, os.path.join(mapdl_working_dir, "ds.dat"))
    os.rename(fluent_scp_file, os.path.join(fluent_working_dir, "fluent.scp"))
    os.rename(mapdl_scp_file, os.path.join(mapdl_working_dir, "mapdl.scp"))

    return working_dir

# %%
# ``set_inlet_velocity``
# ~~~~~~~~~~~~~~~~~~~~~~
# Modify the Fluent case to adjust the
# inlet velocity on the `"wall_inlet"` velocity inlet boundary
# condition. This function will be called with a varying ``inlet_velocity``
# parameter before each call of ``solve_coupled_analysis`` in
# a sequence of analyses.

def set_inlet_velocity(working_dir, inlet_velocity):
  with pyfluent.launch_fluent(precision="double", processor_count=2) as session:
      case_file = os.path.join(working_dir, "Fluent", "case.cas.h5")
      session.solver.root.file.read(file_type="case", file_name=case_file)
      session.solver.root.setup.boundary_conditions.velocity_inlet[
          "wall_inlet"
      ].vmag.constant = inlet_velocity
      session.solver.tui.file.write_case(case_file)

  print(f"Inlet velocity is set to {inlet_velocity}")

# %%
# ``solve_coupled_analysis``
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Perform a single coupled analysis.
#
# In this example, the only change between successive calls to this function
# is in the content of the Fluent input file that is used. The inlet velocity
# setting is modified in the Fluent file prior to this function being called.
#
# .. note::
#    System Coupling is launched anew for each call of
#    this function.
#
#    The ``with pysyc.launch(...)`` syntax ensures
#    that the System Coupling session is properly exited at the
#    end of the scope defined by the ``with`` block.

def solve_coupled_analysis(working_dir):
    with pysyc.launch(working_dir=working_dir) as syc:
        print("Setting up the coupled analysis")

        fluent_name = syc.setup.add_participant(
            input_file = os.path.join("Fluent", "fluent.scp"))

        mapdl_name = syc.setup.add_participant(
            input_file = os.path.join("Mapdl", "mapdl.scp"))

        fsi_name = syc.setup.add_interface(
            side_one_participant = fluent_name, side_one_regions = ['wall_deforming'],
            side_two_participant = mapdl_name, side_two_regions = ['FSIN_1'])

        syc.setup.add_data_transfer(
            interface = fsi_name, target_side = 'One',
            source_variable = 'INCD', target_variable = 'displacement')

        syc.setup.add_data_transfer(
            interface = fsi_name, target_side = 'Two',
            source_variable = 'force', target_variable = 'FORC')

        syc.setup.solution_control.maximum_iterations = 7

        print("Solving the coupled analysis. This may take a while...")
        syc.solution.solve()

    print("...done!")

# %%
# ``extract_max_displacement``
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use PyDPF to query the MAPDL results for the maximum displacement
# value in the solution.
def extract_max_displacement(working_dir):
  print("Extracting max displacement value")
  model = pydpf.Model(os.path.join(working_dir, "Mapdl", "file.rst"))
  displacements = model.results.displacement()
  fields = displacements.outputs.fields_container()
  value = max([v[0] for v in fields[0].data])
  print("Max displacement value = " + str(value))
  return value

# %%
# ``get_max_displacement``
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Use the functions defined above to:
#
# - Modify the Fluent input file to apply the provided ``inlet_velocity`` setting.
# - Run the coupled analysis based on that setting.
# - Extract and return the maximum displacement value from the MAPDL results.
def get_max_displacement(working_dir, inlet_velocity):
  set_inlet_velocity(working_dir, inlet_velocity)
  solve_coupled_analysis(working_dir)
  return extract_max_displacement(working_dir)

# %%
# ``plot``
# ~~~~~~~~
# Generate an `x-y` plot of the results, showing
# maximum displacement of the plate vs the inlet velocity.
#
def plot(working_dir, x, y):
  fig, ax = plt.subplots()
  ax.plot(x, y, "-o")
  ax.set(
    xlabel="Inlet velocity [m/s]",
    ylabel='Max Displacement [m]',
    title="Plate max displacement vs. inlet velocity")
  ax.grid()
  plt.savefig(os.path.join(working_dir, "displacement"))

# %%
# Run the analyses
# ----------------
# Use the ``get_max_displacement`` function sequentially, with input
# velocity values provided by an initialized ``x`` array.
# The results of the ``get_max_displacement`` calls are used to fill in the
# corresponding values of the ``y`` array. Finally, we can call
# the ``plot`` function to generate a plot from the arrays.

x = np.array([5.0, 10.0, 15.0, 20.0, 25.0])
y = np.array([0.0] * len(x))

working_dir = setup_working_directory()

for index, inlet_velocity in enumerate(x):
  y[index] = get_max_displacement(working_dir, inlet_velocity)

plot(working_dir, x, y)