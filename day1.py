expenses = [int(l) for l in open("day1.input").read().split()]

def find_pair(expenses, target=2020):
    reqs = set()
    for num in expenses:
        if num in reqs:
            return num, target - num
        reqs.add(target - num)

def find_triple(expenses, target=2020):
    for c, num in enumerate(expenses):
        result = find_pair(expenses[:c], target - num)
        if result:
            return result[0], result[1], num

# Part 1 answer
n, m = find_pair(expenses)
print (n * m)

# Part 2 answer
n, m, o = find_triple(expenses)
print (n * m * o)
