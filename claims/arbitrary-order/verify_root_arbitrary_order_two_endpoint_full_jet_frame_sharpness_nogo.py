"""Verify the exact two-endpoint full-root-jet sharpness construction."""

from __future__ import annotations

from collections import Counter
from functools import cache

import sympy as sp

P = 0
Q = 1
C = 2
E = tuple(sp.eye(3).col(i) for i in range(3))
X = sp.Matrix([1, 1, 1])
PHI = {
    P: E[P] - E[C],
    Q: E[Q] - E[C],
}


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def rank(rows: list[sp.Matrix]) -> int:
    return sp.Matrix.vstack(*(row.T for row in rows)).rank()


def permanent_count(matrix: list[list[int]]) -> int:
    size = len(matrix)
    totals = {0: 1}
    for row in matrix:
        updated = {}
        for mask, coefficient in totals.items():
            for column in range(size):
                if not (mask & (1 << column)) and row[column]:
                    new_mask = mask | (1 << column)
                    updated[new_mask] = updated.get(new_mask, 0) + coefficient * row[column]
        totals = updated
    return totals.get((1 << size) - 1, 0)


def build_case(r: int):
    m = r + 2
    roots = tuple(range(r))
    blockers = tuple(range(r, r + m))
    q0 = r + m
    q1 = q0 + 1
    vertices = roots + blockers + (q0, q1)
    blocks: dict[tuple[int, int], sp.Matrix] = {}
    active: dict[tuple[int, int], tuple[int, ...]] = {}

    def add_block(u: int, v: int, matrix: sp.Matrix) -> None:
        assert u != v
        assert (u, v) not in blocks and (v, u) not in blocks
        blocks[u, v] = matrix
        blocks[v, u] = matrix.T

    def add_active(u: int, v: int, colour: int, variable_vertices: tuple[int, ...]) -> None:
        edge = tuple(sorted((u, v)))
        assert edge not in active
        active[edge] = tuple(colour for _ in variable_vertices)

    # Projectively constant root--blocker rows with full span at every root.
    for i, root in enumerate(roots):
        for u, blocker in enumerate(blockers):
            h = E[(i + u) % 3]
            add_block(root, blocker, outer(E[C], h))

    def add_root_root(i: int, colour: int) -> None:
        u, v = roots[i], roots[i + 1]
        matrix = outer(PHI[colour], PHI[colour])
        if colour == P:
            matrix += outer(PHI[P], E[C]) + outer(E[C], PHI[P])
        add_block(u, v, matrix)
        add_active(u, v, colour, (u, v))

    def add_root_endpoint(root: int, endpoint: int, colour: int) -> None:
        add_block(root, endpoint, outer(PHI[colour], E[C]))
        add_active(root, endpoint, colour, (root,))

    def add_blocker_blocker(i: int, colour: int) -> None:
        u, v = blockers[i], blockers[i + 1]
        add_block(u, v, outer(E[colour], E[colour]))
        add_active(u, v, colour, (u, v))

    def add_blocker_endpoint(blocker: int, endpoint: int, colour: int) -> None:
        add_block(blocker, endpoint, outer(E[colour], E[C]))
        add_active(blocker, endpoint, colour, (blocker,))

    if r % 2:
        for i in range(r - 1):
            add_root_root(i, Q if i % 2 == 0 else P)
        add_root_endpoint(roots[0], q0, P)
        add_root_endpoint(roots[-1], q1, Q)

        for i in range(m - 1):
            add_blocker_blocker(i, Q if i % 2 == 0 else P)
        add_blocker_endpoint(blockers[0], q1, P)
        add_blocker_endpoint(blockers[-1], q0, Q)
    else:
        for i in range(r - 1):
            add_root_root(i, P if i % 2 == 0 else Q)
        add_root_endpoint(roots[0], q0, Q)
        add_root_endpoint(roots[-1], q1, Q)

        for i in range(m - 1):
            add_blocker_blocker(i, Q if i % 2 == 0 else P)
        add_blocker_endpoint(blockers[0], q0, P)
        add_blocker_endpoint(blockers[-1], q1, P)

    return roots, blockers, (q0, q1), vertices, blocks, active


