#!/usr/bin/env python3
"""Exact audit of the p=0, q*phi=-1 shared-extension axes.

No construction or proof artifact is imported.  The script reconstructs the
ordinary p=0 bases, the verified shared frame, and all eight one-marked maps.
"""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"

q, phi = sp.symbols("q phi")
h0, h1, h2, h3, lam = sp.symbols("h0 h1 h2 h3 lambda")
hs = (h0, h1, h2, h3)
x = sp.symbols("x0:4")
y = sp.symbols("y0:4")
zvars = x + y


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    n = len(rows)
    dp = {0: sp.Integer(1)}
    for row in rows:
        nxt = {}
        for mask, value in dp.items():
            for column, entry in enumerate(row):
                if not (mask >> column) & 1:
                    key = mask | (1 << column)
                    nxt[key] = nxt.get(key, 0) + value * entry
        dp = {key: sp.expand(value) for key, value in nxt.items()}
    return sp.expand(dp[(1 << n) - 1])


def component_rows():
    A = (1, 1, 0, 0)
    Abar = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    Bbar = (0, 0, 1, -1)
    alpha = (Abar, B, Bbar, Abar)
    beta = (
        tuple(Bbar[j] + q * B[j] for j in range(4)),
        A,
        A,
        tuple(B[j] + phi * Bbar[j] for j in range(4)),
    )
    return alpha, beta


def marked_extended_rows():
    alpha, beta = component_rows()
    aa = [tuple(alpha[i]) + (x[i],) for i in range(4)]
    bb = [
        tuple(sp.expand(beta[i][j] + hs[i] * alpha[i][j]) for j in range(4))
        + (y[i],)
        for i in range(4)
    ]
    return aa, bb


def contract(row, direction: str):
    if direction == "01":
        return (sp.expand(lam * row[0] + row[1]), row[2], row[3], row[4])
    if direction == "23":
        return (row[0], row[1], sp.expand(lam * row[2] + row[3]), row[4])
    raise ValueError(direction)


