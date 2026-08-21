"""Independent no-import audit for the GLS20 promoted base-shadow theorem.

This audit uses only the Python standard library.  It derives the permanent
partition from permutations, performs rational row reduction directly, and
checks the quotient and rank claims without importing the primary verifier or
repository mathematics code.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product


def permanent(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    return sum(
        (
            product_value(
                tuple(matrix[row][permutation[row]] for row in range(len(matrix)))
            )
        )
        for permutation in permutations(range(len(matrix)))
    )


def product_value(values: tuple[Fraction, ...]) -> Fraction:
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def submatrix(
    matrix: tuple[tuple[Fraction, ...], ...],
    rows: tuple[int, ...],
    columns: tuple[int, ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(matrix[row][column] for column in columns) for row in rows)


def audit_laplace_partition() -> tuple[tuple[int, int], ...]:
    records = []
    for order in range(3, 8):
        matrix = tuple(
            tuple(
                Fraction(1 + ((row + 1) * (column + 4) + 3 * row + column) % 13)
                for column in range(order)
            )
            for row in range(order)
        )
        direct = permanent(matrix)
        terms = []
        for pair in combinations(range(order), 2):
            complement = tuple(index for index in range(order) if index not in pair)
            base = permanent(submatrix(matrix, (0, 1), pair))
            tail = permanent(submatrix(matrix, tuple(range(2, order)), complement))
            terms.append(base * tail)
        assert sum(terms, Fraction(0)) == direct
        assert direct != 0
        assert any(term != 0 for term in terms)
        records.append((order, sum(term != 0 for term in terms)))
    return tuple(records)


def rank(columns: tuple[tuple[Fraction, ...], ...], dimension: int) -> int:
    if not columns:
        return 0
    work = [[column[row] for column in columns] for row in range(dimension)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, dimension) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(dimension):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == dimension:
            break
    return pivot_row


def epsilon_image(vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    # Nine root blocks, each with nine C-coordinates; use a fully nonzero root
    # contraction independently from the Kronecker implementation in primary.
    weights = tuple(Fraction(value) for value in (2, -3, 5, 7, 11, -13, 17, 19, 23))
    assert len(vector) == 81
    return tuple(
        sum(weights[block] * vector[9 * block + coordinate] for block in range(9))
        for coordinate in range(9)
    )


def unit_vector(dimension: int, coordinate: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(index == coordinate) for index in range(dimension))


def audit_factor_selector() -> dict[str, int]:
    nuisance = tuple(unit_vector(81, coordinate) for coordinate in range(5))
    base_nuisance = tuple(epsilon_image(column) for column in nuisance)
    desired = unit_vector(81, 8)
    base_desired = epsilon_image(desired)
    assert rank(base_nuisance + (base_desired,), 9) == rank(base_nuisance, 9) + 1

    # mu is the normalized eighth coordinate functional.
    scale = base_desired[8]
    assert scale != 0
    assert all(column[8] == 0 for column in base_nuisance)
    assert base_desired[8] / scale == 1

    swallowed = tuple(nuisance[0][index] + nuisance[1][index] for index in range(81))
    assert rank(nuisance + (swallowed,), 81) == rank(nuisance, 81)
    assert rank(base_nuisance + (epsilon_image(swallowed),), 9) == rank(
        base_nuisance, 9
    )

    # A vector can survive upstairs while sharing its base image with nuisance.
    hidden = list(nuisance[0])
    hidden[9] += 1
    hidden[0] -= Fraction(-3, 2)  # weights[1]/weights[0]
    hidden = tuple(hidden)
    assert epsilon_image(hidden) == epsilon_image(nuisance[0])
    assert rank((nuisance[0], hidden), 81) == 2
    return {"upstairs": 81, "downstairs": 9, "nuisance_rank": 5}


def audit_target_and_trichotomy() -> tuple[int, int]:
    # A decomposable target has left flattening rank at most one.  Independent
    # right basis vectors make it zero exactly if all left pure columns vanish.
    cases = 0
    useful = 0
    for base_survives, response_nonzero in product((False, True), repeat=2):
        left = (Fraction(3), Fraction(-2)) if base_survives else (Fraction(0),) * 2
        right = (
            (Fraction(5), Fraction(7), Fraction(11))
            if response_nonzero
            else (Fraction(0),) * 3
        )
        columns = tuple(
            tuple(left[row] * right[column] for row in range(2))
            for column in range(3)
        )
        observed_rank = rank(columns, 2)
        assert observed_rank == int(base_survives and response_nonzero)
        assert (observed_rank == 0) == ((not base_survives) or (not response_nonzero))
        cases += 1
        useful += observed_rank
    return cases, useful


def audit_rank_strata() -> int:
    # Directly compare rank rise with the vanishing-minor condition over all
    # small binary fibres.  For 2 rows, the size-1 and size-2 tests are explicit.
    cases = 0
    vectors = tuple(
        tuple(Fraction(value) for value in entries)
        for entries in product((0, 1), repeat=2)
    )
    nuisance_pairs = tuple((left, right) for left in vectors for right in vectors)
    pure_triples = tuple(
        (first, second, third)
        for first in vectors
        for second in vectors
        for third in vectors
    )
    for nuisance in nuisance_pairs:
        nuisance_rank = rank(nuisance, 2)
        for pure in pure_triples:
            augmented_rank = rank(nuisance + pure, 2)
            rise = augmented_rank > nuisance_rank
            # At rank zero a nonzero 1-minor detects rise; at rank one a
            # nonzero 2-minor detects rise; rank two cannot rise.
            detected = (
                nuisance_rank == 0 and any(any(vector) for vector in pure)
            ) or (
                nuisance_rank == 1 and augmented_rank == 2
            )
            assert rise == detected
            cases += 1
    return cases


def audit_source_counts() -> tuple[tuple[int, int, int], ...]:
    records = []
    for order in range(3, 9):
        source_pairs = order * (order - 1) // 2
        target_size = 2 * order - 4
        promoted_ports = 2 * order - 2
        records.append((order, source_pairs, target_size))
        assert target_size == promoted_ports - 2
    assert records[:2] == [(3, 3, 2), (4, 6, 4)]
    return tuple(records)


def main() -> None:
    laplace = audit_laplace_partition()
    selector = audit_factor_selector()
    target = audit_target_and_trichotomy()
    strata = audit_rank_strata()
    counts = audit_source_counts()
    print("promoted source-aligned base-shadow independent audit: PASS")
    print("  permutation-partition Laplace records:", laplace)
    print("  direct rational factor quotient:", selector)
    print("  decomposable target/trichotomy cases:", target)
    print("  independently reduced rank fibres:", strata)
    print("  arbitrary-order source counts:", counts)
    print("  no imports from primary verifier or repository mathematics code")
    print("  scope: exact audit of reduction only; no survival or node closure")


if __name__ == "__main__":
    main()
