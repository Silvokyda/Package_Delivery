# Nnamdi Joshua Madakor, ID: 000214961
from queue import Queue
from datetime import timedelta
from HashMap import HashMap
from time import sleep
from Package import Package
import sys
import datetime

'''
************************************************************************************************
                            Truck Class Pseudocode with BIG-O Analysis
************************************************************************************************
        


        __init__ is used to initialize the class properties
************************************************************************************************       
        __init__
        METHOD COMPLEXITY: O(6) -> O(1)
            INITIALIZE TRUCK SPEED:   O(1)
            INITIALIZE TRUCK ID:      O(1)
            INITIALIZE PACKAGES:      O(1)
            INITIALIZE DEL. NODES:    O(1)
            INITIALIZE TRUCK ROUTE:   O(1)
            INITIALIZE PACKAGE COUNT: O(1)
        

        add_package adds packages to the trucks current load and adds loc. to list
************************************************************************************************* 
        add_package
        METHOD COMPLEXITY: O(3) -> O(1)
            ADD PACKAGES TO HASHMAP:               O(1)
            INCREMENT PACKAGES COUNT BY ONE:       O(1)
            ADD THE PACKAGE ADDRESS TO DEL. NODES: O(1)


        remove_package removes packages from the trucks current load, decrements the package
        count, as well as removes the location from the list
************************************************************************************************* 
        remove_package
        METHOD COMPLEXITY: O(3) -> O(1)
            REMOVE PACKAGE FROM HASHMAP:     O(1)
            DECREMENT PACKAGES COUNT BY ONE: O(1)
            REMOVE THE PACKAGE DEL. NODES:   O(1)


        optimize_delivery_route 
        Algorithm used to optimize a deliver route
        Algorithm type: Nearest Neighbor Algorithm
            Starts from home base and calculates the next delivery based on the distance
            (weight) to the next node.
************************************************************************************************* 
        optimize_delivery_route
        METHOD COMPLEXITY: O(5 + 2N + N^2) -> O(N^2)
            SET THE HOME BASE NODE:                  O(1)
            INITIALIZE THE QUEUE FOR THE ROUTE:      O(1)
            INITIALIZE THE VAR. FOR THE NEXT NODE:   O(1)
            INITIALIZE THE DELIVERY DISTANCE:        O(1)
            COPY THE DELIVERY NODES INTO NEW ARRAY:  O(N)
            FOR EVERY DELIVERY NODE, INSPECT EACH
                EDGE AND CHOSE THE NEAREST ONE:      O(N)
            ADD ONE LAST ROUTE RETURNING TO BASE:    O(N)


        get_packages_currently_being_delivered returns a list of packages that are to be
        delivered next. These packages are ultimately stored in package_status_over_time in
        order view package delivery status and different time periods
************************************************************************************************* 
        get_packages_currently_being_delivered
        METHOD COMPLEXITY: O(N + 1) -> O(N)
            CHECK EACH PACKAGE AND FIND NEXT DELIVERY: O(N)
            ADD PACKAGE TO CURRENT PACKAGES LIST:      O(1)


        deliver_packages loops though the packages currently on the truck and delivers them.
        This method also takes time snapshots of all the package at each delivery point.
        This data is later used to look up delivery status over time.
************************************************************************************************* 
        deliver_packages
        METHOD COMPLEXITY: O(N*N) -> O(N^2)
        WHILE THERE ARE STILL PACKAGES ON BOARD, KEEP DELVIERING: O(N)
        RECORD TIME-BASED SNAPSHOT OF ALL PACKAGES, PER DELIVERY: O(N^2) 

                                                                      

        
'''


