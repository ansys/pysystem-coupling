import ansys.fluent.core as pyfluent

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core.participant.fluent_adaptor import SystemCouplingAdaptor
from ansys.systemcoupling.core.participant.manager import ParticipantManager

input("any key...")


def _make_fluent_session(filename: str):
    fluent_args = dict(precision="double", processor_count=2, mode="solver")
    session = pyfluent.launch_fluent(**fluent_args)
    session.file.read(file_type="case", file_name=filename)

    return SystemCouplingAdaptor(session)


syc = pysyc.launch()

mgr = ParticipantManager(syc)

fluid_name = mgr.add_participant(
    pipe_fluid_session := _make_fluent_session("pipefluid/pipefluid.cas.h5")
)
solid_name = mgr.add_participant(
    pipe_solid_session := _make_fluent_session("pipesolid/pipesolid.cas.h5")
)

interface = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["wall"],
    side_two_participant=solid_name,
    side_two_regions=["innerwall"],
)

syc._native_api.AddThermalDataTransfers(Interface=interface)

syc.setup.solution_control.minimum_iterations = 2
syc.setup.solution_control.maximum_iterations = (
    2  # should be 100, but for testing 2 is enough
)

syc.setup.solution_control.available_ports.option = "UserDefined"
syc.setup.solution_control.available_ports.range = "52000,52001,52002"

syc.setup.print_state()

mgr.solve()

pipe_fluid_session.exit()
pipe_solid_session.exit()
syc.exit()
