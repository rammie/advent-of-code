lines = open("input14.txt").readlines()
# grid_width, grid_height = 11, 7
grid_width, grid_height = 101, 103


def copy_grid(grid):
    return [row.copy() for row in grid]


def print_grid(grid):
    for row in grid:
        print("".join(str(v) if v else "." for v in row))
    print()


def parse_robot(line):
    parts = line.split(" ")
    p_str = parts[0].split("=")
    v_str = parts[1].split("=")
    px, py = p_str[1].split(",")
    vx, vy = v_str[1].split(",")
    return {
        "position": (int(px), int(py)),
        "velocity": (int(vx), int(vy)),
    }


def parse_robots(lines):
    return [parse_robot(line) for line in lines]


def set_initial_positions(robots, grid):
    for robot in robots:
        x, y = robot["position"]
        grid[y][x] += 1


def update_robots(robots, grid, seconds=1):
    for robot in robots:
        x, y = robot["position"]
        grid[y][x] -= 1

        nx, ny = (
            (x + seconds * robot["velocity"][0]) % grid_width,
            (y + seconds * robot["velocity"][1]) % grid_height,
        )
        robot["position"] = (nx, ny)
        grid[ny][nx] += 1


def calc_safety(grid):
    mid_x = grid_width // 2
    mid_y = grid_height // 2
    quad1 = sum(sum(row[:mid_x]) for row in grid[:mid_y])
    quad2 = sum(sum(row[mid_x + 1 :]) for row in grid[:mid_y])
    quad3 = sum(sum(row[:mid_x]) for row in grid[mid_y + 1 :])
    quad4 = sum(sum(row[mid_x + 1 :]) for row in grid[mid_y + 1 :])
    return quad1 * quad2 * quad3 * quad4


def get(grid, x, y):
    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return None
    return grid[y][x]


def get_slice(grid, x, y, length):
    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return None
    grid_slice = grid[y][x - length // 2 : x + length // 2 + 1]
    if len(grid_slice) < length:
        return None
    return tuple(grid_slice)


def is_xmas_tree(grid):
    for y in range(grid_height):
        for x in range(grid_width):
            if (
                grid[y][x] == 1
                and get_slice(grid, y + 1, x, 3) == (1, 1, 1)
                and get_slice(grid, y + 2, x, 5) == (1, 1, 1, 1, 1)
                and get_slice(grid, y + 3, x, 7) == (1, 1, 1, 1, 1, 1, 1)
            ):
                return True
    return False


# Part 1
robots = parse_robots(lines)
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
set_initial_positions(robots, grid)
update_robots(robots, grid, seconds=100)
print(calc_safety(grid))


robots = parse_robots(lines)
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
set_initial_positions(robots, grid)

i = 0
while True:
    update_robots(robots, grid, seconds=1)
    i += 1
    if is_xmas_tree(grid):
        print_grid(grid)
        print(i)
        break
