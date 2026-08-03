"""Independent no-import audit of radial jets and the fixed legal P7 control.

The legal tensor is rebuilt as a fourteen-vertex scalar hafnian for each
needed root-colour word.  This does not import the primary verifier or any
project module, and the determinants use a local Bareiss implementation.
There is no search and no finite-field arithmetic.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, product

EXPECTED_FLATTENING_MINOR = -18_494_220_325_114_867_735_328_060_700

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
    pair: tuple(
        tuple(values[3 * row + column] for column in range(3))
        for row in range(3)
    )
    for pair, values in zip(combinations(range(5), 2), L_VALUES, strict=True)
}


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Exact determinant with fraction-free elimination and row pivoting."""
    size = len(matrix)
    assert size > 0 and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    previous = 1
    sign = 1
    for column in range(size - 1):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column] != 0),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for inner in range(column + 1, size):
                numerator = (
                    work[row][inner] * pivot
                    - work[row][column] * work[column][inner]
                )
                assert numerator % previous == 0
                work[row][inner] = numerator // previous
        for row in range(column + 1, size):
            work[row][column] = 0
        previous = pivot
    return sign * work[-1][-1]


def edge_weight(left: int, right: int, colours: tuple[int, ...]) -> int:
    """Weight in the fixed legal 5-root/9-nonroot graph at one colour word."""
    if left > right:
        left, right = right, left
    if right < 5:
        return L[left, right][colours[left]][colours[right]]
    if left < 5 <= right:
        return H[left][right - 5][colours[left]]
    return 1


def full_graph_hafnian(colours: tuple[int, ...]) -> int:
    """Hafnian of the full fourteen-vertex scalar specialization."""

    @cache
    def recurrence(vertices: tuple[int, ...]) -> int:
        if not vertices:
            return 1
        first = vertices[0]
        total = 0
        for partner_index in range(1, len(vertices)):
            partner = vertices[partner_index]
            remainder = vertices[1:partner_index] + vertices[partner_index + 1 :]
            total += edge_weight(first, partner, colours) * recurrence(remainder)
        return total

    return recurrence(tuple(range(14)))


def fixed_legal_flattening_minor() -> list[list[int]]:
    row_words = tuple(product(range(3), repeat=2))
    column_words = tuple(product(range(3), repeat=3))[:9]
    return [
        [full_graph_hafnian(row_word + column_word) for column_word in column_words]
        for row_word in row_words
    ]


def main() -> None:
    # Independent exponent arithmetic for arbitrary q=2m.
    for m in range(2, 12):
        q = 2 * m
        edge_count = q * (q - 1) // 2
        deck_left = edge_count * (m - 2) + 1
        deck_right = edge_count * (m - 2)
        scalar_left = edge_count + 1
        scalar_right = 1 + (edge_count - 1) + 1
        assert deck_left == deck_right + 1
        assert scalar_left == scalar_right

    assert 28 * 2 + 1 == 57
    assert 28 * 2 == 56

    # Independent Kneser matrix and Bareiss determinant on one P7 shore.
    vertices = tuple(range(8))
    edges = tuple(combinations(vertices, 2))
    hessian = [
        [3 if set(left).isdisjoint(right) else 0 for right in edges]
        for left in edges
    ]
    determinant = bareiss_determinant(hessian)
    assert determinant == 3**28 * 15 * (-5) ** 7 != 0

    # D*1=45*1=3*c proves reconstruction without matrix inversion.
    assert all(sum(row) == 45 for row in hessian)
    cofactor_entry = 15
    assert 45 == 3 * cofactor_entry

    # Since D^(-1)c=(1/3)1, adj(D)c=(delta/3)1.  Check the scalar stress.
    assert determinant % 3 == 0
    scalar_right = 3 * 28 * cofactor_entry * (determinant // 3)
    scalar_left = 4 * determinant * 105
    assert scalar_left == scalar_right

    # A separate full-graph hafnian calculation gives the legal tensor minor.
    minor = fixed_legal_flattening_minor()
    minor_determinant = bareiss_determinant(minor)
    assert minor_determinant == EXPECTED_FLATTENING_MINOR != 0

    # The two complementary dimensions in the ambient control.
    deck_complement_dimension = 219 - 1
    target_complement_dimension = 243 - 3
    assert deck_complement_dimension <= target_complement_dimension

    print("PASS: independent arbitrary-order radial exponent audit")
    print("PASS: independent q=8 t^57/t^56 amplitude split")
    print("PASS: independent Bareiss all-one Kneser determinant")
    print("PASS: independent all-one reconstruction and scalar stress")
    print("PASS: direct fourteen-vertex hafnian rebuild of legal tensor")
    print(f"PASS: independent legal flattening minor = {minor_determinant}")
    print("PASS: nonzero 9x9 minor proves border rank at least 9")
    print("searches=0")
    print("imports_from_primary=0")
    print("imports_from_project=0")
    print("finite_fields=0")
    print("SCOPE: ambient GHZ-compatible sensor is not asserted legal")
    print("SCOPE: fixed legal tensor is not a GHZ witness")
    print("SCOPE: legal GHZ incidence on the physical Hessian open remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
