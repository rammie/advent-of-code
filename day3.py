import os
from functools import reduce
from operator import mul

slope = [list(l) for l in open("day3.input").read().split(os.linesep)]

def find_trees(slope, sx=3, sy=1, x=0, y=0, trees=0):
    h, w = len(slope), len(slope[0])
    if y >= h:
        return trees

    has_tree = slope[y][x] == "#"
    return find_trees(slope, sx, sy, (x + sx) % w, y + sy, trees + int(has_tree))


# Part 1 answer
print(find_trees(slope))


# Part 2 answer
trees = [find_trees(slope, sx, sy) for sx, sy in [
    [1, 1],
    [3, 1],
    [5, 1],
    [7, 1],
    [1, 2],
]]
print(reduce(mul, trees, 1))
