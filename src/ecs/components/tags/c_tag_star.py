
class CTagStar:
    def __init__(self, blink_time:float, visible:bool) -> None:
        self.blink_time = blink_time
        self.time_passed = blink_time
        self.visible = visible