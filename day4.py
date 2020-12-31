import os
import re
from functools import reduce
from operator import mul

passports = open("day4.input").read().split(os.linesep + os.linesep)

def validate_height(v):
    match = re.match(r"(\d+)(cm|in)", v)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        if unit == "cm":
            return 150 <= value <= 193
        if unit == "in":
            return 59 <= value <= 76
    return False

validators = {
    "byr": (lambda x: len(x) == 4 and 1920 <= int(x) <= 2002),
    "iyr": (lambda x: len(x) == 4 and 2010 <= int(x) <= 2020),
    "eyr": (lambda x: len(x) == 4 and 2020 <= int(x) <= 2030),
    "hgt": (validate_height),
    "hcl": (lambda x: re.match(r"#[0-9a-f]{6}", x)),
    "ecl": (lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]),
    "pid": (lambda x: re.match(r"[0-9]{9}", x)),
    "cid": (lambda x: True),
}

required_fields = validators.keys()

def parse_passport(raw_passport):
    parts = [p.split(":") for p in raw_passport.split()]
    return {p[0].strip(): p[1].strip() for p in parts}

def is_valid(raw_passport):
    passport = parse_passport(raw_passport)
    missing_fields = list(required_fields - set(passport.keys()))
    if missing_fields not in (["cid"], []):
        return False

    for field, value in passport.items():
        if not validators[field](value):
            return False

    print (passport["hgt"])
    return True

print(sum([is_valid(rp) for rp in passports]))
