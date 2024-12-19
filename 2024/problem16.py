import heapq

grid_str = open("input16.txt").readlines()
grid = [list(row.strip()) for row in grid_str]
grid_width = len(grid[0])
grid_height = len(grid)


def iter_grid(grid):
    for y in range(grid_height):
        for x in range(grid_width):
            yield x, y, grid[y][x]


def get(grid, x, y):
    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return None
    return grid[y][x]


def copy_grid(grid):
    return [row.copy() for row in grid]


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def find(grid, target="S"):
    for x, y, node in iter_grid(grid):
        if node == target:
            return (x, y)


def rotate(dx, dy, clockwise=True):
    if clockwise:
        return (0, dx) if dx != 0 else (-dy, 0)
    return (0, -dx) if dx != 0 else (dy, 0)


def get_moves(score, sx, sy, dx, dy, nodes):
    yield (score + 1000, nodes, sx, sy, *rotate(dx, dy))
    yield (score + 1000, nodes, sx, sy, *rotate(dx, dy, clockwise=False))

    nodes = nodes.copy()
    nodes.add((sx + dx, sy + dy))
    yield (score + 1, nodes, sx + dx, sy + dy, dx, dy)


def navigate(grid, sx, sy, dx, dy):
    nodes = set([(sx, sy)])
    candidates = list(get_moves(0, sx, sy, dx, dy, nodes))
    heapq.heapify(candidates)

    best_nodes = set()
    best_score = float("inf")
    min_scores = {}

    while candidates:
        cscore, cnodes, csx, csy, cdx, cdy = heapq.heappop(candidates)
        min_score_to_reach = min_scores.get((csx, csy, cdx, cdy), float("inf"))
        if cscore > best_score or min_score_to_reach < cscore or grid[csy][csx] == "#":
            continue

        if grid[csy][csx] == "E":
            if cscore < best_score:
                best_score = cscore
                best_nodes.clear()
                best_nodes.update(cnodes)
            elif cscore <= best_score:
                best_nodes.update(cnodes)
            continue

        min_scores[(csx, csy, cdx, cdy)] = cscore
        for c in get_moves(cscore, csx, csy, cdx, cdy, cnodes):
            heapq.heappush(candidates, c)

    return best_score, best_nodes


sx, sy = find(grid, target="S")
score, best_nodes = navigate(grid, sx, sy, 1, 0)
print(score)
print(len(best_nodes))
