"""Sound complete-fibre signed cuts for the recursive hafnian relaxation.

The first cut is the three-binomial obstruction on a 2-by-3 bipartite
patch.  It retains an escape literal for every possible third monomial.
This is a necessary condition for complex weights, not a realizability test.
"""

from __future__ import annotations

from itertools import combinations

from krenn_gu.recursive_hafnian_support import RecursiveHafnianSupportInstance


def two_by_three_hafnian_cuts(instance: RecursiveHafnianSupportInstance):
    """Yield guarded odd signed-circuit clauses for every colour and patch.

    With nonzero x_i=g(a,i), y_i=g(b,i), and zero third matching
    g(a,b)*g(i,j), a zero h(a,b,i,j) implies x_i*y_j+x_j*y_i=0.
    Three such equations on i,j,k are inconsistent over C.  A support may
    escape by losing a cross edge, making a hafnian nonzero, or activating
    a third monomial.  The last option is essential for soundness.
    """

    vertices = tuple(range(instance.n))
    for colour in range(3):
        for a, b in combinations(vertices, 2):
            outside = tuple(vertex for vertex in vertices if vertex not in (a, b))
            for triple in combinations(outside, 3):
                clause = [
                    -instance.edge_variables[(colour, tuple(sorted((left, right))))]
                    for left in (a, b)
                    for right in triple
                ]
                for i, j in combinations(triple, 2):
                    subset = frozenset((a, b, i, j))
                    clause.append(instance.hafnian_variables[(colour, subset)])
                    clause.append(instance.product_variables[(colour, subset, (a, b))])
                yield clause


def add_two_by_three_hafnian_cuts(instance: RecursiveHafnianSupportInstance) -> int:
    count = 0
    for clause in two_by_three_hafnian_cuts(instance):
        instance.cnf.append(clause)
        count += 1
    return count


def add_common_neighbor_parity_cuts(instance: RecursiveHafnianSupportInstance) -> int:
    """Forbid every odd cycle in each guarded common-neighbour ratio graph.

    For fixed c,a,b, every common neighbour i has ratio r_i=Z_ai/Z_bi.
    A zero four-hafnian with no third term forces r_i=-r_j.  Such forced
    edges form a bipartite graph.  Existential parity bits encode exactly
    this graph condition, including odd cycles longer than triangles.

    This parity argument is sound for these particular primitive ratio
    equations.  It does not replace integer-lattice analysis for arbitrary
    matching-monomial equations (e.g. x^2=-1 is perfectly consistent).
    """

    vertices = tuple(range(instance.n))
    count = 0
    for colour in range(3):
        for a, b in combinations(vertices, 2):
            outside = tuple(vertex for vertex in vertices if vertex not in (a, b))
            parity = {
                i: instance.pool.id(("ratio-parity", colour, (a, b), i))
                for i in outside
            }
            for i, j in combinations(outside, 2):
                subset = frozenset((a, b, i, j))
                guards = [
                    -instance.edge_variables[(colour, tuple(sorted((left, right))))]
                    for left in (a, b)
                    for right in (i, j)
                ]
                guards.extend((
                    instance.hafnian_variables[(colour, subset)],
                    instance.product_variables[(colour, subset, (a, b))],
                ))
                instance.cnf.append([*guards, parity[i], parity[j]])
                instance.cnf.append([*guards, -parity[i], -parity[j]])
                count += 2
    return count
