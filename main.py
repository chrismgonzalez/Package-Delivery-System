import os
from datetime import timedelta

from package_delivery import PackageDeliveryProgram


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


(total_distance, packages_hash, packages) = PackageDeliveryProgram.run()


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
        package_id = input('Enter a package ID to lookup: ')

        # finds the package from the package hashtable.
        # Time complexity: 0(n), where n is the container size
        package = packages_hash.find(int(package_id))

        time_string = input('Please enter a timestamp the following format (HH:MM:SS): ')
        (hour, minute, sec) = time_string.split(":")
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        print(package.report(timestamp))

    elif command == 'time':
        time_string = input('Please enter a timestamp the following format (HH:MM:SS): ')
        (hour, minute, sec) = time_string.split(":")
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        # loop through all packages and display them in a nice format
        for package in packages:
            print(package.line_report(timestamp))

    elif command == 'distance':
        print('Total Distance Traveled: {:.2f} miles'.format(total_distance))

    elif command == 'clear':
        clear()

    elif command == 'exit':
        exit()

    else:
        print('Invalid selection. Select a different command')


