"""Exact primary checks for the A6 fixed-completion rank-three block.

This standalone verifier represents the four perfect matchings in the A5
``Q/Q`` and ``Q/C^2`` scalar controls by their actual edge-incidence vectors.
It checks exact affine and difference-lattice ranks, then verifies that adding
one fixed matching and its common nonzero weight preserves every difference.

The mixed-fibre checks are deliberately conditional: they test the algebra
after a compatible fixed completion has attached the four-term zero relation.
They do not assert that such a completion exists in every target fibre.  No
theorem, audit, or repository implementation is imported.  These exact checks
do not resolve the global Krenn--Gu conjecture, whose status is UNRESOLVED.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from typing import TypeAlias

Edge: TypeAlias = tuple[str, str]
Matching: TypeAlias = frozenset[Edge]
Vector: TypeAlias = tuple[int, ...]


def edge(left: str, right: str) -> Edge:
    """Return one undirected edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


def matrix_rank(rows: tuple[tuple[Fraction, ...], ...]) -> int:
    """Compute matrix rank over the rationals by exact row reduction."""

    if not rows:
        return 0
    width = len(rows[0])
    assert all(len(row) == width for row in rows)
    work = [list(row) for row in rows]
    pivot_row = 0

    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def incidence_vectors(matchings: tuple[Matching, ...]) -> tuple[Vector, ...]:
    """Return edge-incidence vectors in a deterministic common coordinate set."""

    coordinates = tuple(sorted(set().union(*matchings)))
    return tuple(
        tuple(int(item in matching) for item in coordinates) for matching in matchings
    )


def assert_perfect_matchings(
    matchings: tuple[Matching, ...], vertices: frozenset[str]
) -> None:
    """Check every represented edge set covers the stated vertices exactly once."""

    for matching in matchings:
        endpoints = tuple(vertex for item in matching for vertex in item)
        assert len(endpoints) == len(vertices)
        assert frozenset(endpoints) == vertices


def subtract(left: Vector, right: Vector) -> Vector:
    """Subtract two integer vectors coordinatewise."""

    assert len(left) == len(right)
    return tuple(a - b for a, b in zip(left, right, strict=True))


def rational_rows(rows: tuple[Vector, ...]) -> tuple[tuple[Fraction, ...], ...]:
    """Embed integer rows in the exact rational coefficient field."""

    return tuple(tuple(Fraction(entry) for entry in row) for row in rows)


def assert_rank_three_simplex(vectors: tuple[Vector, ...]) -> None:
    """Check affine independence and rank three of the difference lattice."""

    assert len(vectors) == 4
    assert len(set(vectors)) == 4
    differences = tuple(subtract(vector, vectors[0]) for vector in vectors[1:])
    all_differences = tuple(
        subtract(vectors[right], vectors[left])
        for left in range(4)
        for right in range(left + 1, 4)
    )
    assert matrix_rank(rational_rows(differences)) == 3
    assert matrix_rank(rational_rows(all_differences)) == 3

    # An affine dependency has coefficients c_i satisfying both sum(c_i)=0
    # and sum(c_i * vectors[i])=0.  The following exact augmented rank four
    # proves there is no nonzero rational, hence no nonzero integer, solution.
    affine_rows = (
        (Fraction(1),) * 4,
        *tuple(
            tuple(Fraction(vector[column]) for vector in vectors)
            for column in range(len(vectors[0]))
        ),
    )
    assert matrix_rank(affine_rows) == 4


def qq_matchings() -> tuple[Matching, ...]:
    """Build the four A5 Q/Q matchings on four length-three odd routes."""

    matchings: list[Matching] = []
    for selected in range(4):
        items: set[Edge] = set()
        for route in range(4):
            left = edge("v", f"p{route}")
            middle = edge(f"p{route}", f"q{route}")
            right = edge(f"q{route}", "w")
            items.update((left, right) if route == selected else (middle,))
        matchings.append(frozenset(items))
    return tuple(matchings)


def qc2_matchings() -> tuple[Matching, ...]:
    """Enumerate the four A5 Q/C2 matchings in its eight-vertex control."""

    rows = tuple(f"u{index}" for index in range(4))
    columns = tuple(f"w{index}" for index in range(4))
    supported = frozenset(
        {
            *(edge("u0", column) for column in columns),
            edge("u1", "w1"),
            edge("u1", "w3"),
            edge("u2", "w0"),
            edge("u2", "w2"),
            edge("u3", "w0"),
            edge("u3", "w1"),
        }
    )
    matchings = tuple(
        frozenset(
            edge(row, column) for row, column in zip(rows, assignment, strict=True)
        )
        for assignment in permutations(columns)
        if all(
            edge(row, column) in supported
            for row, column in zip(rows, assignment, strict=True)
        )
    )
    assert len(matchings) == 4
    return matchings


def matching_weights(matchings: tuple[Matching, ...]) -> tuple[Fraction, ...]:
    """Give only u0--w0 weight -3 and every other supported edge weight 1."""

    negative_edge = edge("u0", "w0")
    return tuple(
        Fraction(-3) if negative_edge in matching else Fraction(1)
        for matching in matchings
    )


def assert_fixed_completion(vectors: tuple[Vector, ...]) -> None:
    """Check a common incidence suffix and weight preserve the attached block."""

    fixed_incidence = (1, 1, 1)
    extended = tuple(vector + fixed_incidence for vector in vectors)
    original_differences = tuple(subtract(vector, vectors[0]) for vector in vectors[1:])
    extended_differences = tuple(
        subtract(vector, extended[0]) for vector in extended[1:]
    )
    assert extended_differences == tuple(
        difference + (0, 0, 0) for difference in original_differences
    )
    assert_rank_three_simplex(extended)

    source_weights = (Fraction(1), Fraction(1), Fraction(1), Fraction(-3))
    completion_weight = Fraction(-5, 7)
    attached_weights = tuple(completion_weight * value for value in source_weights)
    assert all(attached_weights)
    assert sum(attached_weights, start=Fraction(0)) == 0


