p1 = [21, 48, 44, 31, 29, 5, 23, 11, 12, 27, 49, 22, 18, 7, 15, 20, 2, 45, 14, 17, 40, 35, 6, 24, 41]
p2 = [47, 1, 10, 16, 28, 37, 8, 26, 46, 25, 3, 9, 34, 50, 32, 36, 43, 4, 42, 33, 19, 13, 38, 39, 30]

while p1 and p2:
    np1 = p1.pop(0)
    np2 = p2.pop(0)
    if np1 > np2:
        p1.extend([np1, np2])
    else:
        p2.extend([np2, np1])

p = p1 + p2

# Part 1 answer
print(sum([(i + 1) * np for i, np in enumerate(reversed(p))]))

p1 = [21, 48, 44, 31, 29, 5, 23, 11, 12, 27, 49, 22, 18, 7, 15, 20, 2, 45, 14, 17, 40, 35, 6, 24, 41]
p2 = [47, 1, 10, 16, 28, 37, 8, 26, 46, 25, 3, 9, 34, 50, 32, 36, 43, 4, 42, 33, 19, 13, 38, 39, 30]

def recursive_combat(p1, p2, memo=None):
    hand_key = (tuple(p1), tuple(p2))
    game = {"p1": {}, "p2": {}}
    while p1 and p2:
        round_key = (tuple(p1), tuple(p2))
        if round_key in memo:
            p1[:] = memo[round_key][0]
            p2[:] = memo[round_key][1]
            return memo[round_key][2]

        if tuple(p1) in game["p1"] or tuple(p2) in game["p2"]:
            memo[hand_key] = (p1.copy(), p2.copy(), True)
            return True

        game["p1"][tuple(p1)] = True
        game["p2"][tuple(p2)] = True

        np1 = p1.pop(0)
        np2 = p2.pop(0)
        p1_wins =  recursive_combat(p1[:np1].copy(), p2[:np2].copy(), memo) if len(p1) >= np1 and len(p2) >= np2 else (np1 > np2)
        if p1_wins:
            p1.extend([np1, np2])
        else:
            p2.extend([np2, np1])

    memo[hand_key] = (p1.copy(), p2.copy(), bool(p1))
    return bool(p1)


recursive_combat(p1, p2, {})
p = p1 + p2

# Part 2 answer
print(sum([(i + 1) * np for i, np in enumerate(reversed(p))]))
