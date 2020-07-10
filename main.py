import os
from datetime import timedelta


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


clear()

# This is the application to fulfill requirements for the C950
# Data Structures and algorithms 2 performance assessment

print("\t*****************************************")
print("\t**** WGUPS Package Delivery Service  ****")
print("\t*****************************************")


# prompt user to select a choice for what they would like to see


while True:
    print()
    command = input("""\
    Menu:
        id - look for a specific package ID
        time - view delivery status of all packages for a specific time
        distance - display total distance for all trucks
        clear - clear the screen
        exit - quit the program
        Please enter a command: """)

    if command == 'id':
        print('not working yet')

    elif command == 'time':
        print('not working yet')

    elif command == 'distance':
        print('not working yet')

    elif command == 'clear':
        clear()

    elif command == 'exit':
        exit()

    else:
        print('Invalid selection. Select a different command')


