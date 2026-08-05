#!/usr/bin/env python3
"""Shared exact machinery for the disjoint mixed-star slope-divisor
certificates.  Rebuilds the marked weighted binary-extension systems of
verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py at a
FIXED slope value, without the t-free y-elimination (which is exactly
what degenerates on the slope divisors)."""

from __future__ import annotations

import itertools

import sympy as sp

a, b, f, phi = sp.symbols("a b f phi")
T = sp.symbols("t0:4")
Z = sp.symbols("zx0:4") + sp.symbols("zy0:4")

J = f + b * phi**2
KAPPA = phi * (b * f + 1)
ETA = -(b * f + 1)

ALPHA = (
    (0, 0, 1, -1),
    (-a * f + 1, -a * f - 1, f + phi, f - phi),
    (-a * J + ETA, -a * J - ETA, J + KAPPA, J - KAPPA),
    (1, -1, 0, 0),
)
BETA = (
    (a + b, a - b, 0, 2),
    (1, 1, 0, 0),
    (1, 1, 0, 0),
    (0, 0, 1, 1),
)
PHI = sp.expand(
    a**2 * b * f * phi**2 + a**2 * f**2
    - b**2 * f**2 + b**2 * phi**2 - b * f - 1
)
W_DEN = sp.expand(b * (a**2 * f + b))
W_NUM = sp.expand(-(a**2 * f**2 - b**2 * f**2 - b * f - 1))

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = tuple(
    u for u in BITS4 if u not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMS4 = tuple(itertools.permutations(range(4)))


def phi_normal_form(expr):
    """Canonical linear-in-phi representative of W_DEN^k * expr modulo
    Phi (W_DEN is invertible modulo Phi), as in the repo verifier.
    Zero output is equivalent to expr = 0 in K."""
    p = sp.Poly(sp.expand(expr), phi)
    max_q = 0
    terms = []
    for (k,), coeff in p.terms():
        q, rem = divmod(k, 2)
        terms.append((q, rem, coeff))
        max_q = max(max_q, q)
    e = 0
    for q, rem, coeff in terms:
        e += coeff * W_NUM**q * W_DEN**(max_q - q) * phi**rem
    return sp.expand(e)


def perm4(rows):
    return sp.expand(sum(
        sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4
    ))


def weighted3(row, direction, slope):
    if direction == "01":
        return (sp.expand(slope * row[0] + row[1]), row[2], row[3])
    if direction == "23":
        return (row[0], row[1], sp.expand(slope * row[2] + row[3]))
    raise ValueError(direction)


def build_system(direction, slope):
    """Return dict with:
    rows[bits]  : 8-vector of coefficients (polynomials in a,b,f,phi,t)
                  of the binary word `bits` as a linear form in
                  z=(x0..x3,y0..y3);
    A, B        : the 0000 / 1111 diagonal coefficient 8-vectors;
    walpha, wbeta_marked : the weighted 3-column rows.
    """
    marked_beta = tuple(
        tuple(BETA[m][c] + T[m] * ALPHA[m][c] for c in range(4))
        for m in range(4)
    )
    walpha = tuple(
        weighted3(ALPHA[m], direction, slope) for m in range(4)
    )
    wbeta = tuple(
        weighted3(marked_beta[m], direction, slope) for m in range(4)
    )
    alpha_ext = tuple(walpha[m] + (Z[m],) for m in range(4))
    beta_ext = tuple(wbeta[m] + (Z[4 + m],) for m in range(4))
    rows = {}
    for bits in BITS4:
        expr = perm4(tuple(
            beta_ext[m] if bits[m] else alpha_ext[m] for m in range(4)
        ))
        row = []
        for zv in Z:
            coefficient = sp.expand(sp.diff(expr, zv))
            assert not set(coefficient.free_symbols) & set(Z)
            row.append(coefficient)
        reconstructed = sp.expand(
            sum(c * zv for c, zv in zip(row, Z))
        )
        assert sp.expand(expr - reconstructed) == 0, bits
        rows[bits] = row
    return {
        "rows": rows,
        "A": rows[(0, 0, 0, 0)],
        "B": rows[(1, 1, 1, 1)],
        "walpha": walpha,
        "wbeta": wbeta,
        "alpha_ext": alpha_ext,
        "beta_ext": beta_ext,
    }


def one_marked(data, mode, bits3):
    """Row `bits3` of the mode-`mode` one-marked 8x4 contraction
    through the other three binary planes: the other modes (increasing
    order) use beta_ext/alpha_ext per bits3, mode `mode` is replaced by
    a coordinate basis row."""
    others = tuple(m for m in range(4) if m != mode)
    chosen = tuple(
        data["beta_ext"][m] if bit else data["alpha_ext"][m]
        for m, bit in zip(others, bits3)
    )
    row = []
    for col in range(4):
        basis = tuple(sp.Integer(int(i == col)) for i in range(4))
        row.append(perm4((basis,) + chosen))
    return row


def one_marked_mode_zero(data, bits3):
    return one_marked(data, 0, bits3)


def resultant_certificate(expr):
    """Nonzero output proves expr vanishes nowhere on Phi=0 over the
    algebraic closure of C(a,b,f)."""
    reduced = phi_normal_form(expr)
    assert reduced != 0
    if phi not in reduced.free_symbols:
        result = sp.factor(reduced)
    else:
        result = sp.factor(sp.resultant(
            sp.Poly(reduced, phi), sp.Poly(PHI, phi)
        ))
    assert result != 0
    return str(result)


def congruent(u, v):
    """u = v in K?"""
    return phi_normal_form(sp.expand(u - v)) == 0


def sing(expr) -> str:
    return str(sp.expand(expr)).replace("**", "^")
