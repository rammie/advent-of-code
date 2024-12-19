boarding_passes = [l for l in open("day5.input").read().split()]

def bsp_to_int(bsp, lo="F", hi="B", minval=0, maxval=None):
    if not len(bsp):
        return minval

    maxval = 2 ** len(bsp) if maxval is None else maxval
    if bsp[0] == lo:
        maxval = (maxval + minval) // 2
    elif bsp[0] == hi:
        minval = (maxval + minval) // 2
    else:
        assert("invalid input")

    return bsp_to_int(bsp[1:], lo, hi, minval, maxval)


def seat_id(boarding_pass):
    return 8 * bsp_to_int(boarding_pass[:7]) + bsp_to_int(boarding_pass[7:], "L", "R")


def find_my_seat():
    seat_ids = set([seat_id(bp) for bp in boarding_passes])
    for row in range(0, 128):
        for col in range(0, 8):
            sid = 8 * row + col
            if sid not in seat_ids and sid + 1 in seat_ids and sid - 1 in seat_ids:
                return sid


print(find_my_seat())