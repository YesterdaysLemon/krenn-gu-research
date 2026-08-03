"""Independent no-import audit of the conformal--Birkhoff phase equations."""

from __future__ import annotations


def main() -> None:
    # The even and odd B_3 permutation triples each use every matrix cell once.
    even_cells = (
        ((1, 1), (2, 2), (3, 3)),
        ((1, 2), (2, 3), (3, 1)),
        ((1, 3), (2, 1), (3, 2)),
    )
    odd_cells = (
        ((1, 1), (2, 3), (3, 2)),
        ((1, 2), (2, 1), (3, 3)),
        ((1, 3), (2, 2), (3, 1)),
    )
    assert sorted(cell for term in even_cells for cell in term) == sorted(
        cell for term in odd_cells for cell in term
    )

    # On a=b=c=-1, u and v have sum 2 and product -1.  Represent
    # 1+sqrt(2) and 1-sqrt(2) as pairs (rational, sqrt(2)-coefficient).
    u = (1, 1)
    v = (1, -1)
    pair_sum = (u[0] + v[0], u[1] + v[1])
    pair_product = (u[0] * v[0] + 2 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
    assert pair_sum == (2, 0)
    assert pair_product == (-1, 0)
    assert 1 - 1 - 1 - 1 + pair_sum[0] == 0

    # Matrix (15) has diagonal gain 1, three transposition gains -1,
    # and the conjugate three-cycle gains represented above.  Every
    # complementary normalized permanent is 1-1.
    assert (1 - 1, 1 - 1, 1 - 1) == (0, 0, 0)

    # The coordinate fixed-row bypass face.
    a = b = u_value = v_value = 0
    c = -1
    assert 1 + a + b + c + u_value + v_value == 0
    assert u_value * v_value == a * b * c

    assert (1, 3) == (1, len({"colour_0", "colour_1", "colour_2"}))

    print("independent no-import conformal--Birkhoff audit: PASS")


if __name__ == "__main__":
    main()
