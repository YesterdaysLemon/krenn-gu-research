"""Independent bounded audit of the A6 fixed-completion mechanism.

This standard-library program imports no repository code and does not inspect
the primary verifier.  It enumerates perfect matchings of physical Q/Q and
Q/C^2 subdivisions as edge masks, derives their port partitions and exact
rank-three incidence lattices, and then adjoins a disjoint fixed matching.

The fixed completion is only one finite mixed-fibre control.  The written
theorem, not this audit, carries the arbitrary-completion quantifier.  The
small remainder census is likewise a sharp scalar mechanism check: it does
not construct a complete target incidence or prove a global exclusion.  The
global Krenn--Gu conjecture remains UNRESOLVED.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from itertools import product

Edge = tuple[int, int]
Vector = tuple[int, ...]


def edge(left: int, right: int) -> Edge:
    """Return an undirected edge in canonical order."""

    assert left != right
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True)
class Route:
    """One oriented branch-to-branch route in a physical subdivision."""

    name: str
    path: tuple[int, ...]
    edges: tuple[Edge, ...]

    @property
    def length(self) -> int:
        return len(self.edges)


@dataclass(frozen=True)
class Kernel:
    """A beta-three route kernel and its distinguished branch routes."""

    name: str
    order: int
    edges: tuple[Edge, ...]
    routes: tuple[Route, ...]
    sparse_vertex: int
    sparse_routes: tuple[str, ...]


@dataclass(frozen=True)
class KernelEvidence:
    """Exact matching, weight, and incidence data for one kernel."""

    kernel: Kernel
    matchings: tuple[int, ...]
    weights: tuple[Fraction, ...]
    sparse_port_edges: tuple[Edge, ...]
    difference_rows: tuple[Vector, ...]
    lattice_minor: int
    even_port_sums: tuple[Fraction, ...]


def build_kernel(
    name: str,
    branch_count: int,
    specifications: tuple[tuple[str, int, int, int], ...],
    sparse_routes: tuple[str, ...],
) -> Kernel:
    """Build a simple physical graph from labelled route subdivisions."""

    next_vertex = branch_count
    routes: list[Route] = []
    graph_edges: list[Edge] = []
    for route_name, start, finish, length in specifications:
        assert 0 <= start < branch_count
        assert 0 <= finish < branch_count
        assert start != finish and length >= 1
        internal = tuple(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        path = (start, *internal, finish)
        route_edges = tuple(
            edge(path[index], path[index + 1]) for index in range(length)
        )
        routes.append(Route(route_name, path, route_edges))
        graph_edges.extend(route_edges)

    assert len(set(graph_edges)) == len(graph_edges)
    return Kernel(
        name=name,
        order=next_vertex,
        edges=tuple(graph_edges),
        routes=tuple(routes),
        sparse_vertex=0,
        sparse_routes=sparse_routes,
    )


def qq_kernel() -> Kernel:
    """Four internally disjoint length-three odd routes."""

    return build_kernel(
        "Q/Q",
        2,
        tuple((f"r{index}", 0, 1, 3) for index in range(4)),
        tuple(f"r{index}" for index in range(4)),
    )


def qc2_kernel() -> Kernel:
    """Four odd sparse routes and one even cubic-to-cubic route."""

    return build_kernel(
        "Q/C^2",
        3,
        (
            ("vx0", 0, 1, 1),
            ("vx1", 0, 1, 3),
            ("vy0", 0, 2, 1),
            ("vy1", 0, 2, 3),
            ("xy", 1, 2, 2),
        ),
        ("vx0", "vx1", "vy0", "vy1"),
    )


def edge_indices(kernel: Kernel) -> dict[Edge, int]:
    """Index every physical edge once."""

    answer = {item: index for index, item in enumerate(kernel.edges)}
    assert len(answer) == len(kernel.edges)
    return answer


def perfect_matchings(kernel: Kernel) -> tuple[int, ...]:
    """Enumerate full perfect matchings recursively as edge masks."""

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(kernel.order)]
    for index, (left, right) in enumerate(kernel.edges):
        adjacency[left].append((right, index))
        adjacency[right].append((left, index))

    @cache
    def recurse(vertices: int) -> tuple[int, ...]:
        if not vertices:
            return (0,)
        if vertices.bit_count() % 2:
            return ()
        first_bit = vertices & -vertices
        first = first_bit.bit_length() - 1
        remainder = vertices ^ first_bit
        output: list[int] = []
        for neighbour, index in adjacency[first]:
            neighbour_bit = 1 << neighbour
            if not remainder & neighbour_bit:
                continue
            for tail in recurse(remainder ^ neighbour_bit):
                output.append(tail | (1 << index))
        return tuple(sorted(output))

    return recurse((1 << kernel.order) - 1)


def assert_connected(kernel: Kernel) -> None:
    """Check the physical kernel is connected."""

    adjacency = [set() for _ in range(kernel.order)]
    for left, right in kernel.edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached = {0}
    boundary = [0]
    while boundary:
        vertex = boundary.pop()
        for neighbour in adjacency[vertex] - reached:
            reached.add(neighbour)
            boundary.append(neighbour)
    assert reached == set(range(kernel.order))


def incidence(mask: int, width: int) -> Vector:
    """Return the zero-one edge-incidence vector of a matching mask."""

    return tuple((mask >> index) & 1 for index in range(width))


def rational_rank(rows: tuple[Vector, ...]) -> int:
    """Compute exact row rank by Fraction elimination."""

    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    width = len(matrix[0])
    assert all(len(row) == width for row in matrix)
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
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_entry
                for value, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def determinant_three(matrix: tuple[tuple[int, int, int], ...]) -> int:
    """Return the exact determinant of a three-by-three integer matrix."""

    assert len(matrix) == 3
    assert all(len(row) == 3 for row in matrix)
    (a, b, c), (d, e, f), (g, h, i) = matrix
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def matching_weight(mask: int, weights: tuple[Fraction, ...]) -> Fraction:
    """Multiply the weights on one edge-mask matching."""

    answer = Fraction(1)
    for index, value in enumerate(weights):
        if mask & (1 << index):
            answer *= value
    return answer


def port_set(matchings: tuple[int, ...], edge_index: int) -> frozenset[int]:
    """Return matching indices using one endpoint-port edge."""

    edge_bit = 1 << edge_index
    return frozenset(
        index for index, matching in enumerate(matchings) if matching & edge_bit
    )


def weighted_port_sum(
    matchings: tuple[int, ...],
    weights: tuple[Fraction, ...],
    edge_index: int,
) -> Fraction:
    """Sum full matching monomials through one endpoint port."""

    edge_bit = 1 << edge_index
    return sum(
        (
            matching_weight(matching, weights)
            for matching in matchings
            if matching & edge_bit
        ),
        Fraction(0),
    )


def ordered_by_sparse_port(
    kernel: Kernel, matchings: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[Edge, ...]]:
    """Order the four matchings by their unique sparse-site route port."""

    index = edge_indices(kernel)
    route_map = {route.name: route for route in kernel.routes}
    ports = tuple(route_map[name].edges[0] for name in kernel.sparse_routes)
    ordered: list[int] = []
    for item in ports:
        users = port_set(matchings, index[item])
        assert len(users) == 1
        ordered.append(matchings[next(iter(users))])
    assert len(set(ordered)) == 4
    return tuple(ordered), ports


def analyse_kernel(kernel: Kernel) -> KernelEvidence:
    """Derive route ports, exact weights, and the rank-three lattice."""

    assert_connected(kernel)
    assert len(kernel.edges) - kernel.order + 1 == 3
    unordered = perfect_matchings(kernel)
    assert len(unordered) == 4
    allowed_edge_union = 0
    for matching in unordered:
        allowed_edge_union |= matching
    assert allowed_edge_union == (1 << len(kernel.edges)) - 1
    matchings, sparse_ports = ordered_by_sparse_port(kernel, unordered)
    index = edge_indices(kernel)

    even_routes: list[Route] = []
    for route in kernel.routes:
        first = port_set(matchings, index[route.edges[0]])
        last = port_set(matchings, index[route.edges[-1]])
        if route.length % 2:
            assert first == last
            assert len(first) == 1
        else:
            even_routes.append(route)
            assert len(first) == len(last) == 2
            assert first.isdisjoint(last)
            assert first | last == frozenset(range(4))
    assert len(even_routes) == (kernel.name == "Q/C^2")

    vectors = tuple(incidence(mask, len(kernel.edges)) for mask in matchings)
    differences = tuple(
        tuple(value - base for value, base in zip(vector, vectors[0], strict=True))
        for vector in vectors[1:]
    )
    assert rational_rank(differences) == 3
    assert (
        rational_rank(
            tuple(
                tuple(
                    value - base for value, base in zip(vector, vectors[0], strict=True)
                )
                for vector in vectors
            )
        )
        == 3
    )

    port_columns = tuple(index[item] for item in sparse_ports[1:])
    lattice_matrix = tuple(
        tuple(row[column] for column in port_columns) for row in differences
    )
    lattice_minor = determinant_three(lattice_matrix)
    assert lattice_minor == 1

    weights = [Fraction(1)] * len(kernel.edges)
    weights[index[sparse_ports[3]]] = Fraction(-3)
    exact_weights = tuple(weights)
    matching_weights = tuple(matching_weight(mask, exact_weights) for mask in matchings)
    assert matching_weights == (
        Fraction(1),
        Fraction(1),
        Fraction(1),
        Fraction(-3),
    )
    assert sum(matching_weights, Fraction(0)) == 0

    for route in kernel.routes:
        if route.length % 2:
            first_sum = weighted_port_sum(
                matchings, exact_weights, index[route.edges[0]]
            )
            last_sum = weighted_port_sum(
                matchings, exact_weights, index[route.edges[-1]]
            )
            assert first_sum == last_sum
            assert first_sum

    even_port_sums: tuple[Fraction, ...] = ()
    if even_routes:
        even = even_routes[0]
        even_port_sums = tuple(
            weighted_port_sum(matchings, exact_weights, index[item])
            for item in (even.edges[0], even.edges[-1])
        )
        assert set(even_port_sums) == {Fraction(-2), Fraction(2)}
        assert even_port_sums[0] == -even_port_sums[1]

    return KernelEvidence(
        kernel=kernel,
        matchings=matchings,
        weights=exact_weights,
        sparse_port_edges=sparse_ports,
        difference_rows=differences,
        lattice_minor=lattice_minor,
        even_port_sums=even_port_sums,
    )


def matching_word(
    order: int,
    edges: tuple[Edge, ...],
    colours: tuple[int, ...],
    matching: int,
) -> tuple[int, ...]:
    """Return the endpoint-colour word induced by one coloured matching."""

    word: list[int | None] = [None] * order
    for index, ((left, right), colour) in enumerate(zip(edges, colours, strict=True)):
        if not matching & (1 << index):
            continue
        assert word[left] is None and word[right] is None
        word[left] = colour
        word[right] = colour
    assert all(colour is not None for colour in word)
    return tuple(int(colour) for colour in word)


def audit_fixed_completion(evidence: KernelEvidence) -> dict[str, object]:
    """Adjoin two disjoint fixed edges and recheck every invariant."""

    kernel = evidence.kernel
    first_fixed = edge(kernel.order, kernel.order + 1)
    second_fixed = edge(kernel.order + 2, kernel.order + 3)
    completed_edges = (*kernel.edges, first_fixed, second_fixed)
    fixed_mask = (1 << len(kernel.edges)) | (1 << (len(kernel.edges) + 1))
    completed_matchings = tuple(mask | fixed_mask for mask in evidence.matchings)
    completed_weights = (*evidence.weights, Fraction(2), Fraction(-5))
    completion_weight = Fraction(-10)

    original_values = tuple(
        matching_weight(mask, evidence.weights) for mask in evidence.matchings
    )
    completed_values = tuple(
        matching_weight(mask, completed_weights) for mask in completed_matchings
    )
    assert completed_values == tuple(
        completion_weight * value for value in original_values
    )
    assert sum(completed_values, Fraction(0)) == 0
    assert tuple(value / completed_values[0] for value in completed_values[1:]) == (
        Fraction(1),
        Fraction(1),
        Fraction(-3),
    )

    vectors = tuple(
        incidence(mask, len(completed_edges)) for mask in completed_matchings
    )
    differences = tuple(
        tuple(value - base for value, base in zip(vector, vectors[0], strict=True))
        for vector in vectors[1:]
    )
    assert rational_rank(differences) == 3
    assert all(row[-2:] == (0, 0) for row in differences)
    assert tuple(row[:-2] for row in differences) == evidence.difference_rows

    core_index = edge_indices(kernel)
    port_columns = tuple(core_index[item] for item in evidence.sparse_port_edges[1:])
    lattice_matrix = tuple(
        tuple(row[column] for column in port_columns) for row in differences
    )
    assert determinant_three(lattice_matrix) == evidence.lattice_minor == 1

    colours = (0,) * len(kernel.edges) + (1, 2)
    words = {
        matching_word(kernel.order + 4, completed_edges, colours, mask)
        for mask in completed_matchings
    }
    assert len(words) == 1
    word = next(iter(words))
    assert set(word) == {0, 1, 2}

    completed_even_sums: tuple[Fraction, ...] = ()
    even_routes = tuple(route for route in kernel.routes if route.length % 2 == 0)
    if even_routes:
        even = even_routes[0]
        completed_even_sums = tuple(
            weighted_port_sum(completed_matchings, completed_weights, core_index[item])
            for item in (even.edges[0], even.edges[-1])
        )
        assert set(completed_even_sums) == {Fraction(-20), Fraction(20)}
        assert completed_even_sums == tuple(
            completion_weight * value for value in evidence.even_port_sums
        )

    return {
        "fixed_edges": (first_fixed, second_fixed),
        "fixed_weight": completion_weight,
        "affine_rank": rational_rank(differences),
        "lattice_minor": determinant_three(lattice_matrix),
        "matching_weights": completed_values,
        "even_port_sums": completed_even_sums,
        "mixed_word": word,
    }


LaurentPolynomial = dict[tuple[int, int, int], Fraction]


def evaluate_laurent(
    polynomial: LaurentPolynomial,
    point: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    """Evaluate a three-variable Laurent polynomial at a torus point."""

    assert all(value for value in point)
    return sum(
        (
            coefficient
            * product_value(
                base**power for base, power in zip(point, exponent, strict=True)
            )
            for exponent, coefficient in polynomial.items()
        ),
        Fraction(0),
    )


def product_value(values) -> Fraction:
    """Multiply an iterable of rational values."""

    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def audit_rank_three_polynomial(
    evidence: tuple[KernelEvidence, ...],
) -> dict[str, object]:
    """Certify a proper four-term block with no exponent dependency."""

    for item in evidence:
        assert rational_rank(item.difference_rows) == 3
        assert item.lattice_minor == 1

    polynomial: LaurentPolynomial = {
        (0, 0, 0): Fraction(1),
        (1, 0, 0): Fraction(1),
        (0, 1, 0): Fraction(1),
        (0, 0, 1): Fraction(1),
    }
    torus_point = (Fraction(1), Fraction(1), Fraction(-3))
    assert evaluate_laurent(polynomial, torus_point) == 0
    assert evaluate_laurent({(0, 0, 0): Fraction(1)}, torus_point) == 1
    assert all(
        evaluate_laurent({exponent: coefficient}, torus_point)
        for exponent, coefficient in polynomial.items()
    )

    # Evaluation at a nonzero torus point is a unital ring homomorphism.
    # Since 1+X+Y+Z maps to zero while every Laurent monomial maps nonzero,
    # the polynomial is not a unit and its principal ideal is proper.
    assert len(polynomial) == 4

    return {
        "polynomial": "1 + X + Y + Z",
        "proper_nonunit_point": torus_point,
        "difference_rank": 3,
        "unimodular_minor": 1,
    }


def audit_remainder_census(block_width: int) -> dict[str, object]:
    """Enumerate small cancellations among evaluated remainder monomials."""

    evaluated_values = tuple(Fraction(value) for value in (-2, -1, 1, 2))
    counts: dict[int, int] = {}
    witnesses: dict[int, tuple[Fraction, ...]] = {}
    for size in range(6):
        zero_sums = tuple(
            monomial_values
            for monomial_values in product(evaluated_values, repeat=size)
            if sum(monomial_values, Fraction(0)) == 0
        )
        counts[size] = len(zero_sums)
        if zero_sums:
            witnesses[size] = zero_sums[0]
        assert all(all(value for value in row) for row in zero_sums)
        assert not (size == 1 and zero_sums)

        # The scalars above are pointwise evaluated monomial values, not formal
        # Laurent coefficients.  Give each term a fresh formal exponent; these
        # tags are pairwise distinct and disjoint from the block coordinates.
        for monomial_values in zero_sums:
            padded_block_origin = (0,) * (block_width + size)
            remainder_exponents = tuple(
                (0,) * block_width
                + tuple(1 if index == term else 0 for index in range(size))
                for term in range(size)
            )
            assert len(set(remainder_exponents)) == size
            assert all(
                exponent != padded_block_origin for exponent in remainder_exponents
            )
            assert len(monomial_values) == len(remainder_exponents)

    assert counts[0] == 1
    assert counts[1] == 0
    assert all(counts[size] for size in range(2, 6))
    assert set(witnesses) == {0, 2, 3, 4, 5}

    # The general singleton obstruction needs no census: one supported
    # remainder monomial has a nonzero evaluated value and cannot sum to zero.
    assert all(sum((value,), Fraction(0)) != 0 for value in evaluated_values)

    return {
        "evaluated_monomial_value_set": evaluated_values,
        "zero_sum_counts": counts,
        "witnesses": witnesses,
        "possible_sizes_in_census": tuple(sorted(witnesses)),
        "singleton_complement": "impossible for a nonzero monomial",
    }


def main() -> None:
    """Run the independent finite A6 mechanism audit."""

    qq = analyse_kernel(qq_kernel())
    qc2 = analyse_kernel(qc2_kernel())
    qq_completion = audit_fixed_completion(qq)
    qc2_completion = audit_fixed_completion(qc2)
    polynomial = audit_rank_three_polynomial((qq, qc2))
    remainder = audit_remainder_census(len(qq.kernel.edges) + 2)

    print("PASS: independent A6 fixed-completion rank-three block audit")
    print(
        "physical kernel matching counts (Q/Q, Q/C^2): "
        f"({len(qq.matchings)}, {len(qc2.matchings)})"
    )
    print("affine/difference rank: 3; unimodular exponent minor: 1")
    print(f"Q/Q fixed completion: {qq_completion}")
    print(f"Q/C^2 fixed completion: {qc2_completion}")
    print(f"proper Laurent block: {polynomial}")
    print(f"bounded disjoint remainder census: {remainder}")
    print("SCOPE: bounded mechanism audit; arbitrary completion is theorem-level")
    print("NO mixed-target exclusion or realized witness is inferred")
    print("GLOBAL KRENN-GU STATUS: UNRESOLVED")


if __name__ == "__main__":
    main()
