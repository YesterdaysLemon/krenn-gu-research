"""Independent stdlib audit of the S2O binary pullback reduction.

This file imports neither the primary replay nor repository modules. It uses
integer sparse monomials and explicit matching permutations.
"""

from __future__ import annotations

from itertools import permutations

Word = tuple[int, int, int]
Tensor = dict[Word, int]


def put(tensor: Tensor, word: Word, value: int) -> None:
    """Accumulate an integer sparse coefficient."""
    tensor[word] = tensor.get(word, 0) + value
    if tensor[word] == 0:
        del tensor[word]


def root_projection(tensor: Tensor, pivot: int) -> Tensor:
    """Apply the three coordinate projections killing root colour zero."""
    other = 3 - pivot
    return {
        word: value for word, value in tensor.items() if set(word) <= {pivot, other}
    }


def control(
    case: str, pivot: int, partner: int | None
) -> tuple[set[Word], dict[tuple[str, int], Tensor]]:
    """Build only the support/coefficient data needed by the reduction."""
    empty_support = {(0, 0, 0), (1, 1, 1), (2, 2, 2)}
    empty_support.remove((pivot, pivot, pivot))
    slices: dict[tuple[str, int], Tensor] = {
        (u, c): {} for u in ("x", "y", "r") for c in range(3)
    }

    if case == "outside":
        assert partner is None
        put(slices[("r", 0)], (pivot, pivot, pivot), 1)
        put(slices[("r", 0)], (0, 0, 1), -1)
        put(slices[("y", 0)], (0, 1, 0), 1)
        put(slices[("x", 0)], (1, 0, 0), 1)
    elif case == "x":
        assert partner is not None
        put(slices[("r", pivot)], (0, 0, 1), 1)
        put(slices[("x", partner)], (0, 0, 1), -1)
        put(slices[("x", 0)], (pivot, pivot, pivot), 1)
        put(slices[("y", 0)], (0, 1, 0), 1)
    elif case == "y":
        assert partner is not None
        put(slices[("r", pivot)], (0, 0, 1), 1)
        put(slices[("y", partner)], (0, 0, 1), -1)
        put(slices[("y", 0)], (pivot, pivot, pivot), 1)
        put(slices[("x", 0)], (0, 1, 0), 1)
    else:  # pragma: no cover
        raise AssertionError(case)
    return empty_support, slices


def integer_permanent(rows: tuple[tuple[int, int, int], ...]) -> int:
    """Compute a three-by-three permanent without external algebra."""
    total = 0
    for sigma in permutations(range(3)):
        total += rows[0][sigma[0]] * rows[1][sigma[1]] * rows[2][sigma[2]]
    return total


def main() -> None:
    """Reconstruct every projected control through an independent route."""
    specs = [("outside", a, None) for a in (1, 2)]
    specs.extend(
        (case, a, b) for case in ("x", "y") for a, b in ((1, 1), (1, 2), (2, 2))
    )

    for case, pivot, partner in specs:
        other = 3 - pivot
        empty, slices = control(case, pivot, partner)
        projected_empty = {word for word in empty if set(word) <= {pivot, other}}
        projected = {
            key: root_projection(tensor, pivot)
            for key, tensor in slices.items()
            if root_projection(tensor, pivot)
        }
        assert projected_empty == {(other, other, other)}
        assert list(projected.values()) == [{(pivot, pivot, pivot): 1}]
        assert all(
            not root_projection(slices[(u, other)], pivot) for u in ("x", "y", "r")
        )

    # Three columns in the plane u1+u2+u3=0 can have nonzero permanent.
    sharp = (
        (0, 3, 3),
        (1, 3, 2),
        (-1, -6, -5),
    )
    assert all(sum(sharp[row][col] for row in range(3)) == 0 for col in range(3))
    assert integer_permanent(sharp) == -48

    print("independent S2O pullback audit: PASS (8/8)")
    print("common binary residual: OPEN")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
