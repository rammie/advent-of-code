from collections import defaultdict
import heapq

grid_str = open("input20.txt").readlines()
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


def get_moves(sx, sy):
    yield (sx + 1, sy)
    yield (sx - 1, sy)
    yield (sx, sy + 1)
    yield (sx, sy - 1)


def in_bounds(x, y):
    return 0 <= x < grid_width and 0 <= y < grid_height


def shortest_path(grid, sx, sy):
    path = [(sx, sy)]
    nodes = {(sx, sy)}
    candidates = [(0, nodes, path, sx, sy)]
    heapq.heapify(candidates)

    best_path = None
    best_score = float("inf")
    min_scores = {}

    while candidates:
        cscore, cnodes, cpath, csx, csy = heapq.heappop(candidates)
        if grid[csy][csx] == "E":
            if cscore < best_score:
                best_path = cpath
                best_score = cscore
            continue

        for nx, ny in get_moves(csx, csy):
            if not in_bounds(nx, ny):
                continue

            nscore = cscore + 1
            if nscore > best_score:
                continue

            if (nx, ny) in cnodes:
                continue

            if min_scores.get((nx, ny), float("inf")) < nscore:
                continue

            min_scores[(csx, csy)] = nscore
            if grid[ny][nx] != "#":
                nnodes = cnodes.copy()
                nnodes.add((nx, ny))

                npath = cpath.copy()
                npath.append((nx, ny))
                heapq.heappush(candidates, (nscore, nnodes, npath, nx, ny))

    return best_score, best_path


def get_cheat_moves(sx, sy, num_moves, visited=set()):
    moves = []
    for nx, ny in get_moves(sx, sy):
        if in_bounds(nx, ny) and (nx, ny) not in visited:
            visited.add((nx, ny))
            moves.append((num_moves, nx, ny))
            if num_moves > 1:
                moves.extend(get_cheat_moves(nx, ny, num_moves - 1, visited))
    return moves


def get_cheat_moves(sx, sy, num_moves, visited=set()):
    for x in range(-num_moves, num_moves + 1):
        for y in range(-num_moves, num_moves + 1):
            move_count = abs(x) + abs(y)
            if move_count > num_moves:
                continue
            nx, ny = sx + x, sy + y
            if not in_bounds(nx, ny) or (nx, ny) in visited:
                continue

            yield move_count, nx, ny


def navigate(grid, cheat_start, path, target, cheat_length=2):
    path_score = {coord: target - i for i, coord in enumerate(path)}

    sx, sy = path[cheat_start]
    visited = set(path[: cheat_start + 1])
    candidates = []

    for move_num, nx, ny in get_cheat_moves(sx, sy, cheat_length, visited.copy()):
        num_moves = cheat_length - move_num
        if move_num >= 1:
            candidates.append((move_num, nx, ny))

    print(len(candidates))
    # c2 = []
    # for nx, ny in get_moves(sx, sy):
    #     for nx2, ny2 in get_moves(nx, ny):
    #         if in_bounds(nx2, ny2) and (nx2, ny2) not in visited:
    #             c2.append((2, nx2, ny2))
    # candidates = c2

    # assert set(c2) == set(
    #     candidates
    # ), f"(missing) {set(c2) - set(candidates)} (extra){set(candidates) - set(c2)}"

    scores = []
    for num_moves, cx, cy in candidates:
        if grid[cy][cx] != "#":
            scores.append(cheat_start + num_moves + path_score[(cx, cy)])

    return scores


sx, sy = find(grid, target="S")
score_without_cheating, path = shortest_path(grid, sx, sy)
print(score_without_cheating)
print(len(path))
print(path)

scores = []

# for i in range(score_without_cheating):
#     scores.extend(
#         navigate(grid, cheat_start=i, path=path, target=score_without_cheating)
#     )

for i in range(score_without_cheating):
    scores.extend(
        navigate(
            grid,
            cheat_start=i,
            path=path,
            target=score_without_cheating,
            cheat_length=20,
        )
    )


print(scores)

score_counts = defaultdict(int)
for score in scores:
    if score_without_cheating > score:
        score_counts[score_without_cheating - score] += 1


for s in sorted(score_counts):
    print(f"{score_counts[s]} ways to save {s} picoseconds")

print(score_counts)

count = 0
for score in scores:
    if score_without_cheating - score >= 100:
        count += 1

print(count)
