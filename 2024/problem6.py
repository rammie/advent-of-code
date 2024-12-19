grid_str = open("input6.txt").readlines()
grid = [[c for c in line.strip()] for line in grid_str]
max_y = len(grid)
max_x = len(grid[0])


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


def set_X(grid, x , y):
    if grid[y][x] == "X":
        return 0

    grid[y][x] = "X"
    return 1


def rotate(dx, dy):
    if dx == 0:
        return (-dy, 0)
    return (0, dx)


def find_start(grid):
    for y in range(max_y):
        for x in range(max_x):
            if get(grid, x, y) == "^":
                return (x, y)
    raise ValueError("No start")


def path_length(grid):
    x, y = find_start(grid)
    dx, dy = 0, -1
    count = 0
    while True:
        block = get(grid, x + dx, y + dy)
        if block is None:
            return count

        if block == "#":
            dx, dy = rotate(dx, dy)
            continue

        x += dx
        y += dy
        count += set_X(grid, x, y)


def can_exit(grid):
    x, y = find_start(grid)
    dx, dy = 0, -1
    marked = set()
    while True:
        if (x, y, dx, dy) in marked:
            return False

        marked.add((x, y, dx, dy))
        block = get(grid, x + dx, y + dy)
        if block is None:
            return True

        if block == "#":
            dx, dy = rotate(dx, dy)
            continue

        x += dx
        y += dy


def find_time_loops(grid):
    count = 0
    for x in range(max_x):
        for y in range(max_y):
            if grid[y][x] != ".":
                continue

            grid_copy = copy_grid(grid)
            grid_copy[y][x] = "#"
            if not can_exit(grid_copy):
                count += 1
    return count




# Part 1
print(path_length(copy_grid(grid)))

# Part 2
print(find_time_loops(grid))