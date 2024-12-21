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
        return [A]

    shortest_path_length = float("inf")
    best_paths = []
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
            candidate = direction + p
            if len(candidate) < shortest_path_length:
                shortest_path_length = len(candidate)
                best_paths = [candidate]
            elif len(candidate) == shortest_path_length:
                best_paths.append(candidate)

    return best_paths


def get_shortest_sequences(grid, target, curr=A):
    if len(target) == 0:
        return [""]

    next_key = target[0]
    shortest_path_length = float("inf")
    best_paths = []
    candidates = [
        p + path_r
        for path_r in get_shortest_sequences(grid, target[1:], next_key)
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
def calc_shortest_dirpad_sequence_length(sequence, num_dirpads=2, curr=A):
    if not sequence:
        return 0

    parts = sequence.split(A)
    if len(parts) > 2:
        return sum(
            calc_shortest_dirpad_sequence_length(part + A, num_dirpads)
            for part in parts[:-1]
        )

    if num_dirpads == 1:
        car, cdr = sequence[0], sequence[1:]
        rest = calc_shortest_dirpad_sequence_length(cdr, num_dirpads, car)
        return rest + min(len(p) for p in get_shortest_paths(dirpad, curr, car))

    return min(
        calc_shortest_dirpad_sequence_length(dp, num_dirpads - 1)
        for dp in get_shortest_sequences(dirpad, sequence)
    )


def calc_shortest_sequence_length(target, num_dirpads=2):
    return min(
        calc_shortest_dirpad_sequence_length(kp, num_dirpads)
        for kp in get_shortest_sequences(keypad, target)
    )


def calc_complexity(target, num_dirpads=2):
    print("calculating complexity for", target)
    num = int(target[:-1])
    path_len = calc_shortest_sequence_length(target, num_dirpads=num_dirpads)
    print(f"complexity {path_len} * {num}")
    return num * path_len


inputs = open("input21.txt").read().strip().split("\n")
print(sum(calc_complexity(t, num_dirpads=2) for t in inputs))
print(sum(calc_complexity(t, num_dirpads=25) for t in inputs))
