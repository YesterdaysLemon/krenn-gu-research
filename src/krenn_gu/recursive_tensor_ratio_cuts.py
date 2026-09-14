"""Four-coefficient ratio consistency for unrestricted coloured pair blocks.

Fix physical vertices a,b and their colours alpha,beta. Each other vertex i
and colour gamma gives the ratio W_ai(alpha,gamma)/W_bi(beta,gamma), when both
entries are nonzero. Distinct physical neighbours give complete four-vertex
hafnian identities. Same-neighbour colour slots have no direct four-fibre edge.
"""

from __future__ import annotations

import itertools


def add_tensor_ratio_consistency(instance, *, component_closure=False):
    """Append necessary phase constraints; return exact family/variable counts."""
    next_id = instance.cnf.nv
    counts = {"parity_variables": 0, "component_variables": 0,
              "parity_clauses": 0, "component_clauses": 0}

    def allocate():
        nonlocal next_id
        next_id += 1
        return next_id

    for a, b in itertools.combinations(range(instance.n), 2):
        slots = tuple((i, gamma) for i in range(instance.n) if i not in (a, b)
                      for gamma in range(3))
        for alpha, beta in itertools.product(range(3), repeat=2):
            parity = {slot: allocate() for slot in slots}
            counts["parity_variables"] += len(parity)
            connected = {}
            if component_closure:
                connected = {pair: allocate() for pair in itertools.combinations(slots, 2)}
                counts["component_variables"] += len(connected)
                for first, second, third in itertools.combinations(slots, 3):
                    u = connected[(first, second)]
                    v = connected[(first, third)]
                    w = connected[(second, third)]
                    instance.cnf.extend(([-u, -v, w], [-u, -w, v], [-v, -w, u]))
                    counts["component_clauses"] += 3
            for first, second in itertools.combinations(slots, 2):
                i, gamma = first
                j, delta = second
                if i == j:
                    continue
                colours = {a: alpha, b: beta, i: gamma, j: delta}
                vertices = tuple(sorted(colours))
                word = tuple(colours[v] for v in vertices)
                state = vertices, word
                result = instance.coefficients[state]
                third_product = instance.products[(state, (a, b))]
                cross = [instance.entry(a, i, alpha, gamma),
                         instance.entry(b, j, beta, delta),
                         instance.entry(a, j, alpha, delta),
                         instance.entry(b, i, beta, gamma)]
                guard = [-entry for entry in cross]
                p, q = parity[first], parity[second]
                # All cross entries live, s=0, third=0 implies opposite ratios.
                instance.cnf.extend(([*guard, result, third_product, p, q],
                                     [*guard, result, third_product, -p, -q]))
                counts["parity_clauses"] += 2
                if component_closure:
                    component = connected[(first, second)]
                    instance.cnf.append([*guard, result, third_product, component])
                    # Connected opposite ratios cancel the cross terms exactly:
                    # with nonzero cross entries, the result support equals third.
                    for opposite_guard in ((-p, q), (p, -q)):
                        instance.cnf.extend((
                            [*guard, -component, *opposite_guard, -result, third_product],
                            [*guard, -component, *opposite_guard, result, -third_product],
                        ))
                    counts["component_clauses"] += 5
    if instance.cnf.nv != next_id:
        raise AssertionError("unused ratio auxiliary variable")
    return counts
