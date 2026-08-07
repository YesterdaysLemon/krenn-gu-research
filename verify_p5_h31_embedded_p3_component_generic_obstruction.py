#!/usr/bin/env python3
"""Verify the generic H31 obstruction on the embedded-P3 component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import mixed_matrix


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "embedded-p3"
    / "P4_EMBEDDED_P3_PURE_COMPONENT.md")
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def main() -> None:
    cap_s, cap_t, cap_u = sp.symbols("S T U")
    shifts = sp.symbols("t0:4")
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta = (
        (1, 0, 1, cap_t),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    marked_beta = tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    pure = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS4
    }
    assert pure[(1, 1, 1, 1)] == -2
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    shared_alpha = tuple(row[1:] for row in alpha[1:])
    shared_beta = tuple(row[1:] for row in beta[1:])
    pure_p3 = {
        word: sp.factor(
            permanent(
                tuple(
                    shared_beta[mode] if word[mode] else shared_alpha[mode]
                    for mode in range(3)
                )
            )
        )
        for word in WORDS3
    }
    assert pure_p3[(1, 1, 1)] == -2
    assert all(
        value == 0
        for word, value in pure_p3.items()
        if word != (1, 1, 1)
    )

    for distinguished in (1, 2, 3):
        _, diagonal_alpha, _ = mixed_matrix(
            distinguished, alpha, marked_beta
        )
        assert diagonal_alpha == sp.zeros(1, 8)

    p, q, rho = sp.symbols("p q rho")
    x1, x2, x3, z1, z2, z3 = sp.symbols(
        "x1 x2 x3 z1 z2 z3"
    )
    variables = (x1, x2, x3, z1, z2, z3)
    insertion = {}
    for word in WORDS3:
        selected = tuple(
            shared_beta[mode] if word[mode] else shared_alpha[mode]
            for mode in range(3)
        )
        value = 0
        for mode in range(3):
            other_rows = tuple(
                selected[other]
                for other in range(3)
                if other != mode
            )
            extension_value = (
                (x1, x2, x3)[mode]
                if word[mode] == 0
                else (z1, z2, z3)[mode]
            )
            value += extension_value * permanent(
                ((p, q, rho),) + other_rows
            )
        insertion[word] = sp.factor(value)

    ell1 = p - q - rho
    ell2 = p - q + rho
    ell3 = p + q - rho
    ell4 = p + q + rho
    expected_insertion = {
        (0, 0, 0): ell4 * x1 + ell1 * x2 + ell2 * x3,
        (0, 0, 1): ell1 * x2 + ell2 * z3,
        (0, 1, 0): ell4 * x1 + ell1 * z2,
        (0, 1, 1): ell3 * x1 + ell1 * z2,
        (1, 0, 0): ell1 * x2 + ell4 * z1,
        (1, 0, 1): -2 * q * x2,
        (1, 1, 0): ell3 * x3 + ell4 * z1 + ell1 * z2,
        (1, 1, 1): ell3 * (z1 + z3) - 2 * q * z2,
    }
    assert all(
        sp.expand(insertion[word] - expected_insertion[word]) == 0
        for word in WORDS3
    )

    unwanted_words = WORDS3[:-1]
    matrix = sp.Matrix(
        [
            [
                sp.diff(insertion[word], variable)
                for variable in variables
            ]
            for word in unwanted_words
        ]
    )
    expected_minors = (
        -4 * q * rho * ell1 * ell2 * ell3 * ell4,
        0,
        4 * q * (p + rho) * ell1 * ell2 * ell3 * ell4,
        4 * p * q * ell1 * ell2 * ell4**2,
        -4 * q * rho * ell1 * ell2**2 * ell4,
        4 * p * rho * ell1**2 * ell2 * ell4,
        4 * q * rho * ell1 * ell2**2 * ell4,
    )
    maximal_minors = tuple(
        sp.factor(
            matrix.extract(
                tuple(row for row in range(7) if row != omitted),
                range(6),
            ).det()
        )
        for omitted in range(7)
    )
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(
            maximal_minors, expected_minors, strict=True
        )
    )

    line_data = (
        {
            "name": "L1",
            "substitution": {p: q + rho},
            "kernel": sp.Matrix((0, 0, 0, 0, 1, 0)),
            "rows": (1, 3, 4, 5, 6),
            "columns": (0, 1, 2, 3, 5),
            "minor": -32 * q**3 * rho * (q + rho),
        },
        {
            "name": "L2",
            "substitution": {p: q - rho},
            "kernel": sp.Matrix((0, 0, 0, 0, 0, 1)),
            "rows": (0, 2, 3, 4, 6),
            "columns": (0, 1, 2, 3, 4),
            "minor": 32 * q * rho**3 * (q - rho),
        },
        {
            "name": "L4",
            "substitution": {p: -q - rho},
            "kernel": sp.Matrix((0, 0, 0, 1, 0, 0)),
            "rows": (0, 1, 2, 3, 5),
            "columns": (0, 1, 2, 4, 5),
            "minor": 32 * q**3 * rho * (q + rho),
        },
    )
    line_certificates = {}
    for datum in line_data:
        specialized = matrix.subs(datum["substitution"])
        assert specialized * datum["kernel"] == sp.zeros(7, 1)
        certificate = sp.factor(
            specialized.extract(
                datum["rows"], datum["columns"]
            ).det()
        )
        assert sp.expand(certificate - datum["minor"]) == 0
        assert all(entry == 0 for entry in datum["kernel"][:3, :])
        line_certificates[datum["name"]] = {
            "kernel": [
                str(entry) for entry in datum["kernel"]
            ],
            "rank_five_minor": str(sp.factor(datum["minor"])),
        }

    exceptional_points = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, -1),
        (1, 0, -1),
        (0, 1, 1),
        (1, -1, 0),
    )
    projected_alpha = sp.Matrix((1, cap_s, cap_u))
    projected_beta = sp.Matrix((0, 1, cap_t))
    incidence_factors = tuple(
        sp.factor(
            sp.Matrix.hstack(
                projected_alpha,
                projected_beta,
                sp.Matrix(point),
            ).det()
        )
        for point in exceptional_points
    )
    expected_factors = (
        cap_s * cap_t - cap_u,
        -cap_t,
        1,
        cap_s * cap_t - cap_u + 1,
        cap_s * cap_t - cap_t - cap_u,
        -cap_t - 1,
        cap_s * cap_t - cap_u - 1,
        1 - cap_t,
        cap_s * cap_t + cap_t - cap_u,
    )
    assert incidence_factors == expected_factors
    discriminant = sp.factor(sp.prod(incidence_factors))
    expected_discriminant = (
        -cap_t
        * (cap_t - 1)
        * (cap_t + 1)
        * (cap_s * cap_t - cap_u)
        * (cap_s * cap_t - cap_t - cap_u)
        * (cap_s * cap_t + cap_t - cap_u)
        * (cap_s * cap_t - cap_u - 1)
        * (cap_s * cap_t - cap_u + 1)
    )
    assert sp.expand(discriminant - expected_discriminant) == 0
    assert discriminant.subs(
        {cap_s: 2, cap_t: 3, cap_u: 4}
    ) == 720

    all_alpha = insertion[(0, 0, 0)].subs(
        {p: 1, q: cap_s, rho: cap_u}
    )
    for datum in line_data:
        assert sp.factor(
            all_alpha.subs(
                dict(zip(variables, datum["kernel"], strict=True))
            )
        ) == 0

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "squarefree apolar insertion and projective "
            "degeneracy arrangement"
        ),
        "normalized_pure_coefficient": "-2",
        "immediate_zero_diagonal_deletions": [1, 2, 3],
        "remaining_deletion": 0,
        "insertion_matrix_shape": list(matrix.shape),
        "maximal_minors": [str(value) for value in maximal_minors],
        "rank_drop_support": [
            "p-q-rho=0",
            "p-q+rho=0",
            "p+q+rho=0",
            "[1:0:0]",
            "[0:1:0]",
            "[0:0:1]",
        ],
        "generic_line_certificates": line_certificates,
        "projected_line_exception_count": len(exceptional_points),
        "projected_line_discriminant": str(discriminant),
        "nonempty_open_sample": {"S": 2, "T": 3, "U": 4},
        "nonempty_open_sample_discriminant": 720,
        "all_generic_rank_jump_kernels_kill_alpha_diagonal": True,
        "generic_binary_neighbour_exists": False,
        "generic_marked_H31_fibre_empty": True,
        "complete_component_boundary_closed": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
