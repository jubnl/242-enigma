import math
import functools
from tabulate import tabulate

# Rotor Order
n_rotors = 5
r_used = 3
rotor_order_possibilities = math.perm(n_rotors, r_used)

# Rotor Settings
positions_per_rotor = 26
ring_setting_possibilities = int(math.pow(positions_per_rotor, r_used))

# Initial Rotor Positions
initial_rotor_positions = int(math.pow(positions_per_rotor, r_used))

# Plugboard Settings
# Calculating the number of ways to choose pairs from 26 letters using 10 cables
a = [math.perm(26 - i * 2, 2) for i in range(10)]
plugboard_possibilities = functools.reduce(lambda x, y: x * y, a) / math.factorial(10)
# Dividing by 10! to account for the order of cables being irrelevant

# Total Possibilities
total_possibilities = rotor_order_possibilities * ring_setting_possibilities * plugboard_possibilities * initial_rotor_positions
table = tabulate([
    ["Rotor Order", rotor_order_possibilities],
    ["Ring Settings", ring_setting_possibilities],
    ["Initial Rotor Positions", initial_rotor_positions],
    ["Plugboard Settings", plugboard_possibilities],
    ["Total Possibilities", total_possibilities]
], tablefmt="rounded_grid")
print(table)
