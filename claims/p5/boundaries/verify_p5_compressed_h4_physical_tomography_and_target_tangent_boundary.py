"""Primary exact replay for compressed P5 four-hafnian tomography.

The script evaluates three named minors on one fixed legal integer chart.
It performs no graph, support, word, or parameter-family search.
"""

from functools import cache
from itertools import combinations, product

ROOTS = tuple(range(3))
NONROOTS = tuple(range(7))
BLOCKERS = tuple(range(5))
RESIDUALS = (5, 6)
WEIGHTS = (1, 2, 4)
WORDS = tuple(product(range(3), repeat=3))
DELETION_TRIPLES = tuple(combinations(NONROOTS, 3))
EDGES = tuple(combinations(NONROOTS, 2))
SENSOR_COLUMNS = tuple(range(27))
JACOBIAN_ROWS = tuple(range(21))
TARGET_ROWS = (*range(23), 26)
PURE_ROWS = (0, 13, 26)


def covector(root: int, endpoint: int) -> tuple[int, int, int]:
    """Return the fixed legal root--nonroot covector."""

    t = endpoint + 1
    a = t ** WEIGHTS[root]
    if endpoint in BLOCKERS:
        return (1, a, a * a)
    return (1, a, -1 - a)


@cache
def permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Permanent by exact first-row recurrence."""

    if not matrix:
        return 1
    total = 0
    for column, value in enumerate(matrix[0]):
        minor = tuple(
            tuple(row[j] for j in range(len(row)) if j != column)
            for row in matrix[1:]
        )
        total += value * permanent(minor)
    return total


def sensor_matrix() -> list[list[int]]:
    """Build Gamma_3 with rows ternary words and columns deletion triples."""

    rows: list[list[int]] = []
    for word in WORDS:
        row: list[int] = []
        for endpoints in DELETION_TRIPLES:
            matrix = tuple(
                tuple(covector(root, endpoint)[word[root]] for endpoint in endpoints)
                for root in ROOTS
            )
            row.append(permanent(matrix))
        rows.append(row)
    return rows


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    """Return a square integer determinant modulo a prime."""

    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            row for row in range(column, len(work)) if work[row][column]
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            factor = work[row][column] * inverse % prime
            for j in range(column, len(work)):
                work[row][j] = (work[row][j] - factor * work[column][j]) % prime
    return determinant % prime


def h4_jacobian_at_one() -> list[list[int]]:
    """Derivative of (H_(N minus D))_D at the all-one graph."""

    rows: list[list[int]] = []
    for deleted in DELETION_TRIPLES:
        shore = set(NONROOTS) - set(deleted)
        rows.append([int(set(edge).issubset(shore)) for edge in EDGES])
    return rows


def matrix_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    """Multiply rectangular integer matrices."""

    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in zip(*right)]
        for row in left
    ]


def main() -> None:
    for root in ROOTS:
        assert all(sum(covector(root, endpoint)) != 0 for endpoint in BLOCKERS)
        assert all(sum(covector(root, endpoint)) == 0 for endpoint in RESIDUALS)

    gamma = sensor_matrix()
    assert len(gamma) == 27
    assert len(gamma[0]) == len(DELETION_TRIPLES) == 35

    sensor_minor = [[row[column] for column in SENSOR_COLUMNS] for row in gamma]
    sensor_residue = determinant_mod(sensor_minor, 1_000_003)
    assert sensor_residue == 772_431

    deck_jacobian = h4_jacobian_at_one()
    composite_jacobian = matrix_product(gamma, deck_jacobian)
    jacobian_minor = [composite_jacobian[row] for row in JACOBIAN_ROWS]
    jacobian_residue = determinant_mod(jacobian_minor, 1_000_003)
    assert jacobian_residue == 953_249

    augmented = [
        row + [int(index == pure_row) for pure_row in PURE_ROWS]
        for index, row in enumerate(composite_jacobian)
    ]
    target_minor = [augmented[row] for row in TARGET_ROWS]
    target_residue = determinant_mod(target_minor, 1_000_003)
    assert target_residue == 686_920

    all_one_tensor = [3 * sum(row) for row in gamma]
    assert all_one_tensor[1] == 420_840
    assert any(
        value != 0
        for index, value in enumerate(all_one_tensor)
        if index not in PURE_ROWS
    )

    print("PASS: legal five-blocker/two-residual three-root chart")
    print("PASS: Gamma_3 rank = 27 and kernel dimension = 8")
    print("PASS: named 27x27 sensor determinant mod 1000003 = 772431")
    print("PASS: composite physical Jacobian rank = 21")
    print("PASS: named 21x21 determinant mod 1000003 = 953249")
    print("PASS: composite tangent plus diagonal target rank = 24")
    print("PASS: named 24x24 determinant mod 1000003 = 686920")
    print("PASS: all-one physical tensor is not diagonal-target compatible")
    print("searches=0 graph_enumerations=0 support_enumerations=0")
    print("SCOPE: generic finite recovery is only relative to known companions")
    print("SCOPE: physical diagonal-target incidence remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
