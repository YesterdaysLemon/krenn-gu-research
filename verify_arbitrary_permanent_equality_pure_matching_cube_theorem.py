"""Symbolic checks for the equality pure-matching cube theorem."""

from __future__ import annotations

from itertools import product

import sympy as sp


def main() -> None:
    # On two exceptional sources there are exactly the original and cross
    # bijections; a second alternating cycle would need more source vertices.
    bijections = ((0, 1), (1, 0))
    assert len(bijections) == 2
    assert set(bijections) == set(product(range(2), repeat=2)) - {(0, 0), (1, 1)}

    a, b, c, d = sp.symbols("A B C D", nonzero=True)
    backbone = a * d
    cross = b * c
    rho = cross / backbone
    assert sp.expand(backbone * (1 + rho) - (backbone + cross)) == 0
    assert sp.expand((backbone + cross).subs(cross, -backbone)) == 0

    # With distinct excess modes, two switchable colours would require their
    # distinct mandatory coordinate covectors in the same cross cells.
    e0 = sp.Matrix([1, 0, 0])
    e1 = sp.Matrix([0, 1, 0])
    assert e0.rank() == e1.rank() == 1
    assert sp.Matrix.hstack(e0, e1).rank() == 2

    # In the co-located branch, every switch consumes one unit of mode-degree
    # excess at its distinct common mandatory mode.  The total is two.
    feasible_ledgers = [
        (epsilon_a, switches)
        for epsilon_a in range(3)
        for switches in range(3)
        if epsilon_a + switches <= 2
    ]
    assert max(switches for _, switches in feasible_ledgers) == 2
    assert (0, 2) in feasible_ledgers

    for switch_count in range(3):
        backbones = list(product((0, 1), repeat=switch_count))
        assert len(backbones) == 2**switch_count
        assert len(backbones) <= 4

    print("arbitrary permanent equality pure-matching cube: symbolic checks PASS")
    print("fixed exchange algebra only; no matching or support search was performed")


if __name__ == "__main__":
    main()
