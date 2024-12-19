import os
import re

lines = open("day14.input").read().split(os.linesep)
clipper = 0b0000000000000000000000000000111111111111111111111111111111111111

def to_bitmasks(mask):
    ands = 2 ** (36 + 1) - 1
    ors = 0
    for i in range(36):
        if mask[35 - i] == "1":
            ors |= 1 << i
        if mask[35 - i] == "0":
            ands &= (1 << i) ^ (2 ** (36 + 1) - 1)
    return ands, ors


def apply_mask(value, bitmasks):
    ands, ors = bitmasks
    value |= ors
    value &= ands
    value &= clipper
    return value


def apply_mask_v2(value, bitmasks):
    ands, ors = bitmasks
    value |= ors
    value &= clipper
    return value


def apply_floating_mask(value, mask):
    if "X" not in mask:
        return [value]

    x = mask.index("X")
    i = 35 - x
    new_mask = mask.replace("X", "-", 1)
    vals = []
    for v in apply_floating_mask(value, new_mask):
        vals.append(v | (1 << i))
        vals.append(v & ((1 << i) ^ (2 ** (36 + 1) - 1)) & clipper)
    return vals

def decoder_v1(lines):
    mask = None
    memory = {}

    for line in lines:
        if line.startswith("mask"):
            bitmasks = to_bitmasks(line.split(" = ")[1])
            continue

        match = re.match(r"mem\[(\d+)\] = (\d+)", line)
        address = match.group(1)
        value = int(match.group(2))
        memory[address] = apply_mask(value, bitmasks)
    return memory


def decoder_v2(lines):
    mask = None
    memory = {}

    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
            bitmasks = to_bitmasks(mask)
            continue

        match = re.match(r"mem\[(\d+)\] = (\d+)", line)
        address = int(match.group(1))
        value = int(match.group(2))

        address = apply_mask_v2(address, bitmasks)
        for mapped_address in apply_floating_mask(address, mask):
            memory[mapped_address] = value
    return memory


# Part 1 answer
memory = decoder_v1(lines)
print(sum(memory.values()))


# Part 2 answer
memory = decoder_v2(lines)
print(sum(memory.values()))