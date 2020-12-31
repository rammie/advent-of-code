import os

seatchart = open("day11.input").read().split(os.linesep)
seatchart = [list(row) for row in seatchart]

seatchart_next = seatchart
seatchart = None

def psc(seatchart):
    rows = len(seatchart)
    cols = len(seatchart[0])
    for row in seatchart:
        for seat in row:
            print(seat, end="")
        print("")
    print(os.linesep)

def compute_iter(seatchart):
    rows = len(seatchart)
    cols = len(seatchart[0])
    seats = [
        compute_seat(seatchart, ri, ci)
        for ri in range(rows)
        for ci in range(cols)
    ]
    return [seats[i:i + cols] for i in range(0, rows * cols, cols)]

def compute_seat(sc, ri, ci):
    rows = len(sc)
    cols = len(sc[0])
    s = sc[ri][ci]
    cells = ((ri - 1, ci - 1), (ri - 1, ci), (ri - 1, ci + 1), (ri, ci + 1), (ri + 1, ci + 1), (ri + 1, ci), (ri + 1, ci - 1), (ri, ci - 1))
    adj = [sc[r][c] for r, c in cells if 0 <= r < rows and 0 <= c < cols]
    if s == "#" and adj.count("#") >= 4:
        return "L"
    if s == "L" and "#" not in adj:
        return "#"
    return s


def compute_iter2(seatchart):
    rows = len(seatchart)
    cols = len(seatchart[0])
    seats = [
        compute_seat_ray(seatchart, ri, ci)
        for ri in range(rows)
        for ci in range(cols)
    ]
    return [seats[i:i + cols] for i in range(0, rows * cols, cols)]

def cast_ray(sc, ri, ci, dr, dc, rows, cols):
    r, c = ri + dr, ci + dc
    while 0 <= r < rows and 0 <= c < cols:
        if sc[r][c] != ".":
            return sc[r][c]
        r += dr
        c += dc
    return "."


def compute_seat_ray(sc, ri, ci):
    rows = len(sc)
    cols = len(sc[0])
    s = sc[ri][ci]
    dirs = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    adj = [cast_ray(sc, ri, ci, dr, dc, rows, cols) for dr, dc in dirs]
    if s == "#" and adj.count("#") >= 5:
        return "L"
    if s == "L" and "#" not in adj:
        return "#"
    return s

# while seatchart != seatchart_next:
#     seatchart = seatchart_next
#     seatchart_next = None
#     seatchart_next = compute_iter(seatchart)

# psc(seatchart)

# Part 1 answer
# print(sum((row.count("#") for row in seatchart)))



while seatchart != seatchart_next:
    seatchart = seatchart_next
    seatchart_next = None
    seatchart_next = compute_iter2(seatchart)

# Part 2 answer
print(sum((row.count("#") for row in seatchart)))