input_str = open("input15.txt").read()
grid_str, moves_str = input_str.split("\n\n")
grid = [list(row.strip()) for row in grid_str.split("\n")]

moves = "".join(moves_str.split("\n")).strip()

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


print(moves)
print_grid(grid)


def get_score(grid, box="O"):
    score = 0
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == box:
                score += 100 * y + x
    return score


def find_robot(grid):
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == "@":
                return (x, y)
            else:
                print(x, y)


# def move_boxes(grid, bx, by, dx, dy):
#     tx, ty = bx + dx, by + dy
#     while get(grid, tx, ty) == "O":
#         tx += dx
#         ty += dy

#     if get(grid, tx, ty) == "#":
#         return False
#     if get(grid, tx, ty) == ".":
#         grid[ty][tx] = "O"
#         grid[by][bx] = "."
#         return True
#     raise ValueError(get(grid, tx, ty))


# def move_robot(grid, moves, rx, ry):
#     assert get(grid, rx, ry) == "@"
#     if not moves:
#         return grid

#     move = moves[0]
#     if move == ">":
#         dx, dy = 1, 0
#     elif move == "<":
#         dx, dy = -1, 0
#     elif move == "^":
#         dx, dy = 0, -1
#     elif move == "v":
#         dx, dy = 0, 1

#     tx, ty = rx + dx, ry + dy
#     grid_copy = copy_grid(grid)

#     if get(grid_copy, tx, ty) == "#":
#         pass
#     elif get(grid_copy, tx, ty) == ".":
#         grid_copy[ry][rx] = "."
#         grid_copy[ty][tx] = "@"
#         rx, ry = tx, ty
#     elif get(grid_copy, tx, ty) == "O":
#         did_move = move_boxes(grid_copy, tx, ty, dx, dy)
#         if did_move:
#             grid_copy[ry][rx] = "."
#             grid_copy[ty][tx] = "@"
#             rx, ry = tx, ty

#     return move_robot(grid_copy, moves[1:], rx, ry)


import sys

sys.setrecursionlimit(100000)
# rx, ry = find_robot(grid)
# grid = move_robot(grid, moves, rx, ry)
# print(get_score(grid))


def make_part_2_grid(grid):
    new_grid = []
    for y in range(grid_height):
        row = []
        for x in range(grid_width):
            if grid[y][x] == "O":
                row.extend(["[", "]"])
            elif grid[y][x] == "#":
                row.extend(["#", "#"])
            elif grid[y][x] == ".":
                row.extend([".", "."])
            elif grid[y][x] == "@":
                row.extend(["@", "."])
        new_grid.append(row)
    return new_grid


def get_neighbors(grid, x, y, node):
    if get(grid, x + 1, y) == node:
        yield (x + 1, y)
    if get(grid, x - 1, y) == node:
        yield (x - 1, y)
    if get(grid, x, y + 1) == node:
        yield (x, y + 1)
    if get(grid, x, y - 1) == node:
        yield (x, y - 1)


def detect_bug(grid):
    try:
        for y in range(grid_height):
            for x in range(grid_width):
                if grid[y][x] == "[":
                    assert grid[y][x + 1] == "]"
                if grid[y][x] == "]":
                    assert grid[y][x - 1] == "["
    except AssertionError:
        print_grid(grid)
        raise
    return None