class Truck:

    # Time-complexity: O(6) -> O(1)
    # Default constructor
    def __init__(self, id):
        self.SPEED_MPH = 18
        self.id = id
        self.packages = HashMap()
        self.delivery_nodes = set()

        # delivery_route example entry: ['Western Governors University', '10.9']
        self.delivery_route = Queue()
        self.package_count = 0

    # Time-complexity: O(1)
    # This method returns a string with the truck's
    #   ID and remaining package count
    def __str__(self):
        return f"Truck{self.id} has {self.package_count} packages remaining."

    # Time-complexity: O(1)
    # This method returns the truck's packages
    #
    def get_packages(self):
        return self.packages

    # Time-complexity: O(3) -> O(1)
    # This method a a package to the truck,
    #   increments the package_count by 1, and adds
    #   a target delivery node
    def add_package(self, package):
        self.packages.add(package.id, package)
        self.package_count += 1
        self.delivery_nodes.add(package.address_name)

    # Time-complexity: O(3) -> O(1)
    # This method removes a package from the truck,
    #   decrements the package_count by 1, and discards
    #   a target delivery node
    def remove_package(self, package):
        self.packages.remove(package)
        self.package_count -= 1
        self.delivery_nodes.discard(package.address_name)

    # Time-complexity: O(n+n) = O(2n) -> O(n)
    # Algorithm used to optimize a deliver route
    # Algorithm type: Nearest Neighbor Algorithm
    #
    # @param start - starts from the home base, Western Governors University
    # @param nodes_remaining - the delivery locations for the packages on the truck
    #
    # Starts from home base and makes deliveries in order, always going
    #   to the next closest node. Once all the packages have been delviered,
    #   one last trip is made from the last node, back to the origin, this
    #   completing the circuit.
    #
    def optimize_delivery_route(self, node_list):
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

    # Time-complexity: O(n)
    # This function takes in the name of a delivery location and returns
    #   a list of packages that are destined for that location.
    #   This method is used to assist the trucks in their delivery route.
    #
    def get_packages_currently_being_delivered(self, delivery_location_name):
        current_packages = list()
        # 40 total packages to check
        for i in range(1, 41):
            candidate_package = self.packages.get(str(i))
            if candidate_package != None:
                if candidate_package.address_name == delivery_location_name:
                    current_packages.append(candidate_package.id)
        return current_packages

    # Time-complexity: O(n)
    # This method "Delivers" packages
    # 1. The next delivery destination is popped off from the delivery queue
    # 2. Based on the next destination, the packages are selected
    # 3. Drive distance is incremented based off the distance to the next location
    # 4. Drive time is incremented based off the distance and truck speed
    # 5. Current time (as of the deliver) is calculated
    # 6. If it is past 10:20 am, the driver has the option of updating Package #9
    # 7. Historical delivery data is recorded for play-back later.
    # 8. Calculate the time the truck has returned to home base
    # 9. Return the trucks delivery metrics:
    #   [return_time, drive_time_in_hours, drive_distance, package_9_has_been_updated]
    #
    def deliver_packages(self, departure_time, package_handler, package_status_over_time, package_9_has_been_updated):
        return_time = None
        drive_distance = 0
        dont_ask_to_update_9 = False
        # print(f"Departure:    {departure_time}")¥

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

            # Output progress to the user for them a visual
            print(current_time.strftime("%H:%M:%S") + ": Truck" +
                  self.id + " Delivering Package(s) to: '" + next_delivery[0] + "'")
            sleep(0.05)

            # print(current_time)
            # Current time at or later than 10:20 triggers the ability to update Package #9's info
            # self.id == "1" is to only ask this when the first truck runs through the simulation
            if (current_time >= ten_twenty_am and not package_9_has_been_updated and self.id == "1_trip2" and not dont_ask_to_update_9):
                print("")
                print(
                    f"\tDuring delivery, new information has come in about package #9!")
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
                    # Update the HashTable with the new Package information
                    package_handler.packages_hash_table.add("9", Package(
                        "9", "Third District Juvenile Court", "410 S State St", "EOD", "Salt Lake City", "84111", "2", "IN TRANSIT"))
                    print(
                        f"\tPackage #9's address has been updated to: 410 S State St., Salt Lake City, UT 84111!")
                    print("")
                    sleep(1)
                    # The truck that is carrying Package #9 will have it's Map re-balanced/re-optimized
                    package_9_has_been_updated = True
                    # Fix package 9
                elif (answer == "n"):
                    # Keep wrong address (revert if changed from previous run)
                    package_handler.packages_hash_table.add("9", Package(
                        "9", "Council Hall", "300 State St", "EOD", "Salt Lake City", "84103", "2", "Wrong address listed"))
                    dont_ask_to_update_9 = True
                    print("")

            # Record historical data for playbck
            for pack in current_packages:
                temp_package = self.packages.get(pack)
                time_readable = current_time.strftime("%H:%M:%S")
                # print(time_readable)
                temp_package.set_status(f"DELIVERED ({time_readable})")
                self.packages.add(pack, temp_package)
                package_handler.packages_hash_table.add(pack, temp_package)
                package_status_over_time.append([
                    current_time.strftime("%H:%M:%S"), str(package_handler.get_package_by_id(pack))])

                # print(temp_package)

        # Calculate the return time. This will be used to display metrics later
        return_time = departure_time + timedelta(hours=drive_time_in_hours)

        return([return_time, drive_time_in_hours, drive_distance, package_9_has_been_updated])
