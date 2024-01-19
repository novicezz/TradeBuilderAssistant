import modules.input_handler as input_handler

LOGIN_MSG = "NOTE: ALL SETUPS ARE PROCESSED AS STOP-LIMIT ENTRIES; LIMIT ENTRIES AND CORRESPONDING TRADE CRITERIA WILL BE ADDED IN FUTURE UPDATE."
USAGE_MSG = "Enter a command (or type 'help' for more information)"
EXIT_MSG = "Thank you for using the Trade Builder"

VERSION = "0.0.1"

def main():
    print(LOGIN_MSG + "\n\n" + USAGE_MSG)

    active = True
    while active:
        active = input_handler.cycle_input(VERSION)
    print('\n' + f"{EXIT_MSG} - {VERSION}")

if __name__ == '__main__':
    main()