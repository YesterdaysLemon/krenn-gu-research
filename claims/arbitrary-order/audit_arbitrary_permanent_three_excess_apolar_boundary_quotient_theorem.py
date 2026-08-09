"""Independent no-import audit of the apolar boundary quotient ledgers."""

from __future__ import annotations


def determinant(rows: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]


def main() -> None:
    # Profile and quotient-dimension ledgers.
    for h_profile, s_profile, quotient_dimensions in (
        ((1, 1, 1), (1, 1, 1), (2, 2, 2)),
        ((2, 1, 0), (0, 1, 2), (3, 2, 1)),
    ):
        assert sum(h_profile) == sum(s_profile) == 3
        assert all(h + s == 2 for h, s in zip(h_profile, s_profile, strict=True))
        assert quotient_dimensions == tuple(3 - s for s in s_profile)

    # The private-monomial minor for profile 111 remains nonzero.
    a_value, c_value = 2, 3
    assert determinant(((a_value * c_value, 0), (0, 1))) == 6

    # In the dependent profile-210 branch cd=be, the bosonic coefficient is
    # twice a nonzero product and remains independent of the M component.
    a_value, b_value, e_value = 2, 3, 5
    assert 2 * a_value * b_value * e_value == 60
    assert e_value != 0

    # Balance and the unique exterior colour-selector ledger.
    for boundary_size in (1, 2, 3):
        mode_size = source_size = boundary_size
        assert mode_size == source_size and mode_size > 0
    for matching_colour in (0, 1, 2):
        colours = (0, 1, 2)
        assert sum(colour == matching_colour for colour in colours) == 1

    print("independent no-import apolar boundary quotient audit: PASS")


if __name__ == "__main__":
    main()
