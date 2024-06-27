from sys import float_info
from ..Solver import Solver
from ...data.Route import Route, Stop
from ...libs.Hash import HashMap

"""
Insertion class - insertion lowest cost (heuristic) tsp solver
    initialize(route: Route) - initialize data
    finalize(route: Route) - finalize data
    clear() - clear data

    stops: HashMap[float, Stop] - list of stops in route, key: float is stop's position in route
        stops is sorted by key in ascending order. (auto sorted by HashMap) 
        first stop key is always 0.0, last stop key is greater or equal float_info.max / 2
        insert a stop between two stops: key = prev.key / 2 + next.key / 2
        insert a stop at the end: key = stops.end.key / 2 + float_info.max / 2
    set_start(stops: HashMap) - set start stop
    set_end(stops: HashMap) - set end stop

    solve(route: Route) - can be called from outside
    _solve() - internal solver
        algorithm:
        while not all stops are visited:
            get the next stop to insert
            find the best position to insert the stop
            insert the stop
"""
class Insertion(Solver):
    def __init__(self):
        super().__init__()
    
    def clear(self):
        self.route = None
        self.addresses_ids = None
        self.distances_map = None
        self.stops_dict = None
        self.not_visited = None
        self.stops = None

    def initialize(self, route: Route):
        self.route = route

        self.addresses_ids = self.get_addresses_ids(self.route)
        self.distances_map = self.get_distances_map(self.addresses_ids)
        self.stops_dict = self.get_stops_dict(self.route)
        self.not_visited = sorted(self.stops_dict.values(), key=lambda s: s.latest)

        self.stops = HashMap()
        self.set_start(self.stops)
        self.set_end(self.stops)

    def set_start(self, stops: HashMap):
        if self.route.start_address_id in self.stops_dict:
            idx = self.not_visited.index(self.stops_dict[self.route.start_address_id])
            stops[0.0] = self.not_visited.pop(idx)   
        else:
            stops[0.0] = Stop(self.route, [], self.route.start_address_id)

    def set_end(self, stops: HashMap):
        if self.route.round_trip:
            stops[float_info.max / 2] = Stop(self.route, [], self.route.start_address_id)
            self.can_insert_end = False
        elif self.route.end_address_id is not None:
            if self.route.end_address_id in self.stops_dict:
                idx = self.not_visited.index(self.stops_dict[self.route.end_address_id])
                stops[float_info.max / 2] = self.not_visited.pop(idx)
            else:
                stops[float_info.max / 2] = Stop(self.route, [], self.route.end_address_id)
            self.can_insert_end = False
        else:
            stops[float_info.max / 2] = self.not_visited.pop(0)
            self.can_insert_end = True

    def finalize(self, route: Route):
        route.stops = HashMap()
        for stop in self.stops.values():
            route.stops[len(route.stops)] = stop
        self.clear()

    def solve(self, route: Route):
        self.initialize(route)
        self._solve()
        self.finalize(route)
    
    def _solve(self):
        while len(self.not_visited) > 0:
            insert_stop = self.not_visited.pop(0)
            insert_id = insert_stop.address_id

            node = self.stops.end
            insert_after = node
            min_cost = self.distances_map[node.value.address_id][insert_stop.address_id] if self.can_insert_end else float_info.max
            while node is not None and node.prev is not None:
                next_id = node.value.address_id
                prev_id = node.prev.value.address_id
                old_distance = self.distances_map[prev_id][next_id]
                new_distance = self.distances_map[prev_id][insert_id] + self.distances_map[insert_id][next_id]

                cost = new_distance - old_distance
                if cost < min_cost:
                    min_cost = cost
                    insert_after = node.prev
                node = node.prev

            if insert_after.next is None:
                mid = float_info.max / 2 + self.stops.end.key / 2
            else:
                mid = insert_after.key / 2 + insert_after.next.key / 2
            self.stops[mid] = insert_stop
         