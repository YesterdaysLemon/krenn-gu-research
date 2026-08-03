"""Symbolic checks for the equality backbone-colouring glue theorem."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    k0, k1, k2 = sp.symbols("k0 k1 k2")

    balanced = sp.groebner(
        [k0 + k1, k1 + k2 + 1, k2 + k0 + 1],
        k0,
        k1,
        k2,
        modulus=2,
    )
    assert not balanced.contains(sp.S.One)

    unbalanced = sp.groebner(
        [k0 + k1, k1 + k2, k2 + k0 + 1],
        k0,
        k1,
        k2,
        modulus=2,
    )
    assert unbalanced.contains(sp.S.One)

    # Two shared states give parallel overlap edges.  Equal labels are
    # consistent; a one-switch parity flip makes them inconsistent.
    equal_parallel = sp.groebner([k0 + k1, k0 + k1], k0, k1, modulus=2)
    assert not equal_parallel.contains(sp.S.One)
    mismatched_parallel = sp.groebner([k0 + k1, k0 + k1 + 1], k0, k1, modulus=2)
    assert mismatched_parallel.contains(sp.S.One)

    print("arbitrary permanent equality backbone-colouring glue: symbolic checks PASS")
    print("fixed F_2 descent only; no matching or support search was performed")


if __name__ == "__main__":
    main()
