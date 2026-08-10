#!/usr/bin/env python3
"""Independent rational audit of component-21 divisor-generic obstructions."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_DIVISOR_GENERIC_FIBRE_OBSTRUCTIONS.md"
PRIMARY = ROOT / "verify_p5_component21_divisor_generic_fibre_obstructions.py"
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def permanent(rows):
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def add(left, right, coefficient=1):
    return tuple(left[i] + coefficient * right[i] for i in range(4))


def shifted(beta, alpha, h):
    return tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def component_bases(kind):
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    if kind == "p0":
        return (A, add(C, A, 2), C, D), (add(C, B, 2), A, add(B, A, 3), add(A, C, 2))
    if kind == "q0":
        return (C, add(C, A, 2), C, D), (add(A, B, 2), A, add(B, A, 3), add(A, C, 2))
    if kind == "mode3":
        return (add(tuple(3 * value for value in A), C, -2), A, C, D), (
            add(A, B, 2),
            C,
            add(B, A, 1),
            C,
        )
    if kind == "vertical":
        return (add(A, C, -1), add(C, A, 2), C, D), (
            B,
            A,
            add(B, A, 2),
            add(A, C, 2),
        )
    raise ValueError(kind)


def projected_rows(q, extension, alpha, beta):
    common = tuple(index for index in range(4) if index != q)
    return (
        tuple(tuple(alpha[i][j] for j in common) + (extension[i],) for i in range(4)),
        tuple(tuple(beta[i][j] for j in common) + (extension[4 + i],) for i in range(4)),
    )


def contraction_rows(direction, chart, slope, extension, rows, offset):
    output = []
    for i, row in enumerate(rows):
        e = extension[offset + i]
        if chart == "finite" and direction == "D01":
            output.append((slope * row[0] + row[1], row[2], row[3], e))
        elif chart == "finite" and direction == "D23":
            output.append((row[0], row[1], slope * row[2] + row[3], e))
        elif chart == "infinity" and direction == "D01":
            output.append((row[0], row[2], row[3], e))
        elif chart == "infinity" and direction == "D23":
            output.append((row[0], row[1], row[2], e))
        else:
            raise ValueError((direction, chart))
    return tuple(output)


def tensor(alpha, beta):
    return {
        bits: permanent(tuple(beta[i] if bits[i] else alpha[i] for i in range(4)))
        for bits in BITS4
    }


def mixed_rows(alpha, beta, variables):
    coefficients = tensor(alpha, beta)
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[bits], variable) for variable in variables]
            for bits in BITS4
            if bits not in (BITS4[0], BITS4[-1])
        ]
    )
    diagonals = tuple(
        sp.Matrix([[sp.diff(coefficients[bits], variable) for variable in variables]])
        for bits in (BITS4[0], BITS4[-1])
    )
    return mixed, *diagonals


def one_marked(mode, alpha, beta):
    result = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(
                permanent(
                    tuple(basis if other == mode else selected[other] for other in range(4))
                )
            )
        result.append(row)
    return sp.Matrix(result)


def pure_support(alpha, beta):
    return {bits: value for bits, value in tensor(alpha, beta).items() if value != 0}


def h31_rank_diagnostics(alpha, canonical):
    h = (1, 2, 3, 4)
    beta = shifted(canonical, alpha, h)
    z = sp.symbols("z0:8")
    ranks = []
    for q in range(4):
        alpha_p, beta_p = projected_rows(q, z, alpha, beta)
        mixed, d0, d1 = mixed_rows(alpha_p, beta_p, z)
        ranks.append((mixed.rank(), mixed.col_join(d0).rank(), mixed.col_join(d1).rank()))
    return ranks


def main():
    theorem = THEOREM.read_text(encoding="utf-8")
    primary = PRIMARY.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero theorem on four component divisors",
        "remain separate and **UNKNOWN**",
        "broader uniform polynomial attempt timed out",
    ):
        assert phrase in theorem
    assert '"all_exceptional_intersections_closed": False' in primary

    supports = {}
    rank_diagnostics = {}
    for kind, expected in (("p0", 8), ("q0", 8), ("mode3", -8)):
        alpha, beta = component_bases(kind)
        support = pure_support(alpha, beta)
        assert support == {(1, 1, 1, 1): expected}
        supports[kind] = str(expected)
        ranks = h31_rank_diagnostics(alpha, beta)
        assert [entry[0] for entry in ranks] == [2, 2, 7, 7]
        assert [entry[1] for entry in ranks] == [2, 2, 7, 7]
        assert [entry[2] for entry in ranks] == [3, 3, 8, 8]
        rank_diagnostics[kind] = ranks

    alpha, canonical = component_bases("vertical")
    assert pure_support(alpha, canonical) == {(1, 1, 1, 1): 4}
    E = 9
    marking = (0, sp.Rational(-1, 3), 4, 0)
    beta = shifted(canonical, alpha, marking)
    z_symbols = sp.symbols("z0:8")
    s, w, cap_c, lam = sp.symbols("s w C lam")
    e0 = sp.Matrix((-3, 0, 2, 0, 0, 1, 0, 0))
    h31 = []
    for q, sign in ((2, 1), (3, -1)):
        e1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        vector = s * e0 + w * e1
        alpha_p, beta_p = projected_rows(q, vector, alpha, beta)
        coefficients = tensor(alpha_p, beta_p)
        assert all(
            value == 0
            for bits, value in coefficients.items()
            if bits not in (BITS4[0], BITS4[-1])
        )
        d0 = sp.factor(coefficients[BITS4[0]])
        d1 = sp.factor(coefficients[BITS4[-1]])
        assert d0 == -sign * 2 * E * s
        assert sp.factor(d1 + 2 * (6 * s - 2 * w)) == 0
        determinant = sp.factor(one_marked(3, alpha_p, beta_p).extract((0, 4, 6, 7), range(4)).det())
        assert sp.factor(determinant - (-sign) * 2 * s * d0 * d1) == 0
        assert one_marked(3, alpha, beta)[4, q] == -2
        h31.append({"q": q, "diagonals": [str(d0), str(d1)]})

    h22 = []
    for chart in ("finite", "infinity"):
        slope = lam if chart == "finite" else None
        alpha01 = contraction_rows("D01", chart, slope, z_symbols, alpha, 0)
        beta01 = contraction_rows("D01", chart, slope, z_symbols, beta, 4)
        alpha23 = contraction_rows("D23", chart, slope, z_symbols, alpha, 0)
        beta23 = contraction_rows("D23", chart, slope, z_symbols, beta, 4)
        tensor01 = tensor(alpha01, beta01)
        tensor23 = tensor(alpha23, beta23)
        substitution = dict(zip(z_symbols, cap_c * e0, strict=True))
        b01 = sp.factor(tensor01[BITS4[-1]].subs(substitution))
        a23 = sp.factor(tensor23[BITS4[0]].subs(substitution))
        b23 = sp.factor(tensor23[BITS4[-1]].subs(substitution))
        marked23 = one_marked(3, alpha23, beta23).subs(substitution)
        determinant = sp.factor(marked23.extract((0, 4, 6, 7), range(4)).det())
        if chart == "finite":
            assert b01 == 2 * cap_c * (3 * lam - 1)
            assert a23 == 18 * cap_c * (lam - 1)
            assert b23 == -12 * cap_c * (lam + 1)
            assert determinant == -432 * cap_c**3 * (lam + 1) ** 3
        else:
            assert b01 == 6 * cap_c
            assert a23 == 18 * cap_c
            assert b23 == -12 * cap_c
            assert determinant == -432 * cap_c**3
        h22.append({"chart": chart, "diagonals": [str(b01), str(a23), str(b23)], "minor": str(determinant)})

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import rational audit",
                "pure_supports": supports | {"vertical": "4"},
                "H31_rank_diagnostics": rank_diagnostics,
                "vertical_H31": h31,
                "vertical_H22": h22,
                "all_exceptional_intersections_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
