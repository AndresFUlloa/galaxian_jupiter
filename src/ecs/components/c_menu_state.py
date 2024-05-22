from enum import Enum


class CMenuState:
    def __init__(self) -> None:
        self.state = MenuState.START


class MenuState(Enum):
    START = 0
    END = 1
