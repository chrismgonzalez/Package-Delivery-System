from datetime import timedelta
import re

class Package(object):
    END_OF_DAY_TIME = timedelta(hours=17)
    PRIORITY_PACKAGES = [13, 15, 19]
    IS_DELIVERED = 'Package was delivered at {}'
    IS_ON_TRUCK = 'Package is on truck - it left the hub at: {}'
    STILL_AT_HUB = 'Package is still at the hub'

    def __init__(self, identifier, street, city, zipcode, deadline, weight_in_kilograms, notes, destination):
        self.identifier = int(identifier)
        self.street = street
        self.city = city
        self.zipcode = zipcode
        self.deadline = self.convert_to_timestamp(deadline)
        self.weight_in_kilos = weight_in_kilograms
        self.notes = notes
        self.destination = destination

        self.delivered_at = None
        self.ready_at = timedelta(hours=8)
        self.left_hub = None
        self.on_truck = False
        self.truck_availability = [1, 2]
        self.notes = notes

        self.modify_package(notes)

    def line_report(self, time):
        report = self.report(time)

        return report[1:].replace('\n', '  ')

    def report(self, time=timedelta(hours=17)):
        return """
    ID: {}
    Address: {} {}, UT
    Zipcode: {}
    Weight: {}
    Delivery Status: {} \
    """.format(
            self.identifier,
            self.street,
            self.city,
            self.zip,
            self.deadline(),
            self.weight_in_kilos,
            self.status(time)
        )

    def has_deadline(self):
        return self.deadline != self.END_OF_DAY_TIME

    def deadline(self):
        if self.deadline == self.END_OF_DAY_TIME:
            return '{} (EOD)'.format(self.deadline)

        return '{}'.format(self.deadline)

    # this method determines if a package is a high priority based on special information such as a deadline
    def high_priority(self):
        return self.has_deadline() or self.notes != "None" or self.identifier in self.PRIORITY_PACKAGES

    # this is a helper method that determines the current delivery status of the package
    # based on the time passed in as an argument
    def status(self, time):
        if time > self.delivered_at:
            return self.IS_DELIVERED.format(self.delivered_at)
        elif time > self.left_hub:
            return self.IS_ON_TRUCK.format(self.left_hub)

    def convert_to_timestamp(self, time_string):
        if time_string == 'EOD':
            return self.END_OF_DAY_TIME

        (hour, minute, sec) = time_string.split(":")
        return timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

    # this method modifies the state of the package based on package restrictions
    def modify_package(self, notes):
        if re.match('Wrong address listed', notes):
            self.ready_at = timedelta(hours=10, minutes=20)
            self.street = '410 S State St'
            self.zip = 84111
        elif re.match('Delayed', notes):
            self.ready_at = timedelta(hours=9, minutes=5)
        elif re.match('Can only be on truck 2', notes):
            self.truck_availability = [2]