def perfect_matchings(vertices: tuple[int, ...], active: dict[tuple[int, int], tuple[int, ...]]):
    index = {vertex: i for i, vertex in enumerate(vertices)}
    neighbours = {vertex: [] for vertex in vertices}
    for edge in active:
        u, v = edge
        neighbours[u].append(v)
        neighbours[v].append(u)

    @cache
    def recurse(mask: int):
        if mask == 0:
            return ((),)
        low_bit = mask & -mask
        i = low_bit.bit_length() - 1
        u = vertices[i]
        tail = mask ^ low_bit
        result = []
        for v in neighbours[u]:
            bit = 1 << index[v]
            if tail & bit:
                edge = tuple(sorted((u, v)))
                for rest in recurse(tail ^ bit):
                    result.append((edge,) + rest)
        return tuple(result)

    return recurse((1 << len(vertices)) - 1)


def signature(
    matching: tuple[tuple[int, int], ...],
    roots: tuple[int, ...],
    blockers: tuple[int, ...],
    active: dict[tuple[int, int], tuple[int, ...]],
) -> tuple[int, ...]:
    variables = roots + blockers
    positions = {vertex: i for i, vertex in enumerate(variables)}
    word = [-1] * len(variables)
    for edge in matching:
        colour = active[edge][0]
        for vertex in edge:
            if vertex in positions:
                assert word[positions[vertex]] == -1
                word[positions[vertex]] = colour
    assert -1 not in word
    return tuple(word)


