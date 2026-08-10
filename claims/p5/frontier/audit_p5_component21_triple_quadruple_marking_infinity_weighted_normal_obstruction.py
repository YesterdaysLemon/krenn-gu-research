#!/usr/bin/env python3
"""Independent audit of component 21's triple/quadruple marking poles."""

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
    / "P5_COMPONENT21_TRIPLE_QUADRUPLE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md"
)
PRIMARY = (
    ROOT
    / "verify_p5_component21_triple_quadruple_marking_infinity_weighted_normal_obstruction.py"
)
DEPENDENCIES = {
    "claims/p5/frontier/P5_COMPONENT21_PAIRWISE_MARKING_INFINITY_WEIGHTED_NORMAL_OBSTRUCTION.md": (
        "c3912db0023f703d92bf98343478ae4d332d93b4a0eda7d902fa2a0ae099728c"
    ),
    "claims/p5/frontier/verify_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py": (
        "d3fd735b6798aa99888ae74136394d3b6602a8ff59031770f6237b5dab997fad"
    ),
    "claims/p5/frontier/audit_p5_component21_pairwise_marking_infinity_weighted_normal_obstruction.py": (
        "a27e24c97e818acbec437ff8ee62089936eefd4355acdcd46613a0bc0fd1e5c0"
    ),
}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
ZERO = (sp.Integer(0),) * 4
CAP_A = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
CAP_C = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
CAP_B = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
CAP_D = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
POLE_SETS = ((1, 2, 3), (0, 1, 2), (0, 1, 3), (0, 2, 3), (0, 1, 2, 3))


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
        rows = tuple(beta[index] if word[index] else alpha[index] for index in range(4))
        coefficient = sp.factor(permanent_dp(rows))
        if coefficient != 0:
            result["".join(map(str, word))] = str(coefficient)
    return result


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


