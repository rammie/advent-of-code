from itertools import product
import os

initstate = open("day17.input").read().split(os.linesep)

state = {}
state2 = None

min_x = min_y = min_z = 0
max_x = max_y = max_z = 0

for x, row in enumerate(initstate):
    for y, val in enumerate(row):
        state[(x, y, 0)] = val
        max_x = max(x, max_x)
        max_y = max(y, max_y)

def active_neighbors(state, x, y, z):
    coords = product(
        range(x - 1, x + 2),
        range(y - 1, y + 2),
        range(z - 1, z + 2),
    )
    result = sum([
        state.get((nx, ny, nz), ".") == "#"
        for nx, ny, nz in coords
        if (nx, ny, nz) != (x, y, z)
    ])
    return result

for cycle in range(6):
    new_state = {}
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                coords = (x, y, z)
                is_active = state.get(coords, ".") == "#"
                neighbors = active_neighbors(state, *coords)
                if is_active and neighbors in (2, 3):
                    new_state[coords] = "#"
                elif not is_active and neighbors == 3:
                    new_state[coords] = "#"
                else:
                    new_state[coords] = "."

                if new_state[coords] == "#":
                    max_x = max(x, max_x)
                    min_x = min(x, min_x)
                    max_y = max(y, max_y)
                    min_y = min(y, min_y)
                    max_z = max(z, max_z)
                    min_z = min(z, min_z)

    state = new_state 

# Part 1 answer
print(list(state.values()).count("#"))
