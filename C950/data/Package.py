from enum import Enum
from ..libs.dtime import dtime
from ..constants import START_TIME, END_TIME

"""
Package class
    id: int - package id
    address_id: int - address id
    earliest: dtime - earliest delivery time (when package arrives at hub)
    latest: dtime - latest delivery time (delivery deadline)
    weight: int - package weight in kgs
    notes: str - package notes
    status: Status - package status

    route: Route - route that this package is assigned to
    departure_time: dtime - departure time from hub
    delivery_time: dtime - delivery time

    info: str - package info
    str() -> str - alt package info representation
"""
class Package:
    class Status(Enum):
        IN_TRANSIT = 0
        AT_HUB = 1
        EN_ROUTED = 2
        DELIVERED = 3

        def __str__(self):
            return self.name

    def __init__(self, id, address_id, earliest, latest, weight, notes):
        self.id = int(id)
        self.address_id = int(address_id)
        self.weight = int(weight)
        self.notes = notes

        self.earliest = START_TIME if earliest == 'SOD' else dtime(earliest)
        self.latest = END_TIME if latest == 'EOD' else dtime(latest)
        
        self.departure_time = None
        self.delivery_time = None
        self.route = None

    @property
    def info(self):
        from ..WGUPS import WGUPS
        wgups = WGUPS.instance()
        address = wgups.addresses[self.address_id]

        info = f'Package {self.id}: [{str(self.status)}] - {address.full_addr} - {self.weight} kgs - deadline: {self.latest}'
        if self.route is not None:
            info += f'\r\n\t{self.route.id}: {self.route.truck.id} - Departure Time: {self.departure_time} - Delivery Time: {self.delivery_time}'
            if self.delivery_time > self.latest:
                info += '\r\n\t[Warning] Late delivery'
        else:
            info += '\r\n\t[Warning] Not assigned to any route'

        if self.notes != '':
            info += f'\r\n\tNotes: {self.notes}'
        
        return info

    def __str__(self):
        return f'P[{self.id}]: A[{self.address_id}] - {self.earliest} to {self.latest} - {self.weight} kgs - {self.notes}'

    @property
    def status(self):
        from ..WGUPS import WGUPS
        wgups = WGUPS.instance()
        time = wgups.time

        if self.delivery_time is not None and self.delivery_time <= time:
            return Package.Status.DELIVERED
        elif self.departure_time is not None and self.departure_time <= time:
            return Package.Status.EN_ROUTED
        elif self.earliest <= time:
            return Package.Status.AT_HUB
        else:
            return Package.Status.IN_TRANSIT