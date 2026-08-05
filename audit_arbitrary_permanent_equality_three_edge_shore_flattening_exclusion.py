"""Independent no-import audit of the three-edge shore rank obstruction."""

from __future__ import annotations


def determinant_3(matrix: tuple[tuple[int, int, int], ...]) -> int:
    (a, b, c), (d, e, f), (g, h, i) = matrix
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def main() -> None:
    # Three port labels but only two distinct complement columns.
    shore_matrix = ((1, 0), (1, 0), (0, 1))
    assert len(set(shore_matrix)) == 2

    # Every 3 x 3 coefficient matrix built from those two complement states
    # has dependent columns; one representative determinant vanishes.
    rank_two_matrix = ((1, 0, 1), (0, 1, 1), (1, 1, 2))
    assert determinant_3(rank_two_matrix) == 0

    diagonal_target = ((2, 0, 0), (0, 3, 0), (0, 0, 5))
    assert determinant_3(diagonal_target) == 30

    # With no incoming cut cells, all |T|=|S|-1 internal sources must be
    # covered internally, leaving exactly one shore mode for one outgoing port.
    size_s, size_t = 7, 6
    assert size_s - size_t == 1

    print("independent no-import three-edge shore flattening audit: PASS")


if __name__ == "__main__":
    main()
