from collections import defaultdict
import heapq

grid_strs = open("input25.txt").read().split("\n\n")


def parse_grid(grid_str):
    grid = [list(row.strip()) for row in grid_str]
    return [list(row) for row in zip(*grid)]


grids = [parse_grid(grid_str.split("\n")) for grid_str in grid_strs]
max_width = len(grids[0][0])
max_height = len(grids[0])

print(grids)

# height_map = {}
grid_height_map = {}
is_lock_map = {}
for i, grid in enumerate(grids):
    grid_heights = tuple(sum(c == "#" for c in col) - 1 for col in grid)
    # height_map[grid_heights] = grid
    grid_height_map[i] = grid_heights
    is_lock_map[i] = True if grid[0][0] == "#" else False


matches = 0
for i, grid1 in enumerate(grids):
    for j in range(i + 1, len(grids)):
        if is_lock_map[i] == is_lock_map[j]:
            continue

        grid2 = grids[j]
        grid_heights_1 = grid_height_map[i]
        grid_heights_2 = grid_height_map[j]
        can_fit = tuple(
            gh1 + gh2 < max_width - 1
            for gh1, gh2 in zip(grid_heights_1, grid_heights_2)
        )
        if all(can_fit):
            print(grid_heights_1, grid_heights_2)
            matches += 1


print(max_width, max_height)
print(matches)
