equations = open("input7.txt").readlines()


def can_satisfy(test, inputs):
    if not inputs:
        return test == 0

    if len(inputs) == 1:
        return test == inputs[0]

    if test % inputs[0] != 0:
        return can_satisfy(test - inputs[0], inputs[1:])

    return (
        can_satisfy(test - inputs[0], inputs[1:]) or
        can_satisfy(test // inputs[0], inputs[1:])
    )


result = 0
for line in equations:
    test_value_str, rest = line.split(": ")
    test_value = int(test_value_str)
    inputs = [int(r) for r in rest.split(" ")]
    reversed_inputs = list(reversed(inputs))
    if can_satisfy(test_value, reversed_inputs):
        result += test_value

print(result)



def can_satisfy_concat(test, inputs):
    if not inputs:
        return test == 0

    if len(inputs) == 1:
        return test == inputs[0]

    candidates = []

    candidates.append((test - inputs[0], inputs[1:]))

    if test % inputs[0] == 0:
        candidates.append((test // inputs[0], inputs[1:]))

    test_str = str(test)
    for b in range(1, len(test_str)):
        try:
            left = int(test_str[:b])
            right = int(test_str[b:])
        except ValueError:
            continue
        if inputs[0] == right:
            candidates.append((left, inputs[1:]))

    return any(can_satisfy_concat(*c) for c in candidates)



result = 0
for line in equations:
    test_value_str, rest = line.split(": ")
    test_value = int(test_value_str)
    inputs = [int(r) for r in rest.split(" ")]
    reversed_inputs = list(reversed(inputs))
    if can_satisfy_concat(test_value, reversed_inputs):
        result += test_value

print(result)