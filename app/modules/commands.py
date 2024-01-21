# External imports
import os
import platform
# Local imports
from modules.utils      import enum_dict, gen_map
from modules.mechanisms import generate_position
from modules.memory     import MemoryManager

# Constants
COMMANDS = [
    "set [PROPERTY] [VALUE] - Set chosen property to desired setting",
    "get [PROPERTY]         - Get chosen property value",
    "info [PROPERTY]        - Request info about a desired property",
    "map                    - Show map of current trade properties along with their status",
    "run                    - Run current trade and request completion of required fields",
    "clear                  - Clear terminal",
    "save                   - Save trade to memory or storage in python format (TO BE IMPLEMENTED)",
    "load                   - Load trade from memory or storage in python format (TO BE IMPLEMENTED)",
    "import [PATH]          - Import trade from storage (TO BE IMPLEMENTED)",
    "export [PATH]          - Export current trade to storage (TO BE IMPLEMENTED)",
    "exit/done              - Exit this application"
]

# Command actions
def print_help(version: str):
    print(f"Welcome to the Trade Builder version - {version} | Please choose from one of these commands:")
    for cmd in COMMANDS:
        print(cmd)

def set_property(data: list, offset: int):
    source, property = enum_dict(data, MemoryManager.get_set(), offset)
    if source == None:
        return property
    if len(data) <= property + 1 or data[property + 1] == '':
        return f"No value specified for property: {data[property]}"
    elif not source[data[property]].set_element(data[property + 1]):
        return f"Invalid value for property: {data[property]}"
    name = ''
    for i in range(offset, property + 1): name += data[i] + ' '
    return f"{name}successfully set to {data[property + 1]}"

def get_property(data: list, offset: int):
    source, property = enum_dict(data, MemoryManager.get_set(), offset)
    if source == None:
        return property
    name = ''
    for i in range(offset, property + 1): name += data[i] + ' '
    return f"{name}- {source[data[property]].get_element()}"

def get_info(data: list, offset: int):
    source, property = enum_dict(data, MemoryManager.get_set(), offset)
    if source == None:
        return property
    name = ''
    for i in range(offset, property + 1): name += data[i] + ' '
    return f"{name}- {source[data[property]].get_info()}"

def print_map() -> str:
    return (f"Map of current trade\n{gen_map(MemoryManager.get_set())}")

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def run_trade():
    generate_position()