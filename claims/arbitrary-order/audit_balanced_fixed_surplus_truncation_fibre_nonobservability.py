"""Independent bounded audit of the balanced fixed-surplus theorem.

This file deliberately imports no repository verifier.  It uses bitmask
matching/decomposition ledgers and exact rational row reduction on explicit
q=0 and q=1 fibre charts.  The arbitrary-order proof remains the written
matching argument in the owning theorem note.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import comb, factorial
from typing import Callable


Scalar = Fraction
Weight = Callable[[int, int], Scalar]


def even_masks(size: int) -> list[int]:
    return [mask for mask in range(1 << size) if mask.bit_count() % 2 == 0]


def odd_double_factorial(value: int) -> int:
    """Return value!! for odd value, with (-1)!! = 1."""

    if value == -1:
        return 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def matching_weight(mask: int, edge_weight: Weight) -> Scalar:
    """Exact weighted perfect-matching sum on the vertices in mask."""

    @lru_cache(maxsize=None)
    def recurse(state: int) -> Scalar:
        if state == 0:
            return Fraction(1)
        first_bit = state & -state
        first = first_bit.bit_length() - 1
        remainder = state ^ first_bit
        total = Fraction(0)
        partners = remainder
        while partners:
            partner_bit = partners & -partners
            partners ^= partner_bit
            partner = partner_bit.bit_length() - 1
            weight = edge_weight(first, partner)
            if weight:
                total += weight * recurse(remainder ^ partner_bit)
        return total

    return recurse(mask)


def rational_rank(matrix: list[list[Scalar]]) -> int:
    """Fraction-only Gaussian rank, without numerical tolerances."""

    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def companion_entry(
    shore_size: int,
    internal_n_mask: int,
    cross_weight: Weight,
    internal_a_weight: Weight,
) -> Scalar:
    """Sum a balanced companion cell by injections and an A-shore hafnian."""

    full_mask = (1 << shore_size) - 1
    cross_vertices = full_mask ^ internal_n_mask

    @lru_cache(maxsize=None)
    def assign(remaining_n: int, unused_a: int) -> Scalar:
        if remaining_n == 0:
            return matching_weight(unused_a, internal_a_weight)
        n_bit = remaining_n & -remaining_n
        n_vertex = n_bit.bit_length() - 1
        total = Fraction(0)
        candidates = unused_a
        while candidates:
            a_bit = candidates & -candidates
            candidates ^= a_bit
            a_vertex = a_bit.bit_length() - 1
            weight = cross_weight(a_vertex, n_vertex)
            if weight:
                total += weight * assign(
                    remaining_n ^ n_bit, unused_a ^ a_bit
                )
        return total

    return assign(cross_vertices, full_mask)


def feasible_leftover_depths(r: int, q: int) -> set[int]:
    """Depths whose A leftovers can match without an old-root--old-root edge."""

    shore_size = r + q
    full_mask = (1 << shore_size) - 1

    def allowed(left: int, right: int) -> Scalar:
        return Fraction(not (left < r and right < r))

    depths: set[int] = set()
    for mask in range(full_mask + 1):
        if mask.bit_count() % 2:
            continue
        if matching_weight(mask, allowed):
            depths.add(mask.bit_count())
    return depths


def audit_truncation_and_capacity() -> int:
    cases = 0
    for r in range(2, 8):
        for q in range(0, 6):
            m = r + q
            largest_even = 2 * (m // 2)
            expected_depths = set(range(0, min(2 * q, largest_even) + 1, 2))
            actual_depths = feasible_leftover_depths(r, q)
            assert actual_depths == expected_depths

            legal_depths = set(range(0, largest_even + 1, 2))
            forced_depths = legal_depths - actual_depths
            assert bool(forced_depths) == (r >= q + 2)

            surviving_columns = sum(comb(m, depth) for depth in actual_depths)
            formula_columns = sum(
                comb(m, 2 * index) for index in range(min(q, m // 2) + 1)
            )
            assert surviving_columns == formula_columns
            assert len(even_masks(m)) == 2 ** (m - 1)

            if r == q + 1:
                assert not forced_depths
                if q >= 1:
                    assert 3**q < 2 ** (m - 1)
            if r >= 3 and q <= r:
                assert 3**q < 2 ** (r + q - 1)
            cases += 1
    return cases


def audit_top_cut_multiplicity() -> int:
    cases = 0
    for r in range(2, 7):
        for q in range(0, 5):
            outside_size = r + 2 * q
            good_cuts = 0
            for chosen in combinations(range(outside_size), q):
                cut = set(chosen)
                if any(vertex in cut for vertex in range(r)):
                    continue
                if all(
                    len(cut & {r + 2 * index, r + 2 * index + 1}) == 1
                    for index in range(q)
                ):
                    good_cuts += 1
            assert good_cuts == 2**q
            cases += 1
    return cases


def canonical_q0_rank(r: int) -> tuple[int, int]:
    """Canonical q=0 chart: only the all-cross column survives."""

    columns = even_masks(r)
    matrix = [[Fraction(mask == 0) for mask in columns]]
    return rational_rank(matrix), len(columns)


def canonical_q1_rank() -> tuple[int, int]:
    """An explicit canonical q=1 chart inside xi_R tensor L_q^*."""

    r = 3
    shore_size = r + 1
    columns = even_masks(shore_size)
    basis_vectors = [
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    ]

    def coordinate_entry(column: int, coordinate: int) -> Scalar:
        def cross_weight(a_vertex: int, n_vertex: int) -> Scalar:
            if a_vertex < r and n_vertex < r:
                return Fraction(a_vertex == n_vertex)
            if a_vertex == r and n_vertex == r:
                return basis_vectors[0][coordinate]
            return Fraction(0)

        def internal_weight(left: int, right: int) -> Scalar:
            if left == r and right < r:
                return basis_vectors[right][coordinate]
            if right == r and left < r:
                return basis_vectors[left][coordinate]
            return Fraction(0)

        return companion_entry(
            shore_size, column, cross_weight, internal_weight
        )

    matrix = [
        [coordinate_entry(column, coordinate) for column in columns]
        for coordinate in range(3)
    ]
    return rational_rank(matrix), len(columns)


def q0_fibre_matrix(r: int, lam: Scalar, mu: Scalar) -> tuple[list[int], list[list[Scalar]]]:
    columns = even_masks(r)
    rows = columns
    matrix: list[list[Scalar]] = []
    for word_mask in rows:
        row: list[Scalar] = []
        for column_mask in columns:

            def cross_weight(root: int, outside: int) -> Scalar:
                root_uses_b = bool(word_mask & (1 << root))
                return Fraction(0) if root_uses_b or root != outside else lam

            def internal_weight(left: int, right: int) -> Scalar:
                both_use_b = bool(word_mask & (1 << left)) and bool(
                    word_mask & (1 << right)
                )
                return mu if both_use_b else Fraction(0)

            row.append(
                companion_entry(r, column_mask, cross_weight, internal_weight)
            )
        matrix.append(row)
    return columns, matrix


def q1_fibre_matrix(r: int, lam: Scalar, mu: Scalar) -> tuple[list[int], list[list[Scalar]]]:
    shore_size = r + 1
    columns = even_masks(shore_size)
    rows = columns
    matrix: list[list[Scalar]] = []
    for word_mask in rows:
        row: list[Scalar] = []
        for column_mask in columns:

            def cross_weight(a_vertex: int, n_vertex: int) -> Scalar:
                uses_b = bool(word_mask & (1 << a_vertex))
                if a_vertex < r and n_vertex < r:
                    return Fraction(0) if uses_b or a_vertex != n_vertex else lam
                if a_vertex == r and n_vertex == r:
                    return Fraction(0) if uses_b else Fraction(1)
                return Fraction(0)

            def internal_weight(left: int, right: int) -> Scalar:
                if not (
                    word_mask & (1 << left) and word_mask & (1 << right)
                ):
                    return Fraction(0)
                if left < r and right < r:
                    return lam
                return lam * mu

            row.append(
                companion_entry(
                    shore_size, column_mask, cross_weight, internal_weight
                )
            )
        matrix.append(row)
    return columns, matrix


def audit_fibre_ranks() -> tuple[list[str], int]:
    # One concrete ternary covector basis: xi(x)=1 and a,b annihilate x.
    covector_matrix = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(-1), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(-1)],
    ]
    assert rational_rank(covector_matrix) == 3
    root_vector = (Fraction(1), Fraction(1), Fraction(1))
    assert sum(covector_matrix[0][i] * root_vector[i] for i in range(3)) == 1
    assert sum(covector_matrix[1][i] * root_vector[i] for i in range(3)) == 0
    assert sum(covector_matrix[2][i] * root_vector[i] for i in range(3)) == 0

    summaries: list[str] = []
    checked = 0
    for r in (4, 5):
        canonical_rank, column_count = canonical_q0_rank(r)
        assert canonical_rank == 1
        columns, matrix = q0_fibre_matrix(r, Fraction(2), Fraction(3))
        assert len(columns) == column_count
        for row_index, word_mask in enumerate(columns):
            for column_index, column_mask in enumerate(columns):
                expected = Fraction(0)
                if word_mask == column_mask:
                    size = word_mask.bit_count()
                    expected = Fraction(odd_double_factorial(size - 1))
                    expected *= Fraction(2) ** (r - size)
                    expected *= Fraction(3) ** (size // 2)
                assert matrix[row_index][column_index] == expected
        assert rational_rank(matrix) == column_count
        summaries.append(f"q=0,r={r}:1->{column_count}")
        checked += 1

    canonical_rank, _ = canonical_q1_rank()
    assert canonical_rank == 3
    for r in (3, 4):
        columns, matrix = q1_fibre_matrix(r, Fraction(2), Fraction(5))
        for row_index, word_mask in enumerate(columns):
            for column_index, column_mask in enumerate(columns):
                expected = Fraction(0)
                if word_mask == column_mask:
                    size = word_mask.bit_count()
                    expected = Fraction(odd_double_factorial(size - 1))
                    if word_mask & (1 << r):
                        expected *= Fraction(2) ** (r - size // 2 + 1)
                        expected *= Fraction(5)
                    else:
                        expected *= Fraction(2) ** (r - size // 2)
                assert matrix[row_index][column_index] == expected
        assert rational_rank(matrix) == len(columns)
        summaries.append(f"q=1,r={r}:<=3->{len(columns)}")
        checked += 1
    return summaries, checked


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def audit_wick_constants() -> int:
    checked = 0
    for q in range(1, 5):
        vertices = tuple(range(2 * q))
        a_vertices = set(range(q))
        bipartite_matchings = 0
        for matching in perfect_matchings(vertices):
            if all((left in a_vertices) != (right in a_vertices) for left, right in matching):
                bipartite_matchings += 1
        assert bipartite_matchings == factorial(q)

        repeated_row_assignments = 0
        row_types = (0,) * q + (1,) * q
        column_types = row_types
        for assignment in permutations(range(2 * q)):
            if all(
                row_types[row] == column_types[column]
                for row, column in enumerate(assignment)
            ):
                repeated_row_assignments += 1
        assert repeated_row_assignments == factorial(q) ** 2
        assert repeated_row_assignments // bipartite_matchings == factorial(q)
        checked += 1
    return checked


def edge_pointing_multiplicities(vertex_count: int) -> set[int]:
    counts: dict[tuple[tuple[int, int], ...], int] = {}
    vertices = tuple(range(vertex_count))
    for left, right in combinations(vertices, 2):
        remainder = tuple(vertex for vertex in vertices if vertex not in {left, right})
        for rest in perfect_matchings(remainder):
            matching = tuple(sorted(((left, right),) + rest))
            counts[matching] = counts.get(matching, 0) + 1
    return set(counts.values())


def audit_absorption_constants() -> int:
    checked = 0
    for q in range(0, 5):
        assert edge_pointing_multiplicities(2 * q + 2) == {q + 1}
        for p in range(0, 3):
            assert edge_pointing_multiplicities(2 * (q + p + 1)) == {q + p + 1}
            residual = (q + p + 1) - (q + 1)
            assert residual == p
            checked += 1
    return checked


def audit_hall_constants() -> int:
    checked = 0
    for r in range(2, 10):
        for q in range(1, 9):
            common_two_row_possible = 6 * q <= 2 * (r + 2 * q)
            assert common_two_row_possible == (q <= r)
            existing_row_possible = 3 * (q + 1) <= r + 2 * q
            assert existing_row_possible == (r >= q + 3)
            checked += 1

    for q in range(2, 7):
        assignments = [(0, 1)] * q + [(1, 2)] * q + [(2, 0)] * q
        for family_index in (0, 1):
            counts = [
                sum(pair[family_index] == colour for pair in assignments)
                for colour in range(3)
            ]
            assert counts == [q, q, q]
        plane_counts = [
            sum(colour in pair for pair in assignments) for colour in range(3)
        ]
        assert plane_counts == [2 * q, 2 * q, 2 * q]
        assert all(left != right for left, right in assignments)

        repeated = [0] * (q + 1) + [1] * (q + 1) + [2] * (q + 1)
        assert len(repeated) == 3 * (q + 1)
        assert [repeated.count(colour) for colour in range(3)] == [q + 1] * 3
        checked += 1
    return checked


def main() -> None:
    truncation_cases = audit_truncation_and_capacity()
    cut_cases = audit_top_cut_multiplicity()
    fibre_summaries, fibre_cases = audit_fibre_ranks()
    wick_cases = audit_wick_constants()
    absorption_cases = audit_absorption_constants()
    hall_cases = audit_hall_constants()

    print("independent balanced fixed-surplus audit: PASS")
    print(f"truncation/capacity cases: {truncation_cases}")
    print(f"top-cut multiplicity cases: {cut_cases}")
    print("exact fibre ranks: " + ", ".join(fibre_summaries))
    print(
        "constant ledgers: "
        f"fibre={fibre_cases}, Wick={wick_cases}, "
        f"absorption={absorption_cases}, Hall={hall_cases}"
    )
    print(
        "scope: bounded bitmask/decomposition checks and exact rational "
        "fibre charts; arbitrary-order proof is written"
    )
    print("independent_audit: true")
    print("is_krenn_gu_witness: false")
    print("global_conjecture_resolved: false")


if __name__ == "__main__":
    main()
