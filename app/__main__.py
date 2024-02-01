# Local imports
import modules.input_handler as handler

# Constants
VERSION = "0.9.1"

LOGIN_MSG = "NOTE: ALL SETUPS ARE PROCESSED AS STOP-LIMIT ENTRIES; LIMIT ENTRIES AND CORRESPONDING TRADE CRITERIA WILL BE ADDED IN FUTURE UPDATE."
USAGE_MSG = "Enter a command (or type 'help' for more information)"
EXIT_MSG = "Thank you for using the Trade Builder"

# Main func
def main():
    print(LOGIN_MSG + "\n\n" + USAGE_MSG)

    active = True
    while active:
        active = handler.cycle_input(VERSION)
    print(f"\n{EXIT_MSG} - {VERSION}")

# Init idiom
if __name__ == '__main__':
    main()