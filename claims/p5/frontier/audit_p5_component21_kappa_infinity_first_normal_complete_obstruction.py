#!/usr/bin/env python3
"""No-import audit of component 21's normalized kappa-infinity atlas."""

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
THEOREM = ROOT / "P5_COMPONENT21_KAPPA_INFINITY_FIRST_NORMAL_COMPLETE_OBSTRUCTION.md"
PRIMARY = (
    ROOT / "verify_p5_component21_kappa_infinity_first_normal_complete_obstruction.py"
)
DEPENDENCIES = {
    "claims/p5/frontier/P5_COMPONENT21_PQ_ZERO_NORMAL_BLOWUP_TRANSFER_OBSTRUCTION.md": (
        "efcaac7d95ead192dfd4fd6167d3ee1c47eaaddef746fe5c0da85033ab132c1a"
    ),
    "claims/p5/frontier/verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "2f2b64ccf1aca2e6960d8bc4c21a57be2e9cf601d192d85f7e15255b8fa9f697"
    ),
    "claims/p5/frontier/audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py": (
        "e7f8c89c5437f8c3369563820e44e404f3f0603210b99fa1f26c831ecb541dc7"
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


def pluecker(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]):
    return {
        (i, j): sp.expand(left[i] * right[j] - left[j] * right[i])
        for i in range(4)
        for j in range(i + 1, 4)
    }


def mark(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
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


def bases(
    p: sp.Symbol,
    q: sp.Symbol,
    ell: sp.Symbol,
    ell_infinity: bool,
    regular_t: sp.Expr | None,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    row_00 = combine(1, cap_a, p, cap_b)
    row_01 = combine(1, cap_c, q, cap_b)
    mode_2_beta = cap_b if regular_t is None else combine(1, cap_a, regular_t, cap_b)
    if ell_infinity:
        return (row_00, cap_a, cap_c, cap_d), (
            row_01,
            cap_c,
            mode_2_beta,
            cap_c,
        )
    return (
        row_00,
        combine(ell, cap_a, 1, cap_c),
        cap_c,
        cap_d,
    ), (
        row_01,
        cap_a,
        mode_2_beta,
        combine(1, cap_a, ell, cap_c),
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


def direct_certificates() -> dict[str, dict[str, int | bool]]:
    p, q, ell, slope = sp.symbols("p q ell lambda")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse, inverse_a, inverse_b = sp.symbols("v u w")
    results = {}
    for ell_infinity in (False, True):
        alpha, canonical_beta = bases(p, q, ell, ell_infinity, None)
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
            retained = (p, q) + (() if ell_infinity else (ell,)) + shifts
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
            retained = (p, q) + (() if ell_infinity else (ell,)) + shifts
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
    p, q, ell, t, cap_p, cap_q, h2, y2 = sp.symbols("p q ell t P Q h2 y2")
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    raw_finite = bases(p, q, ell, False, t)
    raw_infinity = bases(p, q, ell, True, t)
    sheet_finite = bases(p, q, ell, False, None)
    sheet_infinity = bases(p, q, ell, True, None)
    assert support(*raw_finite) == {"0111": "4*p*t", "1111": "4*q*t"}
    assert support(*raw_infinity) == {
        "0111": "-4*p*t",
        "1111": "-4*q*t",
    }
    assert support(*sheet_finite) == {"0111": "4*p", "1111": "4*q"}
    assert support(*sheet_infinity) == {
        "0111": "-4*p",
        "1111": "-4*q",
    }

    raw_pluecker = pluecker(cap_c, combine(1, cap_a, t, cap_b))
    base_pluecker = pluecker(cap_c, cap_a)
    normal_pluecker = pluecker(cap_c, cap_b)
    assert {
        key: sp.expand(raw_pluecker[key] - base_pluecker[key]) for key in raw_pluecker
    } == {key: sp.expand(t * value) for key, value in normal_pluecker.items()}

    regular_marked_extended = sp.Matrix(
        (*combine(1, cap_a, t, combine(1, cap_b, h2, cap_c)), t * y2)
    )
    assert sp.simplify(
        (regular_marked_extended - sp.Matrix((*cap_a, 0))) / t
        - sp.Matrix((*combine(1, cap_b, h2, cap_c), y2))
    ) == sp.zeros(5, 1)

    double_finite = (
        (
            combine(cap_q, cap_a, -cap_p, cap_c),
            combine(ell, cap_a, 1, cap_c),
            cap_c,
            cap_d,
        ),
        (cap_b, cap_a, cap_b, combine(1, cap_a, ell, cap_c)),
    )
    double_infinity = (
        (combine(cap_q, cap_a, -cap_p, cap_c), cap_a, cap_c, cap_d),
        (cap_b, cap_c, cap_b, cap_c),
    )
    assert support(*double_finite) == {"1111": "4"}
    assert support(*double_infinity) == {"1111": "-4"}
    certificates = direct_certificates()

    for filename, expected in DEPENDENCIES.items():
        assert sha256(ROOT / filename) == expected
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    assert "source-marking infinity" in theorem_text
    assert "equality of pure tensors alone" in theorem_text
    assert "global Krenn--Gu conjecture remains **UNRESOLVED**" in theorem_text

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
    assert primary_output["finite_p_q_dvr_puiseux_cover_complete"] is True
    assert primary_output["arbitrary_source_extension_projective_closed"] is False

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP and Groebner audit",
                "field": "exact characteristic zero",
                "raw_t_support": {
                    "finite_ell": support(*raw_finite),
                    "ell_infinity": support(*raw_infinity),
                },
                "mode_2_first_normal_pluecker_verified": True,
                "marking_extension_rees_row_identity": True,
                "direct_unit_ideals": certificates,
                "double_normal_vertical_kappa_zero_verified": True,
                "finite_p_q_dvr_puiseux_cover_complete": True,
                "p_q_poles_closed": False,
                "arbitrary_source_extension_projective_closed": False,
                "dependency_hashes_verified": True,
                "primary_replay_passed": True,
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
