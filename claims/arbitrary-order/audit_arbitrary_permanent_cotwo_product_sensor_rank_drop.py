"""No-import modular audit of the co-two permanent sensor boundary."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from math import comb


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    """Compute matrix rank over a prime field by custom row reduction."""
    if not matrix:
        return 0
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for row in range(row_count):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * basis) % prime
                for entry, basis in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def cross(left: tuple[int, int, int], right: tuple[int, int, int], prime: int):
    """Return the projective intersection of two line coefficient vectors."""
    return (
        (left[1] * right[2] - left[2] * right[1]) % prime,
        (left[2] * right[0] - left[0] * right[2]) % prime,
        (left[0] * right[1] - left[1] * right[0]) % prime,
    )


def evaluate(line: tuple[int, int, int], point: tuple[int, int, int], prime: int):
    """Evaluate a projective line at a point."""
    return sum(coefficient * coordinate for coefficient, coordinate in zip(line, point, strict=True)) % prime


def star_evaluation_matrix(r: int, prime: int) -> list[list[int]]:
    """Evaluate the products F_pq at every pairwise line intersection."""
    lines = [
        (1, parameter % prime, parameter * parameter % prime)
        for parameter in range(r)
    ]
    pairs = list(combinations(range(r), 2))
    matrix: list[list[int]] = []
    for omitted_row in pairs:
        point = cross(lines[omitted_row[0]], lines[omitted_row[1]], prime)
        assert point != (0, 0, 0)
        row: list[int] = []
        for omitted_column in pairs:
            value = 1
            for index, line in enumerate(lines):
                if index in omitted_column:
                    continue
                value = value * evaluate(line, point, prime) % prime
            row.append(value)
        matrix.append(row)
    return matrix


def audit_star_configuration() -> dict[int, tuple[int, int]]:
    """Audit the full ambient moment sensor by a separate evaluation route."""
    ledger: dict[int, tuple[int, int]] = {}
    for r in range(3, 11):
        ranks = []
        for prime in (101, 103):
            matrix = star_evaluation_matrix(r, prime)
            size = comb(r, 2)
            assert all(
                matrix[row][column] == 0
                for row in range(size)
                for column in range(size)
                if row != column
            )
            assert all(matrix[index][index] for index in range(size))
            rank = rank_mod(matrix, prime)
            assert rank == size
            ranks.append(rank)
        ledger[r] = (ranks[0], ranks[1])
    return ledger


def multiplication_matrix(coefficients: list[int]) -> list[list[int]]:
    """Build v -> uv from the coefficient equations u_p v_q+u_q v_p."""
    r = len(coefficients)
    return [
        [
            coefficients[right] if column == left
            else coefficients[left] if column == right
            else 0
            for column in range(r)
        ]
        for left, right in combinations(range(r), 2)
    ]


def audit_annihilator_ranks() -> dict[int, Counter[int]]:
    """Check every coordinate-support pattern through rank nine."""
    prime = 101
    ledger: dict[int, Counter[int]] = {}
    for r in range(3, 10):
        counts: Counter[int] = Counter()
        for support_mask in range(1, 1 << r):
            coefficients = [
                index + 1 if support_mask & (1 << index) else 0
                for index in range(r)
            ]
            support_size = support_mask.bit_count()
            expected_rank = r - 1 if support_size <= 2 else r
            actual_rank = rank_mod(multiplication_matrix(coefficients), prime)
            assert actual_rank == expected_rank
            counts[actual_rank] += 1
        ledger[r] = counts
    return ledger


def audit_complement_pairing_and_target_rank() -> dict[int, tuple[int, int]]:
    """Check the complement pairing and ternary diagonal flattening ranks."""
    ledger: dict[int, tuple[int, int]] = {}
    for r in range(3, 10):
        pairs = list(combinations(range(r), 2))
        complements = [
            tuple(index for index in range(r) if index not in pair)
            for pair in pairs
        ]
        pairing = [
            [int(set(pair).isdisjoint(complement) and len(pair) + len(complement) == r)
             for complement in complements]
            for pair in pairs
        ]
        pairing_rank = rank_mod(pairing, 101)
        assert pairing_rank == comb(r, 2)

        left_words = list(product(range(3), repeat=2))
        right_words = list(product(range(3), repeat=r - 2))
        target = [
            [int(len(set(left + right)) == 1) for right in right_words]
            for left in left_words
        ]
        target_rank = rank_mod(target, 101)
        assert target_rank == 3
        ledger[r] = (pairing_rank, target_rank)
    return ledger


def cyclic_coordinate_supports() -> list[list[int]]:
    """Encode the local coordinate forms in the P6 block model."""
    supports: list[list[int]] = []
    for block_start in (0, 3):
        for mode_offset in range(3):
            supports.append(
                [block_start + (colour + mode_offset) % 3 for colour in range(3)]
            )
    return supports


def support_span_dimension(supports: list[list[int]], modes: tuple[int, ...]) -> int:
    """Count the distinct nonzero square-free coordinate products."""
    monomials: set[int] = set()
    for word in product(range(3), repeat=len(modes)):
        coordinates = [
            supports[mode][colour]
            for mode, colour in zip(modes, word, strict=True)
        ]
        if len(set(coordinates)) != len(coordinates):
            continue
        monomials.add(sum(1 << coordinate for coordinate in coordinates))
    return len(monomials)


def audit_p6_support_model() -> dict[str, object]:
    """Independently audit sharp rank drop and the failed stronger inequality."""
    supports = cyclic_coordinate_supports()
    all_words = list(product(range(3), repeat=6))
    nonzero_words = []
    for word in all_words:
        coordinates = [supports[mode][colour] for mode, colour in enumerate(word)]
        if len(set(coordinates)) == 6:
            nonzero_words.append(word)
    assert len(nonzero_words) == 36
    assert all((colour,) * 6 in nonzero_words for colour in range(3))
    assert sum(len(set(word)) > 1 for word in nonzero_words) == 33

    left_words = list(product(range(3), repeat=3))
    right_words = list(product(range(3), repeat=3))
    nonzero_set = set(nonzero_words)
    flattening = [
        [int(left + right in nonzero_set) for right in right_words]
        for left in left_words
    ]
    assert rank_mod(flattening, 101) == 1

    four_mode_dimensions = {
        modes: support_span_dimension(supports, modes)
        for modes in combinations(range(6), 4)
    }
    histogram = Counter(four_mode_dimensions.values())
    assert histogram == Counter({3: 6, 9: 9})

    omitted = (1, 4)
    complement = tuple(index for index in range(6) if index not in omitted)
    pair_dimension = support_span_dimension(supports, omitted)
    complement_dimension = support_span_dimension(supports, complement)
    assert pair_dimension == complement_dimension == 9
    assert pair_dimension + complement_dimension == 18
    return {
        "nonzero_words": len(nonzero_words),
        "mixed_nonzero_words": 33,
        "flattening_rank": 1,
        "four_mode_histogram": dict(sorted(histogram.items())),
        "dimension_sum_countermodel": pair_dimension + complement_dimension,
    }


def main() -> None:
    stars = audit_star_configuration()
    annihilators = audit_annihilator_ranks()
    pairings = audit_complement_pairing_and_target_rank()
    p6 = audit_p6_support_model()
    print("arbitrary permanent co-two product-sensor independent audit: PASS")
    print(f"  star-evaluation ranks mod 101/103: {stars}")
    print(f"  annihilator-rank support ledgers: {annihilators}")
    print(f"  (perfect pairing, target flattening) ranks: {pairings}")
    print(f"  P6 support boundary: {p6}")


if __name__ == "__main__":
    main()
