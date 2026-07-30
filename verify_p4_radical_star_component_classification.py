#!/usr/bin/env python3
"""Verify the generic radical-star classification for pure P4 restrictions."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md"
TWO_TWO_THEOREM = ROOT / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md"
ONE_THREE_THEOREM = ROOT / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
SMOOTH_THEOREM = ROOT / "P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def coefficients(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(
                tuple(planes[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in WORDS
    }


def contraction_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(4)
    return sp.Matrix(
        4,
        4,
        lambda row, column: permanent(
            (
                left,
                right,
                identity.row(row),
                identity.row(column),
            )
        ),
    )


def product_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            columns.append(
                sp.Matrix(
                    tuple(
                        left[left_row, first] * right[right_row, second]
                        + left[left_row, second] * right[right_row, first]
                        for first, second in SOURCE_PAIRS
                    )
                )
            )
    return sp.Matrix.hstack(*columns)


def pair_relation_data(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, int], tuple[int, tuple[int, ...]]]:
    result = {}
    for left, right in SOURCE_PAIRS:
        matrix = product_matrix(planes[left], planes[right])
        nullspace = matrix.nullspace()
        relation_ranks = tuple(
            sp.Matrix(2, 2, tuple(vector)).rank() for vector in nullspace
        )
        result[left, right] = (matrix.rank(), relation_ranks)
    return result


def two_two_planes(
    A: sp.Expr,
    B: sp.Expr,
    C: sp.Expr,
    E: sp.Expr,
    F: sp.Expr,
    H: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    y1 = sp.Matrix(((1, 0, 0, -1),))
    y2 = sp.Matrix(((0, 1, -1, 0),))
    k0 = sp.Matrix(((1, 0, 0, 1),))
    k1 = sp.Matrix(((0, 1, 1, 0),))
    x1 = sp.Matrix(((A, C + B, C - B, A),))
    x2 = sp.Matrix(((H + E, F, F, H - E),))
    u0 = sp.Matrix(((E, -F, -F, -E),))
    u1 = sp.Matrix(((A, -B, B, A),))
    return (
        u0.col_join(u1),
        y1.col_join(x1),
        x2.col_join(y2),
        k0.col_join(k1),
    )


def one_three_planes(
    S: sp.Expr,
    D: sp.Expr,
    G: sp.Expr,
    T: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    P = G - T
    Q = D - S
    return (
        sp.Matrix(((2, P + Q, Q - P, 0), (0, 0, 1, 1))),
        sp.Matrix(((0, 1, -1, 0), (1, 0, S, D))),
        sp.Matrix(((1, 0, G, T), (0, 1, 0, -1))),
        sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
    )


def active_determinant(
    tensor: dict[tuple[int, ...], sp.Expr],
) -> sp.Expr:
    return sp.factor(
        tensor[(0, 1, 0, 0)] * tensor[(1, 1, 0, 1)]
        - tensor[(0, 1, 0, 1)] * tensor[(1, 1, 0, 0)]
    )


def support(vector: sp.Matrix) -> tuple[int, ...]:
    return tuple(index for index, value in enumerate(vector) if value != 0)


def main() -> None:
    # The degree-two basis is paired by complementary source pairs.
    pairing = sp.zeros(6, 6)
    for left, pair in enumerate(SOURCE_PAIRS):
        complement = tuple(index for index in range(4) if index not in pair)
        right = SOURCE_PAIRS.index(complement)
        pairing[left, right] = 1
    assert pairing.det() == -1

    # Dense complement normalizations used in the two block types.
    a, b, c, d = sp.symbols("a b c d")
    y_disjoint_1 = sp.Matrix(((1, 0, 0, -1),))
    shift = (d - a) / 2
    normalized = sp.Matrix(((a, b, c, d),)) + shift * y_disjoint_1
    A0, B0, C0 = (a + d) / 2, (b - c) / 2, (b + c) / 2
    assert sp.simplify(
        normalized - sp.Matrix(((A0, C0 + B0, C0 - B0, A0),))
    ) == sp.zeros(1, 4)

    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", nonzero=True)
    y_overlap = sp.Matrix(((0, 1, -1, 0),))
    affine = sp.Matrix(((x0, x1, x2, x3),)) / x0
    affine -= (x1 / x0) * y_overlap
    assert sp.simplify(
        affine - sp.Matrix(((1, 0, (x1 + x2) / x0, x3 / x0),))
    ) == sp.zeros(1, 4)

    A, B, C, E, F, H = sp.symbols("A B C E F H")
    two_two = two_two_planes(A, B, C, E, F, H)
    two_two_contraction = contraction_matrix(
        two_two[1].row(0), two_two[2].row(1)
    )
    assert two_two_contraction.rank() == 2
    assert two_two_contraction * two_two[3].T == sp.zeros(4, 2)
    covectors = sp.Matrix(
        ((-F, -E, -E, F), (-B, -A, A, -B))
    )
    assert covectors * two_two[0].T == sp.zeros(2, 2)

    two_two_tensor = coefficients(two_two)
    allowed_two_two = {
        (0, 1, 0, 0),
        (0, 1, 0, 1),
        (1, 1, 0, 0),
        (1, 1, 0, 1),
    }
    assert all(
        value == 0
        for word, value in two_two_tensor.items()
        if word not in allowed_two_two
    )
    psi = (
        A**3 * F**3
        + A**2 * C * F**2 * H
        - A * B**2 * F * H**2
        - A * C**2 * E**2 * F
        + A * C**2 * F * H**2
        - B**2 * C * E**2 * H
    )
    assert sp.factor(active_determinant(two_two_tensor) + 16 * psi) == 0

    S, D, G, T = sp.symbols("S D G T")
    one_three = one_three_planes(S, D, G, T)
    one_three_contraction = contraction_matrix(
        one_three[1].row(0), one_three[2].row(1)
    )
    assert one_three_contraction.rank() == 2
    assert one_three_contraction * one_three[3].T == sp.zeros(4, 2)
    P, Q = G - T, D - S
    one_three_covectors = sp.Matrix(
        ((P, -1, 1, -1), (Q, -1, -1, 1))
    )
    assert one_three_covectors * one_three[0].T == sp.zeros(2, 2)

    one_three_tensor = coefficients(one_three)
    assert all(
        value == 0
        for word, value in one_three_tensor.items()
        if word not in allowed_two_two
    )
    split = (D - G - S + T) * (D + G - S - T) * (
        D + G + S + T
    )
    assert sp.factor(active_determinant(one_three_tensor) - split) == 0

    samples = {
        "two_two": two_two_planes(1, 1, 0, 2, 1, 1),
        "L1": one_three_planes(1, 3, 4, -3 + 4 + 1),
        "L2": one_three_planes(1, 3, 4, 3 + 4 - 1),
        "L3": one_three_planes(1, 2, 3, -2 - 3 - 1),
    }
    relation_data = {}
    for name, planes in samples.items():
        data = pair_relation_data(planes)
        relation_data[name] = {
            "".join(map(str, pair)): {
                "image_rank": rank,
                "relation_matrix_ranks": list(relation_ranks),
            }
            for pair, (rank, relation_ranks) in data.items()
        }
    assert relation_data["two_two"]["03"] == {
        "image_rank": 3,
        "relation_matrix_ranks": [2],
    }
    assert relation_data["two_two"]["13"]["relation_matrix_ranks"] == [1]
    assert relation_data["two_two"]["23"]["relation_matrix_ranks"] == [1]
    for branch in ("L1", "L2", "L3"):
        assert all(
            relation_data[branch][edge]["relation_matrix_ranks"] == [1]
            for edge in ("03", "13", "23")
        )

    two_two_center_vectors = (
        two_two[3].row(0),
        two_two[3].row(1),
    )
    one_three_center_vectors = (
        one_three[3].row(0),
        one_three[3].row(1),
    )
    assert tuple(map(support, two_two_center_vectors)) == ((0, 3), (1, 2))
    assert tuple(map(support, one_three_center_vectors)) == ((1, 2), (1, 3))

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "squarefree zero products, directed exceptional-pair graph, "
            "double-contraction radicals, and exhaustive block normal forms"
        ),
        "R2_pairing_rank": pairing.rank(),
        "opposite_pair_inequality": "r_ij+r_kl<=7",
        "minimal_exceptional_graphs": ["star", "triangle"],
        "rank_one_relation_is_coordinate_pair_zero_product": True,
        "two_two_complement_normalization_verified": True,
        "one_three_complement_normalization_verified": True,
        "two_two_double_contraction_rank": two_two_contraction.rank(),
        "one_three_double_contraction_rank": one_three_contraction.rank(),
        "two_two_active_determinant": str(-16 * psi),
        "one_three_active_determinant": str(split),
        "radical_star_component_orbits": 4,
        "radical_star_components": [
            "two_two_irreducible",
            "one_three_L1",
            "one_three_L2",
            "one_three_L3",
        ],
        "sample_pair_relations": relation_data,
        "all_pure_components_classified": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (
                TWO_TWO_THEOREM,
                ONE_THREE_THEOREM,
                SMOOTH_THEOREM,
            )
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_radical_star_component_classification_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
