# External imports
from copy                   import deepcopy
# Internal imports
from modules.container  import Container
from modules.attributes     import *

EMPTY_PROPERTIES = {
    "ticker": Container(Ticker, "Ticker symbol\nPossible states: string; will be converted to all caps"),
    "direction": Container(Direction, "Order type\nPossible states: long, short"),
    "szone": {
        "proximal": Container(float, "SZ proximal value\nPossible states: integer; distal value MUST be higher than proximal value"),
        "distal": Container(float, "SZ distal value\nPossible states: integer; distal value MUST be higher than proximal value")
    },
    "dzone": {
        "proximal": Container(float, "DZ proximal value\nPossible states: integer; proximalvalue MUST be higher than proximal value"),
        "distal": Container(float, "DZ distal value\nPossible states: integer; proximal value MUST be higher than distal value")
    },
    "maxrisk": Container(int, "Max position risk\nPossible states: integer"),
    "atr":  Container(float, "Current ATR value\nPossible states: integer; MUST be daily ATR"),
    "accsize": Container(float, "Current account liquidity\nPossible states: integer"),
    "entry": Container(float, "Position entry price\nPossible states: integer"),
    "timeframe": Container(TimeFrame, "Position chart timeframe\nPossible states: 15, hour, day"),
    "trend": {
        "htf": Container(Trend, "Higher time frame trend\nPossible states: up, sideways, down"),
        "itf": Container(Trend, "Intermediate time frame trend\nPossible states: up, sideways, down"),
        "ltf": Container(Trend, "Lower time frame trend\nPossible states: up, sideways, down")
    }
}

class MemoryManager:
    setDict: dict = {}
    activeSet: dict = deepcopy(EMPTY_PROPERTIES)

    @classmethod
    def get_active(cls) -> dict:
        return cls.activeSet
    
    @classmethod
    def get_set(cls, name: str) -> dict:
        if name in cls.setDict:
            return cls.setDict[name]
        return None

    @classmethod
    def refresh_set(cls):
        cls.activeSet = deepcopy(EMPTY_PROPERTIES)

    @classmethod
    def save_set(cls, name: str) -> bool:
        if name in cls.setDict:
            return False
        cls.setDict[name] = deepcopy(cls.activeSet)
        return True
    
    @classmethod
    def overwrite_set(cls, name:str):
        cls.setDict[name] = deepcopy(cls.activeSet)

    @classmethod
    def load_set(cls, name: str) -> bool:
        if name in cls.setDict:
            cls.activeSet = deepcopy(cls.setDict[name])
            return True
        return False

    @classmethod
    def remove_set(cls, name:str) -> bool:
        if name in cls.setDict:
            del cls.setDict[name]
            return True
        return False

    @classmethod
    def show_sets(cls) -> list:
        return list(cls.setDict.keys())

    @classmethod
    def import_set(cls, path: str):
        pass
    
    @classmethod
    def export_set(cls, path: str):
        pass