def move_boxes2(grid, bx, by, dx, dy):
    node = get(grid, bx, by)
    grid_copy = copy_grid(grid)
    tx, ty = bx + dx, by + dy

    try:
        if dx == 1:
            assert node == "[", node
        if dx == -1:
            assert node == "]", f"{node}, ({bx}, {by}), ({dx}, {dy})"
    except AssertionError:
        print_grid(grid)
        raise

    if dx != 0:
        target = get(grid_copy, tx + dx, ty)
        if target == ".":
            lbx = min(tx, tx + dx)
            grid_copy[ty][lbx] = "["
            grid_copy[ty][lbx + 1] = "]"
            grid_copy[by][bx] = "."
            print("*" * 800)
            print(dx, dy)
            print_grid(grid_copy)
            detect_bug(grid_copy)
            return True, grid_copy
        elif target == "#":
            return False, grid
        elif target in ("[", "]"):
            print("DEBUG", tx, ty, dx, dy, bx, by, target)
            print_grid(grid_copy)
            did_move, new_grid = move_boxes2(grid_copy, tx + dx, ty, dx, dy)
            if did_move:
                print_grid(new_grid)
                lbx = min(tx, tx + dx)
                print("DEBUG", tx, ty, dx, dy, bx, by, lbx)
                new_grid[ty][lbx] = "["
                new_grid[ty][lbx + 1] = "]"
                new_grid[by][bx] = "."
                detect_bug(new_grid)
                return True, new_grid
            return False, grid
    else:
        if node == "]":
            bx -= 1

        tx, ty = bx + dx, by + dy
        target = get(grid_copy, tx, ty)
        target2 = get(grid_copy, tx + 1, ty)
        if target == "." and target2 == ".":
            grid_copy[by][bx] = "."
            grid_copy[by][bx + 1] = "."
            grid_copy[ty][tx] = "["
            grid_copy[ty][tx + 1] = "]"
            detect_bug(grid_copy)
            return True, grid_copy
        elif target == "#" or target2 == "#":
            return False, grid
        elif target == "[" and target2 == "]":
            did_move, new_grid = move_boxes2(grid_copy, tx, ty, dx, dy)
            if did_move:
                new_grid[by][bx] = "."
                new_grid[by][bx + 1] = "."
                new_grid[ty][tx] = "["
                new_grid[ty][tx + 1] = "]"
                detect_bug(new_grid)
                return True, new_grid
            return False, grid
        elif target == "]" and target2 == "[":
            did_move1, new_grid = move_boxes2(grid_copy, tx, ty, dx, dy)
            did_move2, new_grid = move_boxes2(new_grid, tx + 1, ty, dx, dy)
            if did_move1 and did_move2:
                new_grid[by][bx] = "."
                new_grid[by][bx + 1] = "."
                new_grid[ty][tx] = "["
                new_grid[ty][tx + 1] = "]"
                detect_bug(new_grid)
                return True, new_grid
            return False, grid
        elif target in ("[", "]"):
            did_move, new_grid = move_boxes2(grid_copy, tx, ty, dx, dy)
            if did_move:
                new_grid[by][bx] = "."
                new_grid[by][bx + 1] = "."
                new_grid[ty][tx] = "["
                new_grid[ty][tx + 1] = "]"
                detect_bug(new_grid)
                return True, new_grid
            return False, grid

        elif target2 in ("[", "]"):
            did_move, new_grid = move_boxes2(grid_copy, tx + 1, ty, dx, dy)
            if did_move:
                new_grid[by][bx] = "."
                new_grid[by][bx + 1] = "."
                new_grid[ty][tx] = "["
                new_grid[ty][tx + 1] = "]"
                detect_bug(new_grid)
                return True, new_grid
            return False, grid

    raise ValueError(get(grid, tx, ty))


def move_robot2(grid, moves, rx, ry):
    assert get(grid, rx, ry) == "@"
    if not moves:
        return grid

    move = moves[0]
    if move == ">":
        dx, dy = 1, 0
    elif move == "<":
        dx, dy = -1, 0
    elif move == "^":
        dx, dy = 0, -1
    elif move == "v":
        dx, dy = 0, 1

    tx, ty = rx + dx, ry + dy
    grid_copy = copy_grid(grid)

    if get(grid_copy, tx, ty) == "#":
        pass
    elif get(grid_copy, tx, ty) == ".":
        grid_copy[ry][rx] = "."
        grid_copy[ty][tx] = "@"
        rx, ry = tx, ty
    elif get(grid_copy, tx, ty) in ("[", "]"):
        did_move, new_grid = move_boxes2(grid_copy, tx, ty, dx, dy)
        if did_move:
            grid_copy = new_grid
            grid_copy[ry][rx] = "."
            grid_copy[ty][tx] = "@"
            rx, ry = tx, ty

    return move_robot2(grid_copy, moves[1:], rx, ry)


ngrid = make_part_2_grid(grid)
grid_width = len(ngrid[0])
grid_height = len(ngrid)
print_grid(ngrid)

rx, ry = find_robot(ngrid)
grid = move_robot2(ngrid, moves, rx, ry)
print_grid(grid)
print(get_score(grid, box="["))
