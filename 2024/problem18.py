import heapq

blocks_str = open("input18.txt").readlines()

blocks_str = [tuple(row.strip().split(",")) for row in blocks_str]
blocks = [(int(x), int(y)) for x, y in blocks_str]
grid_width = grid_height = 0


def get(grid, x, y):
    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return None
    return grid[y][x]


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def get_moves(sx, sy):
    return [
        (sx + 1, sy),
        (sx, sy + 1),
        (sx - 1, sy),
        (sx, sy - 1),
    ]


def navigate(grid, sx, sy):
    candidates = [(0, sx, sy)]
    heapq.heapify(candidates)
    best_score = float("inf")
    min_scores = {}

    while candidates:
        cscore, csx, csy = heapq.heappop(candidates)
        if get(grid, csx, csy) == "E":
            if cscore < best_score:
                best_score = cscore
            continue

        for nx, ny in get_moves(csx, csy):
            nscore = cscore + 1
            if (
                get(grid, nx, ny) in ("E", ".")
                and nscore < min_scores.get((nx, ny), float("inf"))
                and nscore < best_score
            ):
                min_scores[(nx, ny)] = nscore
                heapq.heappush(candidates, (nscore, nx, ny))

    return best_score


grid_width = grid_height = 71
grid = [["." for _ in range(grid_width)] for _ in range(grid_height)]
grid[grid_width - 1][grid_height - 1] = "E"

niter = 1024
for x, y in blocks[:niter]:
    grid[y][x] = "#"

best_score = navigate(grid, 0, 0)
print(best_score)

grid_width = grid_height = 71
grid = [["." for _ in range(grid_width)] for _ in range(grid_height)]
grid[grid_width - 1][grid_height - 1] = "E"

for iter in range(len(blocks)):
    bx, by = blocks[iter]
    grid[by][bx] = "#"
    best_score = navigate(grid, 0, 0)
    if best_score == float("inf"):
        break

print(bx, by)
