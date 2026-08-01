#!/usr/bin/env python3
"""Verify the Hall-deficiency weighted-H22 obstruction on component 18."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = ROOT / "P4_COMMON_SINGLETON_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def common_singleton_rows(
    L: sp.Symbol,
    M: sp.Symbol,
    a: sp.Symbol,
    b: sp.Symbol,
    c: sp.Symbol,
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    sp.Expr,
    sp.Matrix,
    tuple[sp.Matrix, ...],
]:
    """Reconstruct the rational family without importing its verifier."""

    d = -(
        L * b + M * a + M * c + b * c
    ) / (L + a)
    polar = sp.Matrix(((0, M, L), (M, 0, 1), (L, 1, 0)))
    ell = sp.Matrix((1, L, M))
    v1 = sp.Matrix((1, a, b))
    v2 = sp.Matrix((1, c, d))
    raw_v3 = (polar * v1).cross(polar * v2)
    v3 = sp.simplify(raw_v3 / raw_v3[0])
    vectors = (ell, v1, v2, v3)

    singleton = (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0))
    embedded = tuple(
        (sp.Integer(0), *tuple(vector)) for vector in vectors
    )
    alpha = (embedded[0], singleton, singleton, singleton)
    beta = (singleton, embedded[1], embedded[2], embedded[3])
    return alpha, beta, sp.factor(d), raw_v3, vectors


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.expand(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def weighted_01_row(
    row: tuple[sp.Expr, ...],
    extension: sp.Symbol,
    source_scales: tuple[sp.Symbol, ...],
    merge_weights: tuple[sp.Symbol, sp.Symbol],
) -> tuple[sp.Expr, ...]:
    s0, s1, s2, s3 = source_scales
    lam, mu = merge_weights
    return (
        sp.expand(lam * s0 * row[0] + mu * s1 * row[1]),
        sp.expand(s2 * row[2]),
        sp.expand(s3 * row[3]),
        extension,
    )


def weighted_23_row(
    row: tuple[sp.Expr, ...],
    extension: sp.Symbol,
    source_scales: tuple[sp.Symbol, ...],
    merge_weights: tuple[sp.Symbol, sp.Symbol],
) -> tuple[sp.Expr, ...]:
    s0, s1, s2, s3 = source_scales
    nu, omega = merge_weights
    return (
        sp.expand(s0 * row[0]),
        sp.expand(s1 * row[1]),
        sp.expand(nu * s2 * row[2] + omega * s3 * row[3]),
        extension,
    )


def verify_hall_diagonal(
    rows: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, object]:
    common_supports = tuple(
        tuple(index for index, entry in enumerate(row) if entry != 0)
        for row in rows[1:]
    )
    assert common_supports == ((0, 3), (0, 3), (0, 3))
    summands = tuple(
        sp.expand(
            sp.prod(rows[row][permutation[row]] for row in range(4))
        )
        for permutation in PERMUTATIONS
    )
    assert all(summand == 0 for summand in summands)
    diagonal = permanent(rows)
    assert diagonal == 0
    return {
        "common_kernel_row_supports": [list(value) for value in common_supports],
        "hall_row_set_size": 3,
        "hall_column_neighborhood_size": 2,
        "permanent_summands_checked": len(summands),
        "all_kernel_diagonal": str(diagonal),
    }


def main() -> None:
    L, M, a, b, c = sp.symbols("L M a b c")
    shifts = sp.symbols("h0:4")
    source_scales = sp.symbols("s0:4")
    lam, mu, nu, omega = sp.symbols("lambda mu nu omega")
    extensions = sp.symbols("x0:4")

    alpha, beta, d, raw_v3, vectors = common_singleton_rows(L, M, a, b, c)
    _ell, v1, v2, v3 = vectors
    polar = sp.Matrix(((0, M, L), (M, 0, 1), (L, 1, 0)))
    for left, right in ((v1, v2), (v1, v3), (v2, v3)):
        assert sp.factor((left.T * polar * right)[0]) == 0

    pure = {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    kappa = pure[(1, 1, 1, 1)]
    assert all(value == 0 for word, value in pure.items() if word != (1, 1, 1, 1))

    marked_beta = shifted_basis(alpha, beta, shifts)
    marked = {
        word: permanent(
            tuple(
                marked_beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert all(
        value == 0
        for word, value in marked.items()
        if word != (1, 1, 1, 1)
    )
    assert sp.factor(marked[(1, 1, 1, 1)] - kappa) == 0

    sample = {L: -3, M: -2, a: -1, b: -1, c: -1}
    assert sp.factor(d.subs(sample)) == 2
    assert tuple(sp.factor(entry.subs(sample)) for entry in v3) == (1, 3, -1)
    assert sp.factor(raw_v3[0].subs(sample)) == 12
    assert sp.factor(kappa.subs(sample)) == 4

    weighted_01 = tuple(
        weighted_01_row(
            alpha[mode], extensions[mode], source_scales, (lam, mu)
        )
        for mode in range(4)
    )
    weighted_23 = tuple(
        weighted_23_row(
            alpha[mode], extensions[mode], source_scales, (nu, omega)
        )
        for mode in range(4)
    )
    s0, s1, s2, s3 = source_scales
    assert weighted_01[0] == (mu * s1, L * s2, M * s3, extensions[0])
    assert weighted_23[0] == (
        0,
        s1,
        L * nu * s2 + M * omega * s3,
        extensions[0],
    )
    assert all(
        weighted_01[mode] == (lam * s0, 0, 0, extensions[mode])
        for mode in (1, 2, 3)
    )
    assert all(
        weighted_23[mode] == (s0, 0, 0, extensions[mode])
        for mode in (1, 2, 3)
    )

    certificates = {
        "D01": verify_hall_diagonal(weighted_01),
        "D23": verify_hall_diagonal(weighted_23),
    }
    result = {
        "status": "pass",
        "field": "C(L,M,a,b,c)",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "component": COMPONENT.name,
        "component_sha256": sha256(COMPONENT),
        "family_parameters": 5,
        "sample": [-3, -2, -1, -1, -1],
        "sample_v2_third_coordinate": 2,
        "sample_v3": [1, 3, -1],
        "sample_v3_normalizing_coordinate": 12,
        "sample_pure_coefficient": 4,
        "intrinsic_kernel_lines_modes_1_2_3": "C*(1,0,0,0)",
        "all_affine_markings": True,
        "homogeneous_merge_weights": True,
        "projective_slope_endpoints_included": True,
        "all_fifth_coordinate_extensions": True,
        "weighted_diagonal_certificates": certificates,
        "generic_weighted_H22_fibre_empty": True,
        "known_components_generically_H22_closed": 18,
        "component_projective_boundary_closed": False,
        "marked_H31_closed_by_this_theorem": False,
        "marked_H31_companion_theorem": (
            "P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md"
        ),
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "search_used": False,
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h22_common_singleton_component_generic_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