def verify_case(r: int) -> dict[str, object]:
    roots, blockers, endpoints, vertices, blocks, active = build_case(r)
    q0, q1 = endpoints
    m = len(blockers)
    zero = sp.zeros(3)

    def block(u: int, v: int) -> sp.Matrix:
        return blocks.get((u, v), zero)

    # The edge system is a legal loopless symmetric block graph.
    for (u, v), matrix in blocks.items():
        assert u != v
        assert block(v, u) == matrix.T

    # Fully supported, pairwise-zero roots.
    assert all(value != 0 for value in X)
    for i, u in enumerate(roots):
        for v in roots[i + 1 :]:
            assert (X.T * block(u, v) * X)[0] == 0

    # Projective constancy and full common-row span.
    for i, root in enumerate(roots):
        rows = []
        for u, blocker in enumerate(blockers):
            h = E[(i + u) % 3]
            matrix = block(root, blocker)
            assert X.T * matrix == h.T
            assert matrix == outer(E[C], h)
            assert E[P].T * matrix == sp.zeros(1, 3)
            assert E[Q].T * matrix == sp.zeros(1, 3)
            rows.append(h)
        assert rank(rows) == 3

    # Both endpoints are genuine nonblockers at the root slice and effective
    # on the tangent plane.
    for endpoint in endpoints:
        assert all(X.T * block(root, endpoint) == sp.zeros(1, 3) for root in roots)
        tangent_rows = [E[P].T * block(root, endpoint) for root in roots]
        tangent_rows += [E[Q].T * block(root, endpoint) for root in roots]
        assert any(row != sp.zeros(1, 3) for row in tangent_rows)

    # The two incident companion classes at every root span x^perp, while the
    # scalar row a supplies the third dual direction.
    active_colours_by_root = {root: set() for root in roots}
    for edge in active:
        for root in roots:
            if root in edge:
                active_colours_by_root[root].add(active[edge][0])
    for root in roots:
        assert active_colours_by_root[root] == {P, Q}
        assert rank([PHI[P], PHI[Q]]) == 2
        assert (PHI[P].T * X)[0] == (PHI[Q].T * X)[0] == 0
        assert rank([E[C], PHI[P], PHI[Q]]) == 3

    # The stabilized p matching saturates every lower root subset.  On a
    # split root pair, its one-tangent contraction against the fixed partner
    # is nonzero; on an internal pair, its S x S restriction is nonzero.
    p_root_pairs = []
    if r % 2:
        p_endpoint_root = roots[0]
        assert (E[P].T * block(p_endpoint_root, q0) * X)[0] == 1
        p_root_pairs = [(roots[i], roots[i + 1]) for i in range(1, r - 1, 2)]
    else:
        p_endpoint_root = None
        p_root_pairs = [(roots[i], roots[i + 1]) for i in range(0, r - 1, 2)]
    assert len(p_root_pairs) * 2 + int(p_endpoint_root is not None) == r
    for u, v in p_root_pairs:
        assert (E[P].T * block(u, v) * E[P])[0] == 1
        assert (E[P].T * block(u, v) * X)[0] == 1
        assert (X.T * block(u, v) * E[P])[0] == 1
    for subset_mask in range(1 << r):
        subset = {roots[i] for i in range(r) if subset_mask & (1 << i)}
        saturated = set()
        used_partners = set()
        if p_endpoint_root is not None and p_endpoint_root in subset:
            saturated.add(p_endpoint_root)
            used_partners.add(q0)
        for u, v in p_root_pairs:
            if u in subset:
                saturated.add(u)
                used_partners.add(v)
            if v in subset:
                saturated.add(v)
                used_partners.add(u)
        assert saturated == subset
        assert len(used_partners) == len(subset)

    # The fixed-root slice has an explicit nonzero mixed blocker word.  Both
    # endpoints are forced to their unique blocker neighbours, and the roots
    # biject with local blocker indices 1..r.
    base_word = [-1] * m
    if r % 2:
        base_word[0], base_word[-1] = P, Q
    else:
        base_word[0] = base_word[-1] = P
    for i in range(r):
        local_u = i + 1
        base_word[local_u] = (i + local_u) % 3
    assert -1 not in base_word and len(set(base_word)) > 1
    base_matrix = [
        [int(base_word[local_u] == (i + local_u) % 3) for local_u in range(1, r + 1)]
        for i in range(r)
    ]
    mixed_coefficient = permanent_count(base_matrix)
    assert mixed_coefficient >= 1

    matchings = perfect_matchings(vertices, active)
    signatures = Counter(signature(item, roots, blockers, active) for item in matchings)
    expected = {
        (P,) * (r + m): 1,
        (Q,) * (r + m): 1,
    }
    assert signatures == expected

    classes = {}
    for matching in matchings:
        word = signature(matching, roots, blockers, active)
        root_used = frozenset(
            endpoint
            for endpoint in endpoints
            if any(endpoint in edge and (set(edge) & set(roots)) for edge in matching)
        )
        assert len(root_used) % 2 == r % 2
        root_word = word[:r]
        blocker_word = word[r:]
        assert len(set(root_word)) == len(set(blocker_word)) == 1
        assert root_word[0] == blocker_word[0]
        classes[root_used] = (root_word, blocker_word)

    if r % 2:
        assert classes == {
            frozenset({q0}): ((P,) * r, (P,) * m),
            frozenset({q1}): ((Q,) * r, (Q,) * m),
        }
    else:
        assert classes == {
            frozenset(): ((P,) * r, (P,) * m),
            frozenset({q0, q1}): ((Q,) * r, (Q,) * m),
        }

    return {
        "r": r,
        "m": m,
        "parity": "odd" if r % 2 else "even",
        "active_edges": len(active),
        "restricted_matchings": len(matchings),
        "cofactor_classes": len(classes),
        "saturated_subsets": 1 << r,
        "base_mixed_coefficient": mixed_coefficient,
    }


def main() -> None:
    rows = [verify_case(r) for r in range(2, 13)]
    assert {row["parity"] for row in rows} == {"even", "odd"}
    assert all(row["restricted_matchings"] == 2 for row in rows)
    assert all(row["cofactor_classes"] == 2 for row in rows)
    assert all(row["saturated_subsets"] == 1 << row["r"] for row in rows)
    assert all(row["base_mixed_coefficient"] >= 1 for row in rows)
    print("PASS: exact legal two-endpoint full-root-jet frames are sharp")
    print(f"checked root counts: {rows[0]['r']}..{rows[-1]['r']}")
    print("restricted matching count per case: 2")
    print("root-row rank per case: 3")
    print("all root subsets matching-saturated: yes")
    print("undifferentiated mixed coefficient: positive")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
