# Constants
DIRECTIONS = [
    "long",
    "short"
]

TIME_FRAMES = [
    "15",
    "hour",
    "day"
]

TREND_TYPES = [
    "up",
    "sideways",
    "down"
]

# Parent class
class Attribute:
    def __init__(self, val: str, allowed_set: list):
        if val not in allowed_set:
            raise ValueError(f"Invalid initalization {self.__class__.__name__.lower()}")
        self.val = val

# Subclasses
class Direction(Attribute):
    def __init__(self, dir: str):
        super().__init__(dir, DIRECTIONS)
    
class TimeFrame(Attribute):
    def __init__(self, frame: str):
        super().__init__(frame, TIME_FRAMES)

class Trend(Attribute):
    def __init__(self, trend: str):
        super().__init__(trend, TREND_TYPES)