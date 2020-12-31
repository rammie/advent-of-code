import os
from functools import reduce
from operator import mul

lines = open("day20.input").read().split(os.linesep)
tiles = {}
tile_no = None
curr_tile = None
for l in lines:
    if l.startswith("Tile"):
        tile_no = l[:-1].split(" ")[1]
        curr_tile = []
        tiles[tile_no] = curr_tile
    elif l.strip():
        curr_tile.append(l)

def rotate(mask):
    rows = len(mask)
    cols = len(mask[0])
    result = [[0] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            result[c][r] = mask[r][c]
    return flip(["".join(row) for row in result])

def flip(mask):
    return ["".join(reversed(r)) for r in mask]

def flipv(mask):
    return list(reversed(mask))

def pimage(img):
    for r in img:
        print(r)
    print("")


class Tile:

    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.update()
        self.edge_dict = {}
        for e in self.edges:
            self.edge_dict[e] = True
            self.edge_dict["".join(reversed(e))] = True

    def update(self):
        n = len(self.data)
        self.image = [row[1:n - 1] for row in self.data[1:n - 1]]
        self.edges = [
            self.data[0],
            "".join([self.data[i][n - 1] for i in range(n)]),
            self.data[n - 1],
            "".join([self.data[i][0] for i in range(n)]),
        ]

    def flip(self):
        self.data = flip(self.data)
        self.update()

    def flipv(self):
        self.data = flipv(self.data)
        self.update()

    def rotate(self):
        self.data = rotate(self.data)
        self.update()

    def shares_edge(self, t):
        for e in t.edges:
            if e in self.edge_dict:
                return True
        return False


class TileGraph:

    tiles = {}

    adj = {}

    degrees = {}

    def __init__(self, tiles):
        self.tiles = {}
        self.adj = {}
        for t in tiles:
            self.add_tile(t)

        self.degrees = {t_id: len(adj_tiles) for t_id, adj_tiles in self.adj.items()}
        self.corners = [t_id for t_id, adj_tiles in self.adj.items() if len(adj_tiles) == 2]

    def add_tile(self, tile):
        self.adj[tile.id] = []
        for t in self.tiles.values():
            if t.shares_edge(tile):
                self.adj[t.id].append(tile)
                self.adj[tile.id].append(t)
        self.tiles[tile.id] = tile

    def assemble(self):
        tile_image = self.assemble_tiles()
        pimage(tile_image)
        for i in range(len(tile_image)):
            for j in range(len(tile_image[0])):
                self.fix_tile(tile_image, i, j)

        image = []
        m = len(tiles[0].image)
        for row in tile_image:
            for sr in range(m):
                image.append("".join([self.tiles[t].image[sr] for t in row]))
        return image

    def fix_tile(self, tile_image, i, j):
        if i == 0 and j == 0:
            t = self.tiles[tile_image[i][j]]
            t.rotate()
            pimage(t.edges)
            return

        if j == 0:
            # align top edge
            match_tile = tile_image[i - 1][j]
            target_tile = self.tiles[match_tile]
            target = target_tile.edges[2]
            target_index = 0
        else:
            # align left edge
            match_tile = tile_image[i][j - 1]
            target_tile = self.tiles[match_tile]
            target = target_tile.edges[1]
            target_index = 3

        tile = self.tiles[tile_image[i][j]]
        if (j == 0):
            pimage(tile.data)

        while tile.edges[target_index] != target:
            tile.flip()
            if tile.edges[target_index] != target:
                tile.rotate()
            if tile.edges[target_index] != target:
                tile.flip()

        if (j == 0):
            pimage(tile.data)

    def assemble_tiles(self):
        n = int(len(self.tiles) ** 0.5)
        image = [[-1] * n for _ in range(n)]
        curr = self.corners[0]
        pi = pj = 0
        seen = set()
        for i in range(n):
            for j in range(n):
                if i == 0 and j == 0:
                    image[0][0] = curr
                    seen.add(curr)
                    continue

                if (i == 0 or i == n - 1) and (j == 0 or j == n - 1):
                    expected_degree = 2
                elif i == 0 or i == n -1 or j == 0 or j == n - 1:
                    expected_degree = 3
                else:
                    expected_degree = 4

                if expected_degree < 4:
                    for t in self.adj[curr]:
                        if t.id not in seen and self.degrees[t.id] == expected_degree:
                            curr = t.id
                            break
                else:
                    n1 = image[i - 1][j]
                    n2 = image[i][j - 1]
                    adj1 = set([t.id for t in self.adj[n1] if t.id not in seen])
                    adj2 = set([t.id for t in self.adj[n2] if t.id not in seen])
                    intersection = set(adj1).intersection(adj2)
                    curr = list(intersection)[0]

                assert curr not in seen
                image[i][j] = curr
                seen.add(curr)

            curr = image[i][0]

        return image


tiles = [Tile(id, data) for id, data in tiles.items()]
tg = TileGraph(tiles)

# Part 1 answer
print(reduce(mul, [int(t_id) for t_id in tg.corners], 1))

image = tg.assemble()

mask = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".split(os.linesep)

mask = mask[1: len(mask) - 1]

def matches(image, mask, i, j):
    rows = len(mask)
    cols = len(mask[0])
    for r in range(rows):
        for c in range(cols):
            if mask[r][c] == "#" and image[i + r][j + c] != "#":
                return False
    return True

def write_mask(image, mask, i, j):
    rows = len(mask)
    cols = len(mask[0])
    for r in range(rows):
        for c in range(cols):
            if mask[r][c] == "#":
                row = image[i + r]
                idx = j + c
                image[i + r] = row[:idx] + "O" + row[idx + 1:]

def count_masks(image, mask):
    n = len(image)
    counts = [[0] * n for _ in range(n)]
    rows = len(mask)
    cols = len(mask[0])
    for i in range(n - rows + 1):
        for j in range(n - cols + 1):
            counts[i][j] = matches(image, mask, i, j)
            if counts[i][j]:
                write_mask(image, mask, i, j)
    return sum([sum(r) for r in counts])


mask = rotate(rotate(flip(mask)))
masked_image = [row for row in image]
count = count_masks(masked_image, mask)

# Part 2 answer
print(sum([row.count("#") for row in masked_image]))
