grid_str = open("input10.txt").readlines()
grid = [list(row.strip()) for row in grid_str]

max_x = len(grid[0])
max_y = len(grid)


heads = []
ends = []


for y in range(max_y):
    for x in range(max_x):
        node = grid[y][x]
        if node == "0":
            heads.append((x, y))
        if node == "9":
            ends.append((x, y))


def copy_grid(grid):
    return [row.copy() for row in grid]


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def get(grid, x, y):
    if x < 0 or x >= max_x or y < 0 or y >= max_y:
        return None
    return grid[y][x]


def get_neighbors(grid, x, y, node):
    if get(grid, x + 1, y) == node:
        yield (x + 1, y)
    if get(grid, x - 1, y) == node:
        yield (x - 1, y)
    if get(grid, x, y + 1) == node:
        yield (x, y + 1)
    if get(grid, x, y - 1) == node:
        yield (x, y - 1)


def has_path(sx, sy, ex, ey):
    if sx == ex and sy == ey:
        return 1

    node = get(grid, sx, sy)
    if node == "9":
        return 0

    next_node = str(int(node) + 1)
    candidates = [
        (nx, ny) for nx, ny in get_neighbors(grid, sx, sy, next_node)
    ]

    if not candidates:
        return 0

    # print(node, next_node, candidates)
    return sum(has_path(nx, ny, ex, ey) for nx, ny in candidates)


scores = []

for hx, hy in heads:
    score = 0
    for ex, ey in ends:
        score += has_path(hx, hy, ex, ey)
    scores.append(score)

print(scores)
print(sum(scores))