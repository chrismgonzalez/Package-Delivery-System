from datetime import timedelta


class Truck(object):
    MAX_PACKAGES = 15
    SPEED_IN_MPH = 18.0
    SECONDS_IN_HOUR = 3600.0

    def __init__(self, identifier, start_time, start_location):
        self.identifier = identifier
        self.current_time = start_time
        self.start_location = start_location
        self.total_distance = 0
        self.max = self.MAX_PACKAGES
        self.packages = []
        self.locations = set()

    # this method adds the package to the package list and the package location the locations set
    # when the package has been loaded on the truck, it's status is changed to when it left the hub
    def add_package(self, package):
        if len(self.packages) < self.max:
            # add package to package list
            self.packages.append(package)
            # add the package to the locations set()
            self.locations.add(package.destination)

            package.on_truck = True
            package.left_hub = self.current_time

    def is_truck_full(self):
        return len(self.packages) == self.max

    def wait_at_the_hub(self, timestamp):
        self.current_time = timestamp

    # this method is a helper method that helps the program determine if the package
    # can be delivered by the truck and if it is ready for delivery
    def can_be_delivered(self, package):
        return not package.on_truck and self.identifier in package.truck_availability and self.current_time >= package.ready_at

    # greedy algorithm for package sorting
    # time complexity: O(n^2 * log(n)) - n is the number of packages
    def deliver_packages(self, city_map, return_to_hub=True):
        present_location = self.start_location
        locations = list(self.locations)

        while self.packages:
            # sort locations
            # using a set optimizes the sort algorithm
            # multiple packages at a location only needs to sort once
            locations = sorted(locations, key=city_map.distance_from_location(present_location))
            closest_location = locations.pop(0)

            distance = city_map.distance_between_vertices(present_location, closest_location)
            time_to_delivery = self.calculate_travel_time(distance)
            delivered_at = self.current_time + timedelta(seconds=time_to_delivery)

            # this part finds all the packages for the present location
            packages_for_location = [p for p in self.packages if
                                     p.destination.identifier == closest_location.identifier]
            for package in packages_for_location:
                package.delivered_at = delivered_at

                # remove the package from the list of all packages
                # time complexity: O(n)
                self.packages.remove(package)

            # update current location, time, and total distance that the truck has traveled
            present_location = closest_location
            self.total_distance += distance
            self.current_time = delivered_at

        # execute this block if the truck needs to return to the hub and retrieve more packages
        if return_to_hub:
            distance = city_map.distance_between_vertices(present_location, self.start_location)
            return_time = self.calculate_travel_time(distance)

            self.current_time = self.current_time + timedelta(seconds=return_time)
            self.total_distance += distance

            # since we are returning to the hub and packages have been delivered
            # reset the set() to be empty for the next load, if needed
            self.locations = set()

    # this method is used by the greedy algorithm as a helper to calculate travel time over a distance
    def calculate_travel_time(self, distance):
        return (distance / self.SPEED_IN_MPH) * self.SECONDS_IN_HOUR
