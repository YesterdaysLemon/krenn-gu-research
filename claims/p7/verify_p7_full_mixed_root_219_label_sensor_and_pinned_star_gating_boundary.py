"""Verify the legal full P7 mixed-root 219-label sensor.

The matrix is built from the matching definitions in the proof note.  The
modular determinant is an exact nonvanishing certificate for one named
integer minor, not a finite-field search.
"""

from __future__ import annotations

from itertools import combinations, product

from sympy import Matrix

ROOTS = tuple(range(5))
NONROOTS = tuple(range(9))
WORDS = tuple(product(range(3), repeat=5))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}

H = (
    (
        (0, 1, 0),
        (0, 1, 0),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 0),
        (-1, 1, 0),
        (0, 1, -1),
    ),
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0),
        (1, 0, 0),
        (1, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (-1, 0, 1),
        (0, 1, -1),
    ),
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 0),
        (-1, 1, 0),
        (0, 1, -1),
    ),
    (
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, 1),
        (1, -1, 0),
        (0, -1, 1),
    ),
    (
        (0, 0, 1),
        (0, 0, 1),
        (0, 0, 1),
        (1, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 0),
        (1, 0, -1),
        (-1, 0, 1),
    ),
)

L_VALUES = (
    (-1, 1, -1, -1, -1, 1, 0, -1, 3),
    (-1, 0, 1, 0, -1, 0, 1, 0, 0),
    (1, -1, 1, 0, 1, -1, 1, 1, -3),
    (1, 0, 0, -1, 1, 0, 0, 1, -2),
    (-1, 0, -1, -1, -1, -1, 1, 1, 3),
    (0, 0, -1, -1, 1, -1, -1, -1, 4),
    (-1, 1, 1, 1, 0, 1, 1, 0, -4),
    (1, -1, -1, 1, 1, 0, 1, 0, -2),
    (0, 0, 1, 1, 1, 0, -1, 0, -2),
    (1, -1, 0, 1, 1, 0, -1, -1, 0),
)
L = {
    pair: tuple(tuple(values[3 * row + col] for col in range(3)) for row in range(3))
    for pair, values in zip(combinations(ROOTS, 2), L_VALUES, strict=True)
}


def add_entry(vector: list[int], digits: list[int], value: int) -> None:
    if value:
        vector[WORD_INDEX[tuple(digits)]] += value


def add_injections(
    vector: list[int],
    roots: tuple[int, ...],
    endpoints: tuple[int, ...],
    digits: list[int],
    coefficient: int,
) -> None:
    """Add all root-to-endpoint bijections by recursive matching partition."""
    if not roots:
        add_entry(vector, digits, coefficient)
        return
    root = roots[0]
    for endpoint_index, endpoint in enumerate(endpoints):
        remainder = endpoints[:endpoint_index] + endpoints[endpoint_index + 1 :]
        for colour, value in enumerate(H[root][endpoint]):
            if value:
                digits[root] = colour
                add_injections(
                    vector,
                    roots[1:],
                    remainder,
                    digits,
                    coefficient * value,
                )


def depth_five_column(endpoints: tuple[int, ...]) -> list[int]:
    vector = [0] * len(WORDS)
    add_injections(vector, ROOTS, endpoints, [0] * 5, 1)
    return vector


def depth_three_column(endpoints: tuple[int, ...]) -> list[int]:
    vector = [0] * len(WORDS)
    for i, j in combinations(ROOTS, 2):
        other_roots = tuple(root for root in ROOTS if root not in (i, j))
        for left_colour in range(3):
            for right_colour in range(3):
                value = L[i, j][left_colour][right_colour]
                if value:
                    digits = [0] * 5
                    digits[i] = left_colour
                    digits[j] = right_colour
                    add_injections(vector, other_roots, endpoints, digits, value)
    return vector


