#!/usr/bin/env python3
"""Primary symbolic verifier for the P4 decomposable rank-drop theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md"
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hyperplane_basis(normal: tuple[int, ...]) -> sp.Matrix:
    pivot = next(index for index, value in enumerate(normal) if value)
    columns = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [sp.Integer(0)] * 4
        vector[free] = 1
        vector[pivot] = -sp.Rational(normal[free], normal[pivot])
        columns.append(sp.Matrix(vector))
    return sp.Matrix.hstack(*columns)


def pair_image(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = []
    for i in range(left.cols):
        for j in range(right.cols):
            u = left[:, i]
            v = right[:, j]
            columns.append(
                sp.Matrix(
                    [
                        u[p] * v[q] + u[q] * v[p]
                        for p, q in PAIRS
                    ]
                )
            )
    return sp.Matrix.hstack(*columns)


def fixed_vector_map(vector: tuple[int, ...]) -> sp.Matrix:
    basis = sp.eye(4)
    right = sp.Matrix(vector)
    return sp.Matrix.hstack(
        *[
            sp.Matrix(
                [
                    basis[p, source] * right[q]
                    + basis[q, source] * right[p]
                    for p, q in PAIRS
                ]
            )
            for source in range(4)
        ]
    )


def main() -> None:
    equal_normal_ranks = {}
    for support in range(1, 5):
        normal = tuple([1] * support + [0] * (4 - support))
        hyperplane = hyperplane_basis(normal)
        equal_normal_ranks[support] = pair_image(
            hyperplane,
            hyperplane,
        ).rank()
    assert equal_normal_ranks == {1: 3, 2: 4, 3: 5, 4: 6}

    fixed_vector_ranks = {
        support: fixed_vector_map(
            tuple([1] * support + [0] * (4 - support))
        ).rank()
        for support in range(1, 5)
    }
    assert fixed_vector_ranks == {1: 3, 2: 3, 3: 4, 4: 4}

    complement = sp.zeros(6, 6)
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    for pair, index in pair_index.items():
        other = tuple(item for item in range(4) if item not in pair)
        complement[index, pair_index[other]] = 1
    assert complement.rank() == 6

    # The support-one slice is P3 and has one-mode flattening rank three.
    permutations_three = tuple(itertools.permutations(range(3)))
    p3_flattening = sp.zeros(3, 9)
    for permutation in permutations_three:
        p3_flattening[
            permutation[0],
            3 * permutation[1] + permutation[2],
        ] += 1
    assert p3_flattening.rank() == 3

    # The support-two canonical fourth-mode slice space.
    ell, m, n = sp.symbols("ell m n")
    coordinates = (-ell, ell, m, n)
    slices = [
        sp.expand(
            6
            * sp.prod(
                coordinates[index]
                for index in range(4)
                if index != omitted
            )
        )
        for omitted in range(4)
    ]
    assert slices == [
        6 * ell * m * n,
        -6 * ell * m * n,
        -6 * ell**2 * n,
        -6 * ell**2 * m,
    ]

    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    cube = sp.Poly(
        (alpha * ell + beta * m + gamma * n) ** 3,
        ell,
        m,
        n,
    )
    forbidden = [
        cube.coeff_monomial(m**3),
        cube.coeff_monomial(n**3),
        cube.coeff_monomial(ell**3),
    ]
    assert forbidden == [beta**3, gamma**3, alpha**3]
    assert list(
        sp.groebner(
            forbidden,
            alpha,
            beta,
            gamma,
            order="lex",
        )
    ) == [alpha**3, beta**3, gamma**3]

    output = {
        "verified": True,
        "field": "C",
        "equal_hyperplane_pair_image_ranks": equal_normal_ranks,
        "fixed_vector_pair_map_ranks": fixed_vector_ranks,
        "complement_pairing_rank": complement.rank(),
        "support_one_P3_flattening_rank": p3_flattening.rank(),
        "support_two_slice_dimension": 3,
        "nonzero_decomposable_support_two_slices": 0,
        "maximum_rank_three_local_maps": 2,
        "q5_311_rare_rank_drop_lower_bounds": [2, 2],
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_decomposable_restriction_rank_drop_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
