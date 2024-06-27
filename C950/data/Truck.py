"""
Truck class
    id: int - truck id / name
    hub_id: int - hub id
    speed: float - truck speed in mph
    capacity: int - truck capacity
"""
class Truck:
    def __init__(self, id, hub_id, speed, capacity):
        self.id = id
        self.hub_id = int(hub_id)
        self.speed = float(speed)
        self.capacity = int(capacity)
