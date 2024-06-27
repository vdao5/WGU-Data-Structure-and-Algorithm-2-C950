from ..libs.Hash import HashMap, HashSet
from ..libs.dtime import dtime
from ..data.Route import Route, Stop

"""
Solver class - base class for all tsp solvers
    get_addresses_ids(route: Route) -> list[int] - get addresses ids from route's packages ids
    get_distances_map(addresses_ids: list[int]) -> HashMap[int, HashMap[int, float]] - get distances map from addresses ids
        [Changed]: just use the full distances map wgups.distances
    get_stops_dict(route: Route) -> dict[int, Stop] - get list of stops that have packages to be delivered
"""
class Solver:
    def __init__(self):
        from ..WGUPS import WGUPS
        self.wgups = WGUPS.instance()

    def get_addresses_ids(self, route: Route) -> list:
        hs = HashSet()
        hs.insert(route.start_address_id)
        if not route.round_trip and route.end_address_id is not None:
            hs.insert(route.end_address_id)

        for package_id in route.packages_ids:
            hs.insert(self.wgups.packages[package_id].address_id)
        
        addresses_ids = hs.keys()
        return addresses_ids
    
    def get_distances_map(self, addresses_ids: list) -> HashMap:
        return self.wgups.distances

        # distances_map = HashMap(default_value= HashMap(order_by='value', default_value=0.0))

        # for frm in addresses_ids:
        #     for to in addresses_ids:
        #         if frm <= to:
        #             continue
        #         d = self.wgups.distances[frm][to]
        #         distances_map[frm][to] = d
        #         distances_map[to][frm] = d

        # return distances_map
    
    def get_stops_dict(self, route) -> dict:
        sorted = HashMap(default_value=[])
        for id in route.packages_ids:
            package = self.wgups.packages[id]
            sorted[package.address_id].append(id)

        stops_dict = {}
        for address_id, packages_ids in sorted.items():
            stops_dict[address_id] = Stop(route, packages_ids, address_id)

        return stops_dict
    
