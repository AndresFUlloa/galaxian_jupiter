from enum import Enum


class CPlayState:
    def __init__(self) -> None:
        self.state = PlayState.READY


class PlayState(Enum):
    START = 0
    READY = 1
    PLAY = 2
    PAUSE = 3
    GAME_OVER = 4