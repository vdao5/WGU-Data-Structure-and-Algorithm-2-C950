import csv
from .libs.dtime import dtime
from .libs.Hash import HashMap
from .data.Address import Address
from .data.Package import Package
from .data.Truck import Truck
from .data.Route import Route
from .constants import START_TIME, HUB_ID, ADDRESSES_FILENAME, DISTANCES_FILENAME, PACKAGES_FILENAME, TRUCKS_FILENAME, ROUTES_FILENAME

"""
WGUPS class - core of the program
    addresses: HashMap[int, Address]
    distances: HashMap[int, HashMap[int, float]] - distances between addresses
        eg: distance from address 1 to address 2: wgups.distances[1][2]
    packages: HashMap[int, Package]
    trucks: HashMap[str, Truck]
    routes: HashMap[str, Route]

    instance() -> WGUPS - singleton pattern
    load() - load data
        load_addresses() - load addresses from csv file
        load_distances() - load distances from csv file
        load_packages() - load packages from csv file
        load_trucks() - load trucks from csv file
        load_routes() - load routes from csv file
"""
class WGUPS:
    _instance = None

    @staticmethod
    def instance():
        if WGUPS._instance is None:
            WGUPS._instance = WGUPS()
        return WGUPS._instance
    
    def __new__(cls):
        if cls._instance is None:
            self = super(WGUPS, cls).__new__(cls)
            cls._instance = self
            
            self.time = START_TIME
            self.load()

        return cls._instance
    
    def load(self):
        self.load_addresses()
        self.load_distances()
        self.load_packages()
        self.load_trucks()
        self.load_routes()

    def load_addresses(self, filename = ADDRESSES_FILENAME):
        data = HashMap()
        with open(filename) as csv_file:
            addresses = csv.DictReader(csv_file, delimiter=',')
            for address in addresses:
                data.insert( 
                    key = int(address['id']), 
                    value = Address(**address)
                )

        self.addresses = data
    
    def load_distances(self, filename = DISTANCES_FILENAME):
        # Addresses must be loaded before distances
        addresses_ids = [id for id in self.addresses.keys()]
        data = HashMap(default_value= HashMap())
        with open(filename) as csv_file:
            distances = csv.reader(csv_file, delimiter=',')
            distances = list(distances)

            for i in range(len(distances)):
                id_i = addresses_ids[i]
                distances[i] = list(map(float, distances[i]))
                for j in range(len(distances[i])):
                    id_j = addresses_ids[j]
                    d = distances[id_i][id_j]
                    data[id_i][id_j] = d
                    data[id_j][id_i] = d
                
        self.distances = data
    
    def load_packages(self, filename = PACKAGES_FILENAME):
        data = HashMap()
        with open(PACKAGES_FILENAME) as csv_file:
            packages = csv.DictReader(csv_file, delimiter=',')
            for package in packages:
                data.insert( 
                    key = int(package['id']), 
                    value = Package(**package)
                )
        
        self.packages = data

    def load_trucks(self, filename = TRUCKS_FILENAME):
        data = HashMap()
        with open(filename) as csv_file:
            trucks = csv.DictReader(csv_file, delimiter=',')
            for truck in trucks:
                data.insert( 
                    key = truck['id'], 
                    value = Truck(**truck)
                )

        self.trucks = data

    def load_routes(self, filename = ROUTES_FILENAME):
        data = HashMap()
        with open(filename) as csv_file:
            routes = csv.DictReader(csv_file, delimiter=',',skipinitialspace=True)
            for route in routes:
                route['start_time'] = data[route['start_after']].end_time + dtime(minutes= 1) if route['start_after'] != '' else dtime(route['start_time'])
                route['packages_ids'] = [] if route['packages_ids'] == '' else [int(id) for id in route['packages_ids'].split(';')]
                route['start_address_id'] = HUB_ID if route['start_address_id'] == '' else int(route['start_address_id'])
                route['end_address_id'] = None if route['end_address_id'] == '' else int(route['end_address_id'])
                route['round_trip'] = False if route['round_trip'] == 'False' else True

                del route['start_after']

                data.insert( 
                    key = route['id'], 
                    value = Route(**route)
                )

        self.routes = data