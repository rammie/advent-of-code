import os

notes = open("day13.input").read().split(os.linesep)

def argmin(sequence, fn):
    return min((fn(e), e) for e in sequence)[1]

def bus_formula(b, t):
    if t % b == 0:
        return 0
    return (b * (1 + (t // b))) - t

def wins_contest(expected_departures, t):
    return all(bus_formula(b, t) == i for i, b in expected_departures)

min_ts = int(notes[0].strip())
buses = notes[1].split(",")

bus_ids = [int(b) for b in buses if b != "x"]
mods = [(bus_formula(b, min_ts), b) for b in bus_ids]
bus = argmin(mods, lambda x: x[0])

# Part 1 answer
print(bus[0] * bus[1])


expected_departures = [(idx, int(b)) for idx, b in enumerate(buses) if b != "x"]

def find_winner(expected_departures):
    answer = 0
    adder = expected_departures[0][1]
    left = expected_departures[1:]
    while left:
        answer += adder
        for i, b in left[:]:
            if (bus_formula(b, answer) - i) % b == 0:
                left.remove((i, b))
                adder *= b
                print (f"Progress: {left} -> {adder}")

    return answer


answer = find_winner(expected_departures)
# Part 2 answer
print(answer)