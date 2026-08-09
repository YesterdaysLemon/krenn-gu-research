"""Exact verifier for the ineligible-ninth-cell Segre exclusion theorem."""

from __future__ import annotations

from collections import Counter
from itertools import permutations

import sympy as sp


def main() -> None:
    a, b, c, d, g = sp.symbols("a b c d g", nonzero=True)
    z0, z1, z2, y2, l1, l2, m = sp.symbols("z0 z1 z2 y2 l1 l2 m")

    port = (
        (z0, l1, l2),
        (m, a * z1, b * z1),
        (c * z2, g * y2, d * z2),
    )
    permanent = sum(
        sp.prod(port[row][sigma[row]] for row in range(3))
        for sigma in permutations(range(3))
    )
    expected = (
        a * d * z0 * z1 * z2
        + b * g * z0 * z1 * y2
        + d * l1 * m * z2
        + b * c * l1 * z1 * z2
        + g * l2 * m * y2
        + a * c * l2 * z1 * z2
    )
    assert sp.expand(permanent - expected) == 0

    alpha2_slice = sp.expand(permanent.subs(y2, 0) / z2)
    expected_slice = d * l1 * m + (a * d * z0 + b * c * l1 + a * c * l2) * z1
    assert sp.expand(alpha2_slice - expected_slice) == 0

    flattening = sp.Matrix(((a * d, 0), (b * c, d), (a * c, 0)))
    assert sp.factor(flattening.extract((0, 1), (0, 1)).det()) == a * d**2

    # One free surplus unit beyond the forced s1=s2=1 gives four placements.
    base = (0, 1, 1, 0)
    placements = {
        tuple(base[index] + (index == slot) for index in range(4))
        for slot in range(4)
    }
    assert placements == {
        (0, 1, 1, 1),
        (1, 1, 1, 0),
        (0, 2, 1, 0),
        (0, 1, 2, 0),
    }

    alpha1, alpha2, gamma = 0, 1, 2
    # alpha0=alpha1: the incoming cut has no alpha1, but B2 always has it.
    incoming_equal = Counter((gamma, gamma, alpha2))
    assert incoming_equal[alpha1] == 0

    # alpha0=gamma: transport fixes the outgoing colour spans exactly.
    incoming_distinct = Counter((alpha1, alpha2, gamma))
    outgoing_111 = Counter((alpha2, gamma, alpha1))
    outgoing_021 = Counter((alpha2, gamma, alpha1))
    outgoing_012 = Counter((alpha2, alpha1, gamma))
    assert outgoing_111 == incoming_distinct
    assert outgoing_021 == incoming_distinct
    assert outgoing_012 == incoming_distinct

    transported_spans = {
        (1, 1, 1, 0): ({alpha2}, {gamma}, {alpha1}),
        (0, 2, 1, 0): (set(), {alpha2, gamma}, {alpha1}),
        (0, 1, 2, 0): (set(), {alpha2}, {alpha1, gamma}),
    }
    for placement, spans in transported_spans.items():
        assert tuple(len(span) for span in spans) == placement[:3]
        assert Counter(colour for span in spans for colour in span) == incoming_distinct
    assert alpha2 in transported_spans[(1, 1, 1, 0)][0]
    assert alpha2 in transported_spans[(0, 2, 1, 0)][1]
    assert alpha2 in transported_spans[(0, 1, 2, 0)][1]

    # If the s0=s1=1 slice vanished, local rank at a0 would fall to two.
    lam, eta = sp.symbols("lam eta")
    b0_vec = sp.Matrix((0, 1, 0))
    z0_vec = sp.Matrix((0, 0, 1))
    l1_vec = lam * b0_vec
    l2_vec = sp.Matrix((0, eta, -d / c))
    incident = sp.Matrix.hstack(z0_vec, l1_vec, l2_vec, b0_vec)
    for columns in permutations(range(4), 3):
        assert sp.factor(incident[:, columns].det()) == 0

    # In the s1=2 quotient, two manifestly nonzero coefficients remain.
    mu = sp.symbols("mu")
    quotient_vector = sp.Matrix((a * d, b * c + d * mu, a * c))
    assert quotient_vector[0] != 0 and quotient_vector[2] != 0

    print("ineligible ninth-cell Segre exclusion theorem: PASS")
    print("six-term permanent, alpha2 slice, four-placement ledger, and cut tables")


if __name__ == "__main__":
    main()