def assert_qc2_doubletons(
    matchings: tuple[Matching, ...], weights: tuple[Fraction, ...]
) -> None:
    """Check the complementary nonzero exact-negative even-route ports."""

    first_port = edge("u3", "w0")
    second_port = edge("u3", "w1")
    first_indices = frozenset(
        index for index, matching in enumerate(matchings) if first_port in matching
    )
    second_indices = frozenset(
        index for index, matching in enumerate(matchings) if second_port in matching
    )
    assert len(first_indices) == len(second_indices) == 2
    assert first_indices.isdisjoint(second_indices)
    assert first_indices | second_indices == frozenset(range(4))
    first_sum = sum((weights[index] for index in first_indices), start=Fraction(0))
    second_sum = sum((weights[index] for index in second_indices), start=Fraction(0))
    assert (first_sum, second_sum) == (Fraction(2), Fraction(-2))
    assert first_sum != 0 and second_sum != 0
    assert first_sum == -second_sum


def zero_remainder(size: int) -> tuple[Fraction, ...]:
    """Construct a zero-sum remainder of any allowed cardinality."""

    assert size == 0 or size >= 2
    if size == 0:
        return ()
    return (Fraction(1),) * (size - 1) + (Fraction(1 - size),)


def assert_remainder_census(attached: tuple[Fraction, ...]) -> None:
    """Check empty and nonsingleton remainders, including sharp size two."""

    assert len(attached) == 4
    assert all(attached)
    assert sum(attached, start=Fraction(0)) == 0

    # A one-term zero remainder is impossible because its only monomial is
    # assumed nonzero.  This direct check does not rely on a finite search.
    arbitrary_nonzero = Fraction(11, 13)
    assert sum((arbitrary_nonzero,), start=Fraction(0)) == arbitrary_nonzero != 0

    complete_sizes: list[int] = []
    for remainder_size in (0, *range(2, 9)):
        remainder = zero_remainder(remainder_size)
        assert all(remainder)
        assert sum(remainder, start=Fraction(0)) == 0
        complete_fibre = attached + remainder
        assert all(complete_fibre)
        assert sum(complete_fibre, start=Fraction(0)) == 0
        complete_sizes.append(len(complete_fibre))

    assert zero_remainder(2) == (Fraction(1), Fraction(-1))
    assert complete_sizes == [4, 6, 7, 8, 9, 10, 11, 12]
    assert 5 not in complete_sizes


def assert_normalized_generator_is_nonunit() -> None:
    """Evaluate 1+X+Y+Z at a nonzero torus zero to certify nonunitness."""

    torus_point = (Fraction(1), Fraction(1), Fraction(-3))
    assert all(torus_point)
    normalized_value = Fraction(1) + sum(torus_point, start=Fraction(0))
    assert normalized_value == 0

    # Every Laurent monomial, and hence every Laurent-monomial unit over a
    # field, evaluates nonzero at a torus point.  The displayed generator has
    # a torus zero, so it is not a unit.  Independent exponent differences
    # were checked above; coefficient ratios are absorbed into X, Y, and Z.


def main() -> None:
    """Run all exact A6 fixed-completion and remainder checks."""

    qq = qq_matchings()
    qc2 = qc2_matchings()
    qq_vertices = frozenset(
        {
            "v",
            "w",
            *(f"p{index}" for index in range(4)),
            *(f"q{index}" for index in range(4)),
        }
    )
    qc2_vertices = frozenset(
        {*(f"u{index}" for index in range(4)), *(f"w{index}" for index in range(4))}
    )
    assert_perfect_matchings(qq, qq_vertices)
    assert_perfect_matchings(qc2, qc2_vertices)
    qq_vectors = incidence_vectors(qq)
    qc2_vectors = incidence_vectors(qc2)
    assert_rank_three_simplex(qq_vectors)
    assert_rank_three_simplex(qc2_vectors)
    assert_fixed_completion(qq_vectors)
    assert_fixed_completion(qc2_vectors)

    qq_weights = (Fraction(1), Fraction(1), Fraction(1), Fraction(-3))
    qc2_weights = matching_weights(qc2)
    assert sorted(qc2_weights) == [Fraction(-3), Fraction(1), Fraction(1), Fraction(1)]
    assert sum(qq_weights, start=Fraction(0)) == 0
    assert sum(qc2_weights, start=Fraction(0)) == 0
    assert_qc2_doubletons(qc2, qc2_weights)

    completion_weight = Fraction(-5, 7)
    attached = tuple(completion_weight * value for value in qq_weights)
    assert_remainder_census(attached)
    assert_normalized_generator_is_nonunit()

    print("A6 fixed-completion mixed-fibre rank-three verifier: PASS")
    print("  A5 Q/Q and Q/C2 incidence simplices: affine/difference rank 3")
    print("  fixed incidence and nonzero weight preserve all differences and zero sum")
    print("  exact weights: 1,1,1,-3; Q/C2 complementary doubletons: 2,-2")
    print("  zero remainders: size 0 or >=2; size 2 attained; size 1 impossible")
    print("  normalized 1+X+Y+Z has torus zero (1,1,-3), hence is not a unit")
    print("  no rational or integer affine/exponent dependency among the four points")
    print("  scope: conditional on a compatible fixed completion into one mixed fibre")
    print("  global Krenn--Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
