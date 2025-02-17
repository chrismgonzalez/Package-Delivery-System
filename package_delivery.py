import csv
from datetime import timedelta

from package import Package
from location import Location
from hash_table import HashTable
from graph import Graph
from delivery_truck import Truck


class PackageDeliveryProgram(object):
    @staticmethod
    # this is the main function that executes the entire program
    # run initializes new hash tables with predetermined size
    # it also parses the csv files and loads their data in to the respective hash and list
    def run():
        graph = Graph()
        locations_hash = HashTable(20)
        packages_hash = HashTable(40)

        # load location data from csv
        # populate hash table and build the graph with the data

        with open('./csv/location-data.csv') as csvfile:
            location_data = csv.reader(csvfile)

            # loop through the location data
            # complexity: O(n)
            for data_row in location_data:
                location = Location(*data_row)

                locations_hash.insert(location.identifier, location)
                locations_hash.insert(location.address, location)

                graph.add_vertex(location)

        all_packages = []
        high_priority = []
        low_priority = []

        # loop through all package data and create some lists: high and low priority, and all packages
        with open('./csv/package_data.csv') as csvfile:
            package_data = csv.reader(csvfile)

            for row_of_data in package_data:
                package = Package(*(row_of_data+[locations_hash.find(row_of_data[1])]))

                # add the package to the all_packages list
                # and add the package to the package hash table with package info and it's identifier
                all_packages.append(package)
                packages_hash.insert(package.identifier, package)

                # divide the packages further based on low vs high priority
                # these operations have a complexity of 0(1)
                if package.high_priority():
                    high_priority.append(package)
                else:
                    low_priority.append(package)

        # loop through the distance-data.csv and find the distance between locations
        # this is the data that is used to build the edges between vertices in the graph
        with open('./csv/distance_data.csv') as csvfile:
            distance_data = csv.reader(csvfile)

            # loop through each item in the csv file
            # complexity: O(n^2)
            for i, row_of_data in enumerate(distance_data):
                for j, data in enumerate(row_of_data):
                    if data != '':

                        # add a weighted edge to the graph, the weighted edge is the distance between
                        # two vertices
                        # complexity: 0(n)
                        graph.add_weighted_edge(locations_hash.find(i),
                                                locations_hash.find(j),
                                                float(data))

        start_time = timedelta(hours=8)
        start_location = locations_hash.find(0)

        # use only two of the three provided trucks, they will make 2 trips
        trucks = [
            Truck(1, start_time, start_location),
            Truck(2, start_time, start_location)
        ]

        # list of times when trucks should wait to leave the station in order to optimize package distribution
        times_to_leave_hub = [
            timedelta(hours=8),
            timedelta(hours=9, minutes=5),
            timedelta(hours=10, minutes=20)
        ]

        # sort high and low priority lists based on their distance from the main hub: O(n*log(n))
        high_priority = sorted(high_priority, key=graph.distance_to_delivery(start_location))
        low_priority = sorted(low_priority, key=graph.distance_to_delivery(start_location))

        count = 0
        truck_index = 0
        i = 0

        # loop until all packages have been delivered. This should be three loops
        while count < len(all_packages):
            truck = trucks[truck_index]

            if i < len(times_to_leave_hub):
                leave_hub_at = times_to_leave_hub[i]
                truck.wait_at_the_hub(leave_hub_at)

            # filter priority lists based on which packages the given truck can deliver: O(n)
            filtered_high = [p for p in high_priority if truck.can_be_delivered(p)]

            # load high priority packages first
            for package in filtered_high:
                # appending a package to the truck list: O(1)
                truck.add_package(package)
                count += 1

                if truck.is_truck_full():
                    break

            # checks if the truck is full, if not, it adds nearby packages ready to deliver
            if truck.is_truck_full() is not True:
                filter_low_priority = [p for p in low_priority if truck.can_be_delivered(p)]
                for package in filter_low_priority:
                    truck.add_package(package)
                    count += 1

                    if truck.is_truck_full():
                        break

            # truck delivers packages using a greedy algorithm
            # that finds the most optimized path through the graph
            # Time complexity: O(n^2*log(n))
            truck.deliver_packages(graph, (len(all_packages) - count) > truck.max)
            i += 1
            truck_index = i % len(trucks)

        def total_distance(truck):
            return truck.total_distance

        return [sum(map(total_distance, trucks)), packages_hash, all_packages]