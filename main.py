# WGUPS
# VD - 011882467
# C950 - Data Structures and Algorithms II - Performance Assessment

from C950.libs.Hash import HashMap
from C950.WGUPS import WGUPS
from C950.libs.dtime import dtime
from C950.constants import START_TIME, END_TIME

"""
program flow:

main_menu
    view_routes
        view_route_detail_menu
    view_packages_status_menu
        view_packages_status_all
        view_packages_status_one
        view_packages_status_truck
        view_packages_status_change_time
    draw_routes
"""
def main():
    main_title()

    global wgups
    wgups = WGUPS()

    main_menu()

def main_title():
    print('-------------------')
    print('WGUPS')
    print('Vu Dao - 011882467')
    print('C950 - Data Structures and Algorithms II - Performance Assessment')
    print('-------------------')

def main_menu():
    enter = -1
    while enter != '0':
        print('-------------------')
        print('Main menu:')
        print('1. View routes')
        print('2. View packages status at a specific time')
        print('9. Draw routes (matplotlib, numpy, networkx required)')
        print('0. Exit')
        enter = input('Enter your choice: ')
        if enter == '1':
            view_routes()
        elif enter == '2':
            view_packages_status_menu()
        elif enter == '9':
            from graph import draw_routes
            draw_routes(wgups.routes.values())

def view_routes():
    print('-------------------')
    print('Routes:')
    routes_map = HashMap()
    total = {'distance': 0, 'packages': 0, 'late': 0}
    for route in wgups.routes.values():
        d = route.distance
        p = len(route.packages_ids)
        l = len(route.late_packages_ids)
        total['distance'] += d
        total['packages'] += p
        total['late'] += l

        print(f'\t{route.id}: {route.truck.id}, {route.start_time} - {route.end_time}, {d} miles, {p} packages ({l} late)')       
        routes_map[str(len(routes_map) + 1)] = route
    print(f'Total: {total["distance"]} miles, {total["packages"]} packages ({total["late"]} late)')
    
    input('Press "Enter" to continue...')
    view_route_detail_menu(routes_map)

def view_route_detail_menu(routes_map):
    enter = -1
    while enter != '0':
        print('-------------------')
        print('View Route Detail Menu:')
        for i, route in routes_map.items():
            print(f'{i}. {route.id}')
        print('0. Back')
        enter = input('Enter your choice: ')
        if enter in routes_map.keys():
            print('-------------------')
            print(routes_map[enter])

            input('Press "Enter" to continue...')

def view_packages_status_menu():
    enter = -1
    while enter != '0':
        print('-------------------')
        print('Packages Status Menu')
        print(f'Time: {wgups.time}')
        print('1. View all packages status')
        print('2. View a specific package status')
        print('3. View packages status loaded onto a truck')
        print('9. Change time')
        print('0. Back')
        enter = input('Enter your choice: ')
        if enter == '1':
            view_packages_status_all()
        elif enter == '2':
            view_packages_status_one()
        elif enter == '3':
            view_packages_status_truck()
        elif enter == '9':
            view_packages_status_change_time()

def view_packages_status_change_time():
    print('-------------------')
    print('Change time')
    try:
        input_time = input(f'Enter 4 digits time HHMM ({int(START_TIME)} - {int(END_TIME)}): ')
        time = dtime(input_time)
        if time < START_TIME or time > END_TIME:
            raise Exception()
        wgups.time = time
    except:
        print('[Warning] Invalid time format')

def view_packages_status_all():
    print('-------------------')
    print('View status of all packages')
    print(f'Time: {wgups.time}')
    for package in wgups.packages.values():
        print(package.info)

    input('Press "Enter" to continue...')

def view_packages_status_one():
    print('-------------------')
    print('View status of a specific package')
    print(f'Time: {wgups.time}')
    try:
        input_id = input('Enter package id: ')
        package = wgups.packages[int(input_id)]
        print(package.info)
    except:
        print('[Warning] Invalid package id')
        
    input('Press "Enter" to continue...')

def view_packages_status_truck():
    print('-------------------')
    print('View status of all packages loaded onto a truck')
    print(f'Time: {wgups.time}')
    enter = -1
    time = wgups.time
    routes_map = HashMap()

    for route in wgups.routes.values():
        if route.start_time <= time and time <= route.end_time:
            routes_map[str(len(routes_map) + 1)] = route

    while enter != '0':
        if len(routes_map) == 0:
            print('No truck is loaded / enrouting at this time')
            input('Press "Enter" to continue...')
            break
        else:
            for i, route in routes_map.items():
                print(f'{i}. {route.truck.id}')
        print('0. Back')
        enter = input('Enter your choice: ')
        if enter in routes_map.keys():
            print('-------------------')
            route = routes_map[enter]
            print(f'{route.truck.id} ({route.id})')
            print(f'Time: {wgups.time}')
            for stop in route.stops.values():
                for package_id in stop.packages_ids:
                    package = wgups.packages[package_id]
                    print(package.info)
            input('Press "Enter" to continue...')

if __name__ == '__main__':
    main()
