import os

def solve_coupled_analysis():
  import ansys.systemcoupling.core as pysyc

  with pysyc.launch() as syc:

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

def set_inlet_velocity(inlet_velocity):
  import ansys.fluent.core as pyfluent
  with pyfluent.launch_fluent(precision="double", processor_count=2) as session:
      case_file = os.path.join("Fluent", "case.cas.gz")
      session.solver.root.file.read(file_type="case", file_name=case_file)
      session.solver.root.setup.boundary_conditions.velocity_inlet[
          "wall_inlet"
      ].vmag = inlet_velocity
      session.solver.tui.file.write_case(case_file)

  print(f"Inlet velocity is set to {inlet_velocity}")

def extract_max_displacement_value():
  print("Extracting max displacement value")
  import ansys.dpf.core as pydpf
  model = pydpf.Model(os.path.join(os.getcwd(), "Mapdl", "file.rst"))
  displacements = model.results.displacement()
  fields = displacements.outputs.fields_container()
  value = max([v[0] for v in fields[0].data])
  print("Max displacement value = " + str(value))
  return value

def get_max_displacement(inlet_velocity):
  set_inlet_velocity(inlet_velocity)
  solve_coupled_analysis()
  return extract_max_displacement_value()

def plot(x, y):
  import matplotlib.pyplot as plt
  fig, ax = plt.subplots()
  ax.plot(x, y, "-o")
  ax.set(
    xlabel="Inlet velocity [m/s]",
    ylabel='Max Displacement [m]',
    title="Plate max displacement vs. inlet velocity")
  ax.grid()
  plt.show()

# =====================================================================

import numpy as np

x = np.array([5.0, 10.0, 15.0, 20.0, 25.0])
y = np.array([0.0] * len(x))

for index, inlet_velocity in enumerate(x):
  y[index] = get_max_displacement(inlet_velocity)

plot(x, y)
