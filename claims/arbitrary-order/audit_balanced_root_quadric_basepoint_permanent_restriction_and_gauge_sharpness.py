"""Independent no-import audit of the root-quadric basepoint bridge fixture."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from math import factorial

Matrix = tuple[tuple[Fraction, ...], ...]
Vertices = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


def matrix(rows: list[list[int | Fraction]]) -> Matrix:
    """Convert nested rows to an immutable exact matrix."""
    return tuple(tuple(Fraction(value) for value in row) for row in rows)


def transpose(value: Matrix) -> Matrix:
    """Transpose an exact matrix."""
    return tuple(tuple(row) for row in zip(*value, strict=True))


def multiply(left: Matrix, right: Matrix) -> Matrix:
    """Multiply exact matrices."""
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(3)),
                Fraction(0),
            )
            for column in range(3)
        )
        for row in range(3)
    )


def determinant(value: Matrix) -> Fraction:
    """Return an exact determinant by recursive cofactor expansion."""
    size = len(value)
    if size == 1:
        return value[0][0]
    total = Fraction(0)
    for column in range(size):
        minor = tuple(
            tuple(value[row][other] for other in range(size) if other != column)
            for row in range(1, size)
        )
        total += (-1) ** column * value[0][column] * determinant(minor)
    return total


def inverse(value: Matrix) -> Matrix:
    """Invert a nonsingular 3-by-3 matrix by exact elimination."""
    size = len(value)
    augmented = [
        list(value[row])
        + [Fraction(1 if row == column else 0) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                left - factor * right
                for left, right in zip(augmented[row], augmented[column], strict=True)
            ]
    return tuple(tuple(row[size:]) for row in augmented)


IDENTITY = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


@cache
def perfect_matchings(vertices: Vertices) -> tuple[Matching, ...]:
    """Generate labelled perfect matchings independently of the primary."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            result.append(((first, partner),) + tail)
    return tuple(result)


def construction_matrices() -> tuple[Matrix, ...]:
    """Build the rational gauge table without importing SymPy or primary code."""
    return (
        IDENTITY,
        matrix([[-1, 0, 0], [0, 1, -1], [0, 0, -1]]),
        matrix([[0, 0, -1], [0, -1, 0], [1, 0, 0]]),
        matrix([[0, -1, 0], [0, 1, 1], [-1, 0, 1]]),
        matrix([[0, 1, 0], [-1, 0, 0], [0, 0, -1]]),
        matrix([[1, 0, 0], [0, 1, 0], [0, 0, -1]]),
        matrix([[-1, 0, 0], [0, 0, 1], [0, 1, 0]]),
        matrix(
            [
                [0, 0, Fraction(1, 6)],
                [Fraction(1, 3), 0, 0],
                [0, Fraction(1, 3), 0],
            ]
        ),
    )


def coefficient(
    word: tuple[int, ...], blocks: dict[tuple[int, int], Matrix]
) -> Fraction:
    """Evaluate one graph-tensor coefficient by direct matching recursion."""
    total = Fraction(0)
    for matching_value in perfect_matchings(tuple(range(len(word)))):
        term = Fraction(1)
        for left, right in matching_value:
            term *= blocks[(left, right)][word[left]][word[right]]
        total += term
    return total


def audit_matching_bridge() -> dict[int, tuple[int, int]]:
    """Count the exact matchings surviving pairwise root annihilation."""
    ledger: dict[int, tuple[int, int]] = {}
    for m in range(2, 7):
        roots = set(range(m))
        matchings = perfect_matchings(tuple(range(2 * m)))
        survivors = []
        for matching_value in matchings:
            if any(left in roots and right in roots for left, right in matching_value):
                continue
            survivors.append(matching_value)
            assert all(
                (left in roots) != (right in roots) for left, right in matching_value
            )
        assert len(survivors) == factorial(m)
        ledger[m] = (len(matchings), len(survivors))
    return ledger


def quadratic_column(block: Matrix) -> tuple[Fraction, ...]:
    """Return coefficients of x^T block x in the fixed monomial order."""
    return (
        block[0][0],
        block[1][1],
        block[2][2],
        block[0][1] + block[1][0],
        block[0][2] + block[2][0],
        block[1][2] + block[2][1],
    )


def audit_sharpness_fixture() -> dict[str, object]:
    """Audit normalization, basepoint freedom, and latent synchronization."""
    gauges = construction_matrices()
    blocks = {
        (left, right): multiply(transpose(gauges[left]), gauges[right])
        for left in range(8)
        for right in range(left + 1, 8)
    }

    gauge_determinants = tuple(determinant(value) for value in gauges)
    assert gauge_determinants == (
        1,
        1,
        -1,
        1,
        -1,
        -1,
        1,
        Fraction(1, 54),
    )
    block_determinants = {determinant(value) for value in blocks.values()}
    assert block_determinants == {
        Fraction(-1),
        Fraction(1),
        Fraction(-1, 54),
        Fraction(1, 54),
    }

    pure = tuple(coefficient((colour,) * 8, blocks) for colour in range(3))
    mixed = coefficient((0, 0, 1, 1, 1, 1, 1, 1), blocks)
    assert pure == (1, 1, 1)
    assert mixed == -1

    columns = [
        quadratic_column(blocks[(left, right)])
        for left in range(4)
        for right in range(left + 1, 4)
    ]
    coefficient_matrix = tuple(
        tuple(columns[column][row] for column in range(6)) for row in range(6)
    )
    expected = matrix(
        [
            [-1, 0, 0, 0, 0, -1],
            [1, -1, 1, -1, 1, -1],
            [-1, 0, 1, 0, -2, 0],
            [0, 0, -1, 0, 1, 0],
            [0, 0, -1, 0, 1, 1],
            [-1, 0, 1, 1, 0, 0],
        ]
    )
    assert coefficient_matrix == expected
    assert determinant(coefficient_matrix) == -1

    for (left, right), block in blocks.items():
        synchronized = multiply(
            transpose(inverse(gauges[left])), multiply(block, inverse(gauges[right]))
        )
        assert synchronized == IDENTITY

    return {
        "pure_coefficients": pure,
        "mixed_00111111": mixed,
        "root_quadric_determinant": determinant(coefficient_matrix),
        "invertible_blocks": len(blocks),
        "latent_common_form_edges": len(blocks),
    }


def main() -> None:
    bridge = audit_matching_bridge()
    sharpness = audit_sharpness_fixture()
    print("balanced root-quadric basepoint bridge independent audit: PASS")
    print(f"  matching counts (all, all-cross): {bridge}")
    print(f"  exact rational gauge fixture: {sharpness}")


if __name__ == "__main__":
    main()
