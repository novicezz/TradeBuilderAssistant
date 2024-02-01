# External imports
from copy   import deepcopy
import json

class ZoneSpec:
    def __init__(self, lowest: float, zoneSet: dict | None):
        self.lowestFract = lowest
        self.zoneSet = zoneSet
        if(zoneSet == None): self.sizes = None
        else: self.sizes = list(zoneSet.keys()).sort()

    def get_activation(self, szSize: float, entry: float) -> float:
        activation = ZoneSpec.calc_activation(entry, szSize, self.lowestFract)
        if(self.sizes == None):
            return activation
        for i in self.sizes:
            if szSize > i:
                return activation
            activation = ZoneSpec.calc_activation(entry, szSize, self.zoneSet[i])
        return activation

    @staticmethod
    def calc_activation(entry: float, szSize: float, fract: float) -> float:
        return entry + szSize / fract

DEFAULT_CONFIG = {
    "LIQUIDITY_FRACTION": 0.50,
    "TARGETS":  { 0.80: 0.80, 1.00: 0.20 },
    "ZONE_SPEC": ZoneSpec(5, { 0.5: 4, 1.0: 3 }),
    "15":   { "ENTRY_BUFFER":  0.02, "SL_BUFFER": 0.02 },
    "hour": { "ENTRY_BUFFER":  0.02, "SL_BUFFER": 0.10 },
    "day":  { "ENTRY_BUFFER":  0.04, "SL_BUFFER": 0.10 }
}

class ConfigHandler:
    currentConfig: dict = deepcopy(DEFAULT_CONFIG)
    @classmethod
    def fetch(cls, path: str) -> bool | str:
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            return False, e
        if(type(data) != dict):
            return False, "Improper configuration formatting"
        return True, cls.loadtocurrent(data)

    @classmethod
    def loadtocurrent(cls, data: dict) -> str:
        dataKeys = list(data.keys())
        configKeys = cls.converttostr(list(cls.currentConfig.keys()))


        changed = ""
        for i in dataKeys:
            if i in configKeys:
                changed += f"{i} was changed\n"
        return changed
                
    @classmethod
    def reset(cls):
        cls.currentConfig = deepcopy(DEFAULT_CONFIG)

    @staticmethod
    def converttostr(data: list) -> list:
        for i in range(0, len(data)):
            data[i] = str(data[i])
        return data