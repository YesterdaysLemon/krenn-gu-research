"""Independent no-import audit for the GLS45 silent-shore reduction.

The audit imports no project module or third-party package.  It uses separate
finite-field elimination and exhaustive residual-factor/quotient-line
classifications, independently of the SymPy primary verifier.
"""

from __future__ import annotations

from itertools import combinations, product


P = 3
Vector = tuple[int, int, int]
FlatMatrix = tuple[int, ...]


def rank_mod(rows: list[list[int]]) -> int:
    work = [[value % P for value in row] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, P)
        work[pivot_row] = [(value * inverse) % P for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_value) % P
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def vector_rank(vectors: list[Vector]) -> int:
    return rank_mod([list(row) for row in zip(*vectors)]) if vectors else 0


def outer(left: Vector, right: Vector) -> FlatMatrix:
    return tuple((left[i] * right[j]) % P for i in range(3) for j in range(3))


def add(left: FlatMatrix, right: FlatMatrix) -> FlatMatrix:
    return tuple((a + b) % P for a, b in zip(left, right))


def span_rank(matrices: list[FlatMatrix]) -> int:
    return rank_mod([list(row) for row in zip(*matrices)]) if matrices else 0


def nonzero(vector: Vector) -> bool:
    return any(vector)


def check_complete_residual_factorization_atlas() -> None:
    vectors = list(product(range(P), repeat=3))
    allowed = {(2, 0), (0, 2), (1, 1), (1, 0), (0, 1), (0, 0)}
    seen: set[tuple[int, int]] = set()
    counts = {profile: 0 for profile in allowed}
    dense = 0
    sparse = 0
    checked = 0
    for a_0, a_1, b_0, b_1 in product(vectors, repeat=4):
        q = add(outer(a_0, b_1), outer(a_1, b_0))
        if nonzero(q):
            continue
        profile = (vector_rank([a_0, a_1]), vector_rank([b_0, b_1]))
        assert profile in allowed
        seen.add(profile)
        counts[profile] += 1
        if profile == (1, 1):
            active_a = (nonzero(a_0), nonzero(a_1))
            active_b = (nonzero(b_0), nonzero(b_1))
            assert active_a == active_b
            if active_a == (True, True):
                dense += 1
            else:
                assert active_a in ((True, False), (False, True))
                sparse += 1
        checked += 1
    assert seen == allowed
    assert counts == {
        (0, 0): 1,
        (0, 1): 104,
        (0, 2): 624,
        (1, 0): 104,
        (1, 1): 2704,
        (2, 0): 624,
    }
    assert dense > 0 and sparse > 0
    assert checked > 1_000


def check_fixed_factor_intersections() -> None:
    zero = (0, 0, 0)
    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    diagonal = [outer(vector, vector) for vector in basis]
    projective = [
        vector
        for vector in product(range(P), repeat=3)
        if vector != zero
        and next(value for value in vector if value) == 1
    ]

    for a in projective:
        fixed = [outer(a, vector) for vector in basis]
        expected = 5 if sum(value != 0 for value in a) == 1 else 6
        assert span_rank(fixed) == 3
        assert span_rank(diagonal + fixed) == expected

    planes = 0
    for a, b in combinations(projective, 2):
        if vector_rank([a, b]) != 2:
            continue
        fixed = [outer(left, right) for left in (a, b) for right in basis]
        assert span_rank(fixed) == 6
        planes += 1
    assert planes > 0


def check_dense_quotient_line_classification() -> None:
    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    diagonal = [outer(vector, vector) for vector in basis]
    vectors = list(product(range(P), repeat=3))
    compatible = 0

    for i, j in product(range(3), repeat=2):
        for y_prime in vectors:
            if not nonzero(y_prime) or y_prime[i] != 0:
                continue
            row_excess = outer(basis[i], y_prime)
            for x_prime in vectors:
                if not nonzero(x_prime) or x_prime[j] != 0:
                    continue
                column_excess = outer(x_prime, basis[j])
                if span_rank(diagonal + [row_excess, column_excess]) != 4:
                    continue
                compatible += 1
                # The representatives have zero diagonal, so equality of
                # their quotient lines is literal proportionality.
                assert span_rank([row_excess, column_excess]) == 1
                assert i != j
                assert vector_rank([y_prime, basis[j]]) == 1
                assert vector_rank([x_prime, basis[i]]) == 1

                # Hence the aggregate port plane already contains the
                # residual shore and cannot generate a third direction.
                assert vector_rank([basis[i], basis[j], x_prime]) == 2
                assert vector_rank([basis[j], basis[i], y_prime]) == 2
    assert compatible > 0


def check_dense_abstract_span_census() -> None:
    """Exhaust the dense fixed-factor endgame over all F_3 lines/planes."""

    zero = (0, 0, 0)
    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    diagonal = [outer(vector, vector) for vector in basis]
    vectors = list(product(range(P), repeat=3))
    projective = [
        vector
        for vector in vectors
        if vector != zero
        and next(value for value in vector if value) == 1
    ]

    planes: list[list[Vector]] = []
    for normal in projective:
        kernel = [
            vector
            for vector in vectors
            if vector != zero
            and sum(a * b for a, b in zip(normal, vector)) % P == 0
        ]
        first = kernel[0]
        second = next(vector for vector in kernel[1:] if vector_rank([first, vector]) == 2)
        planes.append([first, second])
    spaces = planes + [basis]

    histogram: dict[int, int] = {}
    cases = 0
    for a in projective:
        x_spaces = [space for space in spaces if vector_rank([a, *space]) == 3]
        for b in projective:
            y_spaces = [space for space in spaces if vector_rank([b, *space]) == 3]
            for x_space in x_spaces:
                for y_space in y_spaces:
                    generators = diagonal + [
                        *(outer(a, y) for y in y_space),
                        *(outer(x, b) for x in x_space),
                    ]
                    dimension = span_rank(generators)
                    histogram[dimension] = histogram.get(dimension, 0) + 1
                    assert dimension >= 5
                    cases += 1
    assert cases == 16_900
    assert histogram == {5: 54, 6: 2490, 7: 12684, 8: 1672}


def main() -> None:
    check_complete_residual_factorization_atlas()
    check_fixed_factor_intersections()
    check_dense_quotient_line_classification()
    check_dense_abstract_span_census()
    print("GLS45 silent rank-four shore-profile no-import audit: PASS")


if __name__ == "__main__":
    main()
