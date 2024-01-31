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

    @classmethod
    def fetch(cls, path: str) -> str:
        return ""