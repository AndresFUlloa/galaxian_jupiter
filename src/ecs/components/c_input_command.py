from enum import Enum
from typing import List


class CInputCommand:
    def __init__(self, name: str, keys: List[int]) -> None:
        self.name = name
        self.keys = keys
        self.phase = CommandPhase.NA


class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
