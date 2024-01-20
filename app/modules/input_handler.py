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
    elif check_all(data[0], ['c', 'clear']):
        cmd.clear_terminal()
    elif check_all(data[0], ['e', 'exit', 'd', 'done']):
        return False
    else: 
        print("Invalid input")

    print('')
    return True