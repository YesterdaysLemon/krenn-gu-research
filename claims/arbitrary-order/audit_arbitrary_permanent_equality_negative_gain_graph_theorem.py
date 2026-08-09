"""Independent no-import audit of the equality negative-gain theorem."""

from __future__ import annotations

from fractions import Fraction


def propagate_cycle(length: int, initial: Fraction) -> Fraction:
    value = initial
    for _ in range(length):
        value = -value
    return value


def main() -> None:
    # AD+BC=0 with A=2,B=3,C=5 gives D=-15/2 and gain ratio -1.
    a, b, c, d = Fraction(2), Fraction(3), Fraction(5), Fraction(-15, 2)
    assert a * d + b * c == 0
    assert (b / a) / (d / c) == -1

    initial = Fraction(7, 3)
    assert propagate_cycle(3, initial) == -initial
    assert propagate_cycle(4, initial) == initial

    # Exact switching assignment on a bipartite four-cycle.
    gains = [initial, -initial, initial, -initial]
    assert all(gains[i] == -gains[(i + 1) % 4] for i in range(4))

    # Three individually consistent one-edge fibres can glue on shared
    # vertices to an inconsistent triangle.
    fibre_edges = [((0, 1),), ((1, 2),), ((2, 0),)]
    assert all(len(fibre) == 1 for fibre in fibre_edges)
    assert propagate_cycle(len(fibre_edges), initial) == -initial

    print("independent no-import equality negative-gain graph audit: PASS")


if __name__ == "__main__":
    main()
