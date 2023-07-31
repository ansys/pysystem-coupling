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
    @property
    def participant_type(self) -> str:
        ...

    def get_variables(self) -> List[Variable]:
        ...

    def get_regions(self) -> List[Region]:
        ...

    def get_analysis_type(self) -> str:
        ...

    def connect(self, host: str, port: int, name: str) -> None:
        ...

    def solve(self) -> None:
        ...
