#!/usr/bin/env python3
"""Independent audit of component 21's extension-infinity partial closure."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "verify_p5_component21_finite_base_extension_infinity_partial_closure.py"
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
WORDS = tuple(itertools.product((0, 1), repeat=4))
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


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Subset-DP permanent, independent of the primary's permutation sum."""
    size = len(rows)
    state: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_state: dict[int, sp.Expr] = {}
        for mask, value in state.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_state[new_mask] = next_state.get(new_mask, 0) + value * row[column]
        state = next_state
    return sp.expand(state[(1 << size) - 1])


def bases(
    p: sp.Expr, q: sp.Expr, kappa: sp.Expr, ell: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    return (
        add(cap_a, scale(p, cap_b)),
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    ), (
        add(cap_c, scale(q, cap_b)),
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )


def h31_matrix(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[mode][index] for index in retained) + (extension[mode],)
        for mode in range(4)
    )
    beta_rows = tuple(
        tuple(beta[mode][index] for index in retained) + (extension[4 + mode],)
        for mode in range(4)
    )
    coefficients = []
    for word in WORDS:
        rows = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        coefficients.append(permanent(rows))
    return sp.Matrix(
        [[sp.diff(value, variable) for variable in extension] for value in coefficients]
    )


def project(
    row: tuple[sp.Expr, ...],
    extension: sp.Symbol,
    direction: str,
    chart: str,
    slope: sp.Expr,
) -> tuple[sp.Expr, ...]:
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def contraction_matrix(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    direction: str,
    chart: str,
    slope: sp.Expr,
) -> sp.Matrix:
    alpha_rows = tuple(
        project(alpha[i], extension[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extension[4 + i], direction, chart, slope)
        for i in range(4)
    )
    coefficient_rows = []
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index]
            for index in range(4)
        )
        coefficient = sum(
            selected[index][3]
            * permanent(
                tuple(selected[other][:3] for other in range(4) if other != index)
            )
            for index in range(4)
        )
        coefficient_rows.append(
            [sp.diff(sp.expand(coefficient), variable) for variable in extension]
        )
    return sp.Matrix(coefficient_rows)


def determinant(matrix: sp.Matrix, rows: tuple[int, ...]) -> sp.Expr:
    selected = sp.polys.matrices.DomainMatrix.from_Matrix(matrix[list(rows), :])
    return sp.factor(selected.det().as_expr())


def audit_h31(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    ell: sp.Symbol,
) -> dict[str, object]:
    inverse = sp.Symbol("u")
    matrices = {d: h31_matrix(d, alpha, beta, extension) for d in (2, 3)}
    minors = {
        d: tuple(determinant(matrix, rows) for rows in H31_ROW_SETS)
        for d, matrix in matrices.items()
    }
    assert all(
        sp.cancel(right / left) in (1, -1)
        for left, right in zip(minors[2], minors[3], strict=True)
    )
    generators = tuple(sp.primitive(value)[1] for value in minors[2])
    exceptional = (kappa, ell**2 - 1, q - ell * p)
    for chart_variable in (p, q):
        fitting = sp.groebner(
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
        assert all(fitting.reduce(value)[1] == 0 for value in exceptional)
        assert all(exceptional_basis.reduce(value)[1] == 0 for value in generators)

    seven_rows = (0, 1, 2, 4, 5, 7, 8)
    for epsilon in (1, -1):
        substitution = {q: epsilon * p, kappa: 0, ell: epsilon}
        for distinguished, matrix in matrices.items():
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
            specialized = matrix.subs(substitution)
            assert specialized * vector == sp.zeros(16, 1)
            minor7 = sp.polys.matrices.DomainMatrix.from_Matrix(
                specialized[list(seven_rows), :7]
            ).det().as_expr()
            assert sp.cancel(minor7 / (256 * p**3)) in (1, -1)
    return {"minors": len(generators), "exceptional_kernel_ranks": [7, 7, 7, 7]}


def audit_h22(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    p: sp.Symbol,
    q: sp.Symbol,
    kappa: sp.Symbol,
    ell: sp.Symbol,
) -> dict[str, object]:
    inverse = sp.Symbol("u")
    matrix = contraction_matrix(
        alpha, beta, extension, "D01", "infinity", sp.Integer(0)
    ).col_join(
        contraction_matrix(
            alpha, beta, extension, "D23", "infinity", sp.Integer(0)
        )
    )
    minors = tuple(determinant(matrix, rows) for rows in H22_INFINITY_ROW_SETS)
    generators = tuple(sp.primitive(value)[1] for value in minors)
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

    numeric_alpha, numeric_beta = bases(2, 3, 5, 7)
    numeric_extension = sp.symbols("x0:8")
    finite = contraction_matrix(
        numeric_alpha,
        numeric_beta,
        numeric_extension,
        "D01",
        "finite",
        sp.Integer(1),
    ).col_join(
        contraction_matrix(
            numeric_alpha,
            numeric_beta,
            numeric_extension,
            "D23",
            "finite",
            sp.Integer(1),
        )
    )
    assert finite.rank() == 7
    return {"infinity_minors": len(generators), "finite_weight_rank_witness": 7}


def main() -> None:
    p, q, kappa, ell = sp.symbols("p q kappa ell")
    extension = sp.symbols("z0:8")
    alpha, beta = bases(p, q, kappa, ell)
    h31 = audit_h31(alpha, beta, extension, p, q, kappa, ell)
    h22 = audit_h22(alpha, beta, extension, p, q, kappa, ell)

    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    assert "partial extension compactification, not a properness theorem" in theorem_text
    assert "global Krenn--Gu conjecture remains **UNRESOLVED**" in theorem_text

    replay = subprocess.run(
        [sys.executable, str(PRIMARY)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    primary = json.loads(replay.stdout)
    assert primary["status"] == "pass"
    assert primary["global_conjecture_resolved"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "no repository imports; subset-DP permanent",
                "field": "exact characteristic zero",
                "H31": h31,
                "H22": h22,
                "primary_replay": "pass",
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "dependency_hashes": {path.name: sha256(path) for path in PINNED},
                "theorem_sha256": sha256(THEOREM),
                "primary_sha256": sha256(PRIMARY),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
