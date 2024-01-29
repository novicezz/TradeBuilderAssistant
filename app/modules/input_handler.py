# Local imports
from modules.utils      import check_all
import modules.commands as cmd

def cycle_input(version: str):
    data = input(">> ")
    data = data.lower() # Convert user string to lower case
    data = data.split(' ') # Divide string into a list of words

    if check_all(data[0], ['h', 'help']):
        cmd.print_help(version)
    elif check_all(data[0], ['s', 'set']):
        print(f"SET: {cmd.set_property(data, 1)}")
    elif check_all(data[0], ['g', 'get']):
        print(f"GET: {cmd.get_property(data, 1)}")
    elif check_all(data[0], ['i', 'info']):
        print(f"INFO: {cmd.get_info(data, 1)}")
    elif check_all(data[0], ['m', 'map']):
        print(cmd.print_map(data, 1))
    elif check_all(data[0], ['r', 'run']):
        print(f"Your trade report:\n{cmd.run_trade(data, 1)}")
    elif check_all(data[0], ['c', 'clear']):
        cmd.clear_terminal()
    elif check_all(data[0], ['a', 'access']):
        print(f"--- Memory ---\n{cmd.list_sessions()}")
    elif check_all(data[0], ['w', 'wipe']):
        print(f"WIPE: {cmd.wipe_properties(data, 1)}")
    elif check_all(data[0], ['s', 'save']):
        print(f"SAVE: {cmd.save_session(data, 1)}")
    elif check_all(data[0], ['l', 'load']):
        print(f"LOAD: {cmd.load_session(data, 1)}")
    elif check_all(data[0], ['d', 'delete']):
        print(f"DELETE: {cmd.delete_session(data, 1)}")
    elif check_all(data[0], ['p', 'pull']):
        print(f"PULL: {cmd.pull_file(data, 1)}")
    elif check_all(data[0], ['o', 'output']):
        print(f"OUTPUT: {cmd.output_file(data, 1)}")
    elif check_all(data[0], ['e', 'exit']):
        return False
    else: 
        print("Invalid input")

    print('')
    return True