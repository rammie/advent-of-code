import os

numbers = [int(n) for n in open("day9.input").read().split(os.linesep)]

def is_valid(num, preamble):
    for i, p in enumerate(preamble):
        for j, q in enumerate(preamble):
            if i >= j:
                continue
            if p + q == num:
                return True
    return False

for idx in range(25, len(numbers)):
    if not is_valid(numbers[idx], numbers[idx - 25:idx]):
        break

def find_range(numbers, target):
    for i in range(len(numbers) - 1):
        result = numbers[i]
        for j in range(i + 1, len(numbers)):
            result += numbers[j]
            if result > target:
                break
            if result == target:
                return min(numbers[i:j]) + max(numbers[i:j])
    return None

# Part 1 answer
print (numbers[idx])
target = numbers[idx]


# Part 2 answer
print (find_range(numbers, target))