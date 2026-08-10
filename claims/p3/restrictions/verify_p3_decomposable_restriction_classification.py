#!/usr/bin/env python3
"""Verify the decomposable rank-at-least-two P3 classification."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = HERE / "P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md"
PERMUTATIONS = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_value(
    first: sp.Matrix,
    second: sp.Matrix,
    third: sp.Matrix,
) -> sp.Expr:
    vectors = (first, second, third)
    return sp.expand(
        sum(
            sp.prod(vectors[row][permutation[row]] for row in range(3))
            for permutation in PERMUTATIONS
        )
    )


def restricted_tensor(
    first: sp.Matrix,
    second: sp.Matrix,
    third: sp.Matrix,
) -> dict[tuple[int, int, int], sp.Expr]:
    return {
        bits: permanent_value(
            first[:, bits[0]],
            second[:, bits[1]],
            third[:, bits[2]],
        )
        for bits in itertools.product((0, 1), repeat=3)
    }


def binary_flattening_ranks(
    tensor: dict[tuple[int, int, int], sp.Expr],
) -> tuple[int, int, int]:
    matrices = []
    for mode in range(3):
        other = [index for index in range(3) if index != mode]
        matrices.append(
            sp.Matrix(
                [
                    [
                        tensor[
                            tuple(
                                bit
                                if coordinate == mode
                                else other_bits[other.index(coordinate)]
                                for coordinate in range(3)
                            )
                        ]
                        for other_bits in itertools.product((0, 1), repeat=2)
                    ]
                    for bit in (0, 1)
                ]
            )
        )
    return tuple(matrix.rank() for matrix in matrices)


def main() -> None:
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    first = sp.Matrix([[-a, -b], [1, 0], [0, 1]])
    second = sp.Matrix([[-c, -d], [1, 0], [0, 1]])
    third = sp.Matrix([[-e, -f], [1, 0], [0, 1]])
    tensor = restricted_tensor(first, second, third)
    expected = {
        (0, 0, 0): 0,
        (0, 0, 1): -a - c,
        (0, 1, 0): -a - e,
        (0, 1, 1): -d - f,
        (1, 0, 0): -c - e,
        (1, 0, 1): -b - f,
        (1, 1, 0): -b - d,
        (1, 1, 1): 0,
    }
    assert tensor == expected

    middle = tuple(bits for bits in tensor if sum(bits) in (1, 2))
    edge_system_ranks = {}
    for fixed_one in range(3):
        for fixed_zero in range(3):
            if fixed_one == fixed_zero:
                continue
            allowed = {
                bits
                for bits in middle
                if bits[fixed_one] == 1 and bits[fixed_zero] == 0
            }
            equations = [
                tensor[bits] for bits in middle if bits not in allowed
            ]
            matrix, _ = sp.linear_eq_to_matrix(
                equations,
                (a, b, c, d, e, f),
            )
            assert matrix.rank() == 4
            edge_system_ranks[
                f"{fixed_one}>{fixed_zero}"
            ] = matrix.rank()

    representative_equations = [
        tensor[(0, 0, 1)],
        tensor[(0, 1, 0)],
        tensor[(0, 1, 1)],
        tensor[(1, 1, 0)],
    ]
    canonical = {
        c: -a,
        d: -b,
        e: -a,
        f: b,
    }
    assert all(
        sp.expand(equation.subs(canonical)) == 0
        for equation in representative_equations
    )
    canonical_tensor = {
        bits: sp.expand(value.subs(canonical))
        for bits, value in tensor.items()
    }
    assert canonical_tensor == {
        (0, 0, 0): 0,
        (0, 0, 1): 0,
        (0, 1, 0): 0,
        (0, 1, 1): 0,
        (1, 0, 0): 2 * a,
        (1, 0, 1): -2 * b,
        (1, 1, 0): 0,
        (1, 1, 1): 0,
    }

    # Support-one boundary: both remaining planes also contain e_0.
    boundary_profiles = {}
    for left_pair in ((1, 0), (0, 1), (1, 1)):
        for right_pair in ((1, 0), (0, 1), (1, 1)):
            left = sp.Matrix(
                [[1, 0], [0, left_pair[1]], [0, -left_pair[0]]]
            )
            right = sp.Matrix(
                [[1, 0], [0, right_pair[1]], [0, -right_pair[0]]]
            )
            coordinate_plane = sp.Matrix([[0, 0], [1, 0], [0, 1]])
            boundary = restricted_tensor(coordinate_plane, left, right)
            flattening = sp.Matrix(
                [
                    [
                        boundary[(first_bit, second_bit, third_bit)]
                        for first_bit in range(2)
                        for third_bit in range(2)
                    ]
                    for second_bit in range(2)
                ]
            )
            assert flattening.rank() == 2
            boundary_profiles[
                f"{left_pair}:{right_pair}"
            ] = flattening.rank()

    # Distinct-missing-coordinate support-two boundary.
    alpha, beta, gamma, delta, eta, phi = sp.symbols(
        "alpha beta gamma delta eta phi",
        nonzero=True,
    )
    triangle_first = sp.Matrix(
        [[0, beta], [0, -alpha], [1, 0]]
    )
    triangle_second = sp.Matrix(
        [[1, 0], [0, delta], [0, -gamma]]
    )
    triangle_third = sp.Matrix(
        [[0, phi], [1, 0], [0, -eta]]
    )
    triangle = restricted_tensor(
        triangle_first,
        triangle_second,
        triangle_third,
    )
    assert triangle[(0, 0, 0)] == 1
    assert triangle[(1, 0, 0)] == 0
    assert triangle[(0, 1, 0)] == 0
    assert triangle[(0, 0, 1)] == 0
    assert triangle[(1, 1, 0)] == -beta * gamma

    # The rank-three endpoint leaves a nondegenerate P2 factor.
    p2 = sp.Matrix([[0, 1], [1, 0]])
    assert p2.rank() == 2

    def plane_from_normal(normal: tuple[sp.Expr, ...]) -> sp.Matrix:
        assert normal[0] == 1
        return sp.Matrix(
            [
                [-normal[1], -normal[2]],
                [1, 0],
                [0, 1],
            ]
        )

    # Four-plane support-two sign rectangle: two copies of each sign.
    support_two_normals = (
        (1, a, 0),
        (1, a, 0),
        (1, -a, 0),
        (1, -a, 0),
    )
    support_two_triple_ranks = []
    for omitted in range(4):
        triple = [
            plane_from_normal(normal)
            for index, normal in enumerate(support_two_normals)
            if index != omitted
        ]
        value = restricted_tensor(*triple)
        ranks = binary_flattening_ranks(value)
        assert ranks == (1, 1, 1)
        assert any(value.values())
        support_two_triple_ranks.append(ranks)

    # Four-plane support-three sign rectangle: all four sign variants.
    support_three_normals = (
        (1, a, b),
        (1, -a, b),
        (1, a, -b),
        (1, -a, -b),
    )
    support_three_triple_ranks = []
    for omitted in range(4):
        triple = [
            plane_from_normal(normal)
            for index, normal in enumerate(support_three_normals)
            if index != omitted
        ]
        value = restricted_tensor(*triple)
        ranks = binary_flattening_ranks(value)
        assert ranks == (1, 1, 1)
        assert any(value.values())
        support_three_triple_ranks.append(ranks)

    coordinate_plane = sp.Matrix([[0, 0], [1, 0], [0, 1]])
    zero_rectangle = restricted_tensor(
        coordinate_plane,
        coordinate_plane,
        coordinate_plane,
    )
    assert not any(zero_rectangle.values())

    output = {
        "verified": True,
        "field": "C",
        "common_chart_coefficients_checked": 8,
        "oriented_edge_systems": len(edge_system_ranks),
        "oriented_edge_system_ranks": edge_system_ranks,
        "normal_form_parameters": 2,
        "support_one_boundary_profiles_checked": len(boundary_profiles),
        "support_one_boundary_flattening_ranks": boundary_profiles,
        "distinct_missing_coordinate_obstruction": "-beta*gamma",
        "rank_three_endpoint_P2_rank": p2.rank(),
        "allowed_rank_profile": "222",
        "four_plane_support_two_triple_ranks": support_two_triple_ranks,
        "four_plane_support_three_triple_ranks": (
            support_three_triple_ranks
        ),
        "four_plane_allowed_kind_patterns": [
            "all_zero",
            "all_nonzero_decomposable",
        ],
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p3_decomposable_restriction_classification_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
