# Internal imports
from modules.object import Object
from modules.attributes import *

EMPTY_PROPERTIES = {
    "ticker": Object(str, "Ticker symbol\nPossible states: string; will be converted to all caps"),
    "direction": Object(Direction, "Order type\nPossible states: long, short"),
    "szone": {
        "proximal": Object(float, "SZ proximal value\nPossible states: integer; distal value MUST be higher than proximal value"),
        "distal": Object(float, "SZ distal value\nPossible states: integer; distal value MUST be higher than proximal value")
    },
    "dzone": {
        "proximal": Object(float, "DZ proximal value\nPossible states: integer; proximalvalue MUST be higher than proximal value"),
        "distal": Object(float, "DZ distal value\nPossible states: integer; proximal value MUST be higher than distal value")
    },
    "maxrisk": Object(int, "Max position risk\nPossible states: integer"),
    "atr":  Object(float, "Current ATR value\nPossible states: integer; MUST be daily ATR"),
    "accsize": Object(float, "Current account liquidity\nPossible states: integer"),
    "entry": Object(float, "Position entry price\nPossible states: integer"),
    "timeframe": Object(TimeFrame, "Position chart timeframe\nPossible states: 15, hour, day"),
    "trend": {
        "htf": Object(Trend, "Higher time frame trend\nPossible states: up, sideways, down"),
        "itf": Object(Trend, "Intermediate time frame trend\nPossible states: up, sideways, down"),
        "ltf": Object(Trend, "Lower time frame trend\nPossible states: up, sideways, down")
    }
}

class MemoryManager:
    setDict: dict = {}
    activeSet: dict = EMPTY_PROPERTIES.copy()

    @classmethod
    def get_set(cls) -> dict:
        return cls.activeSet

    @classmethod
    def refresh_set(cls):
        cls.activeSet = EMPTY_PROPERTIES.copy()

    @classmethod
    def save_set(cls, name: str) -> bool:
        if name in cls.setDict:
            return False
        cls.setDict[name] = cls.activeSet.copy()
        return True

    @classmethod
    def load_set(cls, name: str) -> bool:
        if name in cls.setDict:
            cls.activeSet = cls.setDict[name].copy()
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