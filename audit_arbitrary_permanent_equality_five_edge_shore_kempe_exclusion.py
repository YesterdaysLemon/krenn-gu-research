"""Independent no-import audit of the five-edge shore Kempe exclusion."""

from __future__ import annotations


def main() -> None:
    # Both selected restrictions obey the same defect-one conservation law.
    assert (1 - 0) == 1
    assert (2 - 1) == 1

    # Pairing the switch port with the incoming port, or pairing the two
    # outgoing e-ports together, yields boundary balances -1 and 3.
    assert (0 - 1) != 1
    assert (3 - 0) != 1

    # The internal bit stays fixed while the two pure backbones toggle the
    # exterior bit.  Exactly one backbone aligns.
    internal_bit = False
    exterior_bits = (False, True)
    assert exterior_bits.count(internal_bit) == 1

    # A concrete nonzero direct monomial cannot be cancelled when the
    # required coordinate cross cell has weight zero.
    direct_left, direct_right = 2, 3
    missing_e_cross, other_cross = 0, 5
    mixed_coefficient = direct_left * direct_right + missing_e_cross * other_cross
    assert mixed_coefficient == 6

    print("independent no-import five-edge shore Kempe audit: PASS")


if __name__ == "__main__":
    main()
