from dataclasses import dataclass
import threading
import time
from typing import List, Tuple

from ansys.systemcoupling.core.participant.manager import ParticipantManager
from ansys.systemcoupling.core.util.logging import LOG


@dataclass
class Variable:
    name: str
    display_name: str
    tensor_type: str
    is_extensive: bool
    location: str
    quantity_type: str


@dataclass
class Region:
    name: str
    display_name: str
    topology: str
    input_variables: List[str]
    output_variables: List[str]


class Participant:
    def __init__(self):
        self.connect_fail_time = None

    @property
    def participant_type(self) -> str:
        """Type of participant."""
        return "FLUENT"

    def get_variables(self) -> List[Variable]:
        """List of variables that can be transferred from the participant."""
        return []

    def get_regions(self) -> List[Region]:
        """List of regions on which data transfers can occur."""
        return []

    def get_analysis_type(self) -> str:
        """The type of the analysis - "Steady" or "Transient"."""
        return "Transient"

    def connect(self, host: str, port: int, name: str) -> None:
        """Establish connection between the participant solver and System Coupling."""
        if self.connect_fail_time is None:
            time.sleep(2)
            return

        time.sleep(self.connect_fail_time)
        raise RuntimeError("Connection failed")

    def solve(self) -> None:
        """Run the participant's solve operation."""
        time.sleep(5)


class NullObject(object):
    def __getattr__(self, name):
        return NullObject()

    def __call__(self, *args, **kwargs):
        return NullObject()

    def __bool__(self):
        return False

    def __iter__(self):
        return NullObject()

    def __next__(self):
        raise StopIteration()

    def __getitem__(self, k):
        return NullObject()

    def __setitem__(self, k, v):
        pass

    def __add__(self, other):
        return NullObject()

    def __radd__(self, other):
        return NullObject()


class MockSycSession:
    class Setup(NullObject):
        pass

    class Solution(NullObject):
        def __init__(self):
            self.was_aborted = False
            self.fail_time = None
            self.__abort_lock = threading.Lock()

        def abort(self, reason_msg: str = ""):
            with self.__abort_lock:
                self.was_aborted = True

        def _solve(self):
            self.was_aborted = False
            t = 0.0
            for i in range(50):
                with self.__abort_lock:
                    if self.was_aborted:
                        self.was_aborted = True
                        return
                time.sleep(0.1)
                t += 0.1
                if self.fail_time and t >= self.fail_time:
                    raise RuntimeError("Solve failed.")
                LOG.info("Solving...")

    class NativeApi:
        def GetServerInfo(self) -> Tuple[str, int]:
            return "bob", 56789

    def __init__(self):
        self.setup = self.Setup()
        self.solution = self.Solution()
        self._native_api = self.NativeApi()


def test_add_participants():
    syc = MockSycSession()
    part1 = Participant()
    part2 = Participant()

    mgr = ParticipantManager(syc)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)


def test_basic_solve():
    syc = MockSycSession()
    part1 = Participant()
    part2 = Participant()

    mgr = ParticipantManager(syc)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)

    mgr.solve()


def test_solve_with_connection_failure():
    LOG.set_level("INFO")

    syc = MockSycSession()
    part1 = Participant()
    part2 = Participant()

    part1.connect_fail_time = 1

    mgr = ParticipantManager(syc)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)

    syc.solution.was_aborted = False
    mgr.solve()

    assert syc.solution.was_aborted


def test_solve_with_solver_failure():
    LOG.set_level("INFO")

    syc = MockSycSession()
    part1 = Participant()
    part2 = Participant()

    mgr = ParticipantManager(syc)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)

    syc.solution.fail_time = 3
    try:
        mgr.solve()
        assert False, "solve should have thrown!"
    except RuntimeError as e:
        assert str(e) == "Solve failed."
