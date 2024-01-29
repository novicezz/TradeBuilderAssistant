DEFAULT_CONFIG = {
    "LIQUIDITYFRACTION": 0.50,
    "15":   { "ENTRYBUFFER":  0.02, "SLBUFFER": 0.02 },
    "HOUR": { "ENTRYBUFFER":  0.02, "SLBUFFER": 0.10 },
    "DAT":  { "ENTRYBUFFER":  0.04, "SLBUFFER": 0.10 }
}


class ConfigHandler:

    @classmethod
    def fetch(cls, path: str) -> str:
        return ""