from collections import defaultdict

list1 = []
list2 = []

counts2 = defaultdict(int)

for line in open("input1.txt").readlines():
    n1, n2 = line.strip().split("   ")
    list1.append(int(n1))
    list2.append(int(n2))
    counts2[int(n2)] += 1

list1.sort()
list2.sort()

distances = 0
similarity = 0

for i in range(len(list1)):
    distances += abs(int(list1[i]) - int(list2[i]))
    n1 = list1[i]
    if n1 in counts2:
        similarity += n1 * counts2[n1]

print(distances)
print(similarity)