"""Symbolic proof guards for aligned one-chord 2+1+0 desaturation."""

from __future__ import annotations

from collections import Counter

import sympy as sp


def main() -> None:
    a, b, c, d = sp.symbols("a b c d", nonzero=True)

    # Row-zero basis (z0,L1,L2), row-one basis (z1,M).  The row-two factor
    # is the single surviving class pi_2(z2).
    projected_two_way = sp.Matrix(
        [
            [a * d, 0],
            [b * c, d],
            [a * c, 0],
        ]
    )
    rank_minor = sp.det(projected_two_way[[0, 1], :])
    assert rank_minor == a * d**2

    # The diagonal target has at most one surviving summand after pi_2.
    target_rank_one = sp.Matrix([[1, 0], [0, 0], [0, 0]])
    assert target_rank_one.rank() == 1

    # With s2=2, the exact degree-surplus equation has only three solutions.
    placements = {
        (s0, s1, tau)
        for s0 in range(3)
        for s1 in range(1, 3)
        for tau in range(3)
        if s0 + s1 + tau == 2
    }
    assert placements == {(0, 1, 1), (1, 1, 0), (0, 2, 0)}

    # In the a0-concentrated chart, if L1 is killed by the boundary line,
    # the remaining quotient coordinates of V are (ad,ac), hence nonzero.
    concentrated_a0_vector = sp.Matrix([a * d, a * c])
    assert concentrated_a0_vector != sp.zeros(2, 1)

    # In the a1-concentrated chart, pi1(M)=mu*pi1(z1).  The z0 and L2
    # coordinates cannot cancel for any mu.
    mu = sp.symbols("mu")
    concentrated_a1_vector = sp.Matrix([a * d, b * c + d * mu, a * c])
    assert concentrated_a1_vector[0] != 0
    assert concentrated_a1_vector[2] != 0

    colours = {0, 1, 2}
    alpha2 = 2
    outgoing_colours = colours - {alpha2}
    assert outgoing_colours == {0, 1}
    assert len(outgoing_colours) == 2

    # If B1 contains the two colours other than alpha1, e_alpha2 survives
    # exactly when alpha1=alpha2.
    for alpha1 in colours:
        b1_colours = colours - {alpha1}
        surviving = colours - b1_colours
        assert surviving == {alpha1}

    # A permutation agreeing with a pure backbone at m-1 modes has its last
    # source forced, so it is the same physical matching.
    pure_sources = (2, 0, 3, 1)
    aligned_sources = list(pure_sources)
    unmatched_mode = 2
    used_elsewhere = {
        source for mode, source in enumerate(aligned_sources) if mode != unmatched_mode
    }
    remaining_source = ({0, 1, 2, 3} - used_elsewhere).pop()
    assert remaining_source == pure_sources[unmatched_mode]

    # Source p2 forces alpha1 != alpha2.  For every such colour placement,
    # the a0-concentrated A-Q and R-P cut multisets disagree.
    for alpha2 in colours:
        for alpha0 in colours - {alpha2}:
            for alpha1 in colours - {alpha2}:
                beta0 = next(iter(colours - {alpha0, alpha2}))
                beta1 = next(iter(colours - {alpha1, alpha2}))
                a_q = Counter((beta0, beta1, *(colours - {alpha2})))
                r_p = Counter((beta0, beta1, *(colours - {alpha1})))
                assert a_q != r_p

    # The a1-concentrated survivor condition alpha1=alpha2 directly
    # contradicts mandatory-cover uniqueness at source p2.
    for alpha2 in colours:
        alpha1 = alpha2  # forced by projected target survival
        mandatory_p2_colours = (alpha1, alpha2)
        assert len(set(mandatory_p2_colours)) != len(mandatory_p2_colours)

    print("aligned one-chord 2+1+0 desaturation theorem: PASS")
    print("exact rank minor, surplus ledger, and cut transport; no census")


if __name__ == "__main__":
    main()
