import os
from functools import reduce

rules = open("day7.input").read().split(os.linesep)

def parse_bag(contents):
    if "no other bag" in contents:
        return []

    for num_and_bag in contents.split(", "):
        num, bag = num_and_bag.split(" ", 1)
        yield (int(num), bag)

def parse_rule(rule):
    rule = rule.replace("bags", "bag").replace(".", "")
    bag, contents = rule.split(" contain ")
    return bag, list(parse_bag(contents))


def make_ruleset(rules):
    ruleset = {}
    for rule in rules:
        bag, contents = parse_rule(rule)
        for num, b in contents:
            ruleset.setdefault(b, [])
        ruleset[bag] = contents
    return ruleset

def can_contain(bag, tgt_bag, ruleset, memo=None):
    memo = {} if memo is None else memo
    if bag in memo:
        return memo[bag]

    for num, b in ruleset[bag]:
        if b == tgt_bag:
            memo[bag] = True
            return True

        if can_contain(b, tgt_bag, ruleset, memo):
            memo[bag] = True
            return True
    else:
        memo[bag] = False
        return False

    return False


def count_contents(bag, ruleset, memo=None):
    memo = {} if memo is None else memo
    if bag in memo:
        return memo[bag]

    count = 0
    for num, b in ruleset[bag]:
        count += num + num * count_contents(b, ruleset, memo)

    memo[bag] = count
    return count


count = 0
memo = {}
ruleset = make_ruleset(rules)
for bag in ruleset.keys():
    count += can_contain(bag, "shiny gold bag", ruleset, memo)

# Part 1 answer
print(count)


# Part 2 answer
print(count_contents("shiny gold bag", ruleset))
