#!/usr/bin/env python3
"""Verify exclusion of the secondary-gate H31 branch."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_SECONDARY_GATE_EXCLUSION.md"
RANK_TWO_M = (
    REPO_ROOT / "claims" / "p5" / "h31"
    / "single-gate-rank-two-m-exclusion"
    / "P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md"
)
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(
                rows[row][permutation[row]]
                for row in range(size)
            )
            for permutation in itertools.permutations(range(size))
        )
    )


def pair_product(
    first: tuple[sp.Expr, sp.Expr, sp.Expr],
    second: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> sp.Matrix:
    return sp.Matrix(
        [
            first[1] * second[2] + first[2] * second[1],
            first[0] * second[2] + first[2] * second[0],
            first[0] * second[1] + first[1] * second[0],
        ]
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    output = []
    for bits in BITS3:
        selected: list[tuple[sp.Expr, ...] | None] = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if bits[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                sp.Integer(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis
                        if other == mode
                        else selected[other]  # type: ignore[arg-type]
                        for other in range(4)
                    )
                )
            )
        output.append(coefficient_row)
    return sp.Matrix(output)


def combined_marked(
    mode: int,
    alpha_s: tuple[tuple[sp.Expr, ...], ...],
    beta_s: tuple[tuple[sp.Expr, ...], ...],
    alpha_p: tuple[tuple[sp.Expr, ...], ...],
    beta_p: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    source = one_marked_map(mode, alpha_s, beta_s)
    partial = one_marked_map(mode, alpha_p, beta_p)
    return (
        source[:, :3]
        .row_join(source[:, 3])
        .row_join(sp.zeros(8, 1))
        .col_join(
            partial[:, :3]
            .row_join(sp.zeros(8, 1))
            .row_join(partial[:, 3])
        )
    )


def coefficients(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, sp.Expr]:
    return {
        "".join(map(str, bits)): sp.factor(
            permanent(
                tuple(
                    beta[mode] if bits[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for bits in itertools.product((0, 1), repeat=4)
    }


def substitute_rows(
    rows: tuple[tuple[sp.Expr, ...], ...],
    substitutions: dict[sp.Expr, sp.Expr],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.sympify(entry).subs(substitutions)
            for entry in row
        )
        for row in rows
    )


def verify_line_plane() -> dict[str, object]:
    r, tau = sp.symbols("r tau", nonzero=True)
    a0, v0 = sp.symbols("a0 v0")
    T, X, C, D, E, F = sp.symbols("T X C D E F")
    g = sp.symbols("g", nonzero=True)

    alpha = (
        (0, 0, 0, 1),
        (a0, r, -tau, X),
        (1, 0, 0, C),
        (0, r, -tau, E),
    )
    beta = (
        (v0, r, tau, T),
        (0, 0, 0, g),
        (0, r, tau, D),
        (1, 0, 0, F),
    )
    values = coefficients(alpha, beta)
    assert values["0000"] == -2 * r * tau
    assert values["1111"] == 2 * g * r * tau
    assert values["1000"] == -2 * r * tau * (C * v0 + T)
    assert values["1001"] == 0
    assert values["1010"] == -2 * r * tau * (D * v0 - E * a0)
    assert values["1011"] == 2 * r * tau * (F * a0 + X)
    assert all(
        value == 0
        for word, value in values.items()
        if word not in ("0000", "1111", "1000", "1010", "1011")
    )

    marked = {
        mode: one_marked_map(mode, alpha, beta)
        for mode in range(4)
    }
    assert sp.factor(marked[2][[0, 1, 4, 7], :].det()) == (
        8 * g * r**3 * tau**3 * v0
    )
    assert sp.factor(marked[3][[0, 5, 6, 7], :].det()) == (
        -8 * a0 * g**2 * r**3 * tau**3
    )
    assert sp.factor(marked[1][[0, 3, 6, 7], :].det()) == (
        -8 * E * r**3 * tau**3
    )
    deepest_p = {
        a0: 0,
        v0: 0,
        E: 0,
        T: 0,
        X: 0,
    }
    assert sp.factor(
        marked[0].subs(deepest_p)[[0, 2, 4, 7], :].det()
    ) == 8 * D * g**2 * r**3 * tau**3

    Cs, Cp, Ds, Es, Fs, Fp = sp.symbols(
        "Cs Cp Ds Es Fs Fp"
    )
    gs, gp = sp.symbols("gs gp", nonzero=True)
    alpha_s = (
        (0, 0, 0, 0),
        (0, r, -tau, 0),
        (1, 0, 0, Cs),
        (0, r, -tau, Es),
    )
    beta_s = (
        (0, r, tau, 0),
        (0, 0, 0, gs),
        (0, r, tau, Ds),
        (1, 0, 0, Fs),
    )
    alpha_p = (
        (0, 0, 0, 1),
        (0, r, -tau, 0),
        (1, 0, 0, Cp),
        (0, r, -tau, 0),
    )
    beta_p = (
        (0, r, tau, 0),
        (0, 0, 0, gp),
        (0, r, tau, 0),
        (1, 0, 0, Fp),
    )
    combined0 = combined_marked(
        0,
        alpha_s,
        beta_s,
        alpha_p,
        beta_p,
    )
    combined1 = combined_marked(
        1,
        alpha_s,
        beta_s,
        alpha_p,
        beta_p,
    )
    assert sp.factor(combined0[[0, 2, 4, 8, 15], :].det()) == (
        16 * Ds * gp * gs * r**4 * tau**4
    )
    assert sp.factor(combined1[[6, 7, 8, 11, 15], :].det()) == (
        -16 * Es * r**4 * tau**4
    )

    deepest = {Ds: 0, Es: 0}
    combined0_deep = combined0.subs(deepest)
    combined2_deep = combined_marked(
        2,
        substitute_rows(alpha_s, deepest),
        substitute_rows(beta_s, deepest),
        alpha_p,
        beta_p,
    )
    kernel0 = sp.Matrix([-1, 0, 0, Cs, Cp])
    assert (combined0_deep * kernel0).applyfunc(
        sp.factor
    ) == sp.zeros(16, 1)
    assert sp.factor(
        combined0_deep[
            [0, 4, 8, 15],
            [1, 2, 3, 4],
        ].det()
    ) == 8 * gp * gs * r**3 * tau**3
    assert combined2_deep[:, :3].rank() == 3
    assert sp.factor(
        combined2_deep[
            [7, 8, 9],
            [0, 1, 2],
        ].det()
    ) == 4 * gs * r**2 * tau**2
    assert combined2_deep[:, 3:] == sp.zeros(16, 2)

    H = sp.symbols("H")
    gamma0_s = (-1, 0, 0, Cs)
    gamma2_s = (0, 0, 0, H)
    mixed = sp.factor(
        permanent(
            (
                gamma0_s,
                alpha_s[1],
                gamma2_s,
                (0, r, -tau, 0),
            )
        )
    )
    assert mixed == 2 * H * r * tau

    return {
        "binary_extension_equations": 3,
        "partial_marked_minors": 4,
        "stacked_minors": 4,
        "deepest_mixed_coefficient": str(mixed),
    }


def verify_two_planes() -> dict[str, object]:
    p, q, r, tau = sp.symbols("p q r tau", nonzero=True)
    alpha_parameter, beta_parameter = sp.symbols(
        "alpha_parameter beta_parameter"
    )
    c0, d0 = sp.symbols("c0 d0")
    g = sp.symbols("g", nonzero=True)

    c = (p, q, 0)
    f = (p, -q, 0)
    d = (r, 0, tau)
    e = (r, 0, -tau)
    normal = (0, q * r, p * tau)
    a = tuple(
        left + alpha_parameter * right
        for left, right in zip((1, q / p, 0), normal)
    )
    v = tuple(
        left + beta_parameter * right
        for left, right in zip((1, -q / p, 0), normal)
    )
    assert sp.factor(permanent((a, c, e))) == -2 * q * tau
    assert sp.factor(permanent((v, d, f))) == -2 * q * tau
    assert pair_product(c, f) == sp.zeros(3, 1)
    assert pair_product(d, e) == sp.zeros(3, 1)
    diagonal_first = pair_product(c, e)
    diagonal_second = pair_product(d, f)
    assert sp.factor(
        sp.Matrix.hstack(diagonal_first, diagonal_second)[
            [0, 1],
            :,
        ].det()
    ) == -2 * p * q * tau**2

    K = alpha_parameter * (beta_parameter * p * r - 1)
    L = beta_parameter * (alpha_parameter * p * r + 1)
    C = L * c0
    F = -K * c0
    D = L * d0
    E = -K * d0
    T = K * L * (r * c0 - p * d0)
    X = -T
    alpha = (
        (0, 0, 0, 1),
        a + (X,),
        c + (C,),
        e + (E,),
    )
    beta = (
        v + (T,),
        (0, 0, 0, g),
        d + (D,),
        f + (F,),
    )
    values = coefficients(alpha, beta)
    assert values["0000"] == -2 * q * tau
    assert values["1111"] == -2 * g * q * tau
    assert all(
        value == 0
        for word, value in values.items()
        if word not in ("0000", "1111")
    )
    marked2 = one_marked_map(2, alpha, beta)
    marked3 = one_marked_map(3, alpha, beta)
    assert sp.factor(marked2[[0, 5, 6, 7], :].det()) == (
        8
        * alpha_parameter
        * g**2
        * q**3
        * tau**3
        * (beta_parameter * p * r - 1) ** 2
    )
    assert sp.factor(marked3[[0, 1, 4, 7], :].det()) == (
        -8
        * beta_parameter
        * g
        * q**3
        * tau**3
        * (alpha_parameter * p * r + 1) ** 2
    )

    Cx, Dx, Ex, Fx = sp.symbols("C D E F")
    tangent_data = {}
    tangent_forms = {
        "P0": ((1, q / p, 0), (1, -q / p, 0)),
        "P1": ((1, 0, -tau / r), (1, 0, tau / r)),
    }
    for name, (tangent_a, tangent_v) in tangent_forms.items():
        tangent_alpha = (
            (0, 0, 0, 1),
            tangent_a + (0,),
            c + (Cx,),
            e + (Ex,),
        )
        tangent_beta = (
            tangent_v + (0,),
            (0, 0, 0, g),
            d + (Dx,),
            f + (Fx,),
        )
        marked0 = one_marked_map(0, tangent_alpha, tangent_beta)
        marked1 = one_marked_map(1, tangent_alpha, tangent_beta)
        if name == "P0":
            minors = {
                "F": sp.factor(marked0[[0, 1, 4, 7], :].det()),
                "E": sp.factor(marked0[[0, 2, 4, 7], :].det()),
                "C": sp.factor(marked1[[0, 3, 4, 7], :].det()),
                "D": sp.factor(marked1[[0, 3, 6, 7], :].det()),
            }
            expected = {
                "F": -8 * Fx * g**2 * p * q**3 * tau**3,
                "E": -8 * Ex * g**2 * q**3 * r * tau**3,
                "C": -8 * Cx * q**3 * r * tau**3,
                "D": -8 * Dx * q**3 * r * tau**3,
            }
        else:
            minors = {
                "C": sp.factor(marked0[[0, 1, 4, 7], :].det()),
                "D": sp.factor(marked0[[0, 2, 4, 7], :].det()),
                "E": sp.factor(marked1[[0, 3, 4, 7], :].det()),
                "F": sp.factor(marked1[[0, 3, 5, 7], :].det()),
            }
            expected = {
                "C": 8 * Cx * g**2 * p * q**3 * tau**3,
                "D": 8 * Dx * g**2 * q**3 * r * tau**3,
                "E": 8 * Ex * p * q**3 * tau**3,
                "F": 8 * Fx * p * q**3 * tau**3,
            }
        assert minors == expected
        tangent_data[name] = {
            key: str(value)
            for key, value in minors.items()
        }

    Cs, Ds, Es, Fs = sp.symbols("Cs Ds Es Fs")
    gs, gp = sp.symbols("gs gp", nonzero=True)
    stacked_checks = {}
    deepest_checks = {}
    for name, (tangent_a, tangent_v) in tangent_forms.items():
        alpha_s = (
            (0, 0, 0, 0),
            tangent_a + (0,),
            c + (Cs,),
            e + (Es,),
        )
        beta_s = (
            tangent_v + (0,),
            (0, 0, 0, gs),
            d + (Ds,),
            f + (Fs,),
        )
        alpha_p = (
            (0, 0, 0, 1),
            tangent_a + (0,),
            c + (0,),
            e + (0,),
        )
        beta_p = (
            tangent_v + (0,),
            (0, 0, 0, gp),
            d + (0,),
            f + (0,),
        )
        combined0 = combined_marked(
            0,
            alpha_s,
            beta_s,
            alpha_p,
            beta_p,
        )
        combined1 = combined_marked(
            1,
            alpha_s,
            beta_s,
            alpha_p,
            beta_p,
        )
        if name == "P0":
            stacked = {
                "F": sp.factor(
                    combined0[[0, 1, 4, 7, 8], :].det()
                ),
                "E": sp.factor(
                    combined0[[0, 2, 4, 7, 8], :].det()
                ),
                "C": sp.factor(
                    combined1[[4, 7, 8, 11, 15], :].det()
                ),
                "D": sp.factor(
                    combined1[[6, 7, 8, 11, 15], :].det()
                ),
            }
            expected_stacked = {
                "F": 16 * Fs * gs**2 * p * q**4 * tau**4,
                "E": 16 * Es * gs**2 * q**4 * r * tau**4,
                "C": 16 * Cs * q**4 * r * tau**4,
                "D": 16 * Ds * q**4 * r * tau**4,
            }
        else:
            stacked = {
                "C": sp.factor(
                    combined0[[0, 1, 4, 8, 15], :].det()
                ),
                "D": sp.factor(
                    combined0[[0, 2, 4, 8, 15], :].det()
                ),
                "E": sp.factor(
                    combined1[[4, 7, 8, 11, 15], :].det()
                ),
                "F": sp.factor(
                    combined1[[5, 7, 8, 11, 15], :].det()
                ),
            }
            expected_stacked = {
                "C": 16 * Cs * gp * gs * p * q**4 * tau**4,
                "D": 16 * Ds * gp * gs * q**4 * r * tau**4,
                "E": -16 * Es * p * q**4 * tau**4,
                "F": -16 * Fs * p * q**4 * tau**4,
            }
        assert stacked == expected_stacked
        stacked_checks[name] = {
            key: str(value)
            for key, value in stacked.items()
        }

        zero_extensions = {Cs: 0, Ds: 0, Es: 0, Fs: 0}
        deepest0 = combined0.subs(zero_extensions)
        deepest1 = combined1.subs(zero_extensions)
        deepest2 = combined_marked(
            2,
            substitute_rows(alpha_s, zero_extensions),
            substitute_rows(beta_s, zero_extensions),
            alpha_p,
            beta_p,
        )
        normal_vector = sp.Matrix(
            [0, q * r / (p * tau), 1, 0, 0]
        )
        assert (deepest0 * normal_vector).applyfunc(
            sp.factor
        ) == sp.zeros(16, 1)
        assert (deepest1 * normal_vector).applyfunc(
            sp.factor
        ) == sp.zeros(16, 1)
        assert deepest0.rank() == 4
        assert deepest1.rank() == 4
        assert deepest2[:, :3].rank() == 3
        assert deepest2[:, 3:] == sp.zeros(16, 2)

        H = sp.symbols("H")
        normal_s = (0, q * r / (p * tau), 1, 0)
        gamma2_s = (0, 0, 0, H)
        if name == "P0":
            mixed = sp.factor(
                permanent(
                    (
                        tangent_v + (0,),
                        normal_s,
                        gamma2_s,
                        f + (0,),
                    )
                )
            )
        else:
            mixed = sp.factor(
                permanent(
                    (
                        normal_s,
                        tangent_a + (0,),
                        gamma2_s,
                        f + (0,),
                    )
                )
            )
        assert mixed == -2 * H * q
        deepest_checks[name] = str(mixed)

    return {
        "generic_extension_parameters": ["K", "L", "c0", "d0"],
        "tangent_strata": tangent_data,
        "stacked_checks": stacked_checks,
        "deepest_mixed_coefficients": deepest_checks,
    }


def main() -> None:
    x0, x1, x2 = sp.symbols("x0 x1 x2", nonzero=True)
    full_support_matrix = sp.Matrix(
        [
            [0, x2, x1],
            [x2, 0, x0],
            [x1, x0, 0],
        ]
    )
    assert sp.factor(full_support_matrix.det()) == 2 * x0 * x1 * x2

    a, b = sp.symbols("a b", nonzero=True)
    assert pair_product((a, b, 0), (a, -b, 0)) == sp.zeros(3, 1)
    assert pair_product((a, 0, 0), (a, 0, 0)) == sp.zeros(3, 1)

    line_plane = verify_line_plane()
    two_planes = verify_two_planes()
    output = {
        "verified": True,
        "field": "C",
        "pair_map_full_support_determinant": "2*x0*x1*x2",
        "exceptional_pair_image_support_strata": [
            "line_complementary_plane",
            "two_distinct_coordinate_planes",
        ],
        "line_plane": line_plane,
        "two_planes": two_planes,
        "secondary_gate_H31_lift_possible": False,
        "all_single_gate_H31_excluded": True,
        "all_rank_two_pure_P4_H31_excluded": False,
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "dependency": {
            "file": RANK_TWO_M.name,
            "sha256": sha256(RANK_TWO_M),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_h31_secondary_gate_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
