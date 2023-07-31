import ansys.fluent.core as pyfluent

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import LOG
from ansys.systemcoupling.core.participant.fluent_adaptor import (  # SystemCouplingAdaptor,
    SystemCouplingAdaptor2,
)

# from ansys.systemcoupling.core.participant.manager import ParticipantManager


LOG.set_level("INFO")
LOG.log_to_stdout()

input("any key...")
print("Hello")


def _make_fluent_session(filename: str):
    fluent_args = dict(
        precision="double", processor_count=1, mode="solver", product_version="24.1.0"
    )
    session = pyfluent.launch_fluent(**fluent_args)
    session.file.read(file_type="case", file_name=filename)

    return SystemCouplingAdaptor2(session)


syc = pysyc.launch(use_pyansys_participants=True, version="24.1", extra_args=["-l5"])

pipe_fluid_session = _make_fluent_session("pipefluid/pipefluid.cas.h5")
fluid_name = syc.setup.add_pyansys_participant(participant_session=pipe_fluid_session)

pipe_solid_session = _make_fluent_session("pipesolid/pipesolid.cas.h5")
solid_name = syc.setup.add_pyansys_participant(participant_session=pipe_solid_session)

interface = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["wall"],
    side_two_participant=solid_name,
    side_two_regions=["innerwall"],
)

# syc._native_api.AddThermalDataTransfers(Interface=interface)
# syc._native_api.ActivateHidden.BetaFeatures = True
# syc._native_api.ActivateHidden.AlphaFeatures = True
# syc._native_api.ActivateHidden.LenientValidation = True
syc.setup.solution_control.minimum_iterations = 2
syc.setup.solution_control.maximum_iterations = (
    2  # should be 100, but for testing 2 is enough
)

syc.setup.solution_control.available_ports.option = "UserDefined"
syc.setup.solution_control.available_ports.range = "52000,52001,52002"

syc.setup.print_state()

try:
    syc.solution.solve()
finally:
    pipe_fluid_session.exit()
    pipe_solid_session.exit()
    syc.exit()
