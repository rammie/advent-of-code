from itertools import chain

class Cup:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class CupList:
    def __init__(self, cups_raw):
        self.cups = {}
        prev = None
        self.curr = None
        for c in cups_raw:
            c = int(c)
            cup = Cup(c)
            if not self.curr:
                self.curr = cup

            if prev:
                cup.prev = prev
                prev.next = cup

            self.cups[c] = cup
            prev = cup

        cup.next = self.curr
        self.curr.prev = cup

        n = len(self.cups)
        for c in range(1, 1 + len(self.cups)):
            prev_index = (((c - 1) - 1) % n) + 1
            self.cups[c].prev_index = self.cups[prev_index]

    def move(self):
        curr = cl.curr
        cup_1 = curr.next
        cup_2 = curr.next.next
        cup_3 = curr.next.next.next
        curr.next = cup_3.next
        removed = [cup_1, cup_2, cup_3]

        dest_cup = curr.prev_index
        while dest_cup in removed:
            dest_cup = dest_cup.prev_index

        link_cup = dest_cup.next
        dest_cup.next = cup_1
        cup_3.next = link_cup

        self.curr = self.curr.next

    def __str__(self):
        item = None
        sb = []
        while item != self.curr:
            if item is None:
                item = self.curr
                sb.append(f"({item.value}) ")
            else:
                sb.append(f"{item.value} ")
            item = item.next
        return "".join(sb)


cups = [int(i) for i in "247819356"]

cl = CupList(cups)
for move in range(100):
    cl.move()

# Part 1 answer
print(cl)


cups = chain([int(i) for i in "247819356"], range(10, 1_000_001))

cl = CupList(cups)
for move in range(10_000_000):
    cl.move()

# Part 2 answer
print(cl.cups[1].next.value * cl.cups[1].next.next.value)