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

"""Example case for PyAnsys-side integration of participants in a PySystemCoupling case.

This functionality is still under development and should be regarded as being at best Beta.

Once stable, this needs to be moved to the usual examples location and made into a proper
Sphinx gallery example.
"""

import ansys.fluent.core as pyfluent

import ansys.systemcoupling.core as pysyc
from ansys.systemcoupling.core import LOG

LOG.set_level("INFO")
LOG.log_to_stdout()


def _make_fluent_session(filename: str):
    fluent_args = dict(
        precision="double", processor_count=1, mode="solver", product_version="24.1.0"
    )
    session = pyfluent.launch_fluent(**fluent_args)
    session.file.read(file_type="case", file_name=filename)

    return session


syc = pysyc.launch(version="24.1", extra_args=["-l5"])

pipe_fluid_session = _make_fluent_session("pipefluid/pipefluid.cas.h5")
fluid_name = syc.setup.add_participant(participant_session=pipe_fluid_session)

pipe_solid_session = _make_fluent_session("pipesolid/pipesolid.cas.h5")
solid_name = syc.setup.add_participant(participant_session=pipe_solid_session)
interface = syc.setup.add_interface(
    side_one_participant=fluid_name,
    side_one_regions=["wall"],
    side_two_participant=solid_name,
    side_two_regions=["innerwall"],
)

# Comment this to force validation error on solve. (Currently hangs if this happens.)
syc._native_api.AddThermalDataTransfers(Interface=interface)

syc.setup.solution_control.minimum_iterations = 2
syc.setup.solution_control.maximum_iterations = (
    2  # should be 100, but for testing 2 is enough
)

syc.setup.solution_control.available_ports.option = "UserDefined"

syc.setup.print_state()

try:
    syc.solution.solve()
finally:
    pipe_fluid_session.exit()
    pipe_solid_session.exit()
    syc.exit()
