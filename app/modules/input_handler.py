# External imports
import os
import platform

COMMANDS = [
            "set [PROPERTY] - Set chosen property to desired setting",
            "run            - Run current trade and request completion of required fields",
            "clear          - Clear terminal"
            "exit           - Exit this application"
]

PROPERTIES = {
    "direction": None,
    "szone": { "proximal": None, "distal": None },
    "dzone": { "proximal": None, "distal": None },
    "maxrisk": None,
    "atr":  None,
    "accsize": None,
    "entry": None,
    "timeframe": None,
    "trend": { "htf": None, "itf": None, "ltf": None }
}

def print_help(version):
    print(f"Welcome to the Trade Builder version - {version} | Please choose from one of these commands:")
    for i in COMMANDS:
        print(i)

# Functions:
def cycle_input(version):
    data = input(">> ")
    data = data.lower() # Convert user string to lower case

    if data == 'h' or data == 'help':
        print_help(version)
    elif data.split(' ', 1)[0] == 's' or data.split(' ', 1)[0] == 'set':
            if(data.count(' ') == 0):
                print("SET: No property specified")
            else:
                target = data.split(' ')[1]
                if target in PROPERTIES:
                    result = input(f"Enter {target}: ")
                else:
                    print("SET: Invalid property")
    elif data == 'c' or data == 'clear':
            os.system('cls' if platform.system() == 'Windows' else 'clear')
    elif data == 'exit':
        return False
    else: 
        print("Invalid input")

    print(' ')
    return True
