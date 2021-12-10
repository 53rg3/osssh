import time


class StopWatch:

    startedAt: float

    def __init__(self) -> None:
        self.startedAt = time.time()

    def getElapsedSeconds(self) -> float:
        return round(time.time() - self.startedAt, 2)
