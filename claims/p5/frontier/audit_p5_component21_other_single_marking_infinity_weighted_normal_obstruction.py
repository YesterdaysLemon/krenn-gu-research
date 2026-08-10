#!/usr/bin/env python3
"""Independent audit of component 21's h1/h2/h3 pole normals."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_COMPONENT21_OTHER_SINGLE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py"
)
DEPENDENCIES = {
    "claims/p5/frontier/P5_COMPONENT21_NORMALIZED_PARAMETER_COMPACTIFICATION_COMPLETE_OBSTRUCTION.md": (
        "77bc53e3451358bfc4764fce5e82f870040bf63846b556522a25e6e95d4da8e7"
    ),
    "claims/p5/frontier/verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "c4cebc5eb8ea6f1fe63e83d9ad472c1208cce880dff32b1c8fb75682e78c9ecb"
    ),
    "claims/p5/frontier/audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py": (
        "3336ca78627ca3bc6ef7d69954be7319e7948a7733c52eb5da6a8ad2d9c5c541"
    ),
}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
ZERO = (sp.Integer(0),) * 4
CAP_A = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
CAP_C = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
CAP_B = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
CAP_D = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))


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
        selected = tuple(beta[index] if word[index] else alpha[index] for index in range(4))
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
    return (
        combine(1, CAP_A, p, CAP_B),
        combine(ell, CAP_A, 1, CAP_C),
        CAP_C,
        CAP_D,
    ), (
        combine(1, CAP_C, q, CAP_B),
        CAP_A,
        combine(1, CAP_B, kappa, CAP_A),
        combine(1, CAP_A, ell, CAP_C),
    )


def other_shifts(
    mode: int,
    shifts: tuple[sp.Expr, ...],
) -> tuple[sp.Expr, ...]:
    return tuple(sp.Integer(0) if index == mode else shifts[index] for index in range(4))


def homogeneous_chart(
    mode: int,
    s: sp.Expr,
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(mark(alpha, canonical_beta, other_shifts(mode, shifts)))
    beta[mode] = combine(1, alpha[mode], s, canonical_beta[mode])
    return alpha, tuple(beta)


def first_normal(
    mode: int,
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(mark(alpha, canonical_beta, other_shifts(mode, shifts)))
    alpha = list(alpha)
    alpha[mode] = ZERO
    beta[mode] = canonical_beta[mode]
    return tuple(alpha), tuple(beta)


def weighted_normal(
    mode: int,
    cap_p: sp.Expr,
    cap_q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(0, 0, kappa, ell)
    beta = list(mark(alpha, canonical_beta, other_shifts(mode, shifts)))
    alpha = list(alpha)
    alpha[0] = combine(cap_p, CAP_B, 0, CAP_B)
    beta[0] = combine(shifts[0] * cap_p + cap_q, CAP_B, 0, CAP_B)
    alpha[mode] = ZERO
    beta[mode] = canonical_beta[mode]
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
    p, q, kappa, ell, s, cap_p, cap_q = sp.symbols("p q kappa ell s P Q")
    shifts = sp.symbols("h0:4")
    audited = {}
    for mode in (1, 2, 3):
        retained = (p, q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index != mode
        )
        chart_alpha, chart_beta = homogeneous_chart(
            mode, s, p, q, kappa, ell, shifts
        )
        chart_support = support(chart_alpha, chart_beta)
        assert chart_support == {
            "0111": "4*p*s",
            "1111": "4*s*(h0*p + q)",
        }
        boundary_alpha, boundary_beta = homogeneous_chart(
            mode, 0, p, q, kappa, ell, shifts
        )
        assert support(boundary_alpha, boundary_beta) == {}

        normal_alpha, normal_beta = first_normal(
            mode, p, q, kappa, ell, shifts
        )
        normal_support = support(normal_alpha, normal_beta)
        assert normal_support == {
            "0111": "4*p",
            "1111": "4*(h0*p + q)",
        }
        first_certificates = four_certificates(
            f"h{mode}_first_normal",
            normal_alpha,
            normal_beta,
            retained,
        )

        weighted_alpha, weighted_beta = weighted_normal(
            mode, cap_p, cap_q, kappa, ell, shifts
        )
        weighted_support = support(weighted_alpha, weighted_beta)
        assert weighted_support == {
            "0111": "4*P",
            "1111": "4*(P*h0 + Q)",
        }
        weighted_retained = (cap_p, cap_q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index != mode
        )
        weighted_certificates = four_certificates(
            f"h{mode}_sp_sq_weighted_normal",
            weighted_alpha,
            weighted_beta,
            weighted_retained,
        )
        audited[f"h{mode}_infinity"] = {
            "homogeneous_chart_pure_support": chart_support,
            "boundary_pure_support": {},
            "first_normal_pair_at_mode": ["0", f"b{mode}"],
            "first_normal_pure_support": normal_support,
            "first_normal_zero_locus": "p=q=0",
            "first_normal_unit_ideals": first_certificates,
            "sp_sq_weighted_normal_mode0_pair": [
                "P*B",
                "(h0*P+Q)*B",
            ],
            "sp_sq_weighted_normal_pure_support": weighted_support,
            "sp_sq_weighted_normal_unit_ideals": weighted_certificates,
        }

    for filename, expected in DEPENDENCIES.items():
        assert sha256(ROOT / filename) == expected
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "single-pole charts `h1=infinity`, `h2=infinity`, and `h3=infinity`",
        "monomial `(s_i p,s_i q)` normal",
        "simultaneous marking poles remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    completed = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=REPO_ROOT,
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
    assert primary_output["charts"] == audited
    assert primary_output["pure_support_transfer_used"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP and Groebner audit",
                "field": "exact characteristic zero",
                "single_marking_infinity_modes": [1, 2, 3],
                "charts": audited,
                "dvr_puiseux_order": "min(v(s_i)+v(p), v(s_i)+v(q))",
                "dependency_hashes_verified": True,
                "primary_replay_passed": True,
                "pure_support_transfer_used": False,
                "simultaneous_marking_poles_closed": False,
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
