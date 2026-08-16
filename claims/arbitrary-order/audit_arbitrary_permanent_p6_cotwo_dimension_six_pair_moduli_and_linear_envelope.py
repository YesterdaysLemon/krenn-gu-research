"""Independent no-import audit of the P6 dimension-six pair boundary.

This script uses standalone finite-field elimination at two primes.  It does
not import the primary replay, SymPy, or any repository helper.
"""

from __future__ import annotations

from itertools import combinations

N = 6
EDGES = tuple(combinations(range(N), 2))


def multiply(left: tuple[int, ...], right: tuple[int, ...]) -> list[int]:
    """Independently rebuild one square-free quadratic coefficient vector."""

    return [left[i] * right[j] + left[j] * right[i] for i, j in EDGES]


def rank_mod(rows: list[list[int]], prime: int) -> int:
    """Return matrix rank by standalone modular row reduction."""

    if not rows:
        return 0
    matrix = [[value % prime for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def nullspace_mod(rows: list[list[int]], prime: int) -> list[list[int]]:
    """Return a basis for the right kernel using an independent RREF route."""

    matrix = [[value % prime for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free = [column for column in range(column_count) if column not in pivots]
    basis: list[list[int]] = []
    for free_column in free:
        vector = [0] * column_count
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = (-matrix[row][free_column]) % prime
        basis.append(vector)
    return basis


def dot(left: list[int], right: list[int], prime: int) -> int:
    """Pair degree two with complement-indexed degree four."""

    return sum(a * b for a, b in zip(left, right, strict=True)) % prime


def audit_at_prime(prime: int) -> dict[str, int]:
    """Replay every finite-dimensional assertion over one exact field."""

    basis = (
        (1, 0, 0, 1, 0, 0),
        (0, 1, 0, 0, 1, 0),
        (0, 0, 1, 0, 0, 1),
    )
    assert rank_mod([list(vector) for vector in basis], prime) == 3
    assert {
        index for vector in basis for index, value in enumerate(vector) if value
    } == set(range(6))

    products = {
        (c, d): multiply(basis[c], basis[d]) for c in range(3) for d in range(c, 3)
    }
    keys = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    product_rows = [products[key] for key in keys]
    assert rank_mod(product_rows, prime) == 6

    named_edges = ((0, 3), (1, 4), (2, 5), (0, 1), (0, 2), (1, 2))
    named_minor_rows = [
        [products[key][EDGES.index(edge)] for key in keys] for edge in named_edges
    ]
    assert named_minor_rows == [
        [2, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    assert 8 % prime != 0

    mixed = [products[(0, 1)], products[(0, 2)], products[(1, 2)]]
    diagonal = [products[(0, 0)], products[(1, 1)], products[(2, 2)]]
    assert rank_mod(mixed, prime) == 3
    assert rank_mod(mixed + diagonal, prime) == 6

    envelope = nullspace_mod(mixed, prime)
    assert len(envelope) == 12
    assert all(
        dot(mixed_row, vector, prime) == 0 for mixed_row in mixed for vector in envelope
    )
    restricted_rows = [
        [dot(pair_row, vector, prime) for vector in envelope]
        for pair_row in mixed + diagonal
    ]
    assert restricted_rows[:3] == [[0] * 12 for _ in range(3)]
    assert rank_mod(restricted_rows, prime) == 3
    assert rank_mod(restricted_rows[3:], prime) == 3

    return {
        "prime": prime,
        "pair_rank": rank_mod(mixed + diagonal, prime),
        "mixed_rank": rank_mod(mixed, prime),
        "envelope_dimension": len(envelope),
        "restricted_rank": rank_mod(restricted_rows, prime),
        "named_minor_residue": 8 % prime,
    }


def main() -> None:
    """Run the independent exact audit."""

    profiles = [audit_at_prime(prime) for prime in (101, 103)]
    grassmann_dimension = 3 * 3
    effective_torus_dimension = 6 - 1
    assert grassmann_dimension == 9
    assert effective_torus_dimension == 5
    assert grassmann_dimension - effective_torus_dimension == 4

    print("P6 co-two dimension-six pair-moduli independent audit: PASS")
    print(f"  independent modular profiles: {profiles}")
    print("  Grassmann open / maximum orbit / gap: 9 / 5 / 4")
    print("  factorized four-mode sensor: NOT CONSTRUCTED")
    print("  simultaneous dimension-at-least-six residual: OPEN")
    print("  unrestricted P6 -> Delta_3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
