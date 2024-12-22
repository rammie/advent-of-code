from collections import defaultdict
from itertools import pairwise

inputs = open("input22.txt").readlines()
secret_numbers = [int(x) for x in inputs]


def calc_next(s):
    c = 16777216
    s = ((s * 64) ^ s) % c
    s = ((s // 32) ^ s) % c
    s = ((s * 2048) ^ s) % c
    return s


def calc_next_n_simple(secret, iters=2000):
    last4 = []
    for _ in range(iters):
        secret = calc_next(secret)

        last4.append(secret)
        if len(last4) > 4:
            last4.pop(0)

    return secret


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


def get_window_map(sequence, changes, windows, best_score):
    result = {}
    for i in range(len(changes) - 3):
        key = tuple(changes[i : i + 4])
        if key not in result:
            windows[key] += sequence[i + 4]
            best_score = max(best_score, windows[key])`
    return best_score


def get_window_maps(sequences, all_changes):
    windows = defaultdict(int)
    best_score = 0
    for seq, changes in zip(sequences, all_changes):
        best_score = get_window_map(seq, changes, windows, best_score)
    return best_score


# Part 1
print(sum([calc_next_n_simple(s) for s in secret_numbers]))


# Part 2
sequences = list(list(get_sequence(s)) for s in secret_numbers)
all_changes = list(list(get_changes(s)) for s in sequences)
best_score = get_window_maps(sequences, all_changes)
print(best_score)
