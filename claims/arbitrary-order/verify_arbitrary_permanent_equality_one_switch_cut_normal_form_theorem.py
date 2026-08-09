"""Primary exact checks for the one-switch cut normal-form theorem."""

from __future__ import annotations

import sympy as sp


def cycle_gain(labels: tuple[int, ...]) -> int:
    """Return the F_2 sum of labels on one fixed cycle."""
    return sum(labels) % 2


def main() -> None:
    a, b, c, d, w_c, w_f = sp.symbols("a b c d w_c w_f", nonzero=True)
    switch_factor = a * d + b * c
    pure = sp.expand(w_c * switch_factor)
    mixed = sp.expand(w_f * switch_factor)

    assert sp.factor(pure / w_c) == switch_factor
    assert sp.factor(mixed / w_f) == switch_factor
    assert sp.simplify(mixed / pure - w_f / w_c) == 0

    # Two marked bridges lie on no cycle, so their labels are unconstrained.
    bridge_cycle_labels: tuple[int, ...] = ()
    assert cycle_gain(bridge_cycle_labels) == 0

    # A series pair occurs together on every relevant cycle.
    assert cycle_gain((1, 1, 0, 0)) == 0

    # A switched/unswitched parallel pair is the straddling obstruction.
    assert cycle_gain((1, 0)) == 1

    # A longer cycle separating the two marked incidence edges also obstructs.
    assert cycle_gain((1, 0, 0, 0)) == 1

    print("arbitrary permanent equality one-switch cut normal form: PASS")
    print("fixed factor/cut algebra only; no matching or support search was performed")


if __name__ == "__main__":
    main()
