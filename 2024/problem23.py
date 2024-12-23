edges_str = open("input23.txt").readlines()
edges = [tuple(sorted(x.strip().split("-"))) for x in edges_str]


def find_t_machines(edges):
    machines = set()
    for e1, e2 in edges:
        if e1.startswith("t"):
            machines.add(e1)
        if e2.startswith("t"):
            machines.add(e2)
    return machines


def find_all_connected(edges, match, choose):
    matched_machines = set()
    for e1, e2 in edges:
        if match(e1, e2):
            matched_machines.add(choose(e1, e2))
    return matched_machines


edges_set = set(edges)
three_tuples = set()
t_machines = find_t_machines(edges)
for machine in t_machines:
    d1_machines = find_all_connected(
        edges,
        lambda e1, e2: machine in (e1, e2),
        lambda e1, e2: e1 if e2 == machine else e2,
    )
    for machine1 in d1_machines:
        d2_machines = find_all_connected(
            edges,
            lambda e1, e2: machine1 in (e1, e2)
            and machine not in (e1, e2)
            and (
                (
                    machine1 == e1
                    and ((e2, machine) in edges_set or (machine, e2) in edges_set)
                )
                or (
                    machine1 == e2
                    and ((e1, machine) in edges_set or (machine, e1) in edges_set)
                )
            ),
            lambda e1, e2: e1 if e2 == machine1 else e2,
        )
        for machine2 in d2_machines:
            assert machine != machine1 and machine1 != machine2 and machine != machine2
            three_tuples.add(tuple(sorted([machine, machine1, machine2])))


print(len(three_tuples))

# Part 2

from collections import defaultdict

machines = set()
degrees = defaultdict(int)
machine_edges = defaultdict(set)
for e1, e2 in edges:
    machines.add(e1)
    machines.add(e2)
    degrees[e1] += 1
    degrees[e2] += 1
    machine_edges[e1].add(e2)
    machine_edges[e2].add(e1)

machines_by_degree = sorted(machines, key=lambda m: degrees[m], reverse=True)


def find_clique_with_machine(machine):
    clique = [machine]
    for m in machines_by_degree:
        if m == machine:
            continue
        if all((m, m2) in edges_set or (m2, m) in edges_set for m2 in clique):
            clique.append(m)
    return clique


max_clique = None

for m in machines_by_degree:
    clique = find_clique_with_machine(m)
    if not max_clique or len(clique) > len(max_clique):
        max_clique = clique


print(",".join(sorted(max_clique)))
