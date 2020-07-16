# Chris Gonzalez (ID: 001104301)
# This is the application to fulfill requirements for the C950
# Data Structures and algorithms 2 performance assessment
import os
from datetime import timedelta

from package_delivery import PackageDeliveryProgram


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


(total_distance, packages_hash, packages) = PackageDeliveryProgram.run()


clear()

print("\t*****************************************")
print("\t**** WGUPS Package Delivery Service  ****")
print("\t*****************************************")


# prompt user to select a choice for what they would like to see

while True:
    print("Please use number keys to select an option:")
    print("[1] Lookup package by ID and timestamp")
    print("[2] View all packages at a certain time")
    print("[3] See total distance traveled")
    print("[4] Clear console")
    print("[5] Exit program")
    user_response = input("> ")

    if user_response == str(1):
        package_id = input('Enter a package ID to lookup: ')

        # finds the package from the package hashtable.
        # Time complexity: 0(n), where n is the container size
        package = packages_hash.find(int(package_id))

        time_string = input('Please enter a timestamp the following format (HH:MM:SS, 1P.M. is 13:00:00): ')
        (hour, minute, sec) = time_string.split(":")
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        print(package.report(timestamp))

    elif user_response == str(2):
        time_string = input('Please enter a timestamp the following format (HH:MM:SS): ')
        (hour, minute, sec) = time_string.split(":")
        timestamp = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

        # loop through all packages and display them in a nice format
        for package in packages:
            print(package.line_report(timestamp))

    elif user_response == str(3):
        print('Total Distance Traveled: {:.2f} miles'.format(total_distance))

    elif user_response == str(4):
        clear()

    elif user_response == str(5):
        exit()

    else:
        print('Invalid selection. Select a different command')


