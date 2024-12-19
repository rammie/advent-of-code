machines = []
inputs = open("input13.txt").read()


def parse_button_line(button_str):
    button_parts = button_str.split(": ")[1].split(", ")
    return (int(button_parts[0][1:]), int(button_parts[1][1:]))


def parse_prize_line(prize_line, extra=0):
    parts = prize_line.split(": ")[1].split(", ")
    return (int(parts[0][2:]) + extra, int(parts[1][2:]) + extra)


def parse_machine(machine_desc, extra=0):
    lines = machine_desc.strip().split("\n")
    button_a = parse_button_line(lines[0])
    button_b = parse_button_line(lines[1])
    prize = parse_prize_line(lines[2], extra=extra)
    return (button_a, button_b, prize)


def parse_machines(inputs, extra=0):
    return [
        parse_machine(machine_desc, extra=extra)
        for machine_desc in inputs.split("\n\n")
    ]


def machine_cost(a, b, target, a_cost=3, b_cost=1):
    term = a[0] * b[1] - a[1] * b[0]
    # We assume a[0], b[0], a[1], b[1] are all > 0.
    # There are a few other cases that are not solved by the math below.
    # I didn't bother with them since they do not appear in the input.
    if term == 0 and a[0] == a[1] and b[0] == b[1]:
        raise NotImplementedError("Not implemented.")
    elif term == 0 and a[0] == a[1]:
        count_b = (target[1] * b[0] - target[0] * b[1]) // (b[1] - b[0])
        count_a = (target[1] - count_b * b[1]) // a[1]
    elif term == 0 and b[0] == b[1]:
        count_a = (target[1] * a[0] - target[0] * a[1]) // (a[1] - a[0])
        count_b = (target[1] - count_a * a[1]) // b[1]
    elif term == 0:
        count_b = (target[1] * b[0] - target[0] * b[1]) // (b[1] - b[0])
        count_a = (target[1] * a[0] - target[0] * a[1]) // (a[1] - a[0])
    else:
        count_b = (a[0] * target[1] - a[1] * target[0]) // term
        count_a = (target[1] - count_b * b[1]) // a[1]

    candidate = (count_a * a[0] + count_b * b[0], count_a * a[1] + count_b * b[1])
    return (count_a * a_cost + count_b * b_cost) if candidate == target else False


machines = parse_machines(inputs)
print(sum(machine_cost(*m) for m in machines))

machines = parse_machines(inputs, extra=10000000000000)
print(sum(machine_cost(*m) for m in machines))
