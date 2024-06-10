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

from dataclasses import dataclass
import threading
import time
from typing import List, Optional, Tuple

import pytest

from ansys.systemcoupling.core.participant.manager import ParticipantManager
from ansys.systemcoupling.core.syc_version import SYC_VERSION_DOT
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
    region_discretization_type: str


@dataclass
class NoDiscrTypeRegion:
    # no region_discretization_type field
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


class DictWithAttr(dict[str, object]):
    """
    A dictionary that provides attribute access to its data
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        for k, v in list(self.items()):
            if isinstance(v, dict):
                self[k] = DictWithAttr(v)

    def __setitem__(self, name, value):
        if isinstance(value, dict):
            value = DictWithAttr(value)
        return super().__setitem__(name, value)

    def __getattr__(self, name):
        if name not in self:
            self[name] = DictWithAttr()
        return self[name]

    def __setattr__(self, name, value):
        if value not in self.__dict__:
            self[name] = value
        else:
            super().__setattr__(name, value)

    def __call__(self, *args, **kwargs):
        return NullObject()

    def create(self, name: str):
        self[name] = DictWithAttr()
        return self[name]

    def set_state(self, state: dict[str, object]):
        self.update(state)

    def hasattr(self, attr: str) -> bool:
        return attr in self


class NullObject:
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
    class Setup(DictWithAttr):
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

    mgr = ParticipantManager(syc, SYC_VERSION_DOT)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)


@pytest.mark.parametrize(
    "version, region_has_discr_type, expected_discr_type",
    [
        ("24.2", True, "Point Cloud Region"),
        ("24.2", False, "Mesh Region"),
        ("24.1", False, None),
    ],
)
def test_add_participant_regionstate(
    version: str, region_has_discr_type: bool, expected_discr_type: Optional[str]
):

    syc = MockSycSession()
    part = Participant()
    part.get_regions = lambda: [
        (
            Region("region1", "Region1", "Surface", ["a"], ["b"], "Point Cloud Region")
            if region_has_discr_type
            else NoDiscrTypeRegion("region1", "Region1", "Surface", ["a"], ["b"])
        ),
    ]

    mgr = ParticipantManager(syc, version)
    mgr.add_participant(participant_session=part)

    assert (
        syc.setup.coupling_participant["FLUENT-1"].region["region1"].display_name
        == "Region1"
    )

    if expected_discr_type is None:
        assert (
            "region_discretization_type"
            not in syc.setup.coupling_participant["FLUENT-1"].region["region1"]
        )
    else:
        assert (
            syc.setup.coupling_participant["FLUENT-1"]
            .region["region1"]
            .region_discretization_type
            == expected_discr_type
        )


def test_basic_solve():
    syc = MockSycSession()
    part1 = Participant()
    part2 = Participant()

    mgr = ParticipantManager(syc, SYC_VERSION_DOT)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)

    mgr.solve()


def test_solve_with_connection_failure():
    LOG.set_level("INFO")

    syc = MockSycSession()
    part1 = Participant()
    part2 = Participant()

    part1.connect_fail_time = 1

    mgr = ParticipantManager(syc, SYC_VERSION_DOT)
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

    mgr = ParticipantManager(syc, SYC_VERSION_DOT)
    mgr.add_participant(participant_session=part1)
    mgr.add_participant(participant_session=part2)

    syc.solution.fail_time = 3
    try:
        mgr.solve()
        assert False, "solve should have thrown!"
    except RuntimeError as e:
        assert str(e) == "Solve failed."
