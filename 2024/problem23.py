from collections import defaultdict

edges_str = open("input23.txt").readlines()
edges = set(tuple(sorted(x.strip().split("-"))) for x in edges_str)

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


def find_3_cliques(machines, edges):
    t_edges = {(e1, e2) for e1, e2 in edges if e1.startswith("t") or e2.startswith("t")}
    return {
        tuple(sorted(c + (m,)))
        for c in t_edges
        for m in (m for m in machines if m not in c and degrees[m] >= 2)
        if all((m, m2) in edges or (m2, m) in edges for m2 in c)
    }


machines_by_degree = sorted(machines, key=lambda m: degrees[m], reverse=True)


def find_clique_with_machine(machine):
    clique = [machine]
    for m in machines_by_degree:
        if m == machine:
            continue
        if degrees[m] < len(clique):
            break
        if all((m, m2) in edges or (m2, m) in edges for m2 in clique):
            clique.append(m)
    return clique


max_clique = None
for m in machines_by_degree:
    if max_clique and degrees[m] < len(max_clique):
        break

    clique = find_clique_with_machine(m)
    if not max_clique or len(clique) > len(max_clique):
        max_clique = clique


# Part 1
print(len(find_3_cliques(machines, edges)))


# Part 2
print(",".join(sorted(max_clique)))
