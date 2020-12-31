import os

data = [l.split(": ") for l in open("day2.input").read().split(os.linesep)]

def parse_policy(policy):
    rule_str, char = policy.split(" ")
    rule = tuple(int(i) for i in rule_str.split("-"))
    return rule, char

def is_valid(policy, password):
    (min_pos, max_pos), char = parse_policy(policy)
    return min_pos <= password.count(char) <= max_pos

def is_valid_v2(policy, password):
    allowed, char = parse_policy(policy)
    chars = [password[pos - 1] for pos in allowed]
    return chars.count(char) == 1


# Part 1 answer
result = sum([is_valid(policy, password) for policy, password in data])
print(result)

# Part 2 answer
result = sum([is_valid_v2(policy, password) for policy, password in data])
print(result)
