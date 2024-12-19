import os

data = open("day24.input").read().split(os.linesep)

def parse_flips(row):
    buffer = []
    while row:
        if row[0] in ("e", "w"):
            buffer.append(row[0])
            row = row[1:]
        else:
            buffer.append(row[:2])
            row = row[2:]
    return buffer


flips = [parse_flips(row) for row in data]


tiles = {}


def find_tile(path):
    x, y = 0, 0
    while path:
        move = path.pop(0)
        if move == "e":
            x += 2
        if move == "w":
            x -= 2
        if move == "ne":
            y -= 2
            x += 1
        if move == "nw":
            y -= 2
            x -= 1
        if move == "se":
            y += 2
            x += 1
        if move == "sw":
            y += 2
            x -= 1
    return x, y

for path in flips:
    x, y = find_tile(path)
    tiles.setdefault((x, y), False)
    tiles[(x, y)] = not tiles[(x, y)]

# Part 1 answer
print (sum([1 for v in tiles.values() if v]))

def neighbors(x, y):
    return [
        (x + 2, y),
        (x - 2, y),
        (x + 1, y - 2),
        (x - 1, y - 2),
        (x + 1, y + 2),
        (x - 1, y + 2),
    ]


def get_local(tiles, x, y):
    return [tiles.get((nx, ny), False) for nx, ny in neighbors(x, y)]


def flip_tiles(tiles):
    new_tiles = {}
    coords = set()
    for x, y in tiles:
        coords.add((x, y))
        for nx, ny in neighbors(x, y):
            coords.add((nx, ny))

    for x, y in list(coords):
        val = tiles.get((x, y), False)
        local = get_local(tiles, x, y)
        n_black = sum(local)
        assert 0 <= n_black <= 6
        new_tiles[(x, y)] = val

        if val and (n_black == 0 or n_black > 2):
            new_tiles[(x, y)] = False
        elif not val and n_black == 2:
            new_tiles[(x, y)] = True

    return new_tiles

for i in range(100):
    tiles = flip_tiles(tiles)

# Part 2 answer
print (sum([1 for v in tiles.values() if v]))