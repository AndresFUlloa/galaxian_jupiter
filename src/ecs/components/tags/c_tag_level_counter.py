

class CTagLevelCounter:
    def __init__(self) -> None:
        self.level = 1
        self.delay_to_change = 0.5
        self.level_finished_at = None
