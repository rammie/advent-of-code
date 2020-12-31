from functools import reduce
from operator import mul
import os

lines = open("day16.input").read().split(os.linesep)

rules = []
ticket = None
tickets = []

line = lines.pop(0)
while line != "":
    field, ranges = line.split(": ")
    r1, r2 = ranges.split(" or ")
    r1 = tuple(int(v) for v in r1.split("-"))
    r2 = tuple(int(v) for v in r2.split("-"))
    rules.append((field, r1, r2))
    line = lines.pop(0)

line = lines.pop(0)
ticket = tuple(int(v) for v in lines.pop(0).split(","))

lines.pop(0)
lines.pop(0)
tickets = [tuple(int(v) for v in line.split(",")) for line in lines]

invalid_values = []
valid_tickets = tickets.copy()
for t in tickets:
    for v in t:
        if not any(r1[0] <= v <= r1[1] or r2[0] <= v <= r2[1] for f, r1, r2 in rules):
            invalid_values.append(v)
            valid_tickets.remove(t)

# Part 1 answer
print(sum(invalid_values))

candidates = {}
for f, r1, r2 in rules:
    valid_fidx = set(range(len(ticket)))
    candidates[f] = valid_fidx
    for t in valid_tickets:
        for f_idx in range(len(ticket)):
            v = t[f_idx]
            if f_idx in valid_fidx and not (r1[0] <= v <= r1[1] or r2[0] <= v <= r2[1]):
                valid_fidx.remove(f_idx)


confirmed = {}
while len(confirmed) != len(candidates):
    for f, indexes in candidates.items():
        if f in confirmed:
            continue

        if len(indexes) == 1:
            confirmed[f] = list(indexes)[0]
        else:
            candidates[f] = indexes - set(confirmed.values())

# Part 2 answer
values = []
for f, f_idx in confirmed.items():
    if f.startswith("departure"):
        values.append(ticket[f_idx])

print (reduce(mul, values, 1))