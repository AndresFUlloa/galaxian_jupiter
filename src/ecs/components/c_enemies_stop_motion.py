
class CEnemiesStopMotion:
    def __init__(self, time_to_stop: float, stopped_time: float, prev_velocity: int):
        self.time_to_stop = time_to_stop
        self.remaining_time_to_stop = time_to_stop
        self.stopped_time = stopped_time
        self.remaining_stopped_time = stopped_time
        self.prev_velocity = prev_velocity
        self.stopped = False
