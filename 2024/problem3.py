import re

code = open("input3.txt").read()


def run_code(code):
    matches = re.findall(r"mul\((\d+),(\d+)\)", code, re.MULTILINE)
    result = 0
    for m in matches:
        result += int(m[0]) * int(m[1])
    return result

print(run_code(code))


result = 0
parts = code.split("do()")
for part in parts:
    strips = part.split("don't()")
    result += run_code(strips[0])

print(result)