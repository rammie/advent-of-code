groups = open("day6.input").read().split(os.linesep + os.linesep)

count = 0
for group in groups:
    all_answers = group.strip().replace(os.linesep, "")
    all_chars = set(all_answers)
    count += len(all_chars)


# Part 1 answer
print(count)


count = 0
for group in groups:
    sets = [set(answers) for answers in group.strip().split(os.linesep)]
    count += len(set.intersection(*sets))


# Part 2 answer
print(count)

