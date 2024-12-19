grid_str = open("input12.txt").readlines()
grid = [list(row.strip()) for row in grid_str]

max_x = len(grid[0])
max_y = len(grid)


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


def is_valid(x, y):
    return not (x < 0 or x >= max_x or y < 0 or y >= max_y)


def get_neighbors(x, y):
    yield (x + 1, y)
    yield (x - 1, y)
    yield (x, y + 1)
    yield (x, y - 1)


def label_region(grid, x, y, node):
    if grid[y][x] == ".":
        return (node, [], 0)

    grid[y][x] = "."
    area = 1
    coords = [(x, y)]
    for nx, ny in get_neighbors(x, y):
        if not is_valid(x, y) or get(grid, nx, ny) != node:
            continue
        _, nodes_r, area_r = label_region(grid, nx, ny, node)
        area += area_r
        coords += nodes_r
    return (node, coords, area)


def get_regions(grid):
    regions = []
    for y in range(max_y):
        for x in range(max_x):
            node = grid[y][x]
            if node == ".":
                continue

            node, coords, area = label_region(grid, x, y, node)
            regions.append((node, coords, area))
    return regions


def calc_perimeter(grid, node, coords):
    return len(list(perimeter_nodes(grid, node, coords)))


def perimeter_nodes(grid, node, coords):
    for coord in coords:
        neighbors = list(get_neighbors(*coord))
        for nx, ny in neighbors:
            if not is_valid(nx, ny) or grid[ny][nx] != node:
                yield (nx, ny)


class Side:
    left = 0
    top = 1
    right = 2
    bottom = 3

    all_sides = [left, top, right, bottom]


def get_neighbor_to_side(coord, side):
    x, y = coord
    if side == Side.left:
        return (x - 1, y)
    if side == Side.top:
        return (x, y - 1)
    if side == Side.right:
        return (x + 1, y)
    if side == Side.bottom:
        return (x, y + 1)


def get_side_number(coord, side, coord_side_map):
    if coord not in coord_side_map:
        return None
    return coord_side_map[coord].get(side)


def set_side_number(coord, side, coord_side_map, side_number):
    coord_side_map.setdefault(coord, {})[side] = side_number


def merge_sides(coord_side_map, side, side_number1, side_number2):
    for sides in coord_side_map.values():
        if sides.get(side) == side_number2:
            sides[side] = side_number1


def assign_side(coord, side, side_number, sides, coord_side_map):
    if side in (Side.left, Side.right):
        # Check "side" side of the top and bottom neigbors
        n1 = get_neighbor_to_side(coord, Side.top)
        n2 = get_neighbor_to_side(coord, Side.bottom)
    else:
        # Check "side" side of the left and right neigbors
        n1 = get_neighbor_to_side(coord, Side.left)
        n2 = get_neighbor_to_side(coord, Side.right)

    n1_side_number = n1 and get_side_number(n1, side, coord_side_map)
    n2_side_number = n2 and get_side_number(n2, side, coord_side_map)

    if n1_side_number and n2_side_number:
        merge_side_number = min(n1_side_number, n2_side_number)
        merge_sides(coord_side_map, side, n1_side_number, n2_side_number)
        set_side_number(coord, side, coord_side_map, merge_side_number)
        sides.remove(n2_side_number)
        return side_number + 1

    if n1_side_number:
        set_side_number(coord, side, coord_side_map, n1_side_number)
        return side_number

    if n2_side_number:
        set_side_number(coord, side, coord_side_map, n2_side_number)
        return side_number

    side_number += 1
    set_side_number(coord, side, coord_side_map, side_number)
    sides.add(side_number)
    return side_number + 1


def calc_sides(coords):
    sides = set()
    side_number = 1
    coords_set = set(coords)
    coord_side_map = {}

    for coord in coords:
        for side in Side.all_sides:
            neighbor = get_neighbor_to_side(coord, side)
            if neighbor not in coords_set:
                side_number = assign_side(
                    coord, side, side_number, sides, coord_side_map
                )

    return len(sides)


def fencing_cost(grid, regions):
    return sum(area * calc_perimeter(grid, n, coords) for n, coords, area in regions)


def fencing_cost2(regions):
    return sum(area * calc_sides(coords) for _, coords, area in regions)


grid_copy = copy_grid(grid)
regions = get_regions(grid)
print(fencing_cost(grid, regions))

grid = copy_grid(grid_copy)
regions = get_regions(grid)
print(fencing_cost2(regions))
