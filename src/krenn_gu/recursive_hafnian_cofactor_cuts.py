"""Redundant four-cofactor cuts justified by the global colour equations.

Unlike the one-colour signed cuts, these require the GHZ mixed-word zeros.
They follow already from AP' forcing and its two-/three-colour partition
conditions, so they accelerate the model without strengthening its scope.
"""

from itertools import combinations, product

from krenn_gu.recursive_hafnian_support import RecursiveHafnianSupportInstance


def add_four_cofactor_coverage_cuts(instance: RecursiveHafnianSupportInstance) -> int:
    """A live (n-4)-cofactor forbids matchability in both other colours."""

    if instance.n < 6:
        return 0
    whole = frozenset(range(instance.n))
    count = 0
    for vertices in combinations(range(instance.n), 4):
        a, b, i, j = vertices
        matchings = (((a, b), (i, j)), ((a, i), (b, j)), ((a, j), (b, i)))
        for colour in range(3):
            d, e = (other for other in range(3) if other != colour)
            cofactor = instance.hafnian_literal(colour, whole - set(vertices))
            assert cofactor is not None
            for first, second in product(matchings, repeat=2):
                instance.cnf.append([
                    -cofactor,
                    *(-instance.edge_variables[(d, edge)] for edge in first),
                    *(-instance.edge_variables[(e, edge)] for edge in second),
                ])
                count += 1
    return count
