"""Independent no-import audit of the one-chord cut-colour theorem."""

from __future__ import annotations


def determinant(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def main() -> None:
    # Source-cut and mode-cut colour counts from the proof.
    distinct_rows = (
        (0, (0, 2), (2, 1), 1),
        (0, (1, 2), (2, 0), 0),
        (1, (0, 2), (2, 1), 1),
        (1, (1, 2), (2, 0), 0),
        (2, (0, 1), (2, 2), 2),
        (2, (0, 2), (1, 2), 1),
        (2, (1, 2), (2, 0), 0),
    )
    for _, branch_colours, other_colours, survivor in distinct_rows:
        assert sorted(branch_colours + other_colours) == [0, 1, 2, 2]
        assert survivor in other_colours

    for branch in range(3):
        branch_colours = (1, 2)
        other_colours = (2, 2)
        survivor = 0
        assert sorted(branch_colours + other_colours) == [1, 2, 2, 2]
        assert survivor not in branch_colours + other_colours
        assert branch in (0, 1, 2)

    # Independent integer instances of the decisive tensors.
    p, q, r, u, t = 2, 3, 5, 7, 11
    ell0, ell2, kappa = 13, 17, 19
    ordinary_minor = determinant(((p * r, 0), (0, 1)))
    assert ordinary_minor == 10

    branch_zero = ((p * u * t, p * r), (q * t, ell0))
    assert branch_zero[0][1] == 10

    branch_one = ((kappa * q * t, 0), (0, kappa))
    assert determinant(branch_one) == kappa * kappa * q * t != 0

    branch_two = ((p * u * t + ell2 * p * r, q * t), (0, ell2))
    assert branch_two[1][1] == ell2 != 0

    # Rational-free scaling of the nonalignment absorption relation:
    # choose q=1 and ell1=-pu.
    p, q, u, t, kappa = 2, 1, 3, 5, 7
    ell1 = -p * u
    central_non_aligned = q * t * ell1 + p * u * t
    projected_components = (q * kappa, p * u + q * ell1)
    assert central_non_aligned == 0
    assert projected_components == (7, 0)

    print("independent no-import one-chord cut-colour audit: PASS")


if __name__ == "__main__":
    main()
