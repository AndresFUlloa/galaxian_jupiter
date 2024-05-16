from enum import Enum


class CPlayState:
    def __init__(self) -> None:
        self.state = PlayState.START
        self.current_time = 0.0
        self.current_lvl = 0

class PlayState(Enum):
    START = 0
    READY = 1
    PLAY = 2
    PAUSE = 3
    GAME_OVER = 4