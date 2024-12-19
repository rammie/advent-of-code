cpk = 10604480
dpk = 4126658

def transform(subject, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value

def find_loop_size(public_key, subject=7):
    value = 1
    loop_size = 0
    while value != public_key:
        value *= subject
        value %= 20201227
        loop_size += 1
    return loop_size

card_loop_size = find_loop_size(cpk)
door_loop_size = find_loop_size(dpk)

encryption_key = transform(dpk, card_loop_size)
assert encryption_key == transform(cpk, door_loop_size)

print(encryption_key)
