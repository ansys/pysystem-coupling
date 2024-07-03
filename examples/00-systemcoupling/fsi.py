# import required modules
import ansys.mapdl.core as pymapdl
import ansys.fluent.core as pyfluent
import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import examples

import shutil
import gzip

# Connect to mapdl container
print("Connecting to MAPDL")
mapdl = pymapdl.Mapdl()

#================================

# read in the pre-created Fluent case file and launch Fluent

fluent_cas_file = examples.download_file("plate.cas.gz", "pysystem-coupling/oscillating_plate/Fluent")

shutil.copy(fluent_cas_file, "plate.cas.gz")

fluent_cas_file = "plate.cas.gz"

custom_config = {"fluent_image": "ghcr.io/ansys/pyfluent:v24.2.0"}
print("Launching Fluent Container")
fluent = pyfluent.launch_fluent(
    start_transcript=False, container_dict=custom_config
)
fluent.file.read(file_type="case", file_name=fluent_cas_file)

import time
time.sleep(60)

#================================

# launch System Coupling
print("Launching System Coupling Container")
syc = pysyc.launch(version = "latest")

#================================

mapdl.prep7()

# define material properties
mapdl.mp("DENS", 1, 2550) # density
mapdl.mp("ALPX", 1, 1.2e-05) # thermal expansion coefficient
mapdl.mp("EX", 1, 2500000) # Young's modulus
mapdl.mp("NUXY", 1, 0.35) # Poisson's ratio

# set element types to SOLID186
mapdl.et(1, 186)
mapdl.keyopt(1,2,1)

# make geometry
mapdl.block(10.00, 10.06, 0.0, 1.0, 0.0, 0.4)
mapdl.vsweep(1)

# add fixed support at y=0
mapdl.run("NSEL,S,LOC,Y,0")
mapdl.d("all", "all")

# add FSI interface
mapdl.run("NSEL,S,LOC,X,9.99,10.01")
mapdl.run("NSEL,A,LOC,Y,0.99,1.01")
mapdl.run("NSEL,A,LOC,X,10.05,10.07")
mapdl.cm("FSIN_1", "NODE")
mapdl.sf("FSIN_1", "FSIN", 1)

mapdl.allsel()

mapdl.run("/SOLU")

# set analysis type to steady
mapdl.antype(4)

mapdl.nlgeom("ON") # large deformations
mapdl.kbc(1)
mapdl.trnopt("full","","","","","hht")
mapdl.tintp(0.1)
mapdl.autots("off")
mapdl.run("nsub,1,1,1")
mapdl.run("time,10.0")
mapdl.timint("on")

#================================

syc.start_output()

# add participants
fluid_name = syc.setup.add_participant(participant_session = fluent)
solid_name = syc.setup.add_participant(participant_session = mapdl)

syc.setup.coupling_participant[fluid_name].display_name = "Fluid"
syc.setup.coupling_participant[solid_name].display_name = "Solid"

# add a coupling interface
interface_name = syc.setup.add_interface(
  side_one_participant = fluid_name, side_one_regions = ["wall_deforming"],
  side_two_participant = solid_name, side_two_regions = ["FSIN_1"])

# set up 2-way FSI coupling - add force & displacement data transfers
dt_names = syc.setup.add_fsi_data_transfers(interface = interface_name)

# modify force transfer to apply constant initial loading for the first 0.5 [s]
force_transfer = syc.setup.coupling_interface[interface_name].data_transfer["FORC"]
force_transfer.option = "UsingExpression"
force_transfer.value = "vector(5.0 [N], 0.0 [N], 0.0 [N]) if Time < 0.5 [s] else force"

syc.setup.solution_control.time_step_size = 0.1
syc.setup.solution_control.end_time = 3.0 # shorten the run a bit, full run is 10 seconds

syc.setup.output_control.option = "EveryStep"

syc.setup.solution_control.use_ip_address_when_possible = False

# solve the coupled analysis
syc.solution.solve()

mapdl.finish()

# post-process structural results
mapdl.post1()

"""
mapdl.result.animate_nodal_displacement(
    rnum = 0,
    loop=True,
    add_text=False,
    displacement_factor=1.0,
    show_edges=True,
    cpos="xy")
"""

# post-process fluid results
# ...

# exit
syc.exit()
fluent.exit()
mapdl.exit()
