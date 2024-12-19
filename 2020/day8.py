import os

instructions = open("day8.input").read().split(os.linesep)


def run_code(instructions):
    accumulator = 0
    seen = set()
    lineno = 0
    while True:
        if lineno in seen:
            return accumulator, False
        if lineno >= len(instructions):
            return accumulator, True

        seen.add(lineno)
        line = instructions[lineno]
        opcode, arg = line.split(" ")
        arg = int(arg)
        if opcode == "acc":
            accumulator += arg
            lineno += 1
        elif opcode == "jmp":
            lineno += arg
        elif opcode == "nop":
            lineno += 1

# Part 1 answer
print(run_code(instructions))


for lineno, line in enumerate(instructions):
    if "acc" in line:
        continue

    new_instructions = instructions.copy()
    if "jmp" in line:
        print (f"changed jmp on line {lineno}")
        new_instructions[lineno] = line.replace("jmp", "nop")
    elif "nop" in line:
        print (f"changed nop on line {lineno}")
        new_instructions[lineno] = line.replace("nop", "jmp")

    result = run_code(new_instructions)
    if result[1]:
        break

print(result)