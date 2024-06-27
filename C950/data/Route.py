from ..libs.dtime import dtime
from ..libs.Hash import HashMap
from ..constants import START_TIME, END_TIME, HUB_ID

"""
Stop class - only used by Route class
    route: Route - route that this stop belongs to
    packages_ids: list[int] - list of package ids
    address_id: int - address id
    owner: HashNode - used by route.stops: HashMap to keep track of the stop's position in the route
        (see Hash.HashMap.insert() and Hash.HashMap.remove())

    earliest: dtime - earliest delivery time
    latest: dtime - latest delivery time
    
    distance: float - distance from beginning of route to this stop
    time: dtime - time when truck arrives at this stop

    __str__() -> str - stop info
"""
class Stop:
    def __init__(self, route, packages_ids, address_id):
        self.route = route
        self.packages_ids = packages_ids
        self.address_id = address_id
        self.owner = None
        
        if len(self.packages_ids) > 0:
            from ..WGUPS import WGUPS
            wgups = WGUPS.instance()
            self.earliest = max([wgups.packages[id].earliest for id in self.packages_ids])
            self.latest = min([wgups.packages[id].latest for id in self.packages_ids])
        else:
            self.earliest = START_TIME
            self.latest = END_TIME

    @property
    def distance(self):
        if self.owner is not None and self.owner.prev is not None:
            from ..WGUPS import WGUPS
            wgups = WGUPS.instance()
            prev = self.owner.prev.value
            distance = prev.distance + wgups.distances[prev.address_id][self.address_id]
            return round(distance, 1)
        else:
            return 0
        
    @property
    def time(self):
        t = self.distance / self.route.truck.speed
        return self.route.start_time + dtime(hours = t)
    
    def __str__(self):
        pkgs = ''
        from ..WGUPS import WGUPS
        wgups = WGUPS.instance()
        t = self.time
        for package_id in self.packages_ids:
            package = wgups.packages[package_id]
            status = 'On Time' if t <= package.latest else 'Late'
            pkgs += f'\r\n\t[{status}] {str(package)}'
        addr = wgups.addresses[self.address_id]
        return f'{str(addr)} - {self.distance}mi - {self.time} {pkgs}'

"""
Route class
    id: int - route id / name
    truck: Truck - truck ref
    packages_ids: list[int] - list of package ids
    late_packages_ids: list[int] - list of late packages ids
    stops: HashMap[int, Stop] - list of stops in route, key: int is stop's position in route
    tsp: TSP - tsp solver, default: Insertion

    start_time: dtime - start time of route
    end_time: dtime - end time of route
    start_address_id: int - start address id
    round_trip: bool - if route is round trip
    end_address_id: int - end address id, if round_trip is True then ignore this
    distance: float - total distance of route
    plot_color: str - plot color for drawing route
        eg: 'r': red, 'g': green, 'b': blue, 'm': magenta ...

    initialize() - set up route
    solve() - use tsp solver to solve route
    finalize() - finalize route after solving

    set_start_time() - set start time of route
        if input start_time is earlier than earliest delivery time of packages then auto adjust start time
    set_packages_ids() - set packages ids of route
"""
class Route:
    def __init__(self, id, truck_id, start_time, packages_ids = [], start_address_id = HUB_ID, round_trip = True, end_address_id = None, plot_color = 'r'):
        self.initialize(id, truck_id, start_time, packages_ids, start_address_id, round_trip, end_address_id, plot_color)
        self.solve()


    def initialize(self, id, truck_id, start_time, packages_ids, start_address_id, round_trip, end_address_id, plot_color):
        from ..TSP.Hueristic.Insertion import Insertion
        from ..WGUPS import WGUPS
        self.wgups = WGUPS.instance()
        self.id = id
        self.tsp = Insertion()
        self.truck = self.wgups.trucks[truck_id]
        self.set_packages_ids(packages_ids)
        self.set_start_time(start_time)
        self.start_address_id = start_address_id
        self.round_trip = round_trip
        self.end_address_id = self.start_address_id if round_trip else end_address_id
        self.plot_color = plot_color

    def finalize(self):
        self.late_packages_ids = []
        for stop in self.stops.values():
            for package_id in stop.packages_ids:
                package = self.wgups.packages[package_id]
                package.departure_time = self.start_time
                package.delivery_time = stop.time
            if stop.latest < stop.time:
                self.late_packages_ids.append(package_id)

    def solve(self):
        self.stops = HashMap()
        self.tsp.solve(self)
        self.finalize()

    def __str__(self):
        s = f'[{self.id}]\r\n'
        s += f'\t{self.truck.id}\r\n'
        s += f'\tStart Time: {self.start_time} - End Time: {self.end_time}\r\n'
        s += f'\tDistance: {self.distance} miles\r\n'
        s += f'\tPackages: {len(self.packages_ids)}\r\n'
        s += f'\tLate Packages: {len(self.late_packages_ids)}\r\n'
        s += f'\tStops: {len(self.stops)}\r\n'
        for stop in self.stops.values():
            s += f'{str(stop)}\r\n'
        return s

    @property
    def distance(self):
        return self.stops.end.value.distance
    
    @property
    def end_time(self):
        return self.stops.end.value.time
    
    def set_start_time(self, start_time):
        earliest_start_time = max([self.wgups.packages[id].earliest for id in self.packages_ids])
        if start_time is None:
            self.start_time = earliest_start_time
        elif start_time < earliest_start_time:
            new_start_time = earliest_start_time + dtime(minutes= 1)
            print(f'[Warning] {self.id} {self.truck.id} Start time cannot be earlier than {earliest_start_time}')
            print(f'\tAuto adjusting start time from {start_time} to {new_start_time}')
            self.start_time = new_start_time
        else:
            self.start_time = start_time

    def set_packages_ids(self, packages_ids):
        self.packages_ids = []
        for package_id in packages_ids:
            package = self.wgups.packages[package_id]
            if package.route is None:
                self.packages_ids.append(package_id)
                package.route = self
            else:
                print(f'[{self.truck.id} Route] Package {package_id} is already on a route')
    