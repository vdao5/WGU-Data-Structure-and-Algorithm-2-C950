from C950.libs.Hash import HashMap
from C950.data.Address import Address
from C950.data.Package import Package
from C950.WGUPS import WGUPS
wgups = WGUPS.instance()

"""
NHP3 TASK 2: WGUPS ROUTING PROGRAM IMPLEMENTATION
    Part A: Develop a hash table,
        without using any additional libraries or classes,
        that has an insertion function that takes the package ID as input.
    Part B: Develop a look-up function that takes the package ID as input.
"""
def task_2():
    hash_table = HashMap()
    packages = [
        Package(0, 0, '800', '900', 1, ''),
        Package(1, 1, 'SOD', '1030', 2, ''),
        Package(2, 1, 'SOD', 'EOD', 3, ''),
    ]
    print('-------------------')
    print('TASK 2')
    print('Part A: Inserting packages to hash_table:')
    for package in packages:
        # alt: hash_table[package.id] = package
        hash_table.insert(key = package.id, value = package)

    print('hash_table:')
    for key, package in hash_table.items():
        print(f'\t{key}: {package.info}')
        
    print('Part B: Looking up package id 1 in hash_table:')
    # alt: package_1 = hash_table[1]
    package_1 = hash_table.get_value(1)
    print(f'\t{package_1.info}')

task_2()