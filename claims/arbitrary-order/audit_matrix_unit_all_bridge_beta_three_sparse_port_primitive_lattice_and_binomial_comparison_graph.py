"""Independent exact audit of the A8 sparse-port/comparison mechanisms.

This standalone standard-library audit uses edge bitmasks, recursive perfect-
matching enumeration, maximal-minor gcds, and six-bit comparison graphs.  It
does not import the primary verifier, a theorem document, or repository code.

The exhaustive checks concern four distinguished block terms and bounded
controls.  They do not prove existence of a fixed completion, rank three for a
complete fibre, containment in a binomial lattice, or the occurrence of any
extra comparison direction.  The global Krenn--Gu conjecture is UNRESOLVED.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import gcd
from typing import TypeAlias

Edge: TypeAlias = tuple[int, int]
Vector: TypeAlias = tuple[int, ...]
Exponent: TypeAlias = tuple[int, int, int]
Polynomial: TypeAlias = dict[Exponent, Fraction]


def canonical_edge(left: int, right: int) -> Edge:
    """Canonicalize an undirected edge."""

    assert left != right
    return (left, right) if left < right else (right, left)


def enumerate_matchings(
    vertex_count: int, support: tuple[Edge, ...]
) -> tuple[int, ...]:
    """Enumerate perfect matchings as bitmasks by first-unmatched recursion."""

    assert vertex_count % 2 == 0
    indexed = tuple(canonical_edge(*item) for item in support)
    assert len(set(indexed)) == len(indexed)
    incident = tuple(
        tuple(index for index, item in enumerate(indexed) if vertex in item)
        for vertex in range(vertex_count)
    )

    def visit(used_vertices: int, edge_mask: int) -> tuple[int, ...]:
        if used_vertices == (1 << vertex_count) - 1:
            return (edge_mask,)
        vertex = next(
            item for item in range(vertex_count) if not used_vertices & (1 << item)
        )
        answers: list[int] = []
        for edge_index in incident[vertex]:
            left, right = indexed[edge_index]
            other = right if left == vertex else left
            if used_vertices & (1 << other):
                continue
            answers.extend(
                visit(
                    used_vertices | (1 << vertex) | (1 << other),
                    edge_mask | (1 << edge_index),
                )
            )
        return tuple(answers)

    answer = visit(0, 0)
    assert len(set(answer)) == len(answer)
    return tuple(sorted(answer))


def incidence(mask: int, width: int) -> Vector:
    """Decode a bitmask to its zero-one incidence vector."""

    return tuple(int(bool(mask & (1 << index))) for index in range(width))


def difference(left: Vector, right: Vector) -> Vector:
    """Subtract equal-width integer vectors."""

    assert len(left) == len(right)
    return tuple(a - b for a, b in zip(left, right, strict=True))


def determinant(rows: tuple[Vector, Vector, Vector]) -> int:
    """Compute an exact three-by-three determinant."""

    assert all(len(row) == 3 for row in rows)
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def linear_combination(rows: tuple[Vector, ...], coefficients: Vector) -> Vector:
    """Form an exact integral row combination."""

    assert rows and len(rows) == len(coefficients)
    return tuple(
        sum(
            coefficient * row[column]
            for coefficient, row in zip(coefficients, rows, strict=True)
        )
        for column in range(len(rows[0]))
    )


def audit_sparse_retraction(
    support: tuple[Edge, ...], matchings: tuple[int, ...], ports: tuple[Edge, ...]
) -> None:
    """Audit the primitive rank-three direct summand from a port identity minor."""

    assert len(matchings) == len(ports) == 4
    port_indices = tuple(support.index(canonical_edge(*item)) for item in ports)
    ordered = tuple(
        next(mask for mask in matchings if mask & (1 << port_index))
        for port_index in port_indices
    )
    rows = tuple(incidence(mask, len(support)) for mask in ordered)
    generators = tuple(difference(row, rows[0]) for row in rows[1:])
    selected = port_indices[1:]
    minor = tuple(tuple(row[column] for column in selected) for row in generators)
    assert minor == ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    maximal_minors = tuple(
        determinant(
            tuple(tuple(row[column] for column in columns) for row in generators)
        )
        for columns in combinations(range(len(support)), 3)
    )
    nonzero_minors = tuple(abs(value) for value in maximal_minors if value)
    assert nonzero_minors
    determinantal_divisor = 0
    for value in nonzero_minors:
        determinantal_divisor = gcd(determinantal_divisor, value)
    assert determinantal_divisor == 1

    def project(vector: Vector) -> Vector:
        return tuple(vector[column] for column in selected)

    def retract(vector: Vector) -> Vector:
        return linear_combination(generators, project(vector))

    ambient_basis = tuple(
        tuple(int(row == column) for column in range(len(support)))
        for row in range(len(support))
    )
    assert all(retract(retract(item)) == retract(item) for item in ambient_basis)
    assert all(retract(item) == item for item in generators)

    # In the rational span, the selected ambient coordinates equal the three
    # coefficients.  Thus an ambient-integral vector has integral coefficients,
    # so saturation holds and any containing same-rank lattice collapses.
    for denominator in range(1, 8):
        for numerators in product(range(-5, 6), repeat=3):
            rational_vector = tuple(
                sum(
                    Fraction(numerator, denominator) * row[column]
                    for numerator, row in zip(numerators, generators, strict=True)
                )
                for column in range(len(support))
            )
            integral = all(item.denominator == 1 for item in rational_vector)
            assert integral == all(item % denominator == 0 for item in numerators)

    # A determinant-two lattice is a sharp nonprimitive same-rank control:
    # 2e_1 lies in it while e_1 lies in its index-two saturation.
    nonsaturated = ((2, 0, 0), (0, 1, 0), (0, 0, 1))
    assert abs(determinant(nonsaturated)) == 2
    assert linear_combination(nonsaturated, (1, 0, 0)) == (2, 0, 0)
    assert all(
        linear_combination(nonsaturated, coefficients) != (1, 0, 0)
        for coefficients in product(range(-3, 4), repeat=3)
    )


def qq_control() -> tuple[tuple[Edge, ...], tuple[int, ...], tuple[Edge, ...]]:
    """Build and independently enumerate the four odd-route Q/Q matchings."""

    support: list[Edge] = []
    for route in range(4):
        p_vertex = 2 + 2 * route
        q_vertex = p_vertex + 1
        support.extend(
            (
                canonical_edge(0, p_vertex),
                canonical_edge(p_vertex, q_vertex),
                canonical_edge(q_vertex, 1),
            )
        )
    edges = tuple(support)
    ports = tuple(canonical_edge(0, 2 + 2 * route) for route in range(4))
    matchings = enumerate_matchings(10, edges)
    assert len(matchings) == 4
    return edges, matchings, ports


def qc2_control() -> tuple[tuple[Edge, ...], tuple[int, ...], tuple[Edge, ...]]:
    """Build and independently enumerate the four Q/C2 support matchings."""

    allowed_columns = ({0, 1, 2, 3}, {1, 3}, {0, 2}, {0, 1})
    support = tuple(
        canonical_edge(row, 4 + column)
        for row, columns in enumerate(allowed_columns)
        for column in sorted(columns)
    )
    ports = tuple(canonical_edge(0, 4 + column) for column in range(4))
    matchings = enumerate_matchings(8, support)
    assert len(matchings) == 4
    return support, matchings, ports


def audit_fibre_parity() -> None:
    """Audit balanced blocks, even complements, and the size-six signs."""

    balanced = tuple(
        (1, *tail) for tail in product((-1, 1), repeat=3) if 1 + sum(tail) == 0
    )
    assert len(balanced) == 3
    for block in balanced:
        assert sum(block) == 0
        for remainder_size in range(9):
            zero_masks = tuple(
                mask
                for mask in range(1 << remainder_size)
                if sum(1 if mask & (1 << bit) else -1 for bit in range(remainder_size))
                == 0
            )
            assert bool(zero_masks) == (remainder_size % 2 == 0)
            assert all(
                sum(block)
                + sum(1 if mask & (1 << bit) else -1 for bit in range(remainder_size))
                == 0
                for mask in zero_masks
            )
    size_six_complements = tuple(
        tuple(1 if mask & (1 << bit) else -1 for bit in range(2))
        for mask in range(4)
        if sum(1 if mask & (1 << bit) else -1 for bit in range(2)) == 0
    )
    assert size_six_complements == ((1, -1), (-1, 1))

    for odd_size in (1, 3, 5, 7):
        for mask in range(1 << odd_size):
            scalar = Fraction(
                sum(1 if mask & (1 << bit) else -1 for bit in range(odd_size))
            )
            assert scalar and scalar * (1 / scalar) == 1


def permutation_matching(permutation: tuple[int, ...]) -> frozenset[Edge]:
    """Encode a complete-bipartite matching from its row-to-column permutation."""

    return frozenset(
        canonical_edge(row, 6 + column) for row, column in enumerate(permutation)
    )


def audit_outside_port_landing() -> None:
    """Audit pair directions when zero, one, or two ports lie outside the block."""

    matchings: list[frozenset[Edge]] = []
    for port in range(6):
        tail = tuple(column for column in range(6) if column != port)
        matchings.append(permutation_matching((port, *tail)))
    ports = tuple(canonical_edge(0, 6 + column) for column in range(4))
    projections = tuple(
        tuple(int(item in matching) for item in ports) for matching in matchings
    )
    assert projections == (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
    )
    for left, right in combinations(range(6), 2):
        landing = difference(projections[right], projections[left])
        if right < 4:
            expected = tuple(int(bit == right) - int(bit == left) for bit in range(4))
        elif left < 4:
            expected = tuple(-int(bit == left) for bit in range(4))
        else:
            expected = (0, 0, 0, 0)
        assert landing == expected

    same_port = permutation_matching((0, 2, 1, 3, 4, 5))
    assert same_port != matchings[0]
    assert tuple(int(item in same_port) for item in ports) == projections[0]


def comparison_edges() -> tuple[tuple[int, int], ...]:
    """Return the six labelled comparison edges."""

    return tuple(combinations(range(4), 2))


def degree_pattern(mask: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    """Return a decreasing four-vertex degree pattern."""

    return tuple(
        sorted(
            (
                sum(
                    bool(mask & (1 << bit)) and vertex in item
                    for bit, item in enumerate(edges)
                )
                for vertex in range(4)
            ),
            reverse=True,
        )
    )


def audit_graph_census_and_qc2() -> None:
    """Exhaust 64 graphs, the three balanced cuts, and the Q/C2 criterion."""

    edges = comparison_edges()
    cuts = (0b0011, 0b0101, 0b1001)

    def crosses(item: tuple[int, int], cut: int) -> bool:
        left, right = item
        return bool(cut & (1 << left)) != bool(cut & (1 << right))

    survivors = {
        graph: tuple(
            cut
            for cut in cuts
            if all(
                not graph & (1 << bit) or crosses(item, cut)
                for bit, item in enumerate(edges)
            )
        )
        for graph in range(64)
    }
    closed = frozenset(graph for graph, live in survivors.items() if not live)
    assert all(graph not in closed for graph in range(64) if graph.bit_count() <= 2)
    minimal = tuple(
        graph
        for graph in closed
        if all(
            graph ^ (1 << bit) not in closed for bit in range(6) if graph & (1 << bit)
        )
    )
    assert len(minimal) == 8
    assert all(graph.bit_count() == 3 for graph in minimal)
    patterns = tuple(degree_pattern(graph, edges) for graph in minimal)
    assert patterns.count((2, 2, 2, 0)) == 4
    assert patterns.count((3, 1, 1, 1)) == 4

    path_edges = {(0, 1), (1, 2), (2, 3)}
    path_mask = sum(1 << edges.index(item) for item in path_edges)
    assert survivors[path_mask] == (0b0101,)

    aligned = (1, 1, -1, -1)
    units: set[tuple[int, int]] = set()
    compatible: set[tuple[int, int]] = set()
    for left, right in edges:
        scalar = Fraction(1) + Fraction(aligned[right], aligned[left])
        if scalar:
            assert scalar == 2 and Fraction(1, 2) * scalar == 1
            units.add((left, right))
        else:
            compatible.add((left, right))
    assert units == {(0, 1), (2, 3)}
    assert compatible == {(0, 2), (0, 3), (1, 2), (1, 3)}


def add_polynomials(*items: Polynomial) -> Polynomial:
    """Add exact sparse Laurent polynomials."""

    answer: Polynomial = {}
    for item in items:
        for exponent, coefficient in item.items():
            answer[exponent] = answer.get(exponent, Fraction(0)) + coefficient
            if not answer[exponent]:
                del answer[exponent]
    return answer


def evaluate(polynomial: Polynomial, point: tuple[Fraction, ...]) -> Fraction:
    """Evaluate a sparse Laurent polynomial at an exact torus point."""

    assert len(point) == 3 and all(point)
    answer = Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for coordinate, power in zip(point, exponent, strict=True):
            term *= coordinate**power
        answer += term
    return answer


def audit_exact_laurent_controls() -> None:
    """Audit a localized proper control and exact scalar-unit controls."""

    one = {(0, 0, 0): Fraction(1)}
    x = {(1, 0, 0): Fraction(1)}
    y = {(0, 1, 0): Fraction(1)}
    z = {(0, 0, 1): Fraction(1)}
    xy = {(1, 1, 0): Fraction(1)}
    block = add_polynomials(one, x, y, z)
    aligned_generators = (
        add_polynomials(one, y),
        add_polynomials(one, z),
        add_polynomials(one, xy),
    )
    witness = (Fraction(1), Fraction(-1), Fraction(-1))
    assert evaluate(block, witness) == 0
    assert all(evaluate(item, witness) == 0 for item in aligned_generators)
    port_sums = (add_polynomials(one, x), add_polynomials(y, z))
    assert tuple(evaluate(item, witness) for item in port_sums) == (2, -2)
    assert evaluate(port_sums[0], witness) * evaluate(port_sums[1], witness) != 0

    imbalanced_generators = (
        add_polynomials(one, x),
        add_polynomials(one, y),
        add_polynomials(one, z),
    )
    negatives = tuple(
        {exponent: -coefficient for exponent, coefficient in item.items()}
        for item in imbalanced_generators
    )
    unit_certificate = add_polynomials(block, *negatives)
    assert unit_certificate == {(0, 0, 0): Fraction(-2)}
    assert Fraction(-1, 2) * unit_certificate[(0, 0, 0)] == 1
    assert evaluate(add_polynomials(one, x), witness) == 2
    assert evaluate(add_polynomials(one, y), witness) == 0


def main() -> None:
    """Run the independent exact A8 audit."""

    for support, matchings, ports in (qq_control(), qc2_control()):
        audit_sparse_retraction(support, matchings, ports)
    audit_fibre_parity()
    audit_outside_port_landing()
    audit_graph_census_and_qc2()
    audit_exact_laurent_controls()

    print("A8 independent sparse-port/comparison-graph audit: PASS")
    print("  recursive physical PM census: Q/Q=4 and Q/C2=4")
    print("  maximal-minor gcd=1: port lattice is a primitive direct summand")
    print("  same-rank containment collapses; index-two nonsaturated control survives")
    print("  complete-fibre parity and the two opposite-sign size-six complements pass")
    print("  physical port differences include one-/two-outside and same-port controls")
    print("  64 graphs: minimal closures are 4 triangles and 4 K1,3 stars")
    print("  no <=2-edge closure; P4 has one balanced survivor")
    print("  aligned Q/C2 kills exactly its two within-doubleton comparisons")
    print("  exact Laurent controls: localized proper, imbalanced unit, aligned unit")
    print(
        "  scope: bounded QA; completion/rank/containment/comparisons are assumptions"
    )
    print("  global Krenn--Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
