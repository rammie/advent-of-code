from functools import cache

input_str = open("input19.txt").read()

towels_str, targets_str = input_str.split("\n\n")
towels = tuple(sorted(towels_str.strip().split(", "), key=len))
designs = targets_str.strip().split("\n")


@cache
def find(design, towels):
    if design == "":
        return True

    return any(find(design[len(t) :], towels) for t in towels if design.startswith(t))


@cache
def count(design, towels):
    if design == "":
        return 1

    return sum(count(design[len(t) :], towels) for t in towels if design.startswith(t))


print(sum([find(d, towels) for d in designs]))
print(sum([count(d, towels) for d in designs]))
