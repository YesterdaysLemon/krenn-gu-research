#!/usr/bin/env python3
"""Verify component 21's p=q=0 first-normal blow-up transport."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp
import sys

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
VERTICAL_THEOREM = (
    REPO_ROOT / 'claims/p5/boundaries/P5_COMPONENT21_VERTICAL_U0_PROJECTIVE_BOUNDARY_COMPLETE_OBSTRUCTION.md'
)
VERTICAL_PRIMARY = (
    REPO_ROOT / 'claims/p5/boundaries/verify_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py'
)
VERTICAL_AUDIT = (
    REPO_ROOT / 'claims/p5/boundaries/audit_p5_component21_vertical_u0_projective_boundary_complete_obstruction.py'
)
P4_THEOREM = REPO_ROOT / 'claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md'
P4_PRIMARY = REPO_ROOT / 'claims/p4/classifications/star/coincident-support-rank-one-star/verify_p4_coincident_support_rank_one_star_component.py'
PINNED = {
    VERTICAL_THEOREM: "c95e70fa3e553be9b5a0bfcb052f05cf667e41366edec021e9aa1ea240cfef36",
    VERTICAL_PRIMARY: "3865eaaa58259be64317141870e0fd51b6c9f4b425d369d6e93904404a99e70a",
    VERTICAL_AUDIT: "5eb84e710ef524dd6d2f9fe193c4c67309c89e636df780ebb0d5a6e8662d4065",
    P4_THEOREM: "11422585ed24db3c3a1dd727a648267237d0624fe8574567859e404a6aabc18b",
    P4_PRIMARY: "a170054715c8fc8ec7f1fc1e0dba896c0fdc7d72ed58e41e7f9b8bba23af4adf",
}
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def permanent4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS
        )
    )


def permanent3(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def pure_support(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, str]:
    support = {}
    for word in WORDS:
        rows = tuple(beta[index] if word[index] else alpha[index] for index in range(4))
        coefficient = sp.factor(permanent4(rows))
        if coefficient != 0:
            support["".join(map(str, word))] = str(coefficient)
    return support


def wedge(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] - left[j] * right[i])
            for i in range(4)
            for j in range(i + 1, 4)
        ]
    )


def mark(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


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
        word: permanent4(
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
            row.append(permanent4(square_rows))  # type: ignore[arg-type]
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
                * permanent3(
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
                permanent3(
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
            add(cap_b, scale(kappa, cap_a)),
            cap_c,
        )
    return (
        cap_c,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    ), (
        cap_b,
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
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

    row_00 = add(cap_a, scale(p, cap_b))
    row_01 = add(cap_c, scale(q, cap_b))
    regular_alpha = (
        row_00,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    regular_beta = (
        row_01,
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )
    regular_support = pure_support(regular_alpha, regular_beta)
    assert regular_support == {"0111": "4*p", "1111": "4*q"}

    pluecker_difference = sp.simplify(
        wedge(row_00, row_01)
        - wedge(cap_a, cap_c)
        - q * wedge(cap_a, cap_b)
        - p * wedge(cap_b, cap_c)
    )
    assert pluecker_difference == sp.zeros(6, 1)

    exceptional_plane = add(scale(cap_q, cap_a), scale(-cap_p, cap_c))
    exceptional_pluecker = cap_q * wedge(cap_a, cap_b) + cap_p * wedge(cap_b, cap_c)
    assert wedge(exceptional_plane, cap_b) == exceptional_pluecker

    finite_plane = add(cap_a, scale(-alpha_parameter, cap_c))
    assert sp.simplify(
        wedge(exceptional_plane, cap_b).subs(cap_p, alpha_parameter * cap_q)
        - cap_q * wedge(finite_plane, cap_b)
    ) == sp.zeros(6, 1)
    assert wedge(exceptional_plane, cap_b).subs({cap_p: 0, cap_q: 1}) == wedge(
        cap_a, cap_b
    )
    assert wedge(exceptional_plane, cap_b).subs({cap_p: 1, cap_q: 0}) == -wedge(
        cap_c, cap_b
    )

    vertical_finite_alpha = (
        finite_plane,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    vertical_finite_beta = (
        cap_b,
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )
    alpha_infinity_finite_alpha = (
        cap_c,
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    alpha_infinity_finite_beta = (
        cap_b,
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )
    alpha_infinity_corner_alpha = (cap_c, cap_a, cap_c, cap_d)
    alpha_infinity_corner_beta = (
        cap_b,
        cap_c,
        add(cap_b, scale(kappa, cap_a)),
        cap_c,
    )
    finite_support = pure_support(vertical_finite_alpha, vertical_finite_beta)
    alpha_infinity_finite_support = pure_support(
        alpha_infinity_finite_alpha, alpha_infinity_finite_beta
    )
    alpha_infinity_corner_support = pure_support(
        alpha_infinity_corner_alpha, alpha_infinity_corner_beta
    )
    assert finite_support == {"1111": "4"}
    assert alpha_infinity_finite_support == {"1111": "4"}
    assert alpha_infinity_corner_support == {"1111": "-4"}
    endpoint_certificates = alpha_infinity_unit_certificates()

    dependency_hashes = {path.name: sha256(path) for path in PINNED}
    assert all(sha256(path) == expected for path, expected in PINNED.items())
    theorem_text = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for required in (
        "central zero tensor without a nonzero normal direction",
        "arbitrary ambient, source, or projective degenerations",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    ):
        assert required in theorem_text

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "component": 21,
                "regular_chart_pure_support": regular_support,
                "central_p_equals_q_equals_zero_tensor": "zero",
                "pluecker_normal_identity": True,
                "exceptional_divisor": "[P:Q] -> <Q*A-P*C,B>",
                "finite_chart": "alpha=P/Q",
                "alpha_zero": "[P:Q]=[0:1]",
                "alpha_infinity": "[P:Q]=[1:0]",
                "vertical_pure_support": {
                    "finite_alpha": finite_support,
                    "alpha_infinity_finite_ell": alpha_infinity_finite_support,
                    "alpha_infinity_ell_infinity": alpha_infinity_corner_support,
                },
                "alpha_infinity_direct_unit_ideals": endpoint_certificates,
                "dvr_puiseux_valuation_cover": [
                    "v(p)>v(q): alpha=0",
                    "v(p)=v(q): alpha finite nonzero",
                    "v(p)<v(q): alpha=infinity",
                ],
                "dependency_hashes": dependency_hashes,
                "first_normal_marked_H31_empty": True,
                "first_normal_weighted_H22_empty": True,
                "central_zero_tensor_closed": False,
                "arbitrary_ambient_source_projective_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": sha256(THEOREM),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
