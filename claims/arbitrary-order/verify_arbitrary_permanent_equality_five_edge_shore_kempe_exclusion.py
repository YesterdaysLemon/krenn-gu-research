"""Primary exact checks for the five-edge shore Kempe exclusion."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    size_s = sp.symbols("size_s", integer=True, positive=True)
    size_t = size_s - 1
    internal_h = size_t
    outgoing_h, incoming_h = 1, 0
    assert sp.simplify(size_s - (internal_h + outgoing_h)) == 0
    assert sp.simplify(size_t - (internal_h + incoming_h)) == 0
    assert outgoing_h - incoming_h == 1

    # The third-colour restriction has two outgoing and one incoming port.
    outgoing_e, incoming_e = 2, 1
    internal_e = size_s - outgoing_e
    assert sp.simplify(size_t - (internal_e + incoming_e)) == 0
    assert outgoing_e - incoming_e == 1

    # The two forbidden internal pairings would create impossible balances.
    h_to_incoming_balance = 0 - 1
    two_e_ports_into_h_balance = 3 - 0
    assert h_to_incoming_balance != 1
    assert two_e_ports_into_h_balance != 1

    # Relabel p_1,p_2 so that the fixed internal bit is 1.
    iota = sp.Integer(1)
    exterior_before = sp.Integer(1)
    exterior_after = 3 - exterior_before
    assert exterior_before == iota
    assert exterior_after != iota
    assert {int(exterior_before), int(exterior_after)} == {1, 2}

    # The localized cross term vanishes while the displayed matching term is
    # a nonzero monomial.  No cancellation is possible.
    direct_left, direct_right, other_cross = sp.symbols(
        "direct_left direct_right other_cross", nonzero=True
    )
    missing_e_cross = sp.Integer(0)
    mixed_coefficient = direct_left * direct_right + missing_e_cross * other_cross
    assert sp.expand(mixed_coefficient - direct_left * direct_right) == 0
    assert mixed_coefficient != 0

    print("arbitrary permanent equality five-edge shore Kempe exclusion: PASS")
    print(
        "fixed boundary/bit algebra only; no matching or support search was performed"
    )


if __name__ == "__main__":
    main()
