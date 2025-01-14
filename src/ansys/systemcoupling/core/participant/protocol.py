# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
from typing import List, Protocol


@dataclass
class Variable(Protocol):
    name: str
    display_name: str
    tensor_type: str
    is_extensive: bool
    location: str
    quantity_type: str


@dataclass
class Region(Protocol):
    name: str
    display_name: str
    topology: str
    input_variables: List[str]
    output_variables: List[str]
    region_discretization_type: str = "Mesh Region"


class ParticipantProtocol(Protocol):
    """Protocol class to which PyAnsys sessions that are added to a PySystemCoupling
    session must conform."""

    @property
    def participant_type(self) -> str:
        """Type of participant."""
        ...

    def get_variables(self) -> List[Variable]:
        """List of variables that can be transferred from the participant."""
        ...

    def get_regions(self) -> List[Region]:
        """List of regions on which data transfers can occur."""
        ...

    def get_analysis_type(self) -> str:
        """The type of the analysis - "Steady" or "Transient"."""
        ...

    def connect(self, host: str, port: int, name: str) -> None:
        """Establish connection between the participant solver and System Coupling."""
        ...

    def solve(self) -> None:
        """Run the participant's solve operation."""
        ...
