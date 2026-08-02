"""Verify the exact symmetric-graph lift of the four-row selector seed.

This is deliberately a contraction theorem, not a Question-1 construction.
Six of the eight graph modes are fixed.  The two constant selector columns
come from two of those fixed (herald) modes.
"""

from __future__ import annotations

import itertools
import json
from functools import cache
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def permanent(matrix: sp.Matrix) -> sp.Expr:
    """Small exact permanent by permutations."""
    n = matrix.rows
    assert matrix.cols == n
    return sp.expand(
        sum(
            sp.prod(matrix[i, permutation[i]] for i in range(n))
            for permutation in itertools.permutations(range(n))
        )
    )


def hafnian(matrix: sp.Matrix) -> sp.Expr:
    """Small exact hafnian by a memoized matching recurrence."""
    n = matrix.rows
    assert matrix.cols == n and n % 2 == 0

    @cache
    def recurse(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        total = sp.Integer(0)
        for position in range(1, len(vertices)):
            second = vertices[position]
            rest = vertices[1:position] + vertices[position + 1 :]
            total += matrix[first, second] * recurse(rest)
        return sp.expand(total)

    return recurse(tuple(range(n)))


def main() -> None:
    u, v, w, z, p, q, r, s = sp.symbols("u v w z p q r s")
    selector = sp.Matrix(
        [
            [u, v, 1, 1],
            [w, z, 1, 1],
            [p, q, 2, -2],
            [r, s, 2, -2],
        ]
    )
    zero = sp.zeros(4)
    adjacency = zero.row_join(selector).col_join(selector.T.row_join(zero))

    assert adjacency == adjacency.T
    assert all(adjacency[i, i] == 0 for i in range(8))

    permanent_value = permanent(selector)
    hafnian_value = hafnian(adjacency)
    expected = sp.expand(-8 * (u * z + v * w) + 2 * (p * s + q * r))
    assert sp.expand(permanent_value - expected) == 0
    assert sp.expand(hafnian_value - expected) == 0

    # There are 105 matchings on eight vertices.  Exactly the 4! bipartite
    # matchings survive in the block-off-diagonal graph.
    def matching_terms(vertices: tuple[int, ...]) -> list[sp.Expr]:
        if not vertices:
            return [sp.Integer(1)]
        first = vertices[0]
        terms: list[sp.Expr] = []
        for position in range(1, len(vertices)):
            second = vertices[position]
            rest = vertices[1:position] + vertices[position + 1 :]
            terms.extend(
                adjacency[first, second] * term for term in matching_terms(rest)
            )
        return terms

    terms = matching_terms(tuple(range(8)))
    assert len(terms) == 105
    assert sum(term != 0 for term in terms) == 24

    # A legal d=4 coloured-edge realization.  Left modes are fixed to e0.
    # The first two right modes are variable; the last two are heralds fixed
    # to e0.  Edge-block transposition supplies the opposite orientation.
    e0 = sp.Matrix([1, 0, 0, 0])
    right_vectors = (
        sp.Matrix([u, w, p, r]),
        sp.Matrix([v, z, q, s]),
        e0,
        e0,
    )
    constant_columns = (
        sp.Matrix([1, 1, 2, 2]),
        sp.Matrix([1, 1, -2, -2]),
    )
    edge_blocks: dict[tuple[int, int], sp.Matrix] = {}
    evaluated = sp.zeros(4)
    for left in range(4):
        for right in range(4):
            block = sp.zeros(4)
            if right < 2:
                block[0, left] = 1
            else:
                block[0, 0] = constant_columns[right - 2][left]
            edge_blocks[(left, 4 + right)] = block
            edge_blocks[(4 + right, left)] = block.T
            evaluated[left, right] = (e0.T * block * right_vectors[right])[0]

    assert evaluated == selector
    for (left, right), block in edge_blocks.items():
        assert edge_blocks[(right, left)] == block.T

    # If the two constant modes are merely uncontracted in this same lift,
    # their local maps have rank one.  Therefore this direct herald removal
    # cannot yield a concise diagonal tensor of rank at least two.
    maps = [sp.eye(4), sp.eye(4)]
    for column in constant_columns:
        local_map = column * e0.T
        assert local_map.rank() == 1
        maps.append(local_map)
    assert [local_map.rank() for local_map in maps] == [4, 4, 1, 1]

    output = {
        "status": "exact_symmetric_hafnian_lift_verified",
        "scope": "eight-vertex d=4 bipartite graph with six fixed modes",
        "matching_count": len(terms),
        "nonzero_bipartite_matching_count": sum(term != 0 for term in terms),
        "hafnian": str(hafnian_value),
        "selector_identity": str(expected),
        "right_mode_map_ranks_before_herald_contraction": [4, 4, 1, 1],
        "proved": [
            "the seed permanent is the hafnian of a loopless symmetric block matrix",
            "all 105 full graph matchings were included and exactly 24 survive",
            "the constant columns arise from legal fixed d=4 graph modes",
            "the direct uncontracting of those constant modes has flattening rank one",
        ],
        "not_proved": [
            "compatibility with the fixed Question-2 module support",
            "removal of all herald contractions",
            "a Question-1 counterexample",
            "the global Krenn-Gu conjecture",
        ],
    }
    destination = (
        ROOT / "tmp" / "root_of_unity_selector_symmetric_hafnian_lift_verified.json"
    )
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
