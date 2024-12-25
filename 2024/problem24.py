from collections import defaultdict

input_str = open("input24.txt").read()
values_str, instrs_str = input_str.split("\n\n")
values_lines = (value.strip().split(": ") for value in values_str.split("\n"))
values = {var: int(val) for var, val in values_lines}

instructions_lines = (instr.strip().split(" ") for instr in instrs_str.split("\n"))
instructions = [(l[0], l[2], l[1], l[-1]) for c, l in enumerate(instructions_lines)]


ops = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}


class Instruction:
    def __init__(self, var1, var2, op, result):
        self.var1 = var1
        self.var2 = var2
        self.op = op
        self.result = result

    def __repr__(self):
        return f"{self.var1} {self.op} {self.var2} -> {self.result}"

    def swap_result(self, instr):
        instr.result, self.result = self.result, instr.result

    def __call__(self, values):
        var1 = values.get(self.var1, 0)
        var2 = values.get(self.var2, 0)
        values[self.result] = ops[self.op](var1, var2)

    def __iter__(self):
        return iter((self.var1, self.var2, self.op, self.result))


def simulate(instructions, values, num_bits):
    for _ in range(num_bits):
        for instr in instructions:
            var1 = values.get(instr.var1, 0)
            var2 = values.get(instr.var2, 0)
            values[instr.result] = ops[instr.op](var1, var2)
    return int_from_values(values, "z", num_bits)


def values_dict(values, var="z"):
    return {int(k[1:]): v for k, v in values.items() if k.startswith(var)}


def int_from_values(values, var, num_bits):
    value_dict = values_dict(values, var)
    keys = list(sorted(range(num_bits), reverse=True))
    bin_value = "".join(str(value_dict.get(key, 0)) for key in keys)
    return int(bin_value, 2)


x_dict = values_dict(values, "x")
num_bits = len(x_dict) + 1
instructions = [Instruction(*instr) for instr in instructions]
print(simulate(instructions, values, num_bits))


# Part 2
instructions_by_result = {instr.result: instr for instr in instructions}
instructions_by_inputs = {}
instructions_by_input = defaultdict(list)
for instr in instructions:
    instructions_by_input[instr.var1].append(instr)
    instructions_by_input[instr.var2].append(instr)
    instructions_by_inputs[(instr.var1, instr.var2, instr.op)] = instr
    instructions_by_inputs[(instr.var2, instr.var1, instr.op)] = instr


def var_name(var, bit):
    return f"{var}{bit:02}"


def find_instruction(wire, op):
    return next(instr for instr in instructions_by_input[wire] if instr.op == op)


def swap_wires(wire1, wire2):
    instr1 = instructions_by_result[wire1]
    instr2 = instructions_by_result[wire2]
    instr1.swap_result(instr2)
    instructions_by_result[wire1] = instr2
    instructions_by_result[wire2] = instr1
    return {wire1, wire2}


def binary_addition(x_val, y_val):
    """Reverse engineered from the input."""
    x = [int(b) for b in reversed(f"{x_val:b}")]
    y = [int(b) for b in reversed(f"{y_val:b}")]
    n_bits = len(x)
    z = [0] * (n_bits + 1)

    a_prev = x[0] ^ y[0]
    b_prev = x[0] & y[0]
    d_prev = b_prev
    z[0] = a_prev
    for bit in range(1, n_bits + 1):
        if bit == n_bits:
            z[bit] = d_prev
            break

        a_n = x[bit] ^ y[bit]
        b_n = x[bit] & y[bit]
        c_n = a_n & d_prev
        d_n = c_n | b_n
        z[bit] = a_n ^ d_prev

        a_prev = a_n
        b_prev = d_n
        d_prev = d_n

    z_val = int("".join(str(a) for a in reversed(z)), 2)
    assert x_val + y_val == z_val


def rewire():
    """Work from the first input applying the logic above to make swaps."""
    result = set()
    b_prev = instructions_by_inputs[("x00", "y00", "AND")]
    d_prev = b_prev

    for bit in range(1, num_bits - 1):
        z_n = instructions_by_result[var_name("z", bit)]
        a_n = instructions_by_inputs[(var_name("x", bit), var_name("y", bit), "XOR")]
        b_n = instructions_by_inputs[(var_name("x", bit), var_name("y", bit), "AND")]

        c_n_desc = (a_n.result, d_prev.result, "AND")
        if c_n_desc not in instructions_by_inputs:
            swap = find_instruction(d_prev.result, "AND")
            swapped_var = swap.var2 if swap.var1 == d_prev.result else swap.var1
            c_n_desc = (swapped_var, d_prev.result, "AND")
            result.update(swap_wires(a_n.result, swapped_var))

        c_n = instructions_by_inputs[c_n_desc]
        if c_n.result.startswith("z"):
            swap = find_instruction(a_n.result, "XOR")
            result.update(swap_wires(c_n.result, swap.result))

        d_n_desc = (c_n.result, b_n.result, "OR")
        if d_n_desc not in instructions_by_inputs:
            swap = find_instruction(c_n.result, "OR")
            swapped_var = swap.var2 if swap.var1 == c_n.result else swap.var1
            d_n_desc = (c_n.result, swapped_var, "OR")
            result.update(swap_wires(b_n.result, swapped_var))

        d_n = instructions_by_inputs[d_n_desc]

        z_n_desc = (a_n.result, d_prev.result, "XOR")
        if z_n_desc not in instructions_by_inputs:
            swap = find_instruction(d_prev.result, "XOR")
            swapped_var = swap.var2 if swap.var1 == d_prev.result else swap.var1
            result.update(swap_wires(a_n.result, swapped_var))
        else:
            expected_z_n = instructions_by_inputs[z_n_desc]
            if expected_z_n != z_n:
                result.update(swap_wires(z_n.result, expected_z_n.result))

        b_prev = b_n
        d_prev = d_n
    return result


binary_addition(3, 3)
binary_addition(5, 6)
print(",".join(sorted(b for b in rewire())))
