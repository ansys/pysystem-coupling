import threading
from typing import Dict, List, Tuple

from ansys.systemcoupling.core.participant.protocol import ParticipantProtocol
from ansys.systemcoupling.core.session import Session
from ansys.systemcoupling.core.util.logging import LOG


class ParticipantManager:
    def __init__(self, syc_session: Session):
        self.__participants: Dict[str, ParticipantProtocol] = {}
        self.__syc_session: Session | None = syc_session

    def clear(self):
        self.__participants = {}
        self.__syc_session = None

    def add_participant(self, participant_session: ParticipantProtocol) -> None:
        assert participant_session.participant_type == "FLUENT"

        participant_name = (
            f"{participant_session.participant_type}-{len(self.__participants) + 1}"
        )

        setup = self.__syc_session.setup

        setup.activate_hidden.beta_features = True

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
        exe = self.__syc_session._native_api.GetExecutionCommand(
            ParticipantName=participant_name
        )
        host = exe.split("schost=")[1].split(" ")[0]
        port = exe.split("scport=")[1].split(" ")[0]
        return host, int(port)

    def solve(self):
        syc_solve_thread = threading.Thread(target=self.__syc_session.solution.solve)

        connection_threads = [
            threading.Thread(
                target=participant.syc_connect,
                args=(*self._get_host_and_port(name), name),
            )
            for name, participant in self.__participants.items()
        ]

        LOG.info("Starting SyC solve thread...")
        syc_solve_thread.start()
        LOG.info("Waiting for participants to connect.")
        _start_threads(connection_threads)
        _join_threads(connection_threads)
        LOG.info("Participants connected.")
        connection_threads.clear()

        LOG.info("Starting participant solve threads.")
        partsolve_threads = [
            threading.Thread(target=participant.syc_solve)
            for participant in self.__participants.values()
        ]
        _start_threads(partsolve_threads)

        LOG.info("Waiting for all solve threads to join.")
        syc_solve_thread.join()
        LOG.info("SyC solve joined.")
        _join_threads(partsolve_threads)
        LOG.info("All participant solve threads joined.")


def _start_threads(threads: List[threading.Thread]) -> None:
    for thread in threads:
        thread.start()


def _join_threads(threads: List[threading.Thread]) -> None:
    for thread in threads:
        thread.join()
