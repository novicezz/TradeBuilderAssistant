0# External imports
import os
import platform
# Local imports
from modules.utils      import check_all, enum_dict, get_name, gen_map
from modules.mechanisms import generate_position
from modules.memory     import MemoryManager

# Constants
ALL_SPECIFIER = "all"

# Constants
COMMANDS = [
    "set [PROPERTY] [VALUE]     - Set chosen property to desired setting",
    "get [PROPERTY]             - Get chosen property value",
    "info [PROPERTY/CMD/NAME]   - Request info about a desired property, command or saved trade setup",
    "map [NAME]                 - Show map of current trade properties along with their status | Defaults to current setup",
    "run [NAME]                 - Run current trade setup and request completion of required fields | Defaults to current setup",
    "clear                      - Clear terminal",
    "access                     - Show all trade setups currently saved into memory and their names,and their respective tickers",
    f"wipe [PROPERTY/{ALL_SPECIFIER.upper()}]        - Wipe desired property and resets it to None | Use {ALL_SPECIFIER.lower()} to reset all properties",
    "save [NAME]                - Save current trade setup to memory under specified name",
    "load [NAME]                - Load desired current trade setup from memory",
    "delete [NAME]              - Remove desired trade setup from memory",
    "import [PATH]              - Import trade setup from storage (TO BE IMPLEMENTED)",
    "export [NAME] [PATH]       - Export trade setup to storage | Specify the moniker 'card' to export all setups in memory (TO BE IMPLEMENTED)",
    "help                       - List information about all available features",
    "exit                       - Exit this application"
]

# Command actions
def print_help(version: str):
    print(f"Welcome to the Trade Builder version - {version} | Please choose from one of these commands:")
    for cmd in COMMANDS:
        print(cmd)

def set_property(data: list, offset: int):
    source, property = enum_dict(data, MemoryManager.get_active(), offset)
    if source == None:
        return property
    if len(data) <= property + 1 or data[property + 1] == '':
        return f"No value specified for property: {data[property]}"
    elif not source[data[property]].set_element(data[property + 1]):
        return f"Invalid value for property: {data[property]}"

    name = get_name(data, offset, property)
    return f"{name} successfully set to {source[data[property]]}"

def get_property(data: list, offset: int):
    source, property = enum_dict(data, MemoryManager.get_active(), offset)
    if source == None:
        return property

    name = get_name(data, offset, property)
    return f"{name} - {source[data[property]]}"

def get_info(data: list, offset: int):
    source, property = enum_dict(data, MemoryManager.get_active(), offset)
    if source != None:
        name = get_name(data, offset, property)
        return f"{name} - {source[data[property]].get_info()}"

    for i in COMMANDS:
        cmpr = i.split(' ', 2)[0]
        if data[offset] == cmpr:
            return i

    saveName = get_name(data, offset, len(data) - 1)
    sets = MemoryManager.show_sets()
    if saveName in sets:
        return f"Trade setup | {saveName} - {MemoryManager.get_set(saveName)['ticker']}/{MemoryManager.get_set(saveName)['direction']}"
    return f"{property}, Command not found: {data[offset]}, Saved setup not found: {saveName}"

def print_map(data: list, offset: str) -> str:
    if len(data) <= offset or data[offset] == "": 
        return f"Map of current trade\n{gen_map(MemoryManager.get_active())}"
    
    saveName = get_name(data, offset, len(data) - 1)
    sets = MemoryManager.show_sets()
    if saveName in sets:
        return f"Map of {saveName}\n{gen_map(MemoryManager.get_set(saveName))}"
    return f"Saved setup not found {saveName}"

def run_trade(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "":
        return generate_position(MemoryManager.get_active())

    saveName = get_name(data, offset, len(data) - 1)
    sets = MemoryManager.show_sets()
    if saveName in sets:
        return generate_position(MemoryManager.get_set(saveName))
    else:
        return f"Saved setup not found {saveName}"

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def list_sessions() -> str:
    out = ""
    count = 1
    sets = MemoryManager.show_sets()
    for i in sets:
        if count == len(sets):
            out += f" └──{i} - {MemoryManager.get_set(i)['ticker']}/{MemoryManager.get_set(i)['direction']}"
        elif count == 1:
            out += f" ┌──{i} - {MemoryManager.get_set(i)['ticker']}/{MemoryManager.get_set(i)['direction']}\n"
        else:
            out += f" ├──{i} - {MemoryManager.get_set(i)['ticker']}/{MemoryManager.get_set(i)['direction']}\n"
        count += 1
    return out

def wipe_properties(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "": 
        return "Operation failed, no property names specified"
    if data[offset] == ALL_SPECIFIER:
        MemoryManager.refresh_set()
        return "Successfully wiped all properties from current trade setup"
    source, property = enum_dict(data, MemoryManager.get_active(), offset)
    if source == None:
        return property

    name = get_name(data, offset, property)
    if source[data[property]].get_element() == None:
        return f"{name} was already set to {source[data[property]]}"

    source[data[property]].reset_element()
    return f"{name} successfully set to {source[data[property]]}"

def save_session(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "": 
        return "Operation failed, no save name specified"

    saveName = get_name(data, offset, len(data) - 1)
    if MemoryManager.save_set(saveName):
        return f"Successfully saved current setup to memory as {saveName}"

    if check_all(input(f"Saved trade setup {saveName} already exists. Would you like to overwrite (Y/N)? ").lower(), ['y', 'yes']):
        MemoryManager.overwrite_set(saveName)
        return f"Successfully overwrote existing trade: {saveName}, and saved the current setup to memory"
    return f"Operation failed, {saveName} already exists"

def load_session(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "":
        return "Operation failed, no save name specified"

    saveName = get_name(data, offset, len(data) - 1)
    if MemoryManager.load_set(saveName):
        return f"Successfully loaded {saveName} from memory"
    else:
        return f"Operation failed, {saveName} does not exist"
    
def delete_session(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "":
        return "Operation failed, no save name specified"

    saveName = get_name(data, offset, len(data) - 1)
    if MemoryManager.remove_set(saveName):
        return f"Successfully deleted {saveName} from memory"
    else:
        return f"Operation failed, {saveName} does not exist"

def pull_file(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "":
        return "Operation failed, path specified"

    savePath = get_name(data, offset, len(data) - 1) + ".sve"
    status = MemoryManager.import_set(savePath)
    if status == True:
        return f"Successfully loaded {savePath} from storage, to memory"
    else:
        return f"Operation failed, could not pull {savePath}: {status}"

def output_file(data: list, offset: int) -> str:
    if len(data) <= offset or data[offset] == "":
        return "Operation failed, no path specified"

    savePath = get_name(data, offset, len(data) - 1) + ".sve"
    status = MemoryManager.export_set(MemoryManager.get_active(), savePath)
    if status == True:
        return f"Successfully exported current save from memory, to {savePath}"
    else:
        return f"Operation failed, could not export save to {savePath}: {status}"