from functools import cache

LEFT = L = "<"
RIGHT = R = ">"
UP = U = "^"
DOWN = D = "v"
A = "A"
N = None

keypad = (
    ("7", "8", "9"),
    ("4", "5", "6"),
    ("1", "2", "3"),
    (N, "0", A),
)

dirpad = (
    (N, U, A),
    (L, D, R),
)


def iter_grid(grid):
    grid_height = len(grid)
    grid_width = len(grid[0])
    for y in range(grid_height):
        for x in range(grid_width):
            yield x, y, grid[y][x]


def get(grid, x, y):
    grid_height = len(grid)
    grid_width = len(grid[0])
    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return None
    return grid[y][x]


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def find(grid, target="S"):
    for x, y, node in iter_grid(grid):
        if node == target:
            return (x, y)


def get_moves(x, y):
    return [
        (L, x - 1, y),
        (R, x + 1, y),
        (U, x, y - 1),
        (D, x, y + 1),
    ]


def get_shortest_paths(grid, start, end, visited=None):
    visited = set(visited) if visited else set()
    if start == end:
        return [[A]]

    all_paths = []
    shortest_path_length = float("inf")
    sx, sy = find(grid, start)
    visited.add((sx, sy))
    for direction, mx, my in get_moves(sx, sy):
        mkey = get(grid, mx, my)
        if mkey is None:
            continue
        if (mx, my) in visited:
            continue

        paths = get_shortest_paths(grid, mkey, end, tuple(visited))
        for p in paths:
            candidate = [direction] + p
            if len(candidate) < shortest_path_length:
                shortest_path_length = len(candidate)
                all_paths = [candidate]
            elif len(candidate) == shortest_path_length:
                all_paths.append(candidate)

    return all_paths


@cache
def get_shortest_moves(grid, target, curr=A):
    if len(target) == 0:
        return [[]]

    next_key = target[0]
    best_paths = []
    shortest_path_length = float("inf")
    candidates = [
        p + path_r
        for path_r in get_shortest_moves(grid, target[1:], next_key)
        for p in get_shortest_paths(grid, curr, next_key)
    ]
    for c in candidates:
        if len(c) < shortest_path_length:
            shortest_path_length = len(c)
            best_paths = [c]
        elif len(c) == shortest_path_length:
            best_paths.append(c)
    return best_paths


@cache
def get_nth_dirpad_least_moves(path, iters=2, curr=A):
    if not path:
        return 0

    sequence = "".join(path)
    parts = sequence.split(A)
    if len(parts) > 2:
        least_moves = 0
        for part in parts[:-1]:
            part_arr = list(part)
            part_arr.append(A)
            least_moves += get_nth_dirpad_least_moves(tuple(part_arr), iters)
        return least_moves

    if iters == 1:
        least_moves = float("inf")
        next_key = sequence[0]
        rest_least_moves = get_nth_dirpad_least_moves(sequence[1:], iters, next_key)
        for p in get_shortest_paths(dirpad, curr, next_key):
            candidate = len(p) + rest_least_moves
            least_moves = min(least_moves, candidate)
        return least_moves

    least_moves = float("inf")
    dirpad_paths = get_shortest_moves(dirpad, tuple(path))
    for dp in dirpad_paths:
        new_least_moves = get_nth_dirpad_least_moves(tuple(dp), iters - 1)
        least_moves = min(least_moves, new_least_moves)
    return least_moves


def calc_shortest_sequence_length(target, iters=2):
    least_moves = float("inf")
    for kp in get_shortest_moves(keypad, target):
        candidate = get_nth_dirpad_least_moves(tuple(kp), iters=iters)
        least_moves = min(least_moves, candidate)
    return least_moves


def calc_complexity(target, iters=2):
    print("calculating complexity for", target)
    num = int(target[:-1])
    path_len = calc_shortest_sequence_length(target, iters=iters)
    print(f"complexity {path_len} * {num}")
    return num * path_len


inputs = open("input21.txt").read().strip().split("\n")

print(sum(calc_complexity(t, iters=2) for t in inputs))
print(sum(calc_complexity(t, iters=25) for t in inputs))
