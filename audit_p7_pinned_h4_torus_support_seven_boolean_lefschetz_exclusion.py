"""Independent stdlib audit of the P7 support-seven Boolean-Lefschetz exclusion."""

from fractions import Fraction
from itertools import combinations

VERTICES = tuple(range(7))
PAIRS = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))
FOURS = tuple(combinations(VERTICES, 4))


def bareiss_det(matrix: list[list[int]]) -> int:
    """Exact fraction-free determinant with row pivoting."""
    work = [row[:] for row in matrix]
    size = len(work)
    if any(len(row) != size for row in work):
        raise AssertionError("determinant requires a square matrix")
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if work[row][pivot_index] != 0
                ),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for col in range(pivot_index + 1, size):
                numerator = work[row][col] * pivot - work[row][pivot_index] * work[
                    pivot_index
                ][col]
                if numerator % previous != 0:
                    raise AssertionError("Bareiss division ceased to be exact")
                work[row][col] = numerator // previous
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


def inclusion(
    rows: tuple[tuple[int, ...], ...], cols: tuple[tuple[int, ...], ...]
) -> list[list[int]]:
    return [
        [int(set(col).issubset(row)) for col in cols]
        for row in rows
    ]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in right_t]
        for row in left
    ]


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        divisor = work[rank][column]
        work[rank] = [value / divisor for value in work[rank]]
        for row in range(rank + 1, len(work)):
            if not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def audit_coefficient_tensor() -> None:
    """Compare the row expansion, direct factorization, and reciprocal form."""
    for four in FOURS:
        four_set = set(four)
        for pair in PAIRS:
            pair_set = set(pair)
            # Coefficient of u_k D_pair in the direct sum of four hafnians.
            hafnian_coefficients = [0] * 7
            for omitted in four:
                triple = four_set - {omitted}
                if pair_set.issubset(triple):
                    remaining = triple - pair_set
                    if len(remaining) == 1:
                        hafnian_coefficients[next(iter(remaining))] += 1

            # W34*m_u has one contribution for each intermediate triple.
            factor_coefficients = [0] * 7
            for triple in TRIPLES:
                triple_set = set(triple)
                if triple_set.issubset(four_set) and pair_set.issubset(triple_set):
                    remaining = triple_set - pair_set
                    if len(remaining) == 1:
                        factor_coefficients[next(iter(remaining))] += 1

            assert hafnian_coefficients == factor_coefficients

            expected = [0] * 7
            if pair_set.issubset(four_set):
                for vertex in four_set - pair_set:
                    expected[vertex] = 1
            assert hafnian_coefficients == expected

            # In the reciprocal form, the same two complementary indices
            # carry q. Clearing by prod_U u and E_pair=D_pair/prod_pair u
            # swaps each reciprocal label to the other complementary u label,
            # yielding the same unordered sum.
            reciprocal_indices = {
                next(iter(four_set - set(triple)))
                for triple in TRIPLES
                if pair_set.issubset(triple) and set(triple).issubset(four_set)
            }
            assert reciprocal_indices == (
                four_set - pair_set if pair_set.issubset(four_set) else set()
            )


def main() -> None:
    w23 = inclusion(TRIPLES, PAIRS)
    w34 = inclusion(FOURS, TRIPLES)
    gram23 = multiply(transpose(w23), w23)

    assert len(w23) == 35 and len(w23[0]) == 21
    assert len(w34) == 35 and len(w34[0]) == 35

    # Independently recover the Gram pattern 3I+R^T R.
    for i, pair_i in enumerate(PAIRS):
        for j, pair_j in enumerate(PAIRS):
            expected = 5 if i == j else int(bool(set(pair_i) & set(pair_j)))
            assert gram23[i][j] == expected

    gram_det = bareiss_det(gram23)
    middle_det = bareiss_det(w34)
    assert gram_det == 15 * 8**6 * 3**14
    assert middle_det == -(2**16) * 3**6

    vertices8 = tuple(range(8))
    fours8 = tuple(combinations(vertices8, 4))
    fives8 = tuple(combinations(vertices8, 5))
    w45_8 = inclusion(fives8, fours8)
    assert rational_rank(w45_8) == 56
    assert len(fours8) - 56 == 14

    audit_coefficient_tensor()

    print("PASS: independent universal complement-row coefficient audit")
    print(f"det Gram(W23)={gram_det}")
    print(f"det W34={middle_det}")
    print("PASS: both Boolean incidence factors have the required exact rank")
    print("CONCLUSION: P7 full-edge-torus support-seven circuits are impossible")
    print("PASS: independent primitive Boolean-space dimension = 14")
    print("AUDIT BOUNDARY: support-eight torus intersection remains UNKNOWN")


if __name__ == "__main__":
    main()
