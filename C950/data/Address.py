import csv
from ..libs.Hash import HashMap
from ..constants import ADDRESSES_FILENAME
"""
Address class
    id: int - address id
    name: str - alt name
    addr: str - address
    city: str - city
    state_code: str - state code
    zip_code: str - zip code

    full_addr: str - full address
        eg: 195 W Oakland Ave, Salt Lake City, UT 84115
    
    __str__() -> str - alt representation of address
"""
class Address:
    def __init__(self, id, name, addr, city, state_code, zip_code):
        self.id = int(id)
        self.name = name
        self.addr = addr
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
    
    @property
    def full_addr(self):
        return f'{self.addr}, {self.city}, {self.state_code} {self.zip_code}'

    def __str__(self):
        return f'A[{self.id}]: {self.addr}, {self.city}, {self.state_code} {self.zip_code} - {self.name}'