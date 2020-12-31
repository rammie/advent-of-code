import os

adapters = [int(n) for n in open("day10.input").read().split(os.linesep)]
adapters.sort()

ones = 0
threes = 0
target = 0
for num in adapters:
    if num - target == 1:
        ones += 1
    elif num - target == 3:
        threes += 1
    target = num

# Part 1 answer
print(ones * (threes + 1))


def count_paths(adapters, target=0, start=0, memo=None):
    memo = {} if memo is None else memo
    if not adapters:
        return 1

    if start in memo:
        return memo[start]

    result = sum([
        count_paths(adapters[idx + 1:], candidate, start + idx + 1, memo)
        for idx, candidate in enumerate(adapters[:3])
        if 1 <= candidate - target <= 3
    ])
    memo[start] = result
    return result

# Part 2 answer
print(count_paths(adapters))