import threading
from typing import Dict, List, Tuple

from ansys.systemcoupling.core.participant.protocol import ParticipantProtocol
from ansys.systemcoupling.core.util.logging import LOG


class ParticipantManager:
    def __init__(self, syc_session):
        self.__participants: Dict[str, ParticipantProtocol] = {}
        self.__syc_session = syc_session
        self.__n_connected = 0
        self.__solve_exception = None
        self.__connection_lock = threading.Lock()

    def clear(self):
        self.__participants = {}
        self.__syc_session = None

    def add_participant(self, participant_session: ParticipantProtocol) -> str:
        participant_name = (
            f"{participant_session.participant_type}-{len(self.__participants) + 1}"
        )

        setup = self.__syc_session.setup

        part_state = setup.coupling_participant.create(participant_name)
        part_state.participant_type = participant_session.participant_type
        part_state.use_new_apis = True
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
            part_state.region.create(region.name).set_state(
                {
                    "topology": region.topology,
                    "input_variables": region.input_variables,
                    "output_variables": region.output_variables,
                    "display_name": region.display_name,
                }
            )

        self.__participants[participant_name] = participant_session
        return participant_name

    def _get_host_and_port(self, participant_name: str) -> Tuple[str, int]:
        port, host = self.__syc_session._native_api.GetServerInfo()
        return host, port

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

        # Note that we can't currently use `syc_session.solution.solve` here because
        # that has been overridden/hidden by *this* function
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

    def _participant_connect(
        self, name: str, host_port: Tuple[str, int], participant: ParticipantProtocol
    ) -> None:
        try:
            # TODO
            # We expect this to fail quickly if for some reason the connection
            # cannot be established. However, in some situations we see this hang.
            participant.connect(*host_port, name)
            self._increment_n_connected()
        except Exception as e:
            LOG.error(f"Participant {name} failed to connect. Exception: {e}")

    def _syc_solve(self):
        try:
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
