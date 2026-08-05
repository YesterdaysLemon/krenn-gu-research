#!/usr/bin/env python3
"""Bounded exact reconnaissance of component 19 on the finite p=0 boundary.

This script reconstructs the ordinary four-plane restriction and pair geometry
from P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md.  It makes no weighted-H22
incidence claim and imports no p=0 construction or proof-B artifact.
"""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"

p, q, phi = sp.symbols("p q phi")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows):
    n = len(rows)
    assert all(len(row) == n for row in rows)
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


def displayed_rows():
    A = (1, 1, 0, 0)
    Abar = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    Bbar = (0, 0, 1, -1)
    first = (
        tuple(Abar[j] + p * B[j] for j in range(4)),
        B,
        Bbar,
        Abar,
    )
    second = (
        tuple(Bbar[j] + q * B[j] for j in range(4)),
        A,
        A,
        tuple(B[j] + phi * Bbar[j] for j in range(4)),
    )
    return first, second


def tensor_coefficients():
    first, second = displayed_rows()
    return {
        bits: sp.factor(permanent([
            second[mode] if bits[mode] else first[mode]
            for mode in range(4)
        ]))
        for bits in itertools.product((0, 1), repeat=4)
    }


def pair_matrix(mode_i: int, mode_j: int):
    first, second = displayed_rows()
    rows = []
    for row_i in (first[mode_i], second[mode_i]):
        for row_j in (first[mode_j], second[mode_j]):
            rows.append([
                sp.expand(row_i[a] * row_j[b] + row_i[b] * row_j[a])
                for a, b in itertools.combinations(range(4), 2)
            ])
    return sp.Matrix(rows)


def ordinary_restriction_and_zero_base():
    coeff = tensor_coefficients()
    nonzero = {bits: value for bits, value in coeff.items() if value != 0}
    assert set(nonzero) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert sp.expand(nonzero[(0, 1, 1, 1)] - 4 * p) == 0
    assert sp.expand(nonzero[(1, 1, 1, 1)] - 4 * (q - phi)) == 0

    at_p_zero = {bits: sp.factor(value.subs(p, 0)) for bits, value in coeff.items()}
    at_p_zero_nonzero = {bits: value for bits, value in at_p_zero.items() if value != 0}
    assert set(at_p_zero_nonzero) == {(1, 1, 1, 1)}
    assert sp.expand(at_p_zero_nonzero[(1, 1, 1, 1)] - 4 * (q - phi)) == 0

    zero_groebner = sp.groebner(list(nonzero.values()), p, q, phi, order="lex")
    zero_basis = tuple(poly.as_expr() for poly in zero_groebner.polys)
    assert zero_basis == (p, q - phi)
    jacobian = sp.Matrix((p, q - phi)).jacobian((p, q, phi))
    assert jacobian.rank() == 2
    assert jacobian.extract((0, 1), (0, 1)).det() == 1

    # General first-order arc through p=0,q=phi=r.  The common c direction is
    # tangent to the zero base; a and b are its two normal coordinates.
    u, a, b, c, r = sp.symbols("u a b c r")
    arc = {p: u * a, q: r + u * (b + c), phi: r + u * c}
    leading = {
        bits: sp.expand(value.subs(arc)).coeff(u, 1)
        for bits, value in coeff.items()
    }
    leading_nonzero = {bits: value for bits, value in leading.items() if value != 0}
    assert set(leading_nonzero) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert sp.expand(leading_nonzero[(0, 1, 1, 1)] - 4 * a) == 0
    assert sp.expand(leading_nonzero[(1, 1, 1, 1)] - 4 * b) == 0

    return {
        "ordinary_tensor_support": nonzero,
        "p_zero_tensor_support": at_p_zero_nonzero,
        "zero_base_ideal": zero_basis,
        "zero_base_jacobian_rank": 2,
        "first_order_tensor_directions": leading_nonzero,
        "projectivized_normal_fibre": "P^1_[a:b]",
    }


