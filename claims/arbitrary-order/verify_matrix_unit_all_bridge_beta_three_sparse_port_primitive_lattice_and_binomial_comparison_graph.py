"""Exact QA for the A8 sparse-port lattice and comparison-graph mechanisms.

This standalone standard-library checker reconstructs physical ``Q/Q`` and
``Q/C^2`` perfect-matching controls, extracts the sparse-port identity minor,
and checks the resulting integer retraction and saturation mechanism.  It
also exhausts the 64 simple graphs on four labelled block terms to audit the
balanced-sign comparison-graph classification.

The exhaustive portions are bounded QA for four block terms.  They do not
prove that an A6 fixed completion exists, that a complete fibre has rank
three, that its lattice lies in a binomial core, or that an additional
binomial comparison is forced.  No theorem, audit, or repository module is
imported.  The global Krenn--Gu conjecture remains UNRESOLVED.
"""

from __future__ import annotations

from collections.abc import Iterable
from fractions import Fraction
from itertools import combinations, permutations, product
from typing import TypeAlias

Edge: TypeAlias = tuple[str, str]
Matching: TypeAlias = frozenset[Edge]
IntVector: TypeAlias = tuple[int, ...]
RatVector: TypeAlias = tuple[Fraction, ...]
Graph: TypeAlias = frozenset[tuple[int, int]]
Exponent3: TypeAlias = tuple[int, int, int]
LaurentPolynomial: TypeAlias = dict[Exponent3, Fraction]


