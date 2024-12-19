input_text = open("input5.txt").read()

rules_text, pages_text = input_text.split("\n\n")
all_updates = [line.split(",") for line in pages_text.split("\n")]

rules = {line: True for line in rules_text.split("\n")}

def is_valid_update(pages):
    for i in range(len(pages) - 1):
        p0 = pages[i]
        for j in range(i + 1, len(pages)):
            p1 = pages[j]
            if f"{p0}|{p1}" not in rules:
                return False
    return True


result = 0
for pages in all_updates:
    if is_valid_update(pages):
        mid = len(pages) // 2
        result += int(pages[mid])


print(result)


from collections import defaultdict

rules_helper = defaultdict(set)
for r in rules:
    p0, p1 = r.split("|")
    rules_helper[p0].add(p1)


def fix_ordering(pages):
    fixed = []
    page_set = set(pages)
    while page_set:
        p = page_set.pop()
        if not (page_set - rules_helper[p]):
            fixed.append(p)
        else:
            page_set.add(p)
    return fixed


result = 0
for pages in all_updates:
    if not is_valid_update(pages):
        fixed = fix_ordering(pages)
        assert is_valid_update(fixed)
        mid = len(pages) // 2
        result += int(fixed[mid])


print(result)