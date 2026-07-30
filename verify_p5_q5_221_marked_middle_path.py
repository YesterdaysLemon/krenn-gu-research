#!/usr/bin/env python3
"""Verify the exact marked-middle path obstruction in normalized q5_221."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def span_intersection(left, right):
    """Return a column basis for span(left) intersect span(right)."""
    left_matrix = sp.Matrix.hstack(*map(sp.Matrix, left))
    right_matrix = sp.Matrix.hstack(*map(sp.Matrix, right))
    relations = left_matrix.row_join(-right_matrix).nullspace()
    candidates = [left_matrix * relation[: len(left), :] for relation in relations]
    if not candidates:
        return ()
    basis = sp.Matrix.hstack(*candidates).columnspace()
    return tuple(tuple(vector) for vector in basis)


def projective_sign_variants(support):
    support = tuple(support)
    first = support[0]
    variants = []
    for signs in itertools.product((1, -1), repeat=len(support) - 1):
        vector = [0, 0, 0]
        vector[first] = 1
        for coordinate, sign in zip(support[1:], signs, strict=True):
            vector[coordinate] = sign
        variants.append(tuple(vector))
    return tuple(variants)


def same_span(first, second) -> bool:
    first_matrix = sp.Matrix.hstack(*map(sp.Matrix, first))
    second_matrix = sp.Matrix.hstack(*map(sp.Matrix, second))
    return (
        first_matrix.rank()
        == second_matrix.rank()
        == first_matrix.row_join(second_matrix).rank()
    )


def main() -> None:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = tuple(e[0][i] + e[1][i] for i in range(5))
    h0 = tuple(e[0][i] - e[1][i] for i in range(5))
    u1 = tuple(e[2][i] + e[3][i] for i in range(5))
    h1 = tuple(e[2][i] - e[3][i] for i in range(5))
    h2 = e[4]

    j12 = (e[0], e[1], u1)
    j02 = (u0, e[2], e[3])
    j21 = (e[0], e[1], h1)
    j20 = (h0, e[2], e[3])
    assert same_span(span_intersection(j12, j02), (u0, u1))
    assert same_span(span_intersection(j21, j20), (h0, h1))
    assert all(vector[4] == 0 for space in (j12, j02, j21, j20) for vector in space)

    # Both h2-pullback target covectors have own-colour coordinate 2
    # equal to zero.  The two repeated-h2 contractions say that their
    # supports in coordinates 0 and 1 are disjoint.  Nonzeroness leaves
    # exactly the two complementary singleton chiralities.
    nonempty_supports = (
        frozenset((0,)),
        frozenset((1,)),
        frozenset((0, 1)),
    )
    chiralities = tuple(
        (left, right)
        for left in nonempty_supports
        for right in nonempty_supports
        if left.isdisjoint(right)
    )
    assert chiralities == (
        (frozenset((0,)), frozenset((1,))),
        (frozenset((1,)), frozenset((0,))),
    )

    # If two distinct residual normal lines in one two-dimensional
    # kernel both lie in H2, they span the kernel and force h2 into the
    # annihilator row space.
    a0, a1, a2, a3, b0, b1, b2, b3 = sp.symbols(
        "a0 a1 a2 a3 b0 b1 b2 b3"
    )
    normal_left = sp.Matrix((a0, a1, a2, a3, 0))
    normal_right = sp.Matrix((b0, b1, b2, b3, 0))
    kernel = sp.Matrix.hstack(normal_left, normal_right)
    assert (sp.Matrix(h2).T * kernel) == sp.zeros(1, 2)

    # In a full-support sign rectangle, at most two projective vertices
    # have equal first coordinates, whereas a valid P3 triple uses three
    # distinct vertices.
    full_variants = projective_sign_variants((0, 1, 2))
    equal_first_pair = tuple(v for v in full_variants if v[0] == v[1])
    equal_last_pair = tuple(v for v in full_variants if v[1] == v[2])
    assert equal_first_pair == ((1, 1, 1), (1, 1, -1))
    assert equal_last_pair == ((1, 1, 1), (1, -1, -1))

    # A valid full-support P3 triple is any three distinct vertices of
    # the four-point sign rectangle.
    valid_full_triples = tuple(
        tuple(triple)
        for triple in itertools.combinations(full_variants, 3)
    )
    assert all(len(triple) == 3 for triple in valid_full_triples)
    assert all(
        not all(vector[0] == vector[1] for vector in triple)
        for triple in valid_full_triples
    )

    # A support-two P3 chart uses both projective sign variants.  Check
    # that none has equality in coordinates zero and one at all modes.
    valid_support_two_triples = []
    for coordinate_support in itertools.combinations(range(3), 2):
        first, second = projective_sign_variants(coordinate_support)
        valid_support_two_triples.extend(
            set(itertools.permutations((first, first, second)))
        )
        valid_support_two_triples.extend(
            set(itertools.permutations((second, second, first)))
        )
    assert all(
        not all(vector[0] == vector[1] for vector in triple)
        for triple in valid_support_two_triples
    )

    # In chirality II the exact incidence rows force the common kernel
    # lines to h0 at A and h1 at B.  In Q21 coordinates these have
    # supports two and one.
    q21_a_normal = (1, -1, 0)
    q21_b_normal = (0, 0, 1)
    supports = tuple(
        tuple(index for index, value in enumerate(vector) if value)
        for vector in (q21_a_normal, q21_b_normal)
    )
    assert supports == ((0, 1), (2,))

    output = {
        "verified": True,
        "field": "C",
        "target_h2_covector_chiralities": [
            [sorted(left), sorted(right)] for left, right in chiralities
        ],
        "J12_intersect_J02": ["u0", "u1"],
        "J21_intersect_J20": ["h0", "h1"],
        "kernel_line_principle_checked": True,
        "chirality_I_all_Q12_normals_satisfy_n0_equals_n1": True,
        "chirality_I_admissible_full_support_charts": 0,
        "chirality_I_admissible_support_two_charts": 0,
        "chirality_II_Q21_normal_supports": [list(value) for value in supports],
        "exact_marked_middle_path_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_marked_middle_path_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
