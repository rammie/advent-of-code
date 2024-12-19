from functools import cache

raw_input = open("input17.txt").read()

registers_str, program_code_str = raw_input.split("\n\n")

instructions = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv",
}


class Register:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Register({self.value})"


registers_lines = registers_str.strip().split("\n")
a_value = int(registers_lines[0].split(": ")[1])
b_value = int(registers_lines[1].split(": ")[1])
c_value = int(registers_lines[2].split(": ")[1])

code_strs = program_code_str.strip().split(": ")[1].split(",")
code = [int(x) for x in code_strs]

register_a = Register(a_value)
register_b = Register(b_value)
register_c = Register(c_value)


def get_combo_operand(code, ip):
    combo_operand = code[ip]
    if 0 <= combo_operand <= 3:
        return int(combo_operand)
    if combo_operand == 4:
        return register_a.value
    if combo_operand == 5:
        return register_b.value
    if combo_operand == 6:
        return register_c.value
    if combo_operand == 7:
        raise ValueError("Invalid operand")


def get_literal(code, ip):
    return int(code[ip])


@cache
def run_without_jumps(a_value, b_value, c_value, code, ip):
    outputs = []
    register_a.value = a_value
    register_b.value = b_value
    register_c.value = c_value

    while True:
        try:
            instruction = code[ip]
        except IndexError:
            return ip, outputs, register_a.value, register_b.value, register_c.value

        hr_instruction = instructions[instruction]
        if hr_instruction == "jnz":
            return ip, outputs, register_a.value, register_b.value, register_c.value

        if hr_instruction == "adv":
            # division
            numerator = register_a.value
            denominator = 2 ** get_combo_operand(code, ip + 1)
            register_a.value = numerator // denominator
        elif hr_instruction == "bdv":
            # division
            numerator = register_a.value
            denominator = 2 ** get_combo_operand(code, ip + 1)
            register_b.value = numerator // denominator
        elif hr_instruction == "cdv":
            # division
            numerator = register_a.value
            denominator = 2 ** get_combo_operand(code, ip + 1)
            register_c.value = numerator // denominator
        elif hr_instruction == "bxl":
            literal = get_literal(code, ip + 1)
            register_b.value = register_b.value ^ literal
        elif hr_instruction == "bst":
            value = get_combo_operand(code, ip + 1)
            register_b.value = value % 8
        elif hr_instruction == "bxc":
            literal = get_literal(code, ip + 1)
            register_b.value = register_b.value ^ register_c.value
        elif hr_instruction == "out":
            value = get_combo_operand(code, ip + 1)
            outputs.append(value % 8)

        ip += 2


def run_program(a_value, b_value, c_value, code, ip=0, target=None):
    outputs = []
    register_a.value = a_value
    register_b.value = b_value
    register_c.value = c_value

    while True:
        if target and target[: len(outputs)] != outputs[: len(target)]:
            raise ValueError("No quine found")

        ip, chunk_outputs, a_value, b_value, c_value = run_without_jumps(
            register_a.value, register_b.value, register_c.value, code, ip
        )
        outputs.extend(chunk_outputs.copy())

        try:
            instruction = code[ip]
        except IndexError:
            return outputs

        register_a.value = a_value
        register_b.value = b_value
        register_c.value = c_value

        hr_instruction = instructions[instruction]
        assert hr_instruction == "jnz"
        if register_a.value != 0:
            ip = get_literal(code, ip + 1)
        else:
            ip += 2


output = run_program(a_value, b_value, c_value, tuple(code))
print(",".join((str(o) for o in output)))


def run(a):
    """What the input code is actually doing."""
    outputs = []
    while True:
        outputs.append((a % 8) ^ 4 ^ (a >> ((a % 8) ^ 1)) % 8)
        a = a >> 3
        if a == 0:
            break
    return outputs


def calc_quine(code):
    all_candidates = [[]]
    for c in range(len(code)):
        for result in all_candidates:
            candidates = []
            for i in range(8):
                a_so_far = "".join(str(i) for i in result)
                a_value = int(a_so_far + str(i), 8)
                out = run(a_value)
                cd = c + 1
                if out == code[-cd:]:
                    candidates.append(i)

            if len(candidates) > 1:
                for c in candidates:
                    r = result.copy()
                    r.append(c)
                    all_candidates.append(r)
            elif len(candidates) == 1:
                result.append(candidates[0])
    return int("".join((str(c) for c in all_candidates[-1])), 8)


quine_input = calc_quine(code)
assert run(quine_input) == code
print(quine_input)
