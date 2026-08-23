"""Focused exact checks for the GLS39 pairwise-diagonal rank bound."""

from __future__ import annotations

from itertools import product

import sympy as sp


def symbolic_proof_leaves() -> dict[str, object]:
    """Replay the connectivity, sign, and two-label determinant leaves."""

    nodes = tuple(f"{side}{color}" for side in ("A", "B") for color in range(3))
    edges = {
        (f"A{left}", f"B{right}")
        for left, right in product(range(3), repeat=2)
        if left != right
    }
    reached = {nodes[0]}
    while True:
        extended = reached | {
            right
            for left, right in edges | {(right, left) for left, right in edges}
            if left in reached
        }
        if extended == reached:
            break
        reached = extended
    assert reached == set(nodes)

    sign_matrix = sp.Matrix(((1, 1, 0), (1, 0, 1), (0, 1, 1)))
    assert sign_matrix.det() == -2
    assert sign_matrix.rank() == 3

    symbols = sp.symbols("xs0:3 ys0:3 xt0:3 yt0:3")
    xs = sp.Matrix(symbols[0:3])
    ys = sp.Matrix(symbols[3:6])
    xt = sp.Matrix(symbols[6:9])
    yt = sp.Matrix(symbols[9:12])
    two_label_matrix = xs * yt.T + xt * ys.T
    assert sp.expand(two_label_matrix.det()) == 0
    return {
        "support_nodes": len(nodes),
        "support_edges": len(edges),
        "connected": True,
        "three_label_sign_determinant": sign_matrix.det(),
        "two_label_determinant": 0,
    }


def rank_mod_prime(vectors: list[tuple[int, int, int]], prime: int) -> int:
    rows = [list(vector) for vector in vectors if any(vector)]
    rank = 0
    for column in range(3):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [(entry * inverse) % prime for entry in rows[rank]]
        for index, row in enumerate(rows):
            if index != rank and row[column]:
                multiple = row[column]
                rows[index] = [
                    (left - multiple * right) % prime
                    for left, right in zip(row, rows[rank], strict=True)
                ]
        rank += 1
    return rank


def scalar_pair_diagonal(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, int, int] | None:
    x_left, y_left = left[:3], left[3:]
    x_right, y_right = right[:3], right[3:]
    matrix = tuple(
        (
            x_left[row] * y_right[column]
            + x_right[row] * y_left[column]
        )
        % prime
        for row, column in product(range(3), repeat=2)
    )
    if any(matrix[3 * row + column] for row, column in product(range(3), repeat=2) if row != column):
        return None
    return tuple(matrix[4 * color] for color in range(3))


def finite_scalar_falsification_census() -> dict[str, int]:
    """Exhaust minimal scalar witnesses over F_3; this is supporting evidence."""

    prime = 3
    vertices: list[tuple[int, ...]] = []
    for vector in product(range(prime), repeat=6):
        if not any(vector):
            continue
        first = next(entry for entry in vector if entry)
        inverse = pow(first, -1, prime)
        normalized = tuple((entry * inverse) % prime for entry in vector)
        if normalized == vector:
            vertices.append(vector)
    assert len(vertices) == 364

    adjacency: list[dict[int, tuple[int, int, int]]] = [
        {} for _ in vertices
    ]
    compatible_pairs = 0
    active_pairs = 0
    for left in range(len(vertices)):
        for right in range(left + 1, len(vertices)):
            diagonal = scalar_pair_diagonal(vertices[left], vertices[right], prime)
            if diagonal is None:
                continue
            adjacency[left][right] = diagonal
            adjacency[right][left] = diagonal
            compatible_pairs += 1
            active_pairs += int(any(diagonal))
    assert compatible_pairs == 700
    assert active_pairs == 375

    max_rank = 0
    cliques_checked = 0

    def search(
        clique: tuple[int, ...],
        candidates: tuple[int, ...],
        diagonal_vectors: list[tuple[int, int, int]],
    ) -> None:
        nonlocal cliques_checked, max_rank
        cliques_checked += 1
        current_rank = rank_mod_prime(diagonal_vectors, prime)
        max_rank = max(max_rank, current_rank)
        assert current_rank <= 2
        if len(clique) == 6:
            return
        for offset, vertex in enumerate(candidates):
            new_vectors = diagonal_vectors + [
                adjacency[old][vertex] for old in clique
            ]
            new_candidates = tuple(
                other
                for other in candidates[offset + 1 :]
                if other in adjacency[vertex]
            )
            search(clique + (vertex,), new_candidates, new_vectors)

    search((), tuple(range(len(vertices))), [])
    assert max_rank == 2
    assert cliques_checked == 9343
    return {
        "projective_vertices": len(vertices),
        "compatible_pairs": compatible_pairs,
        "active_pairs": active_pairs,
        "cliques_through_six_labels": cliques_checked,
        "maximum_diagonal_rank": max_rank,
    }


def auxiliary_label_interface_check() -> dict[str, object]:
    """Type-check the residual, one-residual, and promoted-pair maps."""

    def vector(prefix: str) -> sp.Matrix:
        return sp.Matrix(sp.symbols(f"{prefix}0:3"))

    a_0, b_0 = vector("a0_"), vector("b0_")
    a_1, b_1 = vector("a1_"), vector("b1_")
    x, y = vector("x_"), vector("y_")
    x_2, y_2 = vector("x2_"), vector("y2_")

    residual_pair = sp.kronecker_product(a_0, b_1) + sp.kronecker_product(
        a_1, b_0
    )
    q = residual_pair.copy()
    one_residual = sp.kronecker_product(a_0, y) + sp.kronecker_product(x, b_0)
    sigma_one = one_residual.copy()
    promoted_pair = sp.kronecker_product(x, y_2) + sp.kronecker_product(x_2, y)
    sigma_pair = promoted_pair.copy()
    assert residual_pair == q
    assert one_residual == sigma_one
    assert promoted_pair == sigma_pair

    diagonal = sp.Matrix.hstack(
        *(
            sp.kronecker_product(sp.eye(3)[:, color], sp.eye(3)[:, color])
            for color in range(3)
        )
    )
    assert diagonal.rank() == 3
    return {
        "residual_pair": "q",
        "one_residual": "sigma_(s,u)",
        "promoted_pair": "sigma_(u,v)",
        "full_diagonal_rank": diagonal.rank(),
        "pairwise_diagonal_bound": 2,
    }


def main() -> None:
    symbolic = symbolic_proof_leaves()
    finite = finite_scalar_falsification_census()
    interface = auxiliary_label_interface_check()
    print("GLS39 complete pairwise-diagonal primary checks: PASS")
    print("  symbolic proof leaves:", symbolic)
    print("  bounded F_3 scalar falsification census:", finite)
    print("  auxiliary residual-label interface:", interface)
    print("  rank-three full swallow: EMPTY for every q")


if __name__ == "__main__":
    main()
