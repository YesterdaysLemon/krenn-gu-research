#!/usr/bin/env python3
"""Independent audit of the component-21 h0-infinity normal package."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_SINGLE_MARKING_INFINITY_FIRST_NORMAL_OBSTRUCTION.md"
PRIMARY = (
    ROOT / "verify_p5_component21_single_marking_infinity_first_normal_obstruction.py"
)
DEPENDENCIES = {
    "P5_COMPONENT21_NORMALIZED_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md": (
        "41b9f45ef5f65efc6706a3757d5def9318015ec2c25dcda5c111a13aa5c16495"
    ),
    "verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "a395cefece221d2c6df797b55b9f900144a0cea95d568d8633ffb89ab495aaff"
    ),
    "audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "c098f94bf73f9a58b060314647c6048324bef2198509511561f87ec670831d8a"
    ),
}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(rows)
    assert all(len(row) == size for row in rows)
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                target = mask | (1 << column)
                next_states[target] = sp.expand(
                    next_states.get(target, sp.Integer(0)) + coefficient * entry
                )
        states = next_states
    return sp.expand(states[(1 << size) - 1])


def combine(
    left_scale: sp.Expr,
    left: tuple[sp.Expr, ...],
    right_scale: sp.Expr,
    right: tuple[sp.Expr, ...],
) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(left_scale * left[index] + right_scale * right[index])
        for index in range(4)
    )


def support(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, str]:
    result = {}
    for word in WORDS:
        selected = tuple(beta[i] if word[i] else alpha[i] for i in range(4))
        coefficient = sp.factor(permanent_dp(selected))
        if coefficient != 0:
            result["".join(map(str, word))] = str(coefficient)
    return result


def mark(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(combine(1, beta[i], shifts[i], alpha[i]) for i in range(4))


def h31_coefficients(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[mode][index] for index in retained) + (extension[mode],)
        for mode in range(4)
    )
    beta_rows = tuple(
        tuple(beta[mode][index] for index in retained) + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        word: permanent_dp(
            tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    output = []
    for word in itertools.product((0, 1), repeat=3):
        selected = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if word[bit] else alpha[other])
                bit += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(sp.Integer(index == coordinate) for index in range(4))
            rows = tuple(
                basis if other == mode else selected[other] for other in range(4)
            )
            assert all(row is not None for row in rows)
            coefficient_row.append(permanent_dp(rows))  # type: ignore[arg-type]
        output.append(tuple(coefficient_row))
    return sp.Matrix(output)


def h31_obstruction_map(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_rows = tuple(
        tuple(alpha[row][index] for index in retained) + (extension[row],)
        for row in range(4)
    )
    beta_rows = tuple(
        tuple(beta[row][index] for index in retained) + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(3, alpha_rows, beta_rows)


def project(
    row: tuple[sp.Expr, ...],
    extension: sp.Symbol,
    direction: str,
    chart: str,
    slope: sp.Symbol,
) -> tuple[sp.Expr, ...]:
    if (direction, chart) == ("D01", "finite"):
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if (direction, chart) == ("D23", "finite"):
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if (direction, chart) == ("D01", "infinity"):
        return (row[0], row[2], row[3], extension)
    if (direction, chart) == ("D23", "infinity"):
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def contraction(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: tuple[sp.Symbol, ...],
    direction: str,
    chart: str,
    slope: sp.Symbol,
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    dict[tuple[int, ...], sp.Expr],
]:
    alpha_rows = tuple(
        project(alpha[i], extension[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extension[4 + i], direction, chart, slope) for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent_dp(
                    tuple(selected[other][:3] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )
    return alpha_rows, beta_rows, coefficients


def contraction_obstruction_map(
    alpha_rows: tuple[tuple[sp.Expr, ...], ...],
    beta_rows: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    output = []
    for word in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_rows[index] if word[position] else alpha_rows[index]
            for position, index in enumerate((0, 1, 2))
        )
        output.append(
            tuple(
                permanent_dp(
                    tuple(
                        tuple(row[column] for column in range(4) if column != omitted)
                        for row in selected
                    )
                )
                for omitted in range(4)
            )
        )
    return sp.Matrix(output)


def finite_bases(
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    return (
        combine(1, cap_a, p, cap_b),
        combine(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    ), (
        combine(1, cap_c, q, cap_b),
        cap_a,
        combine(1, cap_b, kappa, cap_a),
        combine(1, cap_a, ell, cap_c),
    )


def h0_boundary(
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(mark(alpha, canonical_beta, (sp.Integer(0),) + shifts))
    beta[0] = alpha[0]
    return alpha, tuple(beta)


def joint_normal(
    cap_p: sp.Expr,
    cap_s: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(0, q, kappa, ell)
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    alpha = list(alpha)
    beta = list(mark(tuple(alpha), canonical_beta, (sp.Integer(0),) + shifts))
    alpha[0] = combine(cap_p, cap_b, 0, cap_b)
    beta[0] = combine(
        cap_p,
        cap_b,
        cap_s,
        combine(1, cap_c, q, cap_b),
    )
    return tuple(alpha), tuple(beta)


def monomial_normal(
    cap_p: sp.Expr,
    cap_r: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(0, 0, kappa, ell)
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    alpha = list(alpha)
    beta = list(mark(tuple(alpha), canonical_beta, (sp.Integer(0),) + shifts))
    alpha[0] = combine(cap_p, cap_b, 0, cap_b)
    beta[0] = combine(cap_p + cap_r, cap_b, 0, cap_b)
    return tuple(alpha), tuple(beta)


def unit_groebner(
    label: str,
    equations: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
) -> dict[str, int | bool]:
    basis = sp.groebner(equations, *variables, order="grevlex")
    is_unit = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
    assert is_unit, label
    return {"equations": len(equations), "variables": len(variables), "unit": True}


def four_certificates(
    prefix: str,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    retained: tuple[sp.Symbol, ...],
) -> dict[str, dict[str, int | bool]]:
    slope = sp.Symbol("lambda")
    extension = sp.symbols("z0:8")
    inverse, inverse_a, inverse_b = sp.symbols("v u w")
    results = {}
    for distinguished in (0, 1):
        assert h31_coefficients(distinguished, alpha, beta, extension)[WORDS[0]] == 0
    for distinguished in (2, 3):
        coefficients = h31_coefficients(distinguished, alpha, beta, extension)
        vector = sp.Matrix(extension)
        mixed = sp.Matrix(
            [
                [sp.diff(coefficients[word], value) for value in extension]
                for word in MIXED
            ]
        )
        diagonal_alpha = sp.Matrix(
            [[sp.diff(coefficients[WORDS[0]], value) for value in extension]]
        )
        diagonal_beta = sp.Matrix(
            [[sp.diff(coefficients[WORDS[-1]], value) for value in extension]]
        )
        equations = tuple(mixed * vector) + (
            sp.expand((diagonal_alpha * vector)[0] - 1),
            sp.expand(inverse * (diagonal_beta * vector)[0] - 1),
            *tuple(h31_obstruction_map(distinguished, alpha, beta, extension)),
        )
        label = f"{prefix}_H31_d{distinguished}"
        results[label] = unit_groebner(
            label, equations, extension + (inverse,) + retained
        )
    for chart in ("finite", "infinity"):
        _, _, d01 = contraction(alpha, beta, extension, "D01", chart, slope)
        d23_alpha, d23_beta, d23 = contraction(
            alpha, beta, extension, "D23", chart, slope
        )
        assert d01[WORDS[0]] == 0
        vector = sp.Matrix(extension)
        mixed = sp.Matrix(
            [[sp.diff(d23[word], value) for value in extension] for word in MIXED]
        )
        equations = (
            *(d01[word] for word in WORDS[:-1]),
            sp.expand(d01[WORDS[-1]] - 1),
            *tuple(mixed * vector),
            sp.expand(inverse_a * d23[WORDS[0]] - 1),
            sp.expand(inverse_b * d23[WORDS[-1]] - 1),
            *tuple(contraction_obstruction_map(d23_alpha, d23_beta)),
        )
        chart_retained = retained + ((slope,) if chart == "finite" else ())
        label = f"{prefix}_H22_{chart}_weight"
        results[label] = unit_groebner(
            label,
            equations,
            extension + (inverse_a, inverse_b) + chart_retained,
        )
    assert len(results) == 4
    return results


def main() -> None:
    p, q, kappa, ell, cap_p, cap_s, cap_r, t = sp.symbols("p q kappa ell P S R t")
    h1, h2, h3 = sp.symbols("h1 h2 h3")
    shifts = (h1, h2, h3)

    finite_alpha, finite_canonical_beta = finite_bases(p, q, kappa, ell)
    chart_beta = list(
        mark(finite_alpha, finite_canonical_beta, (sp.Integer(0),) + shifts)
    )
    chart_beta[0] = combine(1, finite_alpha[0], t, finite_canonical_beta[0])
    chart_support = support(finite_alpha, tuple(chart_beta))
    assert chart_support == {"0111": "4*p", "1111": "4*(p + q*t)"}

    boundary_alpha, boundary_beta = h0_boundary(p, q, kappa, ell, shifts)
    boundary_support = support(boundary_alpha, boundary_beta)
    assert boundary_support == {"0111": "4*p", "1111": "4*p"}
    boundary_certificates = four_certificates(
        "h0_infinity_boundary",
        boundary_alpha,
        boundary_beta,
        (p, q, kappa, ell, h1, h2, h3),
    )

    residual_alpha, residual_beta = joint_normal(cap_p, cap_s, q, kappa, ell, shifts)
    residual_support = support(residual_alpha, residual_beta)
    assert residual_support == {
        "0111": "4*P",
        "1111": "4*(P + S*q)",
    }
    residual_certificates = four_certificates(
        "joint_normal",
        residual_alpha,
        residual_beta,
        (cap_p, cap_s, q, kappa, ell, h1, h2, h3),
    )

    monomial_alpha, monomial_beta = monomial_normal(cap_p, cap_r, kappa, ell, shifts)
    monomial_support = support(monomial_alpha, monomial_beta)
    assert monomial_support == {
        "0111": "4*P",
        "1111": "4*(P + R)",
    }
    monomial_certificates = four_certificates(
        "p_sq_monomial_normal",
        monomial_alpha,
        monomial_beta,
        (cap_p, cap_r, kappa, ell, h1, h2, h3),
    )

    for filename, expected in DEPENDENCIES.items():
        assert sha256(ROOT / filename) == expected
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "joint `(s,p)`-normal residual",
        "monomial `(p,sq)` normal",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    completed = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=240,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    primary_output = json.loads(completed.stdout)
    assert primary_output["status"] == "pass"
    assert primary_output["joint_normal_pure_support"] == residual_support
    assert primary_output["p_sq_monomial_normal_pure_support"] == monomial_support
    assert primary_output["pure_support_transfer_used"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP and Groebner audit",
                "field": "exact characteristic zero",
                "h0_infinity_chart_pure_support": chart_support,
                "h0_infinity_boundary_pure_support": boundary_support,
                "h0_infinity_boundary_unit_ideals": boundary_certificates,
                "joint_normal_residual_pair": [
                    "P*B",
                    "P*B + S*(C+q*B)",
                ],
                "joint_normal_pure_support": residual_support,
                "joint_normal_zero_locus": "P=0 and S*q=0",
                "joint_normal_unit_ideals": residual_certificates,
                "p_sq_monomial_normal_residual_pair": [
                    "P*B",
                    "(P+R)*B",
                ],
                "p_sq_monomial_normal_pure_support": monomial_support,
                "p_sq_monomial_normal_unit_ideals": monomial_certificates,
                "dvr_puiseux_order": "min(v(p), v(s)+v(q))",
                "dependency_hashes_verified": True,
                "primary_replay_passed": True,
                "pure_support_transfer_used": False,
                "nonzero_p_sq_monomial_normal_closed": True,
                "zero_P4_restriction_ambient_leading_term_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "primary_sha256": sha256(PRIMARY),
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
