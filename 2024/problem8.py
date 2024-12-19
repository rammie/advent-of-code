from collections import defaultdict

antennas = defaultdict(list)
pairs = defaultdict(list)
antinodes = defaultdict(set)

grid_str = open("input8.txt").readlines()
grid = [list(row.strip()) for row in grid_str]

max_x = len(grid[0])
max_y = len(grid)

def get(grid, x, y):
    if x < 0 or x >= max_x or y < 0 or y >= max_y:
        return None
    return grid[y][x]


def set_antinode(node, x, y):
    grid_val = get(grid, x, y)
    # if grid_val is not None and grid_val != node:
    if grid_val is not None:
        antinodes[node].add((x, y))


for x in range(max_x):
    for y in range(max_y):
        node = grid[y][x]
        if node == ".":
            continue

        antennas[node].append((x, y))


for node, coords in antennas.items():
    for c, x1_y1 in enumerate(coords):
        x1, y1 = x1_y1
        for x2, y2 in coords[c:]:
            pairs[node].append((x1, y1, x2, y2))

#Part 1
# for node in pairs:
#     for x1, y1, x2, y2 in pairs[node]:
#         dx = x2 - x1
#         dy = y2 - y1
#         set_antinode(node, x2 + dx, y2 + dy)
#         set_antinode(node, x1 - dx, y1 - dy)


for node in pairs:
    for x1, y1, x2, y2 in pairs[node]:
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            continue

        n = 0
        while get(grid, x2 + n * dx, y2 + n * dy) is not None:
            print(node, x2 + n * dx, y2 + n * dy)
            set_antinode(node, x2 + n * dx, y2 + n * dy)
            n += 1

        n = 0
        while get(grid, x1 - n * dx, y1 - n * dy) is not None:
            print(node, x1 - n * dx, y1 - n * dy)
            set_antinode(node, x1 - n * dx, y1 - n * dy)
            n += 1


all_antinodes = set()

for coords in antinodes.values():
    for x, y in coords:
        all_antinodes.add((x, y))
        grid[y][x] = "#"

print(len(all_antinodes))

for row in grid:
    print("".join(row))
print()

