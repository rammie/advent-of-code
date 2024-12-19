import os

moves = open("day12.input").read().split(os.linesep)
pos = (0, 0)
face = "E"

faces = ["N", "E", "S", "W"]
rotations = {"R": 90, "L": -90}
dirs = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (-1, 0),
    "W": (1, 0),
}

def inv(tup):
    return (-t for t in tup)

def tuple_sum(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def rotate(face, rotation, arg):
    arg //= rotations[rotation]
    face_index = (faces.index(face) + arg)
    return faces[face_index % len(faces)]

for move in moves:
    instruction = move[0]
    arg = int(move[1:])

    if instruction in dirs:
        pos = tuple_sum(pos, tuple(arg * m for m in dirs[instruction]))

    if instruction == "F":
        pos = tuple_sum(pos, tuple(arg * m for m in dirs[face]))

    if instruction in rotations:
        face = rotate(face, instruction, arg)

# Part 1 answer
print(sum((abs(p) for p in pos)))


pos = (0, 0)
waypoint = (-10, -1)

def rotate_waypoint(waypoint, rotation, arg):
    vec1 = (waypoint[0], 0)
    vec2 = (0, waypoint[1])
    arg //= rotations[rotation]
    for r in range(abs(arg)):
        if arg >= 0:
            waypoint = (waypoint[1], -waypoint[0])
        if arg < 0:
            waypoint = (-waypoint[1], waypoint[0])
    return waypoint

for move in moves:
    instruction = move[0]
    arg = int(move[1:])

    if instruction in dirs:
        waypoint = tuple_sum(waypoint, tuple(arg * m for m in dirs[instruction]))

    if instruction == "F":
        pos = tuple_sum(pos, tuple(arg * m for m in waypoint))

    if instruction in rotations:
        waypoint = rotate_waypoint(waypoint, instruction, arg)


# Part 2 answer
print(sum((abs(p) for p in pos)))