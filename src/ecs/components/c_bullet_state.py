from enum import Enum


class CBulletState:
    def __init__(self) -> None:
        self.state = BulletState.IDLE


class BulletState(Enum):
    IDLE = 0
    SHOT = 1