def edge(left: str, right: str) -> Edge:
    """Return an undirected labelled edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


def subtract(left: IntVector, right: IntVector) -> IntVector:
    """Subtract equal-width integer vectors."""

    assert len(left) == len(right)
    return tuple(a - b for a, b in zip(left, right, strict=True))


def add_scaled(vectors: tuple[IntVector, ...], coefficients: IntVector) -> IntVector:
    """Return an exact integer linear combination of column vectors."""

    assert vectors and len(vectors) == len(coefficients)
    width = len(vectors[0])
    assert all(len(vector) == width for vector in vectors)
    return tuple(
        sum(
            coefficient * vector[column]
            for coefficient, vector in zip(coefficients, vectors, strict=True)
        )
        for column in range(width)
    )


def rational_rank(rows: tuple[IntVector, ...]) -> int:
    """Compute exact row rank over the rationals."""

    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def determinant_three(rows: tuple[IntVector, IntVector, IntVector]) -> int:
    """Return a three-by-three integer determinant."""

    assert all(len(row) == 3 for row in rows)
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def incidence_vectors(
    matchings: tuple[Matching, ...], coordinates: tuple[Edge, ...]
) -> tuple[IntVector, ...]:
    """Represent matching edge incidences in fixed coordinates."""

    return tuple(
        tuple(int(item in matching) for item in coordinates) for matching in matchings
    )


def assert_perfect_matchings(
    matchings: tuple[Matching, ...], vertices: frozenset[str]
) -> None:
    """Check that every edge set covers every vertex exactly once."""

    for matching in matchings:
        endpoints = tuple(vertex for item in matching for vertex in item)
        assert len(endpoints) == len(vertices)
        assert frozenset(endpoints) == vertices


def qq_matchings() -> tuple[Matching, ...]:
    """Build four physical Q/Q matchings on length-three odd routes."""

    answer: list[Matching] = []
    for selected in range(4):
        items: set[Edge] = set()
        for route in range(4):
            left = edge("v", f"p{route}")
            middle = edge(f"p{route}", f"q{route}")
            right = edge(f"q{route}", "w")
            items.update((left, right) if route == selected else (middle,))
        answer.append(frozenset(items))
    return tuple(answer)


def qc2_matchings() -> tuple[Matching, ...]:
    """Enumerate the four physical Q/C2 control matchings by sparse port."""

    rows = tuple(f"u{index}" for index in range(4))
    columns = tuple(f"w{index}" for index in range(4))
    support = frozenset(
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
    unordered = tuple(
        frozenset(
            edge(row, column) for row, column in zip(rows, assignment, strict=True)
        )
        for assignment in permutations(columns)
        if all(
            edge(row, column) in support
            for row, column in zip(rows, assignment, strict=True)
        )
    )
    assert len(unordered) == 4
    return tuple(
        next(matching for matching in unordered if edge("u0", f"w{port}") in matching)
        for port in range(4)
    )


def assert_sparse_port_retraction(
    matchings: tuple[Matching, ...], sparse_ports: tuple[Edge, ...]
) -> tuple[IntVector, ...]:
    """Certify the identity minor and an integral retraction onto differences."""

    assert len(matchings) == len(sparse_ports) == 4
    coordinates = tuple(sorted(set().union(*matchings)))
    vectors = incidence_vectors(matchings, coordinates)
    differences = tuple(subtract(vector, vectors[0]) for vector in vectors[1:])
    port_columns = tuple(coordinates.index(item) for item in sparse_ports[1:])
    identity_minor = tuple(
        tuple(difference[column] for column in port_columns)
        for difference in differences
    )
    assert identity_minor == ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    assert determinant_three(identity_minor) == 1
    assert rational_rank(differences) == 3

    def coefficient_projection(vector: IntVector) -> IntVector:
        return tuple(vector[column] for column in port_columns)

    def retract(vector: IntVector) -> IntVector:
        return add_scaled(differences, coefficient_projection(vector))

    for difference in differences:
        assert retract(difference) == difference
    samples = (
        (0,) * len(coordinates),
        *differences,
        add_scaled(differences, (2, -3, 5)),
        tuple((index % 5) - 2 for index in range(len(coordinates))),
    )
    for sample in samples:
        assert retract(retract(sample)) == retract(sample)

    # Saturation in the ambient integer edge lattice follows constructively:
    # if n*x=sum c_i*u_i, port projection gives n*x_port=c, hence every c_i
    # is divisible by n and x lies in the displayed integer span.
    for modulus in range(2, 7):
        for coefficients in product(range(-6, 7), repeat=3):
            multiple = add_scaled(differences, coefficients)
            if all(value % modulus == 0 for value in multiple):
                assert all(value % modulus == 0 for value in coefficients)
                divided = tuple(value // modulus for value in multiple)
                assert divided == add_scaled(
                    differences,
                    tuple(value // modulus for value in coefficients),
                )
    return differences


def assert_same_rank_superlattice_collapse(differences: tuple[IntVector, ...]) -> None:
    """Check same-rank containment collapses for a primitive sublattice."""

    assert rational_rank(differences) == 3
    width = len(differences[0])
    port_columns = tuple(
        next(
            column
            for column in range(width)
            if difference[column] == 1
            and all(
                other[column] == 0 for other in differences if other is not difference
            )
        )
        for difference in differences
    )
    assert len(set(port_columns)) == 3

    # Rational combinations which are integral in the ambient lattice must
    # have integral coefficients, because the selected port coordinates are
    # exactly those coefficients.
    for denominator in range(2, 7):
        for numerators in product(range(-6, 7), repeat=3):
            rational_vector: RatVector = tuple(
                sum(
                    Fraction(numerator, denominator) * difference[column]
                    for numerator, difference in zip(
                        numerators, differences, strict=True
                    )
                )
                for column in range(width)
            )
            if all(value.denominator == 1 for value in rational_vector):
                assert all(numerator % denominator == 0 for numerator in numerators)

    # A nonsaturated same-rank control shows why the identity minor matters.
    bad_lattice = ((2, 0, 0), (0, 1, 0), (0, 0, 1))
    superlattice = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    assert rational_rank(bad_lattice) == rational_rank(superlattice) == 3
    assert add_scaled(bad_lattice, (1, 0, 0)) == (2, 0, 0)
    assert superlattice[0] not in {
        add_scaled(bad_lattice, coefficients)
        for coefficients in product(range(-2, 3), repeat=3)
    }
    assert 2 * superlattice[0][0] == bad_lattice[0][0]


def balanced_signs() -> tuple[tuple[int, int, int, int], ...]:
    """Return the three normalized two-plus/two-minus sign restrictions."""

    answer = tuple(
        (1, *tail) for tail in product((-1, 1), repeat=3) if 1 + sum(tail) == 0
    )
    assert set(answer) == {
        (1, 1, -1, -1),
        (1, -1, 1, -1),
        (1, -1, -1, 1),
    }
    return answer


def assert_full_fibre_sign_parity() -> None:
    """Check contained complete-fibre survival forces an even complement."""

    block_signs = balanced_signs()
    for block in block_signs:
        assert sum(block) == 0
        for remainder_size in range(8):
            zero_remainders = tuple(
                signs
                for signs in product((-1, 1), repeat=remainder_size)
                if sum(signs) == 0
            )
            assert bool(zero_remainders) == (remainder_size % 2 == 0)
            for remainder in zero_remainders:
                assert sum((*block, *remainder)) == 0

    size_six_remainders = tuple(
        signs for signs in product((-1, 1), repeat=2) if sum(signs) == 0
    )
    assert size_six_remainders == ((-1, 1), (1, -1))

    # Any odd remainder gives a nonzero integer scalar.  Its exact reciprocal
    # is a unit certificate in the binomial-core quotient.
    for remainder_size in (1, 3, 5, 7):
        for remainder in product((-1, 1), repeat=remainder_size):
            scalar = Fraction(sum(remainder))
            assert scalar != 0
            assert scalar * (1 / scalar) == 1


def complete_bipartite_matching(order: int, port: int, rotate: int = 0) -> Matching:
    """Construct one physical K_(order,order) matching using u0--w_port."""

    assert order >= 2 and 0 <= port < order
    remaining_columns = [index for index in range(order) if index != port]
    if remaining_columns:
        shift = rotate % len(remaining_columns)
        remaining_columns = remaining_columns[shift:] + remaining_columns[:shift]
    assignment = (port, *remaining_columns)
    return frozenset(
        edge(f"u{row}", f"w{column}") for row, column in enumerate(assignment)
    )


def assert_physical_port_pair_landing() -> None:
    """Check block-pair and outside-port projections on physical matchings."""

    order = 6
    vertices = frozenset(
        {
            *(f"u{index}" for index in range(order)),
            *(f"w{index}" for index in range(order)),
        }
    )
    matchings = tuple(complete_bipartite_matching(order, port) for port in range(order))
    same_port_alternative = complete_bipartite_matching(order, 0, rotate=1)
    assert_perfect_matchings((*matchings, same_port_alternative), vertices)
    coordinates = tuple(edge("u0", f"w{port}") for port in range(4))
    projections = incidence_vectors(matchings, coordinates)
    assert projections == (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
    )
    assert incidence_vectors((same_port_alternative,), coordinates)[0] == projections[0]

    for left, right in combinations(range(order), 2):
        landing = subtract(projections[right], projections[left])
        if left < 4 and right < 4:
            expected = tuple(
                int(index == right) - int(index == left) for index in range(4)
            )
        elif left < 4:
            expected = tuple(-int(index == left) for index in range(4))
        else:
            expected = (0, 0, 0, 0)
        assert landing == expected

    # Two distinct physical matchings using the same core port also project
    # to zero difference; projection alone must not identify their full edge
    # difference with zero.
    full_coordinates = tuple(sorted(matchings[0] | same_port_alternative))
    full_vectors = incidence_vectors(
        (matchings[0], same_port_alternative), full_coordinates
    )
    assert subtract(projections[0], projections[0]) == (0, 0, 0, 0)
    assert subtract(full_vectors[1], full_vectors[0]) != (0,) * len(full_coordinates)


def cut_from_signs(signs: tuple[int, int, int, int]) -> frozenset[int]:
    """Return the positive side of one normalized balanced sign cut."""

    assert signs[0] == 1 and sum(signs) == 0
    return frozenset(index for index, sign in enumerate(signs) if sign == 1)


def edge_crosses_cut(item: tuple[int, int], positive: frozenset[int]) -> bool:
    """Return whether an edge joins opposite sides of a sign cut."""

    left, right = item
    return (left in positive) != (right in positive)


def degree_sequence(graph: Graph) -> tuple[int, int, int, int]:
    """Return the decreasing degree sequence of a four-vertex graph."""

    return tuple(
        sorted(
            (sum(vertex in item for item in graph) for vertex in range(4)),
            reverse=True,
        )
    )


def assert_comparison_graph_classification() -> None:
    """Exhaust all simple four-vertex comparison graphs and minimal closures."""

    edges = tuple(combinations(range(4), 2))
    cuts = tuple(cut_from_signs(signs) for signs in balanced_signs())
    assert set(cuts) == {
        frozenset((0, 1)),
        frozenset((0, 2)),
        frozenset((0, 3)),
    }
    graphs = tuple(
        frozenset(item for bit, item in enumerate(edges) if mask & (1 << bit))
        for mask in range(1 << len(edges))
    )

    survivors = {
        graph: tuple(
            cut for cut in cuts if all(edge_crosses_cut(item, cut) for item in graph)
        )
        for graph in graphs
    }
    closed = frozenset(graph for graph, live in survivors.items() if not live)
    assert all(graph not in closed for graph in graphs if len(graph) <= 2)

    minimal_closed = tuple(
        graph
        for graph in closed
        if all(frozenset(graph - {item}) not in closed for item in graph)
    )
    assert len(minimal_closed) == 8
    assert all(len(graph) == 3 for graph in minimal_closed)
    assert {degree_sequence(graph) for graph in minimal_closed} == {
        (2, 2, 2, 0),  # triangle: odd binomial dependency
        (3, 1, 1, 1),  # K_1,3: forced imbalanced block signs
    }
    assert sum(degree_sequence(graph) == (2, 2, 2, 0) for graph in minimal_closed) == 4
    assert sum(degree_sequence(graph) == (3, 1, 1, 1) for graph in minimal_closed) == 4

    path_four = frozenset(((0, 1), (1, 2), (2, 3)))
    assert degree_sequence(path_four) == (2, 2, 1, 1)
    assert survivors[path_four] == (frozenset((0, 2)),)


def assert_qc2_pair_criterion() -> None:
    """Check within-doubleton comparisons kill the aligned Q/C2 survivor."""

    signs = (1, 1, -1, -1)
    first_doubleton = frozenset((0, 1))
    second_doubleton = frozenset((2, 3))
    within = {tuple(sorted(item)) for item in (first_doubleton, second_doubleton)}
    all_edges = tuple(combinations(range(4), 2))
    killed: list[tuple[int, int]] = []
    compatible: list[tuple[int, int]] = []
    for left, right in all_edges:
        scalar = Fraction(1) + Fraction(signs[right], signs[left])
        if scalar:
            killed.append((left, right))
            assert scalar == 2
            assert (left, right) in within
            assert scalar * Fraction(1, 2) == 1
        else:
            compatible.append((left, right))
            assert (left, right) not in within
    assert set(killed) == {(0, 1), (2, 3)}
    assert set(compatible) == {(0, 2), (0, 3), (1, 2), (1, 3)}


def evaluate_laurent(
    polynomial: LaurentPolynomial, point: tuple[Fraction, Fraction, Fraction]
) -> Fraction:
    """Evaluate a sparse Laurent polynomial exactly at a nonzero torus point."""

    assert all(point)
    return sum(
        (
            coefficient
            * product_value(
                coordinate**power
                for coordinate, power in zip(point, exponent, strict=True)
            )
            for exponent, coefficient in polynomial.items()
        ),
        Fraction(0),
    )


def product_value(values: Iterable[Fraction]) -> Fraction:
    """Multiply an iterable of exact rational values."""

    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def monomial(exponent: Exponent3) -> LaurentPolynomial:
    """Return one coefficient-one Laurent monomial."""

    return {exponent: Fraction(1)}


def polynomial_sum(*polynomials: LaurentPolynomial) -> LaurentPolynomial:
    """Add sparse Laurent polynomials exactly."""

    answer: LaurentPolynomial = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            answer[exponent] = answer.get(exponent, Fraction(0)) + coefficient
            if answer[exponent] == 0:
                del answer[exponent]
    return answer


def assert_sharp_laurent_controls() -> None:
    """Check one proper aligned control and two exact unit mechanisms."""

    one = monomial((0, 0, 0))
    x = monomial((1, 0, 0))
    y = monomial((0, 1, 0))
    z = monomial((0, 0, 1))
    xy = monomial((1, 1, 0))
    block = polynomial_sum(one, x, y, z)

    aligned_point = (Fraction(1), Fraction(-1), Fraction(-1))
    aligned_core = (
        polynomial_sum(one, y),
        polynomial_sum(one, z),
        polynomial_sum(one, xy),
    )
    assert all(evaluate_laurent(item, aligned_point) == 0 for item in aligned_core)
    assert evaluate_laurent(block, aligned_point) == 0
    q_x = polynomial_sum(one, x)
    q_y = polynomial_sum(y, z)
    assert evaluate_laurent(q_x, aligned_point) == 2
    assert evaluate_laurent(q_y, aligned_point) == -2

    # The common nonzero torus zero proves the aligned core plus block remains
    # proper even after localizing by q_x*q_y.
    assert (
        evaluate_laurent(q_x, aligned_point) * evaluate_laurent(q_y, aligned_point) != 0
    )

    # Imbalanced unit control with r_i=u_i.  The exact identity
    # p_B-(1+X)-(1+Y)-(1+Z)=-2 gives an explicit ideal certificate for 1.
    imbalanced_core = (
        polynomial_sum(one, x),
        polynomial_sum(one, y),
        polynomial_sum(one, z),
    )
    difference = polynomial_sum(
        block,
        *(
            {exponent: -coefficient for exponent, coefficient in item.items()}
            for item in imbalanced_core
        ),
    )
    assert difference == {(0, 0, 0): Fraction(-2)}
    assert Fraction(-1, 2) * next(iter(difference.values())) == 1

    # Adding the within-doubleton comparison 1+X to the aligned quotient has
    # scalar 2, while a cross-doubleton comparison 1+Y has scalar zero.
    assert evaluate_laurent(polynomial_sum(one, x), aligned_point) == 2
    assert evaluate_laurent(polynomial_sum(one, y), aligned_point) == 0


def main() -> None:
    """Run all exact A8 finite mechanism checks."""

    qq = qq_matchings()
    qq_vertices = frozenset(
        {
            "v",
            "w",
            *(f"p{index}" for index in range(4)),
            *(f"q{index}" for index in range(4)),
        }
    )
    assert_perfect_matchings(qq, qq_vertices)
    qq_differences = assert_sparse_port_retraction(
        qq, tuple(edge("v", f"p{index}") for index in range(4))
    )
    assert_same_rank_superlattice_collapse(qq_differences)

    qc2 = qc2_matchings()
    qc2_vertices = frozenset(
        {*(f"u{index}" for index in range(4)), *(f"w{index}" for index in range(4))}
    )
    assert_perfect_matchings(qc2, qc2_vertices)
    qc2_differences = assert_sparse_port_retraction(
        qc2, tuple(edge("u0", f"w{index}") for index in range(4))
    )
    assert_same_rank_superlattice_collapse(qc2_differences)

    assert_full_fibre_sign_parity()
    assert_physical_port_pair_landing()
    assert_comparison_graph_classification()
    assert_qc2_pair_criterion()
    assert_sharp_laurent_controls()

    print("A8 sparse-port primitive-lattice/comparison-graph verifier: PASS")
    print("  Q/Q and Q/C2 sparse-port identity minors give integral retractions")
    print(
        "  primitive rank-three lattice: every same-rank integer superlattice collapses"
    )
    print(
        "  contained full fibre: surviving complement is even; size 6 has opposite signs"
    )
    print(
        "  physical port landing: pair, same-port, one-outside, and both-outside checked"
    )
    print(
        "  all 64 comparison graphs: minimal closures are 4 triangles and 4 K1,3 stars"
    )
    print("  no graph with <=2 edges closes all cuts; P4 leaves one balanced survivor")
    print("  aligned Q/C2: exactly the two within-doubleton comparisons are units")
    print("  sharp Laurent controls: aligned proper, imbalanced unit, within-port unit")
    print(
        "  scope: bounded four-term QA; no completion, rank, containment, or edge is forced"
    )
    print("  global Krenn--Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
