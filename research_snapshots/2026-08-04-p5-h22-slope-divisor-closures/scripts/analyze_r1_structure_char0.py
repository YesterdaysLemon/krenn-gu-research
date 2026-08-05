#!/usr/bin/env python3
"""Exact characteristic-zero structure of the D_23 pencil at r=1 on the
disjoint mixed-star component.

Prints the reduced structure of the 14x8 mixed matrix M(t) at r=1 over
K=C(a,b,f)[phi]/(Phi):
  * which entries vanish identically (mod Phi);
  * the universal-kernel (y_3 column) identities;
  * the diagonal A structure A = c_0 x_0;
  * factored nonzero entries.
"""

from __future__ import annotations

import itertools

import sympy as sp

a, b, f, phi, r = sp.symbols("a b f phi r")
T = sp.symbols("t0:4")

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
MIXED = tuple(
    u for u in BITS4 if u not in ((0, 0, 0, 0), (1, 1, 1, 1))
)


def phi_reduce(expr):
    """Reduce mod phi^2 = W_NUM/W_DEN, clearing denominators by a
    W_DEN power (a unit mod Phi)."""
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


def perm3(rows):
    (a0, a1, a2), (b0, b1, b2), (c0, c1, c2) = rows
    return sp.expand(
        a0 * (b1 * c2 + b2 * c1)
        + a1 * (b0 * c2 + b2 * c0)
        + a2 * (b0 * c1 + b1 * c0)
    )


def weighted23(row, slope):
    return (row[0], row[1], sp.expand(slope * row[2] + row[3]))


def main():
    slope = sp.Integer(1)
    walpha = [weighted23(ALPHA[m], slope) for m in range(4)]
    wbeta = [weighted23(BETA[m], slope) for m in range(4)]

    print("== weighted rows at r=1 (D_23) ==")
    for m in range(4):
        print(f"  walpha[{m}] = {walpha[m]}")
        print(f"  wbeta [{m}] = {wbeta[m]}")

    # pattern permanents P3[m][pattern]: rows j != m, bit=1 -> beta_j
    print("\n== pattern 3x3 permanents mod Phi (slot m; pattern over "
          "others, 1=beta) ==")
    P3 = {}
    for m in range(4):
        others = [j for j in range(4) if j != m]
        for pattern in itertools.product((0, 1), repeat=3):
            rows = tuple(
                wbeta[j] if bit else walpha[j]
                for j, bit in zip(others, pattern)
            )
            value = phi_reduce(perm3(rows))
            P3[(m, pattern)] = value
            tag = "ZERO" if value == 0 else sp.factor(value)
            print(f"  m={m} pattern={pattern}: {tag}")

    # universal kernel: y_3 column of every mixed word with bits_3=1
    print("\n== y_3-column (universal kernel) check ==")
    all_zero = True
    for bits in MIXED:
        if bits[3] != 1:
            continue
        # y_3 coefficient = perm3 over rows 0,1,2 marked per bits with
        # marking t; multilinear expansion touches patterns
        # (b0',b1',b2') <= (bits0,bits1,bits2).  All must vanish.
        for sub in itertools.product((0, 1), repeat=3):
            if all(s <= bb for s, bb in zip(sub, bits[:3])):
                if P3[(3, sub)] != 0:
                    all_zero = False
                    print(f"  word {bits}: pattern {sub} NONZERO")
    print(f"  all mixed y_3 coefficients vanish for all t: {all_zero}")

    # diagonal A structure
    print("\n== diagonal A (0000) ==")
    for m in range(4):
        value = P3[(m, (0, 0, 0))]
        if value == 0:
            print(f"  coeff x_{m}: 0")
        else:
            print(f"  coeff x_{m}: {sp.factor(value)}")
            res = sp.factor(
                sp.resultant(sp.Poly(value, phi), sp.Poly(PHI, phi))
            ) if phi in value.free_symbols else sp.factor(value)
            print(f"    resultant/content vs Phi: {res}")

    # diagonal B on the universal kernel: y_3 coefficient of 1111 word
    print("\n== diagonal B on the universal kernel ==")
    print(f"  all-beta pattern perm3 (m=3): {P3[(3, (1, 1, 1))]}")
    # t-dependence: patterns strictly below (1,1,1) all vanish -> B on
    # kernel is marking-independent.
    tdep = [
        P3[(3, sub)]
        for sub in itertools.product((0, 1), repeat=3)
        if sub != (1, 1, 1)
    ]
    print(f"  lower patterns all zero: {all(v == 0 for v in tdep)}")

    # full matrix structure: which slots are nonzero, degree in t
    print("\n== mixed matrix structure at r=1 (slot: nonzero pattern) ==")
    for bits in MIXED:
        desc = []
        for m in range(4):
            marked = [j for j in range(4) if j != m and bits[j] == 1]
            terms = []
            for k in range(len(marked) + 1):
                for S in itertools.combinations(marked, k):
                    pattern = tuple(
                        1 if (bits[j] == 1 and j not in S) else 0
                        for j in range(4)
                        if j != m
                    )
                    if P3[(m, pattern)] != 0:
                        mono = "*".join(f"t{j}" for j in S) or "1"
                        terms.append(mono)
            if terms:
                slot = f"x{m}" if bits[m] == 0 else f"y{m}"
                desc.append(f"{slot}[{'+'.join(terms)}]")
        print(f"  word {''.join(map(str, bits))}: {'  '.join(desc)}")


if __name__ == "__main__":
    main()
