# External imports
import os
import platform
# Local imports
from modules.object     import Object
from modules.attributes import *
from modules.utils      import enum_dict

# Constants
COMMANDS = [
    "set [PROPERTY] [VALUE] - Set chosen property to desired setting",
    "get [PROPERTY]         - Get chosen property value",
    "info [PROPERTY]        - Request info about a desired property",
    "map                    - Show map of properties along with their status (TO BE IMPLEMENTED)",
    "run                    - Run current trade and request completion of required fields (TO BE IMPLEMENTED)",
    "clear                  - Clear terminal",
    "import [PATH]          - Import trade from storage (TO BE IMPLEMENTED)",
    "export [PATH]          - Export current trade to storage (TO BE IMPLEMENTED)",
    "exit/done              - Exit this application"
]

PROPERTIES = {
    "direction": Object(Direction, "Order type\nPossible states: long, short"),
    "szone": { "proximal": Object(float, "SZ proximal value\nPossible states: integer; distal value MUST be higher than proximal value"), "distal": Object(float, "SZ distal value\nPossible states: integer; distal value MUST be higher than proximal value") },
    "dzone": { "proximal": Object(float, "DZ proximal value\nPossible states: integer; proximalvalue MUST be higher than proximal value"), "distal": Object(float, "DZ distal value\nPossible states: integer; proximal value MUST be higher than distal value") },
    "maxrisk": Object(int, "Max position risk\nPossible states: integer"),
    "atr":  Object(float, "Current ATR value\nPossible states: integer; MUST be daily ATR"),
    "accsize": Object(int, "Current account liquidity\nPossible states: integer"),
    "entry": Object(float, "Position entry price\nPossible states: integer"),
    "timeframe": Object(TimeFrame, "Position chart timeframe\nPossible states: 15, hour, day"),
    "trend": { "htf": Object(Trend, "Higher time frame trend\nPossible states: up, sideways, down"), "itf": Object(Trend, "Intermediate time frame trend\nPossible states: up, sideways, down"), "ltf": Object(Trend, "Lower time frame trend\nPossible states: up, sideways, down") }
}

# Command actions
def print_help(version: str):
    print(f"Welcome to the Trade Builder version - {version} | Please choose from one of these commands:")
    for cmd in COMMANDS:
        print(cmd)

def set_property(data: list, offset: int):
    source, property = enum_dict(data, PROPERTIES, offset)
    if source == None:
        return property
    if len(data) <= property + 1 or data[property + 1] == '':
        return f"No value specified for property: {data[property]}"
    elif source[data[property]].set_element(data[property + 1]):
        name = ''
        for i in range(offset, property + 1): name += data[i] + ' '
        return f"{name}successfuly set to {data[property + 1]}"
    else:
        return f"Invalid value for property: {data[property]}"

def get_property(data: list, offset: int):
    source, property = enum_dict(data, PROPERTIES, offset)
    if source == None:
        return property
    else:
        name = ''
        for i in range(offset, property + 1): name += data[i] + ' '
        return f"{name}- {source[data[property]].get_element()}"

def get_info(data: list, offset: int):
    source, property = enum_dict(data, PROPERTIES, offset)
    if source == None:
        return property
    else:
        name = ''
        for i in range(offset, property + 1): name += data[i] + ' '
        return f"{name}- {source[data[property]].get_info()}"
    
def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')