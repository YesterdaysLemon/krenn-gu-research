"""Independent no-import audit of binary quotient coherence."""

from fractions import Fraction
from itertools import combinations

ZERO = (Fraction(0), Fraction(0))
E0 = (Fraction(1), Fraction(0))
E1 = (Fraction(0), Fraction(1))

TYPES = {
    "0": (ZERO, ZERO),
    "X": (E0, ZERO),
    "Y": (ZERO, E0),
    "B": (E0, (Fraction(2), Fraction(0))),
    "G": (E0, E1),
}


def tensor(left, right):
    return tuple(a * b for a in left for b in right)


def two_column_rank(left, right):
    left_nonzero = any(left)
    right_nonzero = any(right)
    if not left_nonzero and not right_nonzero:
        return 0
    if not left_nonzero or not right_nonzero:
        return 1
    pivot = next(index for index, value in enumerate(left) if value)
    ratio = right[pivot] / left[pivot]
    return 1 if all(r == ratio * ell for ell, r in zip(left, right)) else 2


def pair_rank(left, right):
    return two_column_rank(
        tensor(left[0], right[0]),
        tensor(left[1], right[1]),
    )


def main():
    incompatible = {
        (left, right)
        for left in TYPES
        for right in TYPES
        if pair_rank(TYPES[left], TYPES[right]) == 2
    }
    assert incompatible == {
        ("G", "B"),
        ("B", "G"),
        ("G", "G"),
    }

    common_line = [
        ((Fraction(1),), (Fraction(value),)) for value in range(1, 8)
    ]
    assert all(
        pair_rank(common_line[left], common_line[right]) == 1
        for left, right in combinations(range(7), 2)
    )

    one_plane = [TYPES["G"]] + [
        TYPES["X"] if index % 2 else TYPES["Y"] for index in range(1, 7)
    ]
    assert all(
        pair_rank(one_plane[left], one_plane[right]) <= 1
        for left, right in combinations(range(7), 2)
    )

    print("AUDIT PASS: exact five-type compatibility table")
    print("AUDIT PASS: both seven-mode global alternatives are sharp")
    print("searches=0")


if __name__ == "__main__":
    main()
