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
