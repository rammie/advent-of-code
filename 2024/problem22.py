from collections import defaultdict
from itertools import pairwise

inputs = open("input22.txt").readlines()
secret_numbers = [int(x) for x in inputs]


def calc_next(s):
    c = 16777216
    s = ((s << 6) ^ s) % c
    s = ((s >> 5) ^ s) % c
    s = ((s << 11) ^ s) % c
    return s


def calc_next_n(secret, iters=2000):
    yield secret
    for _ in range(iters):
        secret = calc_next(secret)
        yield secret


def get_sequence(secret, iters=2000):
    for secret in calc_next_n(secret, iters):
        yield secret % 10


def get_changes(sequence):
    for s1, s2 in pairwise(sequence):
        yield s2 - s1


def iter_index(iter, cache, index):
    curr_index = len(cache)
    while curr_index <= index:
        cache.append(next(iter))
        curr_index += 1
    return cache[index]


def get_window_map(sequence, windows, best_score):
    seen = set()
    changes = list(get_changes(sequence))
    for i in range(len(changes) - 3):
        key = tuple(changes[i : i + 4])
        if key not in seen:
            seen.add(key)
            windows[key] += sequence[i + 4]
            best_score = max(best_score, windows[key])
    return best_score


def get_window_maps():
    windows = defaultdict(int)
    best_score = 0
    for s in secret_numbers:
        sequence = list(get_sequence(s))
        best_score = get_window_map(sequence, windows, best_score)
    return best_score


# Part 1
print(sum(list(calc_next_n(s))[-1] for s in secret_numbers))


# Part 2
print(get_window_maps())
