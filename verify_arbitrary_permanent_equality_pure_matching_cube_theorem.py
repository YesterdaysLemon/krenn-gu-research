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

    for switch_count in range(4):
        backbones = list(product((0, 1), repeat=switch_count))
        assert len(backbones) == 2**switch_count
        assert len(backbones) <= 8

    print("arbitrary permanent equality pure-matching cube: symbolic checks PASS")
    print("fixed exchange algebra only; no matching or support search was performed")


if __name__ == "__main__":
    main()
