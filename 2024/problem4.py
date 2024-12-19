ws = open("input4.txt").readlines()
ws = [line.strip() for line in ws]
max_y = len(ws)
max_x = len(ws[0])


def get(ws, x, y):
    if x < 0 or x >= max_x or y < 0 or y >= max_y:
        return None
    return ws[y][x]


def get_candidate_direction(ws, x, y, dx, dy, l=4):
    candidate = []
    for _ in range(l):
        char = get(ws, x, y)
        if char is None:
            return None

        candidate.append(char)
        x += dx
        y += dy
    return "".join(candidate)


def get_candidates(ws, x, y):
    candidates = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            candidate = get_candidate_direction(ws, x, y, dx, dy)
            if candidate:
                candidates.append(candidate)
    return candidates


def find_all_xmas(ws):
    count = 0
    for y in range(len(ws)):
        for x in range(0, len(ws[y])):
            candidates = get_candidates(ws, x, y)
            count += sum(c == "XMAS" for c in candidates)
    return count

print(find_all_xmas(ws))


def get_diagonals(ws, x, y):
    if x < 1 or x >= max_x - 1 or y < 1 or y >= max_y - 1:
        return None

    char = get(ws, x, y)
    return [
        get(ws, x - 1, y - 1) + char + get(ws, x + 1, y + 1),
        get(ws, x + 1, y - 1) + char + get(ws, x - 1, y + 1),
    ]


def find_x_mas_at(ws, x, y):
    if get(ws, x, y) != "A":
        return 0
    candidates = get_diagonals(ws, x, y)
    if not candidates:
        return 0
    if all(c in ("MAS", "SAM") for c in candidates):
        return 1
    return 0

def find_all_x_mas(ws):
    count = 0
    for y in range(len(ws)):
        for x in range(0, len(ws[y])):
            count += find_x_mas_at(ws, x, y)
    return count


print(find_all_x_mas(ws))