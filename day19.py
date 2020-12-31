import os
import re

lines = open("day19.input").read().split(os.linesep)

rules = {}

line = lines.pop(0)
while line != "":
    ruleno, text = line.split(": ")
    rules[ruleno] = text
    line = lines.pop(0)

messages = lines

def assemble(ruleno, memo):
    if ruleno in memo:
        memo[ruleno]
        if callable(memo[ruleno]):
            memo[ruleno] = memo[ruleno](memo)
        return memo[ruleno]

    text = rules[ruleno].strip()
    result = assemble_text(text, memo)
    memo[ruleno] = result
    return result
    

def assemble_text(text, memo):
    if text.startswith("\""):
        clause = text[1]
    elif " | " in text:
        parts = text.split(" | ")
        clause = "|".join(assemble_text(p, memo) for p in parts)
    elif " " in text:
        clause = "".join(assemble_text(p, memo) for p in text.split(" "))
    elif text.endswith("+") and text[:-1].isnumeric():
        clause = assemble(text[:-1], memo)
        clause = fr"{clause}+"
    elif text.isnumeric():
        clause = assemble(text, memo)
    return fr"({clause})"


memo = {}
regex = "^" + assemble('0', memo) + "$"

# Part 1 answer
print(sum([re.match(regex, m) is not None for m in messages]))

memo = {}
rules["8"] = "42+"

def rule11(memo):
    r42 = assemble("42", memo)
    r31 = assemble("31", memo)
    clauses = []
    for n in range(1, 15):
        clauses.append((fr"{r42}" * n) + (fr"{r31}" * n))
    clause = "|".join(fr"({c})" for c in clauses)
    return fr"({clause})"

memo["11"] = rule11


regex = "^" + assemble('0', memo) + "$"
print(regex)

# Part 2 answer
print(sum([re.match(regex, m) is not None for m in messages]))