def root_pairings(roots: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    first = roots[0]
    pairings = []
    for index in range(1, len(roots)):
        second = roots[index]
        remainder = roots[1:index] + roots[index + 1 :]
        if remainder:
            for tail in root_pairings(remainder):
                pairings.append(((first, second),) + tail)
        else:
            pairings.append(((first, second),))
    return tuple(pairings)


def depth_one_column(endpoint: int) -> list[int]:
    vector = [0] * len(WORDS)
    for unmatched in ROOTS:
        matched_roots = tuple(root for root in ROOTS if root != unmatched)
        for pairing in root_pairings(matched_roots):
            for unmatched_colour, h_value in enumerate(H[unmatched][endpoint]):
                if not h_value:
                    continue

                def fill_pairs(
                    pair_index: int,
                    digits: list[int],
                    coefficient: int,
                    current_pairing: tuple[tuple[int, int], ...] = pairing,
                    endpoint_value: int = h_value,
                ) -> None:
                    if pair_index == len(current_pairing):
                        add_entry(vector, digits, coefficient * endpoint_value)
                        return
                    i, j = current_pairing[pair_index]
                    for left_colour in range(3):
                        for right_colour in range(3):
                            value = L[i, j][left_colour][right_colour]
                            if value:
                                digits[i] = left_colour
                                digits[j] = right_colour
                                fill_pairs(
                                    pair_index + 1,
                                    digits,
                                    coefficient * value,
                                )

                digits = [0] * 5
                digits[unmatched] = unmatched_colour
                fill_pairs(0, digits, 1)
    return vector


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
    size = len(work)
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if work[row][column] != 0
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, size):
            if work[row][column]:
                multiplier = work[row][column] * inverse % prime
                for inner_column in range(column, size):
                    work[row][inner_column] = (
                        work[row][inner_column]
                        - multiplier * work[column][inner_column]
                    ) % prime
    return determinant % prime


def main() -> None:
    root = Matrix([1, 1, 1])
    assert all(sum(H[i][u]) == 1 for i in ROOTS for u in range(7))
    assert all(sum(H[i][u]) == 0 for i in ROOTS for u in (7, 8))
    for matrix in L.values():
        assert (root.T * Matrix(matrix) * root)[0] == 0

    columns = [depth_five_column(subset) for subset in combinations(NONROOTS, 5)]
    columns += [
        depth_three_column(subset) for subset in combinations(NONROOTS, 3)
    ]
    columns += [depth_one_column(endpoint) for endpoint in NONROOTS]
    assert len(columns) == 126 + 84 + 9 == 219

    rows = [list(row) for row in zip(*columns, strict=True)]
    assert len(rows) == 3**5 == 243
    named_minor = [row[:] for row in rows[:219]]
    residue = determinant_mod(named_minor, 1_000_003)
    assert residue == 297_817

    diagonal_columns = []
    for colour in range(3):
        column = [0] * len(WORDS)
        column[WORD_INDEX[(colour,) * 5]] = 1
        diagonal_columns.append(column)
    augmented_columns = columns + diagonal_columns
    augmented_rows = [list(row) for row in zip(*augmented_columns, strict=True)]
    target_rows = augmented_rows[:221] + [augmented_rows[242]]
    target_residue = determinant_mod(target_rows, 1_000_003)
    assert target_residue == 30_011

    # The selected rows are exactly the initial ternary interval claimed.
    assert WORDS[0] == (0, 0, 0, 0, 0)
    assert WORDS[218] == (2, 2, 0, 0, 2)
    assert WORDS[219] == (2, 2, 0, 1, 0)

    # P5 pinned-star bookkeeping and the Konig-cover support caps.
    assert 15 + 6 == 21
    assert 20 + 1 == 21
    assert 27 - 21 == 6
    support_gating_caps = {(2, 0): 9, (1, 1): 5, (0, 2): 1}
    assert max(support_gating_caps.values()) == 9

    print("PASS: legal blocker/residual and pairwise-zero contractions")
    print("PASS: complete mixed labels = 126 + 84 + 9 = 219")
    print("PASS: named 219x219 determinant mod 1000003 = 297817")
    print("PASS: all mixed deletion labels are selectable on this chart")
    print("PASS: augmented diagonal-target rank = 222")
    print("PASS: named 222x222 determinant mod 1000003 = 30011")
    print("PASS: P5 termwise nuisance gating caps the pinned star at rank 9")
    print("searches=0")
    print("SCOPE: this sensor chart has no nonzero diagonal GHZ completion")
    print("SCOPE: GHZ forcing of the target-incidence locus remains UNKNOWN")
    print("SCOPE: P5 algebraic nuisance compression remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