def binary_coefficients(direction: str):
    aa, bb = marked_extended_rows()
    aa = [contract(row, direction) for row in aa]
    bb = [contract(row, direction) for row in bb]
    coeff = {}
    for bits in itertools.product((0, 1), repeat=4):
        coeff[bits] = permanent([bb[i] if bits[i] else aa[i] for i in range(4)])
    mixed = [value for bits, value in coeff.items()
             if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    return mixed, coeff[(0, 0, 0, 0)], coeff[(1, 1, 1, 1)]


def one_marked_map(mode: int, alpha, beta):
    rows = []
    others = [index for index in range(4) if index != mode]
    for bits in itertools.product((0, 1), repeat=3):
        selected = {other: beta[other] if bits[k] else alpha[other]
                    for k, other in enumerate(others)}
        row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            row.append(permanent([
                basis if index == mode else selected[index]
                for index in range(4)
            ]))
        rows.append(row)
    return sp.Matrix(rows)


def exact_axis_audit():
    t, X, Y, Z = sp.symbols("t X Y Z")
    q_value = -1 / phi
    r = q_value - phi
    branch = {q: q_value, lam: 1, h0: 0, h1: 0, h2: t, h3: 0}

    mixed01, A01, B01 = binary_coefficients("01")
    mixed23, A23, B23 = binary_coefficients("23")
    combined = sp.Matrix([
        [sp.expand(equation).coeff(variable) for variable in zvars]
        for equation in mixed01 + mixed23
    ]).subs(branch)

    vX = sp.Matrix((0, -1 / r, phi / r, 0, 1, 0, 0, 0))
    vY = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vZ = sp.Matrix((0, -q_value / r, 1 / r, 0, 0, 0, 0, 1))
    for vector in (vX, vY, vZ):
        assert all(sp.cancel(value) == 0 for value in combined * vector)
    complete_minor = sp.factor(combined.extract(
        (2, 9, 10, 12, 15), (0, 1, 2, 3, 6)
    ).det())
    expected_complete = 1024 * (phi**2 + 1) ** 2 / phi**3
    assert sp.cancel(complete_minor - expected_complete) == 0
    assert combined.rank() == 5

    extension = X * vX + Y * vY + Z * vZ
    extension_sub = dict(zip(zvars, extension))
    F = phi * X + Z
    G = r * Y - t * F
    H = X + q_value * Z
    diagonals = tuple(sp.factor(value.subs(branch).subs(extension_sub))
                      for value in (A01, B01, A23, B23))
    expected_diagonals = (0, 4 * G, -4 * F / r, 4 * H)
    assert all(sp.cancel(a - b) == 0 for a, b in zip(diagonals, expected_diagonals))

    alpha5, beta5 = marked_extended_rows()
    maps = {}
    for direction in ("01", "23"):
        alpha_d = [contract(row, direction) for row in alpha5]
        beta_d = [contract(row, direction) for row in beta5]
        for mode in range(4):
            maps[(direction, mode)] = one_marked_map(mode, alpha_d, beta_d).subs(branch).subs(extension_sub)

    records = {}
    for axis, axis_sub, coordinate in (
        ("X_zero", {X: 0}, Z),
        ("Z_zero", {Z: 0}, X),
    ):
        axis_maps = {key: matrix.subs(axis_sub) for key, matrix in maps.items()}
        generic_profiles = {
            direction: tuple(axis_maps[(direction, mode)].rank() for mode in range(4))
            for direction in ("01", "23")
        }
        assert generic_profiles == {
            "01": (3, 1, 1, 3),
            "23": (3, 3, 4, 3),
        }

        obstruction_minor = sp.factor(
            axis_maps[("23", 2)].extract((0, 1, 2, 7), range(4)).det()
        )
        expected_obstruction = (
            64 * Y * Z**2 * phi / (phi**2 + 1)
            if axis == "X_zero"
            else -64 * X**2 * Y * phi / (phi**2 + 1)
        )
        assert sp.cancel(obstruction_minor - expected_obstruction) == 0

        survivor_maps = {key: matrix.subs(Y, 0) for key, matrix in axis_maps.items()}
        survivor_profiles = {
            direction: tuple(survivor_maps[(direction, mode)].rank() for mode in range(4))
            for direction in ("01", "23")
        }
        assert survivor_profiles == {
            "01": (3, 1, 1, 3),
            "23": (3, 3, 3, 3),
        }

        # Fixed maximal-rank witnesses for every one-marked map on the survivor.
        if axis == "X_zero":
            witness_specs = {
                ("01", 0): ((3, 5, 7), (0, 1, 2), -16 * Z**3 * phi**2 * t**2 / (phi**2 + 1)**2),
                ("01", 1): ((7,), (0,), -2 * Z * t),
                ("01", 2): ((7,), (1,), -2 * Z * (phi + 1) / phi),
                ("01", 3): ((4, 5, 7), (0, 1, 3), -32 * Z**2 * t * (phi + 1) / (phi * (phi**2 + 1)**2)),
                ("23", 0): ((0, 3, 7), (0, 1, 2), 16 * Z**3 * phi**3 / (phi**2 + 1)**2),
                ("23", 1): ((0, 1, 7), (0, 1, 2), -16 * Z**3 * phi / (phi**2 + 1)**2),
                ("23", 2): ((0, 1, 7), (0, 1, 2), 16 * Z**3 * phi / (phi**2 + 1)**2),
                ("23", 3): ((0, 5, 7), (0, 1, 3), -32 * Z**2 / (phi * (phi**2 + 1)**2)),
            }
        else:
            witness_specs = {
                ("01", 0): ((1, 3, 7), (0, 1, 3), -32 * X**2 * phi**4 * t * (phi - 1) / (phi**2 + 1)**2),
                ("01", 1): ((7,), (0,), -2 * X * phi * t),
                ("01", 2): ((7,), (1,), -2 * X * (phi - 1)),
                ("01", 3): ((5, 6, 7), (0, 1, 2), -16 * X**3 * phi**2 * t**2 / (phi**2 + 1)**2),
                ("23", 0): ((0, 3, 7), (0, 1, 3), 32 * X**2 * phi**3 / (phi**2 + 1)**2),
                ("23", 1): ((0, 1, 7), (0, 1, 2), 16 * X**3 * phi**4 / (phi**2 + 1)**2),
                ("23", 2): ((0, 1, 7), (0, 1, 2), 16 * X**3 * phi**2 / (phi**2 + 1)**2),
                ("23", 3): ((0, 5, 7), (0, 1, 2), 16 * X**3 * phi**4 / (phi**2 + 1)**2),
            }
        checked_witnesses = {}
        for key, (rows, columns, expected) in witness_specs.items():
            witness = sp.factor(survivor_maps[key].extract(rows, columns).det())
            assert sp.cancel(witness - expected) == 0
            checked_witnesses[key] = witness

        # On Y=0, FGH!=0 is equivalent to coordinate*t!=0 on either axis.
        axis_F = sp.factor(F.subs(axis_sub).subs(Y, 0))
        axis_G = sp.factor(G.subs(axis_sub).subs(Y, 0))
        axis_H = sp.factor(H.subs(axis_sub).subs(Y, 0))
        assert coordinate in axis_F.free_symbols or coordinate in axis_H.free_symbols
        assert t in axis_G.free_symbols

        records[axis] = {
            "generic_rank_profiles": generic_profiles,
            "D23_mode2_rows_0127_obstruction": obstruction_minor,
            "survivor_equations": "Y=0, coordinate!=0, t!=0",
            "survivor_F_G_H": (axis_F, axis_G, axis_H),
            "survivor_rank_profiles": survivor_profiles,
            "survivor_rank_witnesses": checked_witnesses,
        }

    return complete_minor, diagonals, records


def main():
    complete_minor, diagonals, records = exact_axis_audit()
    print("source_sha256", sha256(SOURCE))
    print("parameter_relation", "q=-1/phi")
    print("required_parameter_open", "phi*(phi^2-1)*(phi^2+1)!=0")
    print("complete_shared_minor", complete_minor)
    print("diagonals_A01_B01_A23_B23", diagonals)
    for axis, record in records.items():
        print("axis", axis)
        for key, value in record.items():
            print(key, value)
    print("QPHI_MINUS_ONE_NONAXIS_OBSTRUCTION_VERIFIED")
    print("QPHI_MINUS_ONE_Y_ZERO_AXIS_SURVIVORS_VERIFIED")
    print("ACTUAL_WEIGHTED_H22_LIFT_STATUS_UNKNOWN")


if __name__ == "__main__":
    main()
