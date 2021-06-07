from time import time
from queue import Queue
from datetime import timedelta
from HashMap import HashMap
from Package import Package
import sys
import datetime


class Truck:

    def __init__(self, id):
        self.SPEED_MPH = 18
        self.id = id
        self.packages = HashMap()
        self.delivery_nodes = set()

        # delivery_route (example): ['Western Governors University', '10.9']
        self.delivery_route = Queue()
        self.package_count = 0

    def __str__(self):
        return f"Truck{self.id} has {self.package_count} packages remaining."

    def get_packages(self):
        return self.packages

    def add_package(self, package):
        self.packages.add(package.id, package)
        self.package_count += 1
        self.delivery_nodes.add(package.address_name)

    def remove_package(self, package):
        self.packages.remove(package)
        self.package_count -= 1
        self.delivery_nodes.discard(package.address_name)

    def calculate_best_delivery_route(self, node_list):
        current_node = "Western Governors University"
        self.delivery_route = Queue()
        next_node_for_delivery_route = None
        total_distance = 0
        nodes_remaining = set()
        nodes_remaining = self.delivery_nodes.copy()
        while (len(nodes_remaining) > 0):
            edges = node_list.get(current_node).edges
            shortest_distance = sys.maxsize

            for edge in edges:
                if edge.to_node in nodes_remaining:
                    if float(edge.weight) < shortest_distance:
                        shortest_distance = float(edge.weight)
                        current_node = edge.to_node
                        next_node_for_delivery_route = [
                            edge.to_node, edge.weight]

                        # print(f"New shortest distance: {shortest_distance}")
            nodes_remaining.discard(current_node)
            # print(f"{shortest_distance}")
            total_distance += shortest_distance
            self.delivery_route.put(next_node_for_delivery_route)

        # Must drive back to the hub
        edges = node_list.get(current_node).edges
        for edge in edges:
            if (edge.to_node == "Western Governors University"):
                total_distance += float(edge.weight)
                next_node_for_delivery_route = [edge.to_node, edge.weight]
                break
        self.delivery_route.put(next_node_for_delivery_route)
        return(total_distance)

    def get_packages_currently_being_delivered(self, delivery_location_name):
        current_packages = list()
        # 40 total packages to check
        for i in range(1, 41):
            candidate_package = self.packages.get(str(i))
            if candidate_package != None:
                if candidate_package.address_name == delivery_location_name:
                    current_packages.append(candidate_package.id)
        # for package in self.packages:
        #    if (package.address_name == delivery_location_name):
        #        current_packages.append(package.id)
        # return current_packages
        return current_packages

    def save_historical_package_data(self, package_handler, package_status_over_time, historical_entry):
        current_packges = list()
        for i in range(1, 41):
            current_packges.append(
                str(package_handler.packages_hash_table.get(str(i))))
        package_status_over_time.append([historical_entry[0], current_packges])

    # O(N)
    # Args: Departure Time
    # Returns: [return_time, drive_time, drive_distance]

    def deliver_packages(self, departure_time, package_handler, package_status_over_time, package_9_has_been_updated):
        return_time = None
        drive_distance = 0
        #print(f"Departure:    {departure_time}")

        while (self.delivery_route.qsize() > 0):
            # next_delivery entries contain an array as folows:
            # next_delivery[0] = 'Western Governors University'
            # next_delivery[1] = '10.9'
            next_delivery = self.delivery_route.get()

            # next_delivery entries contain an array as folows:
            # next_delivery[0] = 'Western Governors University'
            # next_delivery[1] = '10.9'
            # get current packages being delivered
            current_packages = self.get_packages_currently_being_delivered(
                next_delivery[0])

            # next_delivery entries contain an array as folows:
            # next_delivery[0] = 'Western Governors University'
            # next_delivery[1] = '10.9'
            # calculate running distnce
            drive_distance += float(next_delivery[1])

            # Calculate drive time
            drive_time_in_hours = drive_distance / self.SPEED_MPH

            # Calculate current time
            current_time = departure_time + \
                timedelta(hours=drive_time_in_hours)

            # Create a time object to see if we are able to update package #9
            ten_twenty_am = datetime.datetime(2021, 7, 1, 10, 20, 0, 0)

            # print(current_time)
            # Current time at or later than 10:20 triggers the ability to update Package #9's info
            # self.id == "1" is to only ask this when the first truck runs through the simulation
            if (current_time >= ten_twenty_am and not package_9_has_been_updated and self.id == "1"):
                print(
                    f"\tDuring the route, new information has come in about package #9!")
                print(
                    f"\tWould you like to correct the address for package #9? Enter 'y' or 'n'")
                answer = input(">")
                # Fix Package #9
                while (answer != "y" and answer != "n"):
                    print(
                        f"\tInvalid Response. During the route, new information has come in about package #9!")
                    print(
                        f"\tWould you like to correct the address for package #9? Enter 'y' or 'n'")
                    answer = input(">")

                if (answer == "y"):
                    package_handler.packages_hash_table.add("9", Package(
                        "9", "Third District Juvenile Court", "410 S State St", "EOD", "Salt Lake City", "84111", "2", "IN TRANSIT"))
                    print(
                        f"\tPackage #9's address has been updated to: 410 S State St., Salt Lake City, UT 84111!")
                    package_9_has_been_updated = True
                    # Fix package 9
                elif (answer == "n"):
                    # Keep wrong address (revert if changed from previous run)
                    package_handler.packages_hash_table.add("9", Package(
                        "9", "Council Hall", "300 State St", "EOD", "Salt Lake City", "84103", "2", "Wrong address listed"))

            for pack in current_packages:
                temp_package = self.packages.get(pack)
                time_readable = current_time.strftime("%H:%M:%S")
                # print(time_readable)
                temp_package.set_status(f"DELIVERED ({time_readable})")
                self.packages.add(pack, temp_package)
                package_handler.packages_hash_table.add(pack, temp_package)
                package_status_over_time.append([
                    current_time.strftime("%H:%M:%S"), str(package_handler.get_package_by_id(pack))])
                #self.save_historical_package_data(package_handler, package_status_over_time, [current_time.strftime("%Y/%m/%d, %H:%M:%S"), package_handler.packages_hash_table])

                # print(temp_package)
            #print(f"Package ({current_packages}) delivered")
            #print(f"Current time: {current_time}")

        #nine_hours_from_now = datetime.now() + timedelta(hours=9)
        return_time = departure_time + timedelta(hours=drive_time_in_hours)
        #print(f"({self.id}) Departure: {departure_time}")
        #print(f"({self.id}) Return:    {return_time}")
        #print(f"({self.id}) Distance:  {round(float(drive_distance),2)} miles")
        #print(f"({self.id}) Time:      {round(float(drive_time_in_hours),2)} hours")
        # print("")
        return([return_time, drive_time_in_hours, drive_distance, package_9_has_been_updated])
