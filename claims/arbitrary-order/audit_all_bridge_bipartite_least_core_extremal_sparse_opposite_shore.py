"""Independent bounded audit of the extremal sparse-shore reduction.

This audit deliberately imports no repository module and does not inspect or
import the primary verifier.  Bipartite supports are integer bitmasks,
perfect matchings are permutation masks, and all weighted calculations use
``Fraction`` arithmetic.

The exhaustive census through equal shores of size four and the two exact
weighted controls are finite QA.  They do not prove the arbitrary-order
written theorem and they do not search for Krenn--Gu witnesses.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from functools import cache, reduce
from itertools import combinations, pairwise, permutations
from operator import or_

Pair = tuple[int, int]
PermutationMatching = tuple[int, ...]


def edge_bit(shore_size: int, left: int, right: int) -> int:
    return 1 << (left * shore_size + right)


@cache
def permutation_data(
    shore_size: int,
) -> tuple[tuple[PermutationMatching, int], ...]:
    output: list[tuple[PermutationMatching, int]] = []
    for image in permutations(range(shore_size)):
        mask = 0
        for left, right in enumerate(image):
            mask |= edge_bit(shore_size, left, right)
        output.append((image, mask))
    return tuple(output)


def perfect_matchings(shore_size: int, support: int) -> tuple[int, ...]:
    return tuple(
        matching_mask
        for _, matching_mask in permutation_data(shore_size)
        if matching_mask & support == matching_mask
    )


def shore_degrees(shore_size: int, support: int) -> tuple[list[int], list[int]]:
    left_degree = [0] * shore_size
    right_degree = [0] * shore_size
    for left in range(shore_size):
        for right in range(shore_size):
            if support & edge_bit(shore_size, left, right):
                left_degree[left] += 1
                right_degree[right] += 1
    return left_degree, right_degree


def full_adjacency(shore_size: int, support: int) -> list[set[int]]:
    adjacency = [set() for _ in range(2 * shore_size)]
    for left in range(shore_size):
        for right in range(shore_size):
            if not support & edge_bit(shore_size, left, right):
                continue
            right_vertex = shore_size + right
            adjacency[left].add(right_vertex)
            adjacency[right_vertex].add(left)
    return adjacency


def connected_without(adjacency: list[set[int]], removed: int | None = None) -> bool:
    remaining = [vertex for vertex in range(len(adjacency)) if vertex != removed]
    if not remaining:
        return True
    reached = {remaining[0]}
    queue = deque([remaining[0]])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour == removed or neighbour in reached:
                continue
            reached.add(neighbour)
            queue.append(neighbour)
    return len(reached) == len(remaining)


def incident_bits(shore_size: int, vertex: int, support: int) -> tuple[int, ...]:
    if vertex < shore_size:
        candidates = (
            edge_bit(shore_size, vertex, right) for right in range(shore_size)
        )
    else:
        right = vertex - shore_size
        candidates = (
            edge_bit(shore_size, left, right) for left in range(shore_size)
        )
    return tuple(bit for bit in candidates if support & bit)


def port_counts(
    shore_size: int, vertex: int, support: int, matchings: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(
        sum(bool(matching & bit) for matching in matchings)
        for bit in incident_bits(shore_size, vertex, support)
    )


def trace_two_hub_routes(
    shore_size: int,
    support: int,
    first_hub: int,
    second_hub: int,
) -> tuple[tuple[int, ...], ...]:
    """Trace all routes when every non-hub vertex has degree two."""
    adjacency = full_adjacency(shore_size, support)
    routes: list[tuple[int, ...]] = []
    used_internal: set[int] = set()
    used_edges: set[frozenset[int]] = set()
    for neighbour in sorted(adjacency[first_hub]):
        path = [first_hub, neighbour]
        previous, current = first_hub, neighbour
        while current != second_hub:
            assert current != first_hub
            assert len(adjacency[current]) == 2
            choices = adjacency[current] - {previous}
            assert len(choices) == 1
            following = next(iter(choices))
            assert following not in path
            path.append(following)
            previous, current = current, following
        internal = set(path[1:-1])
        assert not internal & used_internal
        used_internal.update(internal)
        used_edges.update(frozenset((left, right)) for left, right in pairwise(path))
        routes.append(tuple(path))

    support_edges = {
        frozenset((left, shore_size + right))
        for left in range(shore_size)
        for right in range(shore_size)
        if support & edge_bit(shore_size, left, right)
    }
    assert used_edges == support_edges
    assert used_internal == set(range(2 * shore_size)) - {first_hub, second_hub}
    return tuple(routes)


def audit_sparse_vertex(
    shore_size: int,
    support: int,
    matchings: tuple[int, ...],
    beta: int,
    sparse_vertex: int,
) -> str:
    """Check the exact opposite-shore dichotomy at one sparse vertex."""
    adjacency = full_adjacency(shore_size, support)
    degrees = [len(neighbours) for neighbours in adjacency]
    number = len(matchings)
    assert beta >= 2
    assert degrees[sparse_vertex] == number == beta + 1

    sparse_ports = port_counts(shore_size, sparse_vertex, support, matchings)
    assert len(sparse_ports) == beta + 1
    assert set(sparse_ports) == {1}

    if sparse_vertex < shore_size:
        own_shore = set(range(shore_size))
        opposite_shore = set(range(shore_size, 2 * shore_size))
    else:
        own_shore = set(range(shore_size, 2 * shore_size))
        opposite_shore = set(range(shore_size))

    own_excess = sum(degrees[vertex] - 2 for vertex in own_shore)
    opposite_excess = sum(degrees[vertex] - 2 for vertex in opposite_shore)
    assert own_excess == opposite_excess == beta - 1
    assert degrees[sparse_vertex] - 2 == beta - 1
    assert all(
        degrees[vertex] == 2 for vertex in own_shore - {sparse_vertex}
    )

    opposite_branch = sorted(
        vertex for vertex in opposite_shore if degrees[vertex] >= 3
    )
    assert 1 <= len(opposite_branch) <= beta - 1

    if len(opposite_branch) == 1:
        opposite_hub = opposite_branch[0]
        assert degrees[opposite_hub] == beta + 1
        assert all(
            degrees[vertex] == 2
            for vertex in opposite_shore - {opposite_hub}
        )
        routes = trace_two_hub_routes(
            shore_size, support, sparse_vertex, opposite_hub
        )
        assert len(routes) == beta + 1
        assert all((len(route) - 1) % 2 == 1 for route in routes)
        return "two_hub"

    assert 2 <= len(opposite_branch) <= beta - 1
    for vertex in opposite_branch:
        degree = degrees[vertex]
        assert 3 <= degree <= beta
        counts = port_counts(shore_size, vertex, support, matchings)
        assert len(counts) == degree
        assert all(count >= 1 for count in counts)
        assert sum(counts) == number
        assert any(count >= 2 for count in counts)
    return "multi_branch"


def enumerate_core_census() -> dict[int, dict[str, object]]:
    summaries: dict[int, dict[str, object]] = {}
    for shore_size in (2, 3, 4):
        matching_covered = 0
        equality_profiles: Counter[tuple[object, ...]] = Counter()
        sparse_cases = 0
        sparse_two_hub = 0
        sparse_multi_branch = 0
        beta_three_sparse_profiles: Counter[tuple[int, ...]] = Counter()

        for support in range(1, 1 << (shore_size * shore_size)):
            left_degree, right_degree = shore_degrees(shore_size, support)
            degrees_by_shore = left_degree + right_degree
            if min(degrees_by_shore) < 2:
                continue

            adjacency = full_adjacency(shore_size, support)
            if not connected_without(adjacency):
                continue

            matchings = perfect_matchings(shore_size, support)
            if not matchings:
                continue
            allowed_union = reduce(or_, matchings, 0)
            if allowed_union != support:
                continue

            matching_covered += 1
            edge_count = support.bit_count()
            beta = edge_count - 2 * shore_size + 1
            number = len(matchings)
            assert beta >= 1

            left_excess = sum(degree - 2 for degree in left_degree)
            right_excess = sum(degree - 2 for degree in right_degree)
            assert left_excess == right_excess == beta - 1
            assert all(degree <= beta + 1 for degree in degrees_by_shore)

            # A nontrivial connected matching-covered graph is 2-connected.
            assert all(
                connected_without(adjacency, removed=vertex)
                for vertex in range(2 * shore_size)
            )

            if number != beta + 1:
                continue

            profile = (
                beta,
                number,
                tuple(sorted(left_degree, reverse=True)),
                tuple(sorted(right_degree, reverse=True)),
            )
            equality_profiles[profile] += 1

            sparse_vertices = [
                vertex
                for vertex, degree in enumerate(degrees_by_shore)
                if degree >= 3 and degree == number == beta + 1
            ]
            for sparse_vertex in sparse_vertices:
                sparse_cases += 1
                outcome = audit_sparse_vertex(
                    shore_size, support, matchings, beta, sparse_vertex
                )
                if outcome == "two_hub":
                    sparse_two_hub += 1
                else:
                    sparse_multi_branch += 1

            if shore_size == 4 and beta == 3 and sparse_vertices:
                beta_three_sparse_profiles[
                    tuple(sorted(degrees_by_shore, reverse=True))
                ] += 1

        summaries[shore_size] = {
            "matching_covered": matching_covered,
            "equality_profiles": equality_profiles,
            "sparse_cases": sparse_cases,
            "sparse_two_hub": sparse_two_hub,
            "sparse_multi_branch": sparse_multi_branch,
            "beta_three_sparse_profiles": beta_three_sparse_profiles,
        }

    assert summaries[2]["matching_covered"] == 1
    assert summaries[3]["matching_covered"] == 34
    assert summaries[4]["matching_covered"] == 6785

    m2_profiles = summaries[2]["equality_profiles"]
    assert isinstance(m2_profiles, Counter)
    assert m2_profiles == Counter({(1, 2, (2, 2), (2, 2)): 1})

    m3_profiles = summaries[3]["equality_profiles"]
    assert isinstance(m3_profiles, Counter)
    assert m3_profiles == Counter(
        {
            (1, 2, (2, 2, 2), (2, 2, 2)): 6,
            (2, 3, (3, 2, 2), (3, 2, 2)): 18,
            (3, 4, (3, 3, 2), (3, 3, 2)): 9,
        }
    )

    m4_profiles = summaries[4]["equality_profiles"]
    assert isinstance(m4_profiles, Counter)
    beta_three_equality = Counter(
        {
            profile: count
            for profile, count in m4_profiles.items()
            if profile[0] == 3
        }
    )
    assert beta_three_equality == Counter(
        {
            (3, 4, (3, 3, 2, 2), (3, 3, 2, 2)): 864,
            (3, 4, (4, 2, 2, 2), (3, 3, 2, 2)): 288,
            (3, 4, (3, 3, 2, 2), (4, 2, 2, 2)): 288,
            (3, 4, (4, 2, 2, 2), (4, 2, 2, 2)): 96,
        }
    )

    beta_three_profiles = summaries[4]["beta_three_sparse_profiles"]
    assert isinstance(beta_three_profiles, Counter)
    assert beta_three_profiles == Counter(
        {
            (4, 3, 3, 2, 2, 2, 2, 2): 576,
            (4, 4, 2, 2, 2, 2, 2, 2): 96,
        }
    )
    return summaries


def support_from_rows(rows: tuple[str, ...]) -> int:
    shore_size = len(rows)
    assert all(len(row) == shore_size for row in rows)
    support = 0
    for left, row in enumerate(rows):
        for right, value in enumerate(row):
            assert value in {"0", "1"}
            if value == "1":
                support |= edge_bit(shore_size, left, right)
    return support


def matching_weight(
    shore_size: int,
    image: PermutationMatching,
    weights: dict[Pair, Fraction],
) -> Fraction:
    value = Fraction(1)
    for left, right in enumerate(image):
        bit = edge_bit(shore_size, left, right)
        if not weights.get((left, right), Fraction(0)):
            return Fraction(0)
        assert bit
        value *= weights[left, right]
    return value


def subpermanent(
    left_vertices: tuple[int, ...],
    right_vertices: tuple[int, ...],
    weights: dict[Pair, Fraction],
) -> Fraction:
    assert len(left_vertices) == len(right_vertices)
    total = Fraction(0)
    for image in permutations(right_vertices):
        value = Fraction(1)
        for left, right in zip(left_vertices, image):
            edge_weight = weights.get((left, right), Fraction(0))
            if not edge_weight:
                value = Fraction(0)
                break
            value *= edge_weight
        total += value
    return total


def supported_subpermanent_count(
    shore_size: int,
    support: int,
    left_vertices: tuple[int, ...],
    right_vertices: tuple[int, ...],
) -> int:
    assert len(left_vertices) == len(right_vertices)
    total = 0
    for image in permutations(right_vertices):
        if all(
            support & edge_bit(shore_size, left, right)
            for left, right in zip(left_vertices, image)
        ):
            total += 1
    return total


def weighted_port_data(
    shore_size: int,
    support: int,
    weights: dict[Pair, Fraction],
    vertex: int,
) -> tuple[tuple[Pair, int, Fraction], ...]:
    supported = [
        (image, matching_mask)
        for image, matching_mask in permutation_data(shore_size)
        if matching_mask & support == matching_mask
    ]
    output: list[tuple[Pair, int, Fraction]] = []
    for bit in incident_bits(shore_size, vertex, support):
        position = bit.bit_length() - 1
        pair = divmod(position, shore_size)
        terms = [
            matching_weight(shore_size, image, weights)
            for image, matching_mask in supported
            if matching_mask & bit
        ]
        output.append((pair, len(terms), sum(terms, Fraction(0))))
    return tuple(output)


def audit_weighted_least_residual(
    rows: tuple[str, ...],
    special_edge: Pair,
    expected_beta: int,
    expected_degrees: tuple[tuple[int, ...], tuple[int, ...]],
    expected_minor_count: int,
    expected_minor_values: set[Fraction],
) -> tuple[int, tuple[Fraction, ...], dict[int, tuple[tuple[Pair, int, Fraction], ...]]]:
    shore_size = len(rows)
    support = support_from_rows(rows)
    left_degree, right_degree = shore_degrees(shore_size, support)
    assert (tuple(left_degree), tuple(right_degree)) == expected_degrees
    beta = support.bit_count() - 2 * shore_size + 1
    assert beta == expected_beta

    supported = [
        (image, matching_mask)
        for image, matching_mask in permutation_data(shore_size)
        if matching_mask & support == matching_mask
    ]
    assert reduce(or_, (mask for _, mask in supported), 0) == support
    assert len(supported) == beta + 1

    weights = {
        (left, right): Fraction(1)
        for left in range(shore_size)
        for right in range(shore_size)
        if support & edge_bit(shore_size, left, right)
    }
    assert special_edge in weights
    weights[special_edge] = Fraction(-3)
    full_weights = tuple(
        matching_weight(shore_size, image, weights) for image, _ in supported
    )
    assert sorted(full_weights) == [Fraction(-3), Fraction(1), Fraction(1), Fraction(1)]
    assert sum(full_weights, Fraction(0)) == 0

    proper_values: list[Fraction] = []
    for size in range(1, shore_size):
        for left_vertices in combinations(range(shore_size), size):
            for right_vertices in combinations(range(shore_size), size):
                count = supported_subpermanent_count(
                    shore_size,
                    support,
                    left_vertices,
                    right_vertices,
                )
                if not count:
                    continue
                value = subpermanent(left_vertices, right_vertices, weights)
                assert value != 0
                proper_values.append(value)
    assert len(proper_values) == expected_minor_count
    assert set(proper_values) == expected_minor_values

    adjacency = full_adjacency(shore_size, support)
    port_tables = {
        vertex: weighted_port_data(
            shore_size, support, weights, vertex
        )
        for vertex, neighbours in enumerate(adjacency)
        if len(neighbours) >= 3
    }
    return beta, full_weights, port_tables


def audit_exact_countermodels() -> None:
    beta, _, ports = audit_weighted_least_residual(
        rows=("011", "111", "111"),
        special_edge=(1, 1),
        expected_beta=3,
        expected_degrees=((2, 3, 3), (2, 3, 3)),
        expected_minor_count=17,
        expected_minor_values={
            Fraction(-3),
            Fraction(-2),
            Fraction(1),
            Fraction(2),
        },
    )
    assert beta == 3
    assert len(ports) == 4
    assert all(sorted(count for _, count, _ in table) == [1, 1, 2] for table in ports.values())
    assert all(total != 0 for table in ports.values() for _, _, total in table)

    beta, _, ports = audit_weighted_least_residual(
        rows=("1111", "0101", "1010", "1100"),
        special_edge=(0, 0),
        expected_beta=3,
        expected_degrees=((4, 2, 2, 2), (3, 3, 2, 2)),
        expected_minor_count=51,
        expected_minor_values={
            Fraction(-3),
            Fraction(-2),
            Fraction(-1),
            Fraction(1),
            Fraction(2),
        },
    )
    assert beta == 3
    sparse_table = ports[0]
    assert [(count, total) for _, count, total in sparse_table] == [
        (1, Fraction(-3)),
        (1, Fraction(1)),
        (1, Fraction(1)),
        (1, Fraction(1)),
    ]
    opposite_tables = (ports[4], ports[5])
    assert [sorted(count for _, count, _ in table) for table in opposite_tables] == [
        [1, 1, 2],
        [1, 1, 2],
    ]
    assert all(
        total != 0 for table in opposite_tables for _, _, total in table
    )
    assert sorted(total for _, _, total in opposite_tables[0]) == [
        Fraction(-3),
        Fraction(1),
        Fraction(2),
    ]
    assert sorted(total for _, _, total in opposite_tables[1]) == [
        Fraction(-2),
        Fraction(1),
        Fraction(1),
    ]


def main() -> None:
    summaries = enumerate_core_census()
    print(
        "connected bipartite matching-covered census (shore size: count):",
        {size: data["matching_covered"] for size, data in summaries.items()},
    )
    print(
        "equality profiles through 3+3:",
        {
            size: dict(data["equality_profiles"])
            for size, data in summaries.items()
            if size <= 3
        },
    )
    print(
        "beta=3 sharp equality profiles on 4+4:",
        {
            profile: count
            for profile, count in summaries[4]["equality_profiles"].items()
            if profile[0] == 3
        },
    )
    print(
        "beta=3 sparse 4+4 degree-profile census:",
        dict(summaries[4]["beta_three_sparse_profiles"]),
    )
    print("shore-excess and extremal sparse opposite-shore dichotomy: PASS")
    print("matching-covered 2-connectivity and two-hub odd routes: PASS")
    print("multi-branch opposite-shore aggregate port counts: PASS")
    audit_exact_countermodels()
    print("K_(3,3)-edge equality-simplex exact least residual: PASS")
    print("order-eight sparse-site/multi-aggregate exact least residual: PASS")
    print(
        "scope: bounded exact QA through 4+4 plus two rational controls; "
        "the written proof carries the arbitrary-order quantifiers"
    )
    print("independence: no repository imports and no primary-verifier imports")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
