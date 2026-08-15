"""Primary exact checks for the same-mode common/noncommon exclusion."""

from __future__ import annotations

import sympy as sp


def column(*entries: int) -> sp.Matrix:
    return sp.Matrix(entries)


def projection_matrices() -> tuple[sp.Matrix, sp.Matrix]:
    phi_1 = sp.Matrix(
        (
            (0, 1, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 1),
            (-1, 0, -1, 1, 0, 0),
        )
    )
    phi_2 = sp.Matrix(
        (
            (1, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 1),
            (0, -1, -1, 1, 0, 0),
        )
    )
    return phi_1, phi_2


def normalized_line(vector: sp.Matrix) -> tuple[sp.Rational, ...]:
    first = next(entry for entry in vector if entry != 0)
    return tuple(sp.Rational(entry, first) for entry in vector)


def main() -> None:
    phi_1, phi_2 = projection_matrices()
    assert phi_1.rank() == phi_2.rank() == 4

    kernel_1 = phi_1.nullspace()
    kernel_2 = phi_2.nullspace()
    assert len(kernel_1) == len(kernel_2) == 2

    common = sp.Matrix.vstack(phi_1, phi_2).nullspace()
    n = column(0, 0, 1, 1, 0, 0)
    assert len(common) == 1
    assert normalized_line(common[0]) == normalized_line(n)

    lines = {
        "N": n,
        "A0": column(1, 0, 0, 1, 0, 0),
        "C0": column(1, 0, -1, 0, 0, 0),
        "A1": column(0, 1, 0, 1, 0, 0),
        "C1": column(0, 1, -1, 0, 0, 0),
    }
    zero = sp.zeros(4, 1)
    assert phi_1 * lines["N"] == phi_2 * lines["N"] == zero
    for name in ("A0", "C0"):
        assert phi_1 * lines[name] == zero
    for name in ("A1", "C1"):
        assert phi_2 * lines[name] == zero

    forbidden = (
        ("N", "A1", phi_2),
        ("N", "C1", phi_2),
        ("A0", "N", phi_1),
        ("C0", "N", phi_1),
    )
    for left, right, projection in forbidden:
        pair = sp.Matrix.hstack(lines[left], lines[right])
        assert pair.rank() == 2
        assert projection * pair == sp.zeros(4, 2)

        # Any three-space L containing this pair has restricted nullity at
        # least two, so its restricted projection rank is at most one.
        z = column(0, 0, 0, 0, 1, 0)
        local_basis = sp.Matrix.hstack(lines[left], lines[right], z)
        assert local_basis.rank() == 3
        assert (projection * local_basis).rank() <= 1

    # The common line by itself is compatible with the rank-two floor: a
    # sample local three-space has nullity exactly one for both families.
    sample = sp.Matrix.hstack(n, column(1, 0, 0, 0, 0, 0), column(0, 1, 0, 0, 0, 0))
    assert sample.rank() == 3
    assert (phi_1 * sample).rank() == (phi_2 * sample).rank() == 2

    print("ambient kernels: PASS (2,2 with common line N)")
    print("same-mode N/non-N pairs: PASS (restricted rank <= 1)")
    print("N/N boundary: OPEN (not excluded by rank-nullity)")


if __name__ == "__main__":
    main()
