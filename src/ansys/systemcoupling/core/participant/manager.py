# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

import threading
from typing import Dict, List, Tuple

from ansys.systemcoupling.core.participant.protocol import ParticipantProtocol
from ansys.systemcoupling.core.syc_version import compare_versions
from ansys.systemcoupling.core.util.logging import LOG


class ParticipantManager:
    """Manages a System Coupling solution in which the participant solvers are
    provided as "session" objects from other PyAnsys APIs.

    These objects must conform (in a Python "duck typing" sense) to the
    ``ParticipantProtocol`` protocol.

    The ParticipantManager will play a role whenever participants are added to the
    analysis using the ``add_participant`` command with ``participant_session`` being the one
    and only argument.

    In this case, the manager creates ``coupling_participant`` data model objects
    based on queries to the session object. It will also store the session object
    for later use if a solve is initiated.

    If ``solve`` is called on the manager, it will coordinate both the connection of the
    participants to System Coupling and, subsequently, the invocation of their solve
    operations. In standard System Coupling terms, the solves that are initiated from
    the "PyAnsys" environment will be regarded by the System Coupling solver as
    "externally managed".

    .. warning:
        This facility should be regarded as sub-Beta level.
        It is likely to be subject to further development, and has fairly limited utility
        until more participant types support the protocol.
    """

    def __init__(self, syc_session, server_version: str):
        self.__participants: Dict[str, ParticipantProtocol] = {}
        self.__syc_session = syc_session
        self.__connection_lock = threading.Lock()
        self.__server_version = server_version
        self.clear()

    def clear(self):
        self.__participants: Dict[str, ParticipantProtocol] = {}
        self.__n_connected = 0
        self.__solve_exception = None

    def add_participant(self, participant_session: ParticipantProtocol) -> str:
        if compare_versions(self.__server_version, "24.1") < 0:
            raise RuntimeError(
                f"System Coupling server version '{self.__server_version}' is too low to"
                "support this form of 'add_participant'. Minimum version is '24.1'."
            )
        participant_name = (
            f"{participant_session.participant_type}-{len(self.__participants) + 1}"
        )

        setup = self.__syc_session.setup

        part_state = setup.coupling_participant.create(participant_name)
        part_state.participant_type = participant_session.participant_type
        part_state.participant_analysis_type = participant_session.get_analysis_type()
        part_state.execution_control.option = "ExternallyManaged"

        setup.analysis_control.analysis_type = (
            participant_session.get_analysis_type()
        )  # TODO: this logic isn't quite right, maybe delegate to controller

        for variable in participant_session.get_variables():
            part_state.variable.create(variable.name).set_state(
                {
                    "tensor_type": variable.tensor_type,
                    "is_extensive": variable.is_extensive,
                    "location": variable.location,
                    "quantity_type": variable.quantity_type,
                    "participant_display_name": variable.display_name,
                    "display_name": variable.display_name.replace(
                        " ", "_"
                    ),  # TODO: delegate this to controller
                }
            )

        for region in participant_session.get_regions():
            region_state = {
                "topology": region.topology,
                "input_variables": region.input_variables,
                "output_variables": region.output_variables,
                "display_name": region.display_name,
            }
            if compare_versions(self.__server_version, "24.2") >= 0:
                region_state.update(
                    {
                        "region_discretization_type": (
                            region.region_discretization_type
                            if hasattr(region, "region_discretization_type")
                            else "Mesh Region"
                        )
                    }
                )
            part_state.region.create(region.name).set_state(region_state)

        self.__participants[participant_name] = participant_session
        return participant_name

    def solve(self):
        self.__solve_exception = None
        self._clear_n_connected()

        if len(self.__participants) == 0:
            # Fall back to normal solve
            self.__syc_session.solution._solve()
            return

        # TODO : if we *don't* check for validation error before solve, and
        # leave it for the SyC Solve() to find them, we see participants hang
        # during connection. (This is independent of PySyC.)

        if any(
            msg
            for msg in self.__syc_session.setup.get_status_messages()
            if msg["level"] == "Error"
        ):
            raise RuntimeError(
                "The setup data contains errors. solve() cannot proceed until these are fixed."
            )

        syc_solve_thread = threading.Thread(target=self._syc_solve)
        try:
            self._do_solve(syc_solve_thread)
        finally:
            syc_solve_thread.join()
            LOG.info("SyC solve joined.")

        if self.__solve_exception:
            raise self.__solve_exception

    def _do_solve(self, syc_solve_thread):
        connection_threads = [
            threading.Thread(
                target=lambda host_port, name=name, part=participant: self._participant_connect(
                    name, host_port, part
                ),
                args=(self._get_host_and_port(name), name, participant),
            )
            for name, participant in self.__participants.items()
        ]

        LOG.info("Starting SyC solve thread...")
        syc_solve_thread.start()
        LOG.info("Waiting for participants to connect.")
        _start_threads(connection_threads)
        _join_threads(connection_threads)
        connection_threads.clear()
        if self._get_n_connected() < len(self.__participants):
            LOG.error("Some participants were unable to connect to System Coupling.")
            self.__syc_session.solution.abort()
        else:
            LOG.info("Participants connected.")

            LOG.info("Starting participant solve threads.")
            partsolve_threads = [
                threading.Thread(target=participant.solve)
                for participant in self.__participants.values()
            ]
            _start_threads(partsolve_threads)

            LOG.info("Waiting for all solve threads to join.")
            _join_threads(partsolve_threads)
            LOG.info("All participant solve threads joined.")

    def _clear_n_connected(self) -> None:
        with self.__connection_lock:
            self.__n_connected = 0

    def _get_n_connected(self) -> int:
        with self.__connection_lock:
            return self.__n_connected

    def _increment_n_connected(self) -> None:
        with self.__connection_lock:
            self.__n_connected += 1

    def _get_host_and_port(self, participant_name: str) -> Tuple[str, int]:
        port, host = self.__syc_session._native_api.GetServerInfo()
        return host, port

    def _participant_connect(
        self, name: str, host_port: Tuple[str, int], participant: ParticipantProtocol
    ) -> None:
        try:
            participant.connect(*host_port, name)
            self._increment_n_connected()
        except Exception as e:
            LOG.error(f"Participant {name} failed to connect. Exception: {e}")

    def _syc_solve(self):
        try:
            # We use `syc_session.solution._solve` here as it is
            # the lower level solve command. `sys_session.solution.solve`
            # would bring us recursively back into *this* function
            self.__syc_session.solution._solve()
        except Exception as e:
            self.__solve_exception = e
            LOG.error(f"Solve terminated with exception: {e}.")


def _start_threads(threads: List[threading.Thread]) -> None:
    for thread in threads:
        thread.start()


def _join_threads(threads: List[threading.Thread]) -> None:
    for thread in threads:
        thread.join()
