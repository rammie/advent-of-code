start = [9, 19, 1, 6, 0, 5, 4]
# start = [0, 3, 6]
turns = {}

def emit(c, turn):
    turns[c] = (turns[c][1], turn) if c in turns else (turn, turn)

prev = None
for turn in range(0, 30000000):
    if start:
        prev = start[0]
        start = start[1:]
        emit(prev, turn)
    else:
        if prev not in turns:
            emit(prev, turn)
        else:
            nextn = turns[prev][1] - turns[prev][0]
            emit(nextn, turn)
            prev = nextn

print (prev)