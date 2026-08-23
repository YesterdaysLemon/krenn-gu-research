"""Independent no-import audit for the GLS47 complete-pair exclusion.

The audit uses only exact finite-field arithmetic and a representation unlike
the symbolic primary.  It exhausts quotient complements, rank-one physical
diagonal candidates, external vectors, and triangle-block multiplicities.
The written proof carries the characteristic-zero theorem.
"""

from __future__ import annotations

from itertools import combinations, product


PRIME = 3


def rank_mod(rows: list[list[int]] | tuple[tuple[int, ...], ...]) -> int:
    """Exact row rank over F3."""

    work = [[entry % PRIME for entry in row] for row in rows]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, PRIME)
        work[rank] = [(entry * inverse) % PRIME for entry in work[rank]]
        for index, row in enumerate(work):
            if index == rank or row[column] == 0:
                continue
            multiple = row[column]
            work[index] = [
                (left - multiple * right) % PRIME
                for left, right in zip(row, work[rank], strict=True)
            ]
        rank += 1
    return rank


def projective_vectors(length: int) -> tuple[tuple[int, ...], ...]:
    representatives = []
    for vector in product(range(PRIME), repeat=length):
        first = next((entry for entry in vector if entry), None)
        if first is None:
            continue
        inverse = pow(first, -1, PRIME)
        normalized = tuple((entry * inverse) % PRIME for entry in vector)
        if normalized == vector:
            representatives.append(vector)
    return tuple(representatives)


def add_scaled(
    left: tuple[int, ...],
    right: tuple[int, ...],
    scale: int,
) -> tuple[int, ...]:
    return tuple(
        (a + scale * b) % PRIME for a, b in zip(left, right, strict=True)
    )


def as_rows(matrix: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(matrix[3 * row : 3 * row + 3]) for row in range(3))


def rank_one_factors(
    matrix: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    rows = as_rows(matrix)
    if rank_mod(rows) != 1:
        return None
    column = next(
        tuple(rows[row][index] for row in range(3))
        for index in range(3)
        if any(rows[row][index] for row in range(3))
    )
    row = next(candidate for candidate in rows if any(candidate))
    return column, row


def quotient_complement_census() -> dict[str, int]:
    """Audit that any rank-one physical basis kills skew and diagonal zeros."""

    sym01 = (0, 1, 0, 1, 0, 0, 0, 0, 0)
    sym02 = (0, 0, 1, 0, 0, 0, 1, 0, 0)
    sym12 = (0, 0, 0, 0, 0, 1, 0, 1, 0)
    symmetric_basis = (sym01, sym02, sym12)
    quotient_lines = projective_vectors(6)
    coefficient_lines = projective_vectors(4)
    admissible = 0
    maximum_rank_one = 0
    for d0, d1, d2, k01, k02, k12 in quotient_lines:
        complement = (
            d0,
            k01,
            k02,
            0,
            d1,
            k12,
            0,
            0,
            d2,
        )
        rank_one = []
        for coefficients in coefficient_lines:
            matrix = (0,) * 9
            for scale, basis in zip(coefficients[:3], symmetric_basis, strict=True):
                matrix = add_scaled(matrix, basis, scale)
            matrix = add_scaled(matrix, complement, coefficients[3])
            factors = rank_one_factors(matrix)
            if factors is not None:
                rank_one.append(factors)
        maximum_rank_one = max(maximum_rank_one, len(rank_one))

        has_physical_basis = False
        for triple in combinations(rank_one, 3):
            left = tuple(factors[0] for factors in triple)
            right = tuple(factors[1] for factors in triple)
            if rank_mod(left) == 3 and rank_mod(right) == 3:
                has_physical_basis = True
                break
        if not has_physical_basis:
            continue
        admissible += 1
        assert k01 == k02 == k12 == 0
        assert d0 and d1 and d2

    assert len(quotient_lines) == 364
    assert admissible > 0
    return {
        "quotient_lines": len(quotient_lines),
        "admissible_rank_one_bases": admissible,
        "maximum_rank_one_points": maximum_rank_one,
    }


def outer(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a * b % PRIME for a in left for b in right)


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % PRIME for a, b in zip(left, right, strict=True))


def in_normal_space(matrix: tuple[int, ...], diagonal: tuple[int, ...]) -> bool:
    rows = as_rows(matrix)
    if any(rows[row][column] != rows[column][row] for row in range(3) for column in range(3)):
        return False
    matrix_diagonal = tuple(rows[index][index] for index in range(3))
    return rank_mod((matrix_diagonal, diagonal)) <= 1


def pair_with_coordinate(
    left: tuple[int, ...],
    right: tuple[int, ...],
    color: int,
) -> tuple[int, ...]:
    unit = tuple(1 if index == color else 0 for index in range(3))
    return add(outer(left, unit), outer(unit, right))


def label_lock_census() -> dict[str, int]:
    """Exhaust every vector in every full-support diagonal normal form."""

    full_diagonals = tuple(
        vector for vector in projective_vectors(3) if all(vector)
    )
    vectors = tuple(product(range(PRIME), repeat=3))
    external_compatible = 0
    block_compatible = 0
    for diagonal in full_diagonals:
        for left, right in product(vectors, repeat=2):
            external = all(
                in_normal_space(pair_with_coordinate(left, right, color), diagonal)
                for color in range(3)
            )
            if external:
                external_compatible += 1
                assert not any(left)
                assert not any(right)

            for color in range(3):
                mates = tuple(index for index in range(3) if index != color)
                block = all(
                    in_normal_space(pair_with_coordinate(left, right, mate), diagonal)
                    for mate in mates
                )
                if not block:
                    continue
                block_compatible += 1
                assert left == right
                assert all(
                    entry == 0 for index, entry in enumerate(left) if index != color
                )

    assert len(full_diagonals) == 4
    assert external_compatible == len(full_diagonals)
    return {
        "full_diagonal_lines": len(full_diagonals),
        "external_compatible": external_compatible,
        "block_compatible": block_compatible,
    }


def main() -> None:
    complements = quotient_complement_census()
    locks = label_lock_census()
    print("GLS47 independent no-import rank-four exclusion audit: PASS")
    print("  F3 quotient/rank-one-basis census:", complements)
    print("  F3 external/block-lock census:", locks)
    print("  every admissible complement is symmetric with full diagonal")
    print("  every external vector is zero; each triangle block is scalar")
    print("  finite F3 audit is not the characteristic-zero proof")
    print("  ranks >=5 and global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
