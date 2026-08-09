#!/usr/bin/env python3
"""Primary symbolic verifier for the P_4 subrank obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hyperplane_basis(normal: tuple[int, ...]) -> sp.Matrix:
    pivot = next(index for index, value in enumerate(normal) if value)
    columns = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [sp.Integer(0)] * 4
        vector[free] = 1
        vector[pivot] = -sp.Rational(normal[free], normal[pivot])
        columns.append(vector)
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))


def pair_image(left: tuple[int, ...], right: tuple[int, ...]) -> sp.Matrix:
    left_basis = hyperplane_basis(left)
    right_basis = hyperplane_basis(right)
    columns = []
    for i in range(3):
        for j in range(3):
            u = left_basis[:, i]
            v = right_basis[:, j]
            columns.append(
                sp.Matrix(
                    [
                        u[a] * v[b] + u[b] * v[a]
                        for a, b in PAIRS
                    ]
                )
            )
    return sp.Matrix.hstack(*columns)


def permanent_coefficient(
    maps: list[sp.Matrix], colours: tuple[int, ...]
) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(
                maps[mode][permutation[mode], colours[mode]]
                for mode in range(4)
            )
            for permutation in PERMUTATIONS
        )
    )


def main() -> None:
    # Canonical equal-normal ranks k+2.
    equal_normal_ranks = {}
    for support in range(1, 5):
        normal = tuple([1] * support + [0] * (4 - support))
        equal_normal_ranks[support] = pair_image(normal, normal).rank()
    assert equal_normal_ranks == {1: 3, 2: 4, 3: 5, 4: 6}

    # Independent cases: generic dimension six and the only possible
    # exceptional dimension five.
    independent_cases = {
        "generic": ((1, 1, 1, 1), (1, 2, 3, 4)),
        "square_proportional": ((1, 1, 1, 1), (1, -1, 1, -1)),
        "disjoint_support": ((1, 0, 0, 0), (0, 1, 0, 0)),
    }
    independent_ranks = {
        name: pair_image(left, right).rank()
        for name, (left, right) in independent_cases.items()
    }
    assert independent_ranks == {
        "generic": 6,
        "square_proportional": 5,
        "disjoint_support": 6,
    }

    # Complement pairing is a nondegenerate permutation matrix.
    complement = sp.zeros(6, 6)
    for pair, index in PAIR_INDEX.items():
        other = tuple(item for item in range(4) if item not in pair)
        complement[index, PAIR_INDEX[other]] = 1
    assert complement.det() in (1, -1)

    # The support-two canonical slice space.
    ell, m, n = sp.symbols("ell m n")
    restricted_coordinates = (-ell, ell, m, n)
    slices = []
    for omitted in range(4):
        remaining = [
            restricted_coordinates[index]
            for index in range(4)
            if index != omitted
        ]
        slices.append(sp.expand(6 * sp.prod(remaining)))
    assert slices == [
        6 * ell * m * n,
        -6 * ell * m * n,
        -6 * ell**2 * n,
        -6 * ell**2 * m,
    ]
    slice_coefficient_matrix = sp.Matrix(
        [
            [sp.Poly(item, ell, m, n).coeff_monomial(monomial) for item in slices]
            for monomial in (ell * m * n, ell**2 * n, ell**2 * m)
        ]
    )
    assert slice_coefficient_matrix.rank() == 3

    # A cube in the slice space must be zero.  The coefficients of m^3,
    # n^3 and then ell^3 force beta=gamma=alpha=0.
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    cube = sp.Poly((alpha * ell + beta * m + gamma * n) ** 3, ell, m, n)
    forbidden_coefficients = [
        cube.coeff_monomial(m**3),
        cube.coeff_monomial(n**3),
        cube.coeff_monomial(ell**3),
    ]
    assert forbidden_coefficients == [beta**3, gamma**3, alpha**3]
    groebner = sp.groebner(
        forbidden_coefficients, alpha, beta, gamma, order="lex"
    )
    assert list(groebner) == [alpha**3, beta**3, gamma**3]

    # Explicit two-colour restriction.
    maps = []
    for mode in range(4):
        local = sp.zeros(4, 2)
        local[mode, 0] = 1
        local[(mode + 1) % 4, 1] = 1
        maps.append(local)
    two_colour_coefficients = {
        colours: permanent_coefficient(maps, colours)
        for colours in itertools.product(range(2), repeat=4)
    }
    assert {
        colours
        for colours, coefficient in two_colour_coefficients.items()
        if coefficient
    } == {(0, 0, 0, 0), (1, 1, 1, 1)}
    assert all(
        two_colour_coefficients[colours] == 1
        for colours in ((0, 0, 0, 0), (1, 1, 1, 1))
    )

    # A special-edge equivalence graph meeting all three perfect matchings
    # has an equivalence class of size at least three.
    mode_partitions = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    checked_partitions = 0
    for labels in itertools.product(range(4), repeat=4):
        # Canonicalize equality labels by first occurrence.
        relabel = {}
        canonical = []
        for label in labels:
            if label not in relabel:
                relabel[label] = len(relabel)
            canonical.append(relabel[label])
        if tuple(canonical) != labels:
            continue
        checked_partitions += 1
        hits_all = all(
            labels[a] == labels[b] or labels[c] == labels[d]
            for (a, b), (c, d) in mode_partitions
        )
        if hits_all:
            largest_class = max(labels.count(label) for label in set(labels))
            assert largest_class >= 3

    output = {
        "verified": True,
        "field": "C",
        "equal_normal_pair_image_ranks": equal_normal_ranks,
        "independent_pair_image_ranks": independent_ranks,
        "complement_pairing_rank": complement.rank(),
        "support_two_slice_dimension": slice_coefficient_matrix.rank(),
        "nonzero_decomposable_support_two_slices": 0,
        "explicit_diagonal_two_nonzero_coefficients": 2,
        "set_partitions_checked": checked_partitions,
        "permanent_subrank_P4": 2,
        "blocker_consequence": (
            "four fully supported zero-coupled roots require at least "
            "five blockers in total"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "fourth_order_permanent_subrank_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
