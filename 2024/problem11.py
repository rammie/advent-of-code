from functools import cache

inputs = "572556 22 0 528 4679021 1 10725 2790"
current = tuple(int(i) for i in inputs.split(" "))


def blink_stone(stone):
    if stone == 0:
        return [1]
    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        half_digits = len(str_stone) // 2
        return [int(str_stone[:half_digits]), int(str_stone[half_digits:])]
    return [stone * 2024]

def blink(stones):
    result = []
    for stone in stones:
        result += blink_stone(stone)
    return tuple(result)

@cache
def blink_count(current, num_iter=25):
    if not num_iter or not current:
        return len(current)
    return (blink_count(blink((current[0], )), num_iter - 1) + blink_count(current[1:], num_iter))

print(blink_count(current, num_iter=25))
print(blink_count(current, num_iter=75))
