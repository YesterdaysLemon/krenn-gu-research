"""Independent no-import audit of the common/noncommon exclusion."""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, Iterable

Vector = tuple[Fraction, ...]
Projection = Callable[[Vector], Vector]


def vector(*entries: int) -> Vector:
    return tuple(Fraction(entry) for entry in entries)


def phi_1(v: Vector) -> Vector:
    x_0, x_1, x_2, x_3, x_4, x_5 = v
    return (x_1, x_4, x_5, x_3 - x_2 - x_0)


def phi_2(v: Vector) -> Vector:
    x_0, x_1, x_2, x_3, x_4, x_5 = v
    return (x_0, x_4, x_5, x_3 - x_2 - x_1)


def rank(columns: Iterable[Vector]) -> int:
    cols = list(columns)
    if not cols:
        return 0
    rows = [list(row) for row in zip(*cols, strict=True)]
    pivot_row = 0
    for col in range(len(cols)):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][col]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [entry / scale for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [
                    entry - scale * base
                    for entry, base in zip(rows[row], rows[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def killed(projection: Projection, v: Vector) -> bool:
    return projection(v) == vector(0, 0, 0, 0)


def main() -> None:
    lines = {
        "N": vector(0, 0, 1, 1, 0, 0),
        "A0": vector(1, 0, 0, 1, 0, 0),
        "C0": vector(1, 0, -1, 0, 0, 0),
        "A1": vector(0, 1, 0, 1, 0, 0),
        "C1": vector(0, 1, -1, 0, 0, 0),
    }

    # Reconstruct the common ambient kernel directly from the coordinate
    # equations.  A vector killed by both maps has x0=x1=x4=x5=0 and x3=x2.
    n = lines["N"]
    assert killed(phi_1, n) and killed(phi_2, n)
    intersection_equations = (
        vector(1, 0, 0, 0, 0, 0),
        vector(0, 1, 0, 0, 0, 0),
        vector(0, 0, -1, 1, 0, 0),
        vector(0, 0, 0, 0, 1, 0),
        vector(0, 0, 0, 0, 0, 1),
    )
    assert rank(intersection_equations) == 5
    assert all(sum(a * b for a, b in zip(row, n, strict=True)) == 0 for row in intersection_equations)

    for name in ("A0", "C0"):
        assert killed(phi_1, lines[name])
    for name in ("A1", "C1"):
        assert killed(phi_2, lines[name])

    forbidden = (
        ("N", "A1", phi_2),
        ("N", "C1", phi_2),
        ("A0", "N", phi_1),
        ("C0", "N", phi_1),
    )
    for left, right, projection in forbidden:
        pair = (lines[left], lines[right])
        assert rank(pair) == 2
        assert all(killed(projection, v) for v in pair)

        # Rank-nullity on a three-dimensional local plane: two independent
        # killed vectors force rank at most 3-2=1, contradicting the proved
        # target-dependent rank floor of two.
        forced_upper_rank = 3 - rank(pair)
        assert forced_upper_rank == 1

    # N/N contributes only one independent killed direction and therefore
    # does not itself contradict the rank-two floor.
    assert rank((n, n)) == 1
    assert 3 - rank((n, n)) == 2

    print("independent common-kernel reconstruction: PASS")
    print("four common/noncommon rank-nullity exclusions: PASS")
    print("proportional N/N case: OPEN")


if __name__ == "__main__":
    main()