def p_zero_pair_geometry():
    matrices = [pair_matrix(i, j).subs(p, 0)
                for i, j in itertools.combinations(range(4), 2)]
    generic_profile = tuple(matrix.rank() for matrix in matrices)
    assert generic_profile == (3, 3, 4, 3, 3, 3)

    # Edge 01: rank three exactly when q!=0, otherwise rank two.
    edge01 = matrices[0]
    edge01_rank3 = sp.factor(edge01.extract((0, 2, 3), (1, 2, 5)).det())
    assert edge01_rank3 == 4 * q
    assert edge01.subs(q, 0).rank() == 2
    edge01_rank2 = sp.factor(edge01.subs(q, 0).extract((0, 3), (1, 2)).det())
    assert edge01_rank2 == -2

    # Edge 02 and the fixed triangle edges have unconditional rank-three
    # witnesses on phi!=0 (indeed edges 02,12,13 already have unit witnesses).
    assert matrices[1].extract((0, 2, 3), (1, 4, 5)).det() == -4
    assert matrices[3].rank() == 3
    assert matrices[4].rank() == 3
    edge23_rank3 = sp.factor(matrices[5].extract((0, 1, 3), (1, 2, 5)).det())
    assert edge23_rank3 == 4 * phi

    # Edge 03 is rank four off (q-phi)*(phi*q-1)=0.
    edge03 = matrices[2]
    # The matrix is 4x6; use a fixed maximal minor from the component theorem.
    edge03_rank4 = sp.factor(edge03.extract((0, 1, 2, 3), (0, 1, 2, 5)).det())
    assert sp.expand(edge03_rank4 + 8 * (q - phi) * (phi * q - 1)) == 0

    on_q_equals_phi = edge03.subs(q, phi)
    q_equals_phi_rank3 = sp.factor(on_q_equals_phi.extract((0, 1, 2), (0, 1, 2)).det())
    assert sp.expand(q_equals_phi_rank3 + 4 * (phi**2 - 1)) == 0
    assert on_q_equals_phi.rank() == 3

    on_reciprocal = edge03.subs(q, 1 / phi)
    reciprocal_rank3 = sp.factor(on_reciprocal.extract((0, 1, 3), (0, 1, 5)).det())
    assert sp.cancel(reciprocal_rank3 - 4 * (phi - 1) * (phi + 1) ** 2 / phi) == 0
    assert on_reciprocal.rank() == 3

    endpoint_ranks = {}
    for epsilon in (+1, -1):
        endpoint = edge03.subs({q: epsilon, phi: epsilon})
        assert endpoint.rank() == 2
        endpoint_ranks[epsilon] = 2

    # Profiles at the zero-restriction base p=0,q=phi.
    zero_base_profile = tuple(matrix.subs(q, phi).rank() for matrix in matrices)
    assert zero_base_profile == (3, 3, 3, 3, 3, 3)
    zero_base_endpoint_profiles = {
        epsilon: tuple(matrix.subs({q: epsilon, phi: epsilon}).rank()
                       for matrix in matrices)
        for epsilon in (+1, -1)
    }
    assert zero_base_endpoint_profiles == {
        +1: (3, 3, 2, 3, 3, 3),
        -1: (3, 3, 2, 3, 3, 3),
    }

    # phi=0 is not in the component chart, but record the finite formula's
    # limiting pair profile without promoting it to an ordinary component point.
    excluded_phi_zero_profile = tuple(matrix.subs({q: 0, phi: 0}).rank()
                                      for matrix in matrices)
    assert excluded_phi_zero_profile == (2, 3, 3, 3, 3, 2)

    return {
        "p_zero_generic_pair_profile": generic_profile,
        "edge01_rank3_witness": edge01_rank3,
        "edge03_rank4_witness": edge03_rank4,
        "edge03_q_equals_phi_rank3_witness": q_equals_phi_rank3,
        "edge03_phi_q_equals_one_rank3_witness": reciprocal_rank3,
        "zero_base_pair_profile_phi_squared_not_one": zero_base_profile,
        "zero_base_endpoint_profiles": zero_base_endpoint_profiles,
        "excluded_phi_zero_limiting_profile": excluded_phi_zero_profile,
    }


def main():
    ordinary = ordinary_restriction_and_zero_base()
    pairs = p_zero_pair_geometry()
    print("source_sha256", sha256(SOURCE))
    for key, value in ordinary.items():
        print(key, value)
    for key, value in pairs.items():
        print(key, value)
    print("FINITE_P0_GEOMETRY_VERIFIED")
    print("WEIGHTED_H22_STATUS_UNKNOWN")


if __name__ == "__main__":
    main()
