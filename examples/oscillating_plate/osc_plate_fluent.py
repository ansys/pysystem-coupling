# --------------------------------------------------------------------#
# This script closely follows the System Coupling "Oscillating Plate" #
# tutorial (Fluent version) that uses the native System Coupling      #
# command line interface. Commands, data model assignments, etc.      #
# have been translated to the equivalent facilities exposed by        #
# pySystemCoupling.                                                   #
# --------------------------------------------------------------------#

import ansys.systemcoupling.core as pysystemcoupling

# Launch a remote System Coupling instance and return a "client" object
# that allows us to interact with System Coupling via an API exposed
# into the current Python environment.

syc = pysystemcoupling.launch()

# import time
# time.sleep(15)

# Access 'setup' API
setup = syc.setup

# Create analysis #
# --------------- #

# Load participants
setup.add_participant(input_file="mapdl.scp")
setup.add_participant(input_file="fluent.scp")

# Verify loading of participant
setup.coupling_participant.keys()

## Create interfaces and data transfers by specifying participant regions

# Note: instead of direct datamodel assignment, we could have used
# the command setup.add_interface(...) here, which would have been
# closer to the original tutorial. The approach here provides more
# illustration of datamodel interactions via the API.

interface_name = "interface-1"
interface = setup.coupling_interface.create(interface_name)
interface.side["One"].coupling_participant = "MAPDL-1"
interface.side["One"].region_list = ["FSIN_1"]
interface.side["Two"].coupling_participant = "FLUENT-2"
interface.side["Two"].region_list = ["wall_deforming"]

# Use commands to add data transfers
force_transfer_name = setup.add_data_transfer(
    interface=interface_name,
    target_side="One",
    side_one_variable="FORC",
    side_two_variable="force",
)

disp_transfer_name = setup.add_data_transfer(
    interface=interface_name,
    target_side="Two",
    side_one_variable="INCD",
    side_two_variable="displacement",
)

# Verify creation of interface
setup.coupling_interface.keys()

# Verify interface sides and data transfers
setup.coupling_interface[interface_name].print_state()

# Modify settings #
# --------------- #

# View contents of `solution_control`
setup.solution_control.print_state()

# Change `time_step_size` setting
setup.solution_control.time_step_size = "0.1 [s]"
# Verify setting
# input("press key to continue")
setup.solution_control.time_step_size

# Change `end_time`
setup.solution_control.end_time = "1.0 [s]"

# View `output_control`
setup.output_control.print_state()

# Set `option` in `output_control`
# (First see valid options)
setup.output_control.get_property_options("option")
setup.output_control.option = "StepInterval"

# View `output_control` again
setup.output_control.print_state()

# Change `output_frequency`
setup.output_control.output_frequency = 2

# Review setup #
# ------------ #

# Note that print_setup is not currently exposed in the official
# pysystemcoupling API, but we can access the 'native' API.
native_api = syc.native_api

# Also note that we do not get any output from the remote SyC
# process by default - need to turn output streaming on and off.
syc.start_output()
native_api.PrintSetup()

# Notice that the above command uses the normal SyC naming.
# Similarly, we can access the usual datamodel identifiers
# via the same native_api back door:
native_api.OutputControl.PrintState()

# Run solution #
# ------------ #

# access "solution" API
solution = syc.solution

solution.solve()
# (Note: `solve()` is also currently exposed directly via the
# top-level `syc` object, as are `interrupt` and `abort`. These
# last two are exposed *only* at the top level. This is a work
# in progress - eventually everything will be rationalised to
# the "solution" API.)

# ===================================================================
# ======================= RESTART RUN ===============================
# ===================================================================

# access the "case" API
case = syc.case

# Perform restart run; we will change end time to 1.5 [s]

# Clear and reload
case.clear_state()
case.open()

# Extend analysis #
# --------------- #

# View `solution_control`, change `end-time` and verify setting
setup.solution_control.print_state()
setup.solution_control.end_time = "1.5 [s]"
setup.solution_control.print_state()

# Change additional settings #
# -------------------------- #

# Change `convergence_target` and `ramping_option` of "Force" data transfer
force_transfer = setup.coupling_interface[interface_name].data_transfer[
    force_transfer_name
]
force_transfer.print_state()
force_transfer.convergence_target = 0.001
force_transfer.ramping_option = "Linear"

setup.solution_control.minimum_iterations = 2

# Review setup again (using "native" API) #
# --------------------------------------- #
native_api.PrintSetup()

# Restart solution #
# ---------------- #
solution.solve()

# Stop streaming output from SyC
syc.end_output()

# shutdown this SyC instance
syc.exit()

# (Note that this `syc` object is now "defunct" and any attempt to
# use it to perform any further actions will yield an error. To do
# more in the current Python session, create a new syc instance
# using `syc = pysystemcoupling.launch()` again.)
