#!/usr/bin/env python3
"""Verify component 21's extension-kernel marked-H31 leading obstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_p5_component21_normalized_parameter_compactification_complete_obstruction import (
    finite_bases,
)
from verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction import (
    WORDS,
    h31_coefficients,
    h31_obstruction_map,
    mark,
)

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_EXTENSION_KERNEL_MARKED_H31_LEADING_OBSTRUCTION.md"
PINNED = {
    ROOT / "P5_COMPONENT21_FINITE_BASE_EXTENSION_INFINITY_PARTIAL_CLOSURE.md": (
        "ea72ae9db0954b9dbeefc058bf3c14916896a4ff65282e241bbc6396cf3a91e0"
    ),
    ROOT / "verify_p5_component21_finite_base_extension_infinity_partial_closure.py": (
        "b8b9237b02f3c6ae7b4c702b9bc6a26c27c5a5580827d47584ac1226d9addd92"
    ),
    ROOT / "audit_p5_component21_finite_base_extension_infinity_partial_closure.py": (
        "949272bd0a727697566d756562fbf0dd03c5e21f577d0ec2d5a3c69109e5a271"
    ),
    ROOT / "verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "a395cefece221d2c6df797b55b9f900144a0cea95d568d8633ffb89ab495aaff"
    ),
    ROOT / "verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "c946ccc0bc6bf74b123dc9b41ce9ab3d6b813296161ae48ac8c436ec17d33f53"
    ),
}
SEVEN_ROWS = (0, 1, 2, 4, 5, 7, 8)
SEVEN_COLUMNS = tuple(range(7))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coefficient_matrix(
    coefficients: dict[tuple[int, ...], sp.Expr],
    extension: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    return sp.Matrix(
        [[sp.diff(coefficients[word], value) for value in extension] for word in WORDS]
    )


def marked_kernel(
    epsilon: int,
    distinguished: int,
    p: sp.Symbol,
    shifts: tuple[sp.Symbol, ...],
) -> tuple[sp.Expr, ...]:
    sign = -1 if distinguished == 2 else 1
    alpha_part = (
        -sp.Rational(1, 2),
        -epsilon,
        sp.Integer(0),
        sp.Rational(sign, 2) / p,
    )
    beta_part = (
        sp.Rational(epsilon, 2),
        sp.Integer(0),
        -sp.Rational(1, 2) / p,
        sp.Integer(1),
    )
    return alpha_part + tuple(
        sp.expand(beta_part[mode] + shifts[mode] * alpha_part[mode])
        for mode in range(4)
    )


def verify_case(
    epsilon: int,
    distinguished: int,
    p: sp.Symbol,
    shifts: tuple[sp.Symbol, ...],
    extension: tuple[sp.Symbol, ...],
) -> dict[str, object]:
    alpha, unmarked_beta = finite_bases(p, epsilon * p, 0, epsilon)
    beta = mark(alpha, unmarked_beta, shifts)
    kernel = sp.Matrix(marked_kernel(epsilon, distinguished, p, shifts))

    coefficients = h31_coefficients(distinguished, alpha, beta, extension)
    matrix = coefficient_matrix(coefficients, extension)
    kernel_image = matrix * kernel
    assert all(sp.factor(value) == 0 for value in kernel_image)

    obstruction = h31_obstruction_map(
        distinguished, alpha, beta, extension
    )
    assert obstruction.shape == (8, 4)
    assert all(
        sp.Poly(entry, *extension).total_degree() <= 1 for entry in obstruction
    )
    evaluated = obstruction.subs(dict(zip(extension, kernel, strict=True)))
    assert sp.factor(evaluated[0, 2]) == 1
    kernel_scale = sp.Symbol("c", nonzero=True)
    scaled = obstruction.subs(
        dict(zip(extension, kernel_scale * kernel, strict=True))
    )
    assert sp.factor(scaled[0, 2]) == kernel_scale

    unmarked_coefficients = h31_coefficients(
        distinguished, alpha, unmarked_beta, extension
    )
    unmarked_matrix = coefficient_matrix(unmarked_coefficients, extension)
    minor = sp.factor(
        sp.polys.matrices.DomainMatrix.from_Matrix(
            unmarked_matrix[list(SEVEN_ROWS), list(SEVEN_COLUMNS)]
        )
        .det()
        .as_expr()
    )
    assert sp.cancel(minor / (256 * p**3)) in (1, -1)

    return {
        "epsilon": epsilon,
        "distinguished": distinguished,
        "coefficient_kernel_dimension": 1,
        "marked_kernel": [str(sp.factor(value)) for value in kernel],
        "selected_obstruction_entry": str(evaluated[0, 2]),
        "scaled_obstruction_entry": str(scaled[0, 2]),
        "selected_obstruction_row": "000",
        "selected_obstruction_column": 2,
        "seven_minor": str(minor),
        "obstruction_linear_in_extension": True,
    }


def main() -> None:
    p = sp.Symbol("p", nonzero=True)
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    cases = [
        verify_case(epsilon, distinguished, p, shifts, extension)
        for epsilon in (1, -1)
        for distinguished in (2, 3)
    ]
    assert all(case["selected_obstruction_entry"] == "1" for case in cases)

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "every fixed-order marked-`H31` extension-pole arc",
        "Finite-weight `H22` common-kernel directions",
        "arbitrary source transformations",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "finite_nonzero_sheet_marked_H31_extension_poles_closed": True,
                "cases": cases,
                "subordinate_normal_terms_can_cancel": False,
                "finite_weight_H22_kernel_normals_closed": False,
                "zero_base_parameter_infinity_marking_poles_closed": False,
                "arbitrary_source_ambient_projective_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "dependency_hashes": dependency_hashes,
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
