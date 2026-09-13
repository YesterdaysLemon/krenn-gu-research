"""Necessary support consistency of all Laplace expansions of one coefficient.

Writing t_uv = W_uv * h_(A-uv), every vertex equation is sum_u t_uv = h_A.
For any integer potential y, sum_(uv) (y_u+y_v)t_uv = sum_v y_v h_A.
The routines below only detect a single surviving term in this exact identity.
They do not assert that feasible independent t values come from source weights.
"""

from __future__ import annotations

from itertools import combinations, product


def bipartite_component_potentials(n, edges):
    neighbours = [set() for _ in range(n)]
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    seen = set()
    for root in range(n):
        if root in seen:
            continue
        signs, todo, bipartite = {root: 1}, [root], True
        seen.add(root)
        while todo:
            u = todo.pop()
            for v in sorted(neighbours[u]):
                if v in signs:
                    if signs[v] == signs[u]:
                        bipartite = False
                else:
                    signs[v] = -signs[u]
                    seen.add(v)
                    todo.append(v)
        if bipartite:
            yield tuple(signs.get(v, 0) for v in range(n))


def find_incidence_obstruction(n, edges, result_nonzero):
    """Discover a signed row-sum certificate; None is not weight realization."""
    edges = tuple(sorted(edges))
    if result_nonzero:
        for potential in bipartite_component_potentials(n, edges):
            if sum(potential):
                return {"kind": "nonzero_result", "potential": potential}
    for selected in edges:
        for potential in bipartite_component_potentials(n, [e for e in edges if e != selected]):
            u, v = selected
            if potential[u] + potential[v] and (not result_nonzero or sum(potential) == 0):
                return {"kind": "nonzero_term", "edge": selected, "potential": potential}
    return None


def verify_incidence_obstruction(n, edges, result_nonzero, certificate):
    """Check the displayed integer identity without graph search or elimination."""
    try:
        if type(n) is not int or n < 1 or type(result_nonzero) is not bool:
            return False
        edges = tuple(tuple(edge) for edge in edges)
        if len(set(edges)) != len(edges) or any(
            len(edge) != 2 or any(type(v) is not int for v in edge)
            or not 0 <= edge[0] < edge[1] < n for edge in edges
        ):
            return False
        potential = tuple(certificate["potential"])
        if len(potential) != n or any(type(v) is not int for v in potential):
            return False
        surviving = [edge for edge in edges if potential[edge[0]] + potential[edge[1]]]
        if certificate["kind"] == "nonzero_result":
            return result_nonzero and sum(potential) != 0 and not surviving
        if certificate["kind"] == "nonzero_term":
            selected = tuple(certificate["edge"])
            return (len(selected) == 2 and all(type(v) is int for v in selected)
                    and surviving == [selected] and (not result_nonzero or sum(potential) == 0))
        return False
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def incidence_identity_cuts(result, products, potential):
    """Necessary CNF clauses for one displayed signed vertex sum.

    products maps local unordered pairs to truthful nonzero t indicators.
    Only nonzero coefficients matter to the no-singleton rule, not their signs.
    """
    terms = [variable for (u, v), variable in sorted(products.items()) if potential[u] + potential[v]]
    if sum(potential):
        yield [-result, *terms]
    for index, variable in enumerate(terms):
        yield [-variable, *([result] if sum(potential) else []), *terms[:index], *terms[index+1:]]


def add_diagonal_incidence_cuts(instance, *, full_balance=True, pair_differences=True):
    """Bounded family: all pair differences; full-set unbalanced accessibility.

    The full-set family uses only the nonzero-result clause. Generating every
    no-singleton clause for every potential would be much larger. Every emitted
    clause is separately justified by the displayed integer row-sum identity.
    """
    counts = {"pair_differences": 0, "full_balance": 0}
    for (colour, subset), result in instance.hafnian_variables.items():
        vertices = tuple(sorted(subset))
        positions = {v: i for i, v in enumerate(vertices)}
        products = {(positions[u], positions[v]): instance.product_variables[(colour, subset, (u, v))]
                    for u, v in combinations(vertices, 2)}
        if pair_differences:
            for u, v in combinations(range(len(vertices)), 2):
                potential = tuple(1 if i == u else -1 if i == v else 0 for i in range(len(vertices)))
                for clause in incidence_identity_cuts(result, products, potential):
                    instance.cnf.append(clause)
                    counts["pair_differences"] += 1
        if full_balance and len(subset) == instance.n:
            for potential in product((-1, 0, 1), repeat=instance.n):
                if not sum(potential) or 1 not in potential or -1 not in potential:
                    continue
                # One representative of y and -y, which have identical clauses.
                if next(value for value in potential if value) < 0:
                    continue
                terms = [variable for (u, v), variable in products.items() if potential[u] + potential[v]]
                instance.cnf.append([-result, *terms])
                counts["full_balance"] += 1
    return counts
