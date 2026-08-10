#!/usr/bin/env python3
"""Verify component 21's finite-base extension-infinity partial closure."""

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
    contraction,
    h31_coefficients,
)

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_FINITE_BASE_EXTENSION_INFINITY_PARTIAL_CLOSURE.md"
PINNED = {
    ROOT / "P5_COMPONENT21_NORMALIZED_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md": (
        "41b9f45ef5f65efc6706a3757d5def9318015ec2c25dcda5c111a13aa5c16495"
    ),
    ROOT / "verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "a395cefece221d2c6df797b55b9f900144a0cea95d568d8633ffb89ab495aaff"
    ),
    ROOT / "audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "c098f94bf73f9a58b060314647c6048324bef2198509511561f87ec670831d8a"
    ),
}

H31_ROW_SETS = (
    (0, 1, 2, 3, 4, 5, 7, 8),
    (0, 2, 3, 4, 6, 8, 9, 15),
    (0, 1, 2, 4, 6, 7, 8, 10),
    (0, 1, 2, 4, 5, 6, 7, 8),
    (0, 3, 4, 6, 7, 8, 9, 15),
    (0, 1, 3, 4, 6, 7, 8, 12),
    (0, 1, 2, 4, 5, 7, 8, 15),
    (0, 2, 3, 4, 7, 8, 9, 15),
    (0, 2, 3, 4, 7, 8, 12, 15),
)
H22_INFINITY_ROW_SETS = (
    (2, 3, 7, 16, 17, 18, 20, 24),
    (10, 11, 15, 16, 18, 19, 20, 24),
    (2, 3, 7, 16, 17, 20, 22, 24),
    (2, 3, 7, 16, 18, 20, 21, 24),
    (6, 7, 16, 17, 18, 20, 21, 24),
    (10, 11, 15, 16, 18, 20, 22, 24),
    (14, 15, 16, 18, 19, 20, 22, 24),
    (10, 11, 15, 16, 19, 20, 22, 24),
    (10, 11, 15, 16, 18, 20, 23, 24),
    (14, 15, 16, 18, 19, 20, 23, 24),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coefficient_matrix(
    coefficients: dict[tuple[int, ...], sp.Expr],
    extension: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    return sp.Matrix(
        [[sp.diff(coefficients[word], value) for value in extension] for word in WORDS]
    )


def determinant(matrix: sp.Matrix, rows: tuple[int, ...]) -> sp.Expr:
    domain_matrix = sp.polys.matrices.DomainMatrix.from_Matrix(matrix[list(rows), :])
    return sp.factor(domain_matrix.det().as_expr())


def reduced(expressions: tuple[sp.Expr, ...], basis: sp.GroebnerBasis) -> bool:
    return all(basis.reduce(expression)[1] == 0 for expression in expressions)


def h31_fitting_cover(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    ell: sp.Symbol,
) -> dict[str, object]:
    inverse = sp.Symbol("u")
    matrices = {
        distinguished: coefficient_matrix(
            h31_coefficients(distinguished, alpha, beta, extension), extension
        )
        for distinguished in (2, 3)
    }
    minors = {
        distinguished: tuple(
            determinant(matrix, rows) for rows in H31_ROW_SETS
        )
        for distinguished, matrix in matrices.items()
    }
    assert all(
        sp.simplify(right / left) in (1, -1)
        for left, right in zip(minors[2], minors[3], strict=True)
    )

    generators = tuple(sp.primitive(value)[1] for value in minors[2])
    exceptional = (kappa, ell**2 - 1, q - ell * p)
    charts = {}
    for chart_variable in (p, q):
        basis = sp.groebner(
            generators + (inverse * chart_variable - 1,),
            inverse,
            p,
            q,
            kappa,
            ell,
            order="grevlex",
        )
        exceptional_basis = sp.groebner(
            exceptional,
            inverse,
            p,
            q,
            kappa,
            ell,
            order="grevlex",
        )
        assert reduced(exceptional, basis)
        assert reduced(generators, exceptional_basis)
        charts[str(chart_variable)] = {
            "groebner_basis": [str(sp.factor(item.as_expr())) for item in basis.polys],
            "exceptional_ideal": ["kappa", "ell^2 - 1", "q - ell*p"],
        }

    kernels = {}
    seven_rows = (0, 1, 2, 4, 5, 7, 8)
    seven_columns = tuple(range(7))
    for epsilon in (1, -1):
        substitution = {q: epsilon * p, kappa: 0, ell: epsilon}
        for distinguished, matrix in matrices.items():
            specialized = matrix.subs(substitution)
            sign = -1 if distinguished == 2 else 1
            vector = sp.Matrix(
                (
                    -sp.Rational(1, 2),
                    -epsilon,
                    0,
                    sign / (2 * p),
                    sp.Rational(epsilon, 2),
                    0,
                    -1 / (2 * p),
                    1,
                )
            )
            assert specialized * vector == sp.zeros(16, 1)
            minor7 = sp.factor(
                sp.polys.matrices.DomainMatrix.from_Matrix(
                    specialized[list(seven_rows), list(seven_columns)]
                )
                .det()
                .as_expr()
            )
            assert sp.simplify(minor7 / (256 * p**3)) in (1, -1)
            kernels[f"epsilon_{epsilon}_d{distinguished}"] = {
                "generator": [str(sp.factor(value)) for value in vector],
                "rank": 7,
                "seven_minor": str(minor7),
            }
    return {
        "selected_minors": [str(value) for value in minors[2]],
        "charts": charts,
        "exceptional_curves": "kappa=0, ell=epsilon, q=epsilon*p, p!=0",
        "kernels": kernels,
    }


def stacked_contraction_matrix(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    chart: str,
    slope: sp.Expr,
) -> sp.Matrix:
    blocks = []
    for direction in ("D01", "D23"):
        _, _, coefficients = contraction(
            alpha, beta, extension, direction, chart, slope
        )
        blocks.append(coefficient_matrix(coefficients, extension))
    return blocks[0].col_join(blocks[1])


def h22_infinity_cover(
    matrix: sp.Matrix,
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    ell: sp.Symbol,
) -> dict[str, object]:
    inverse = sp.Symbol("u")
    minors = tuple(determinant(matrix, rows) for rows in H22_INFINITY_ROW_SETS)
    generators = tuple(sp.primitive(value)[1] for value in minors)
    charts = {}
    for chart_variable in (p, q):
        basis = sp.groebner(
            generators + (inverse * chart_variable - 1,),
            inverse,
            p,
            q,
            kappa,
            ell,
            order="grevlex",
        )
        assert len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
        charts[str(chart_variable)] = "unit"
    return {
        "selected_minors": [str(value) for value in minors],
        "p_nonzero_chart": charts["p"],
        "q_nonzero_chart": charts["q"],
        "rank_on_nonzero_sheet": 8,
    }


def finite_weight_kernel_witness() -> dict[str, object]:
    extension = sp.symbols("x0:8")
    alpha, beta = finite_bases(2, 3, 5, 7)
    matrix = stacked_contraction_matrix(
        alpha, beta, extension, "finite", sp.Integer(1)
    )
    rank = matrix.rank()
    assert rank == 7
    return {
        "point": [2, 3, 5, 7, 1],
        "stacked_extension_rank": rank,
        "coupled_normal_closed": False,
    }


def main() -> None:
    p, q, kappa, ell = sp.symbols("p q kappa ell")
    extension = sp.symbols("z0:8")
    alpha, beta = finite_bases(p, q, kappa, ell)

    h31 = h31_fitting_cover(alpha, beta, extension, p, q, kappa, ell)
    h22_matrix = stacked_contraction_matrix(
        alpha, beta, extension, "infinity", sp.Integer(0)
    )
    h22 = h22_infinity_cover(h22_matrix, p, q, kappa, ell)
    finite_witness = finite_weight_kernel_witness()

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "finite-base extension-infinity partial closure",
        "finite-weight `H22` common-kernel directions remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "finite_marking_rank_invariance": "invertible triangular change",
                "marked_H31_extension_infinity": h31,
                "H22_weight_infinity_extension_infinity": h22,
                "finite_weight_boundary": finite_witness,
                "h31_exceptional_kernel_normals_closed": False,
                "finite_weight_H22_kernel_normals_closed": False,
                "zero_base_and_parameter_infinity_closed": False,
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