def marked_rows(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    canonical_beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(combine(1, canonical_beta[i], shifts[i], alpha[i]) for i in range(4))


def marking_chart(
    poles: tuple[int, ...],
    inverse_markings: tuple[sp.Expr, ...],
    p: sp.Expr,
    q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(p, q, kappa, ell)
    beta = list(
        marked_rows(
            alpha,
            canonical_beta,
            tuple(0 if index in poles else shifts[index] for index in range(4)),
        )
    )
    for index in poles:
        beta[index] = combine(
            1, alpha[index], inverse_markings[index], canonical_beta[index]
        )
    return alpha, tuple(beta)


def weighted_normal(
    poles: tuple[int, ...],
    cap_p: sp.Expr,
    cap_q: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    alpha, canonical_beta = finite_bases(0, 0, kappa, ell)
    beta = list(
        marked_rows(
            alpha,
            canonical_beta,
            tuple(0 if index in poles else shifts[index] for index in range(4)),
        )
    )
    alpha = list(alpha)
    alpha[0] = combine(cap_p, CAP_B, 0, CAP_B)
    if 0 in poles:
        beta[0] = combine(cap_p + cap_q, CAP_B, 0, CAP_B)
        nonzero_poles = tuple(index for index in poles if index != 0)
    else:
        beta[0] = combine(shifts[0] * cap_p + cap_q, CAP_B, 0, CAP_B)
        nonzero_poles = poles
    for index in nonzero_poles:
        alpha[index] = ZERO
        beta[index] = canonical_beta[index]
    return tuple(alpha), tuple(beta)


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
            beta_rows[index] if word[index] else alpha_rows[index]
            for index in range(4)
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


def obstruction_rows(
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


def unit_groebner(
    label: str,
    equations: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
) -> dict[str, int | bool]:
    basis = sp.groebner(equations, *variables, order="grevlex")
    is_unit = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
    assert is_unit, label
    return {"equations": len(equations), "variables": len(variables), "unit": True}


def h22_certificates(
    prefix: str,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    retained: tuple[sp.Symbol, ...],
) -> dict[str, dict[str, int | bool]]:
    slope = sp.Symbol("lambda")
    extension = sp.symbols("z0:8")
    inverse_a, inverse_b = sp.symbols("u w")
    results = {}
    for chart in ("finite", "infinity"):
        _, _, d01 = contraction(alpha, beta, extension, "D01", chart, slope)
        d23_alpha, d23_beta, d23 = contraction(
            alpha, beta, extension, "D23", chart, slope
        )
        assert sp.expand(d01[WORDS[0]]) == 0
        vector = sp.Matrix(extension)
        mixed_matrix = sp.Matrix(
            [[sp.diff(d23[word], value) for value in extension] for word in MIXED]
        )
        equations = (
            *(d01[word] for word in WORDS[:-1]),
            sp.expand(d01[WORDS[-1]] - 1),
            *tuple(mixed_matrix * vector),
            sp.expand(inverse_a * d23[WORDS[0]] - 1),
            sp.expand(inverse_b * d23[WORDS[-1]] - 1),
            *tuple(obstruction_rows(d23_alpha, d23_beta)),
        )
        chart_retained = retained + ((slope,) if chart == "finite" else ())
        label = f"{prefix}_H22_{chart}_weight"
        results[label] = unit_groebner(
            label,
            equations,
            extension + (inverse_a, inverse_b) + chart_retained,
        )
    return results


def main() -> None:
    p, q, kappa, ell, cap_p, cap_q = sp.symbols("p q kappa ell P Q")
    inverse_markings = sp.symbols("s0:4")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    audited = {}
    for poles in POLE_SETS:
        label = "_".join(f"h{index}" for index in poles) + "_infinity"
        chart_alpha, chart_beta = marking_chart(
            poles, inverse_markings, p, q, kappa, ell, shifts
        )
        chart_support = support(chart_alpha, chart_beta)
        nonzero_poles = tuple(index for index in poles if index != 0)
        product_s = sp.prod(inverse_markings[index] for index in nonzero_poles)
        if 0 in poles:
            expected_chart = {
                "0111": str(sp.factor(4 * product_s * p)),
                "1111": str(
                    sp.factor(4 * product_s * (p + inverse_markings[0] * q))
                ),
            }
            order = "min(v(S)+v(p), v(s_0)+v(S)+v(q))"
            monomials = ("S*p", "s_0*S*q")
        else:
            expected_chart = {
                "0111": str(sp.factor(4 * product_s * p)),
                "1111": str(sp.factor(4 * product_s * (shifts[0] * p + q))),
            }
            order = "min(v(S)+v(p), v(S)+v(q))"
            monomials = ("S*p", "S*q")
        assert chart_support == expected_chart
        boundary_inverse = tuple(
            sp.Integer(0) if index in poles else inverse_markings[index]
            for index in range(4)
        )
        boundary_alpha, boundary_beta = marking_chart(
            poles, boundary_inverse, p, q, kappa, ell, shifts
        )
        assert support(boundary_alpha, boundary_beta) == {}

        normal_alpha, normal_beta = weighted_normal(
            poles, cap_p, cap_q, kappa, ell, shifts
        )
        normal_support = support(normal_alpha, normal_beta)
        if 0 in poles:
            expected_normal = {"0111": "4*P", "1111": "4*(P + Q)"}
        else:
            expected_normal = {"0111": "4*P", "1111": "4*(P*h0 + Q)"}
        assert normal_support == expected_normal
        hall = {}
        for distinguished in range(4):
            all_alpha = h31_coefficients(
                distinguished, normal_alpha, normal_beta, extension
            )[WORDS[0]]
            assert sp.expand(all_alpha) == 0
            hall[f"distinguished_{distinguished}"] = True
        retained = (cap_p, cap_q, kappa, ell) + tuple(
            shifts[index] for index in range(4) if index not in poles
        )
        certificates = h22_certificates(
            "_".join(f"h{index}" for index in poles) + "_weighted_normal",
            normal_alpha,
            normal_beta,
            retained,
        )
        audited[label] = {
            "poles": list(poles),
            "homogeneous_chart_pure_support": chart_support,
            "corner_pure_support": {},
            "controlling_monomials": list(monomials),
            "dvr_puiseux_order": order,
            "weighted_normal_pure_support": normal_support,
            "h31_all_alpha_hall_deficiencies": hall,
            "h22_weighted_normal_unit_ideals": certificates,
        }

    for filename, expected in DEPENDENCIES.items():
        assert sha256(ROOT / filename) == expected
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "the four triple and one quadruple simultaneous marking-pole corners",
        "all-alpha diagonal is identically zero",
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
        timeout=180,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    primary_output = json.loads(completed.stdout)
    assert primary_output["status"] == "pass"
    assert primary_output["charts"] == audited
    assert primary_output["h31_hall_deficient_orientations"] == 20
    assert primary_output["h22_unit_ideals"] == 10
    assert primary_output["pure_support_transfer_used"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP and Groebner audit",
                "field": "exact characteristic zero",
                "triple_quadruple_marking_infinity_pole_sets": [
                    list(poles) for poles in POLE_SETS
                ],
                "charts": audited,
                "h31_hall_deficient_orientations": 20,
                "h22_unit_ideals": 10,
                "dependency_hashes_verified": True,
                "primary_replay_passed": True,
                "pure_support_transfer_used": False,
                "all_triple_quadruple_nonzero_P4_weighted_normals_closed": True,
                "parameter_boundary_intersections_closed": False,
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
