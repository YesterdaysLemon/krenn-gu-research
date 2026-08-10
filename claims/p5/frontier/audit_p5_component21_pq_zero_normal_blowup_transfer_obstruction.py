#!/usr/bin/env python3
"""Independent no-import audit of the component-21 p=q=0 blow-up transfer."""

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
THEOREM = ROOT / "P5_COMPONENT21_PQ_ZERO_NORMAL_BLOWUP_TRANSFER_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py"
DEPENDENCIES = {
    "claims/p5/boundaries/P5_COMPONENT21_VERTICAL_U0_PROJECTIVE_BOUNDARY_COMPLETE_OBSTRUCTION.md": (
        "c95e70fa3e553be9b5a0bfcb052f05cf667e41366edec021e9aa1ea240cfef36"
    ),
    "claims/p5/boundaries/verify_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py": (
        "3865eaaa58259be64317141870e0fd51b6c9f4b425d369d6e93904404a99e70a"
    ),
    "claims/p5/boundaries/audit_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py": (
        "5eb84e710ef524dd6d2f9fe193c4c67309c89e636df780ebb0d5a6e8662d4065"
    ),
    "claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md": (
        "11422585ed24db3c3a1dd727a648267237d0624fe8574567859e404a6aabc18b"
    ),
    "claims/p4/classifications/star/coincident-support-rank-one-star/verify_p4_coincident_support_rank_one_star_component.py": (
        "a170054715c8fc8ec7f1fc1e0dba896c0fdc7d72ed58e41e7f9b8bba23af4adf"
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


def linear_combination(
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
            result["".join(str(bit) for bit in word)] = str(coefficient)
    return result


def pluecker(row_0: tuple[sp.Expr, ...], row_1: tuple[sp.Expr, ...]):
    return {
        (i, j): sp.expand(row_0[i] * row_1[j] - row_0[j] * row_1[i])
        for i in range(4)
        for j in range(i + 1, 4)
    }


def mark(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(linear_combination(1, beta[i], shifts[i], alpha[i]) for i in range(4))


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
        row = []
        for coordinate in range(4):
            basis = tuple(sp.Integer(index == coordinate) for index in range(4))
            square_rows = tuple(
                basis if other == mode else selected[other] for other in range(4)
            )
            assert all(item is not None for item in square_rows)
            row.append(permanent_dp(square_rows))  # type: ignore[arg-type]
        output.append(tuple(row))
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


def endpoint_bases(
    kappa: sp.Symbol,
    ell: sp.Symbol,
    ell_infinity: bool,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    if ell_infinity:
        return (cap_c, cap_a, cap_c, cap_d), (
            cap_b,
            cap_c,
            linear_combination(1, cap_b, kappa, cap_a),
            cap_c,
        )
    return (
        cap_c,
        linear_combination(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    ), (
        cap_b,
        cap_a,
        linear_combination(1, cap_b, kappa, cap_a),
        linear_combination(1, cap_a, ell, cap_c),
    )


def unit_groebner(
    label: str,
    equations: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
) -> dict[str, int | bool]:
    basis = sp.groebner(equations, *variables, order="grevlex")
    is_unit = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
    assert is_unit, label
    return {"equations": len(equations), "variables": len(variables), "unit": True}


def alpha_infinity_unit_certificates() -> dict[str, dict[str, int | bool]]:
    kappa, ell, slope = sp.symbols("kappa ell lambda")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse, inverse_a, inverse_b = sp.symbols("v u w")
    results = {}
    for ell_infinity in (False, True):
        alpha, canonical_beta = endpoint_bases(kappa, ell, ell_infinity)
        beta = mark(alpha, canonical_beta, shifts)
        ell_label = "ell_infinity" if ell_infinity else "finite_ell"
        for distinguished in (0, 1):
            coefficients = h31_coefficients(distinguished, alpha, beta, extension)
            assert coefficients[WORDS[0]] == 0
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
            retained = (kappa,) + (() if ell_infinity else (ell,)) + shifts
            label = f"H31_{ell_label}_d{distinguished}"
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
            retained = (kappa,) + (() if ell_infinity else (ell,)) + shifts
            if chart == "finite":
                retained += (slope,)
            label = f"H22_{ell_label}_{chart}_weight"
            results[label] = unit_groebner(
                label,
                equations,
                extension + (inverse_a, inverse_b) + retained,
            )
    assert len(results) == 8
    return results


def main() -> None:
    p, q, kappa, ell, cap_p, cap_q, alpha_parameter = sp.symbols(
        "p q kappa ell P Q alpha"
    )
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    row_00 = linear_combination(1, cap_a, p, cap_b)
    row_01 = linear_combination(1, cap_c, q, cap_b)
    alpha = (
        row_00,
        linear_combination(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    )
    beta = (
        row_01,
        cap_a,
        linear_combination(1, cap_b, kappa, cap_a),
        linear_combination(1, cap_a, ell, cap_c),
    )
    regular_support = support(alpha, beta)
    assert regular_support == {"0111": "4*p", "1111": "4*q"}

    base_pluecker = pluecker(cap_a, cap_c)
    family_pluecker = pluecker(row_00, row_01)
    first_normal = {
        key: sp.expand(
            (family_pluecker[key] - base_pluecker[key]).subs({p: cap_p, q: cap_q})
        )
        for key in base_pluecker
    }
    exceptional_row = linear_combination(cap_q, cap_a, -cap_p, cap_c)
    exceptional_pluecker = pluecker(exceptional_row, cap_b)
    assert first_normal == exceptional_pluecker

    finite_row = linear_combination(1, cap_a, -alpha_parameter, cap_c)
    finite_pluecker = pluecker(finite_row, cap_b)
    assert {
        key: sp.expand(exceptional_pluecker[key].subs(cap_p, alpha_parameter * cap_q))
        for key in exceptional_pluecker
    } == {key: sp.expand(cap_q * value) for key, value in finite_pluecker.items()}
    assert {
        key: value.subs({cap_p: 0, cap_q: 1})
        for key, value in exceptional_pluecker.items()
    } == pluecker(cap_a, cap_b)
    assert {
        key: value.subs({cap_p: 1, cap_q: 0})
        for key, value in exceptional_pluecker.items()
    } == {key: -value for key, value in pluecker(cap_c, cap_b).items()}

    vertical_alpha = (
        finite_row,
        linear_combination(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    )
    vertical_beta = (
        cap_b,
        cap_a,
        linear_combination(1, cap_b, kappa, cap_a),
        linear_combination(1, cap_a, ell, cap_c),
    )
    alpha_infinity_finite_alpha = (
        cap_c,
        linear_combination(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    )
    alpha_infinity_finite_beta = (
        cap_b,
        cap_a,
        linear_combination(1, cap_b, kappa, cap_a),
        linear_combination(1, cap_a, ell, cap_c),
    )
    alpha_infinity_corner_alpha = (cap_c, cap_a, cap_c, cap_d)
    alpha_infinity_corner_beta = (
        cap_b,
        cap_c,
        linear_combination(1, cap_b, kappa, cap_a),
        cap_c,
    )
    assert support(vertical_alpha, vertical_beta) == {"1111": "4"}
    assert support(alpha_infinity_finite_alpha, alpha_infinity_finite_beta) == {
        "1111": "4"
    }
    assert support(alpha_infinity_corner_alpha, alpha_infinity_corner_beta) == {
        "1111": "-4"
    }
    endpoint_certificates = alpha_infinity_unit_certificates()

    for filename, expected in DEPENDENCIES.items():
        assert sha256(REPO_ROOT / filename) == expected
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    assert "does **not** classify the central zero" in theorem_text
    assert "arbitrary-order local-to-global reduction remains open" in theorem_text
    assert "global Krenn--Gu conjecture remains **UNRESOLVED**" in theorem_text

    completed = subprocess.run(
        (sys.executable, str(PRIMARY)),
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    primary_output = json.loads(completed.stdout)
    assert primary_output["status"] == "pass"
    assert primary_output["first_normal_marked_H31_empty"] is True
    assert primary_output["first_normal_weighted_H22_empty"] is True
    assert primary_output["central_zero_tensor_closed"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP and Pluecker audit",
                "field": "exact characteristic zero",
                "regular_chart_pure_support": regular_support,
                "first_normal_equals_vertical_exceptional_plane": True,
                "projective_normal_charts": ["alpha=P/Q", "alpha=infinity"],
                "unequal_valuation_endpoints_covered": True,
                "alpha_infinity_direct_unit_ideals": endpoint_certificates,
                "dependency_hashes_verified": True,
                "primary_replay_passed": True,
                "first_normal_marked_H31_empty": True,
                "first_normal_weighted_H22_empty": True,
                "central_zero_tensor_closed": False,
                "arbitrary_ambient_source_projective_closed": False,
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
