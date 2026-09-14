"""Independent audit of the common-star at-most-two-port obstruction.

This checker deliberately does not import the owning verifier or project
scientific code.  It checks the shared-neighbor polynomial symbolically,
exhausts the finite local support patterns, and reconstructs the sharp
14-component control by a matrix-identity route.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path


Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]


def poly_add(*terms: Polynomial) -> Polynomial:
    out: defaultdict[Monomial, int] = defaultdict(int)
    for term in terms:
        for monomial, coefficient in term.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def poly_scale(term: Polynomial, coefficient: int) -> Polynomial:
    return {m: coefficient * c for m, c in term.items() if coefficient * c}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: defaultdict[Monomial, int] = defaultdict(int)
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] += coefficient_left * coefficient_right
    return {m: c for m, c in out.items() if c}


def atom(name: str) -> Polynomial:
    return {(name,): 1}


ONE_POLY: Polynomial = {(): 1}


def matching_layers(
    vertex_count: int, edges: dict[tuple[int, int], Polynomial]
) -> dict[int, Polynomial]:
    """Enumerate matchings by covered-vertex mask."""
    layers: dict[int, Polynomial] = {0: ONE_POLY}
    for (u, v), weight in edges.items():
        edge_mask = (1 << u) | (1 << v)
        additions: list[tuple[int, Polynomial]] = []
        for mask, value in layers.items():
            if not mask & edge_mask:
                additions.append((mask | edge_mask, poly_mul(value, weight)))
        for mask, value in additions:
            layers[mask] = poly_add(layers.get(mask, {}), value)
    return layers


def check_shared_neighbor_identity(common_neighbors: int = 3) -> dict:
    """Expand the physical double-hafnian polynomial behind equation (10)."""
    vertex_count = common_neighbors + 2
    center: dict[tuple[int, int], Polynomial] = {(0, 1): atom("P")}
    leaf: dict[tuple[int, int], Polynomial] = {(0, 1): atom("R")}
    for j in range(common_neighbors):
        w = j + 2
        center[0, w] = atom(f"A{j}")
        leaf[0, w] = atom(f"B{j}")
        center[1, w] = atom(f"C{j}")
        leaf[1, w] = atom(f"D{j}")

    center_layers = matching_layers(vertex_count, center)
    leaf_layers = matching_layers(vertex_count, leaf)
    actual: Polynomial = {}
    for mask, center_value in center_layers.items():
        actual = poly_add(
            actual,
            poly_mul(center_value, leaf_layers.get(mask, {})),
        )

    s: Polynomial = {}
    t: Polynomial = {}
    h: Polynomial = {}
    x: Polynomial = {}
    y: Polynomial = {}
    for j in range(common_neighbors):
        s = poly_add(s, poly_mul(atom(f"A{j}"), atom(f"B{j}")))
        t = poly_add(t, poly_mul(atom(f"C{j}"), atom(f"D{j}")))
        h = poly_add(
            h,
            poly_mul(
                poly_mul(atom(f"A{j}"), atom(f"B{j}")),
                poly_mul(atom(f"C{j}"), atom(f"D{j}")),
            ),
        )
        x = poly_add(x, poly_mul(atom(f"A{j}"), atom(f"D{j}")))
        y = poly_add(y, poly_mul(atom(f"B{j}"), atom(f"C{j}")))
    expected = poly_add(
        poly_mul(poly_add(ONE_POLY, s), poly_add(ONE_POLY, t)),
        poly_mul(atom("P"), atom("R")),
        poly_mul(x, y),
        poly_scale(h, -2),
    )
    if actual != expected:
        raise AssertionError(poly_add(actual, poly_scale(expected, -1)))

    wrong_without_correction = poly_add(expected, poly_scale(h, 2))
    mutation_residual = poly_add(actual, poly_scale(wrong_without_correction, -1))
    if mutation_residual != poly_scale(h, -2):
        raise AssertionError(mutation_residual)
    return {
        "common_neighbors": common_neighbors,
        "monomials": len(actual),
        "identity_exact": True,
        "omit_minus_2h_mutation_residual_terms": len(mutation_residual),
    }


def pair_partitions(size: int) -> list[tuple[tuple[int, int], ...]]:
    """Return all partitions of range(size) into unordered pairs."""
    if size == 0:
        return [()]
    first = 0
    out = []
    for partner in range(1, size):
        rest = [v for v in range(1, size) if v != partner]
        for sub in pair_partitions(size - 2):
            # Relabel the recursive range onto the surviving vertices.
            relabel = {i: rest[i] for i in range(size - 2)}
            pairs = ((first, partner),) + tuple(
                tuple(sorted((relabel[u], relabel[v]))) for u, v in sub
            )
            out.append(tuple(sorted(pairs)))
    return sorted(set(out))


def pair_graphs(size: int) -> list[frozenset[tuple[int, int]]]:
    """All unions of K2,2 blocks between two named parts of equal size."""
    partitions = pair_partitions(size)
    graphs = set()
    for left in partitions:
        for right in partitions:
            for permutation in itertools.permutations(range(len(right))):
                edges = set()
                for i, left_pair in enumerate(left):
                    right_pair = right[permutation[i]]
                    edges.update(itertools.product(left_pair, right_pair))
                graphs.add(frozenset(edges))
    return sorted(graphs, key=lambda graph: sorted(graph))


def connected_components(
    part_size: int,
    ab: frozenset[tuple[int, int]],
    ac: frozenset[tuple[int, int]],
    bc: frozenset[tuple[int, int]],
) -> list[set[tuple[int, int]]]:
    adjacency: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for left_part, right_part, edges in ((0, 1, ab), (0, 2, ac), (1, 2, bc)):
        for left, right in edges:
            u = (left_part, left)
            v = (right_part, right)
            adjacency[u].add(v)
            adjacency[v].add(u)
    unseen = {(part, i) for part in range(3) for i in range(part_size)}
    components = []
    while unseen:
        root = next(iter(unseen))
        queue = deque([root])
        component = {root}
        unseen.remove(root)
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    queue.append(v)
        components.append(component)
    return components


def common_third_counts(
    edge: tuple[tuple[int, int], tuple[int, int]],
    edge_sets: dict[tuple[int, int], frozenset[tuple[int, int]]],
) -> int:
    (part_u, u), (part_v, v) = edge
    third = 3 - part_u - part_v

    def adjacent(part_x: int, x: int, part_y: int, y: int) -> bool:
        if part_x < part_y:
            return (x, y) in edge_sets[part_x, part_y]
        return (y, x) in edge_sets[part_y, part_x]

    size = 4
    return sum(
        adjacent(part_u, u, third, w) and adjacent(part_v, v, third, w)
        for w in range(size)
    )


def check_local_support_exhaustion() -> dict:
    """Exhaust all pair-block graphs on four states of each color."""
    size = 4
    graphs = pair_graphs(size)
    if len(graphs) != 18:
        raise AssertionError(len(graphs))
    valid = 0
    all_k222 = 0
    matching_type = 0
    mixed_type = 0
    for ab, ac, bc in itertools.product(graphs, repeat=3):
        edge_sets = {(0, 1): ab, (0, 2): ac, (1, 2): bc}
        counts = []
        for (left_part, right_part), edges in edge_sets.items():
            counts.extend(
                common_third_counts(
                    ((left_part, left), (right_part, right)), edge_sets
                )
                for left, right in edges
            )
        if not counts or min(counts) == 0:
            continue
        valid += 1
        components = connected_components(size, ab, ac, bc)
        k222 = all(
            len(component) == 6
            and Counter(part for part, _index in component) == Counter({0: 2, 1: 2, 2: 2})
            for component in components
        )
        unique_triangle = all(count == 1 for count in counts)
        if k222:
            if set(counts) != {2}:
                raise AssertionError(counts)
            all_k222 += 1
        elif unique_triangle:
            matching_type += 1
        else:
            mixed_type += 1
    if mixed_type:
        raise AssertionError(mixed_type)
    if not all_k222 or not matching_type:
        raise AssertionError((all_k222, matching_type))
    return {
        "part_size": size,
        "pair_block_graphs": len(graphs),
        "triples_checked": len(graphs) ** 3,
        "edge_triangle_valid": valid,
        "k222_type": all_k222,
        "unique_triangle_type": matching_type,
        "mixed_type": mixed_type,
    }


@dataclass(frozen=True)
class Q3:
    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    def __add__(self, other: object) -> Q3:
        value = q3(other)
        return Q3(self.rational + value.rational, self.radical + value.radical)

    __radd__ = __add__

    def __neg__(self) -> Q3:
        return Q3(-self.rational, -self.radical)

    def __sub__(self, other: object) -> Q3:
        return self + -q3(other)

    def __mul__(self, other: object) -> Q3:
        value = q3(other)
        return Q3(
            self.rational * value.rational + 3 * self.radical * value.radical,
            self.rational * value.radical + self.radical * value.rational,
        )

    __rmul__ = __mul__

    def inverse(self) -> Q3:
        norm = self.rational**2 - 3 * self.radical**2
        if not norm:
            raise ZeroDivisionError
        return Q3(self.rational / norm, -self.radical / norm)

    def __truediv__(self, other: object) -> Q3:
        return self * q3(other).inverse()

    def __bool__(self) -> bool:
        return bool(self.rational or self.radical)

    def text(self) -> str:
        if not self.radical:
            return str(self.rational)
        return f"({self.rational})+({self.radical})*sqrt(3)"


def q3(value: object) -> Q3:
    if isinstance(value, Q3):
        return value
    if isinstance(value, (int, Fraction)):
        return Q3(Fraction(value))
    raise TypeError(value)


ZERO = Q3()
ONE = q3(1)
MINUS_HALF = q3(Fraction(-1, 2))
ROOT_WEIGHT = Q3(Fraction(2), Fraction(1))
COMPONENTS = tuple((part, fiber) for part in range(7) for fiber in range(2))
POSITIONS = (0, 1, 3)
STEP_LABEL = {
    (POSITIONS[b] - POSITIONS[a]) % 7: (a, b)
    for a in range(3)
    for b in range(3)
    if a != b
}


def port_vector(own: int, neighbor: int) -> tuple[Q3, Q3]:
    others = sorted(set(range(3)) - {own})
    return (ONE, ONE if neighbor == others[0] else ROOT_WEIGHT)


def control_edges() -> tuple[tuple[int, int, int, int, Q3, Q3], ...]:
    edges = []
    for u, (part_u, fiber_u) in enumerate(COMPONENTS):
        for v in range(u + 1, len(COMPONENTS)):
            part_v, fiber_v = COMPONENTS[v]
            if part_u == part_v:
                continue
            a, b = STEP_LABEL[(part_v - part_u) % 7]
            center = port_vector(a, b)[fiber_u] * port_vector(b, a)[fiber_v]
            leaf = MINUS_HALF / center
            edges.append((u, v, a, b, center, leaf))
    return tuple(edges)


def matrix_product(left: list[list[Q3]], right: list[list[Q3]]) -> list[list[Q3]]:
    size = len(left)
    return [
        [sum((left[u][w] * right[w][v] for w in range(size)), ZERO) for v in range(size)]
        for u in range(size)
    ]


def check_control_matrix_identities() -> tuple[dict, dict, tuple]:
    edges = control_edges()
    size = len(COMPONENTS)
    matrices: dict[tuple[str, int, int], list[list[Q3]]] = {}
    for kind in ("A", "B", "Q"):
        for a in range(3):
            for b in range(3):
                matrices[kind, a, b] = [[ZERO for _ in range(size)] for _ in range(size)]
    state_edges = []
    ports = Counter()
    for u, v, a, b, center, leaf in edges:
        for x, y, own, other, own_center, own_leaf in (
            (u, v, a, b, center, leaf),
            (v, u, b, a, center, leaf),
        ):
            matrices["A", own, other][x][y] = own_center
            matrices["B", own, other][x][y] = own_leaf
            matrices["Q", own, other][x][y] = own_center * own_leaf
            state_edges.append(((x, own), (y, other)))
            ports[x, own, other] += 1
    if len(edges) != 84 or set(ports.values()) != {2} or len(ports) != 84:
        raise AssertionError((len(edges), Counter(ports.values()), len(ports)))

    s1_rows = 0
    same_rows = 0
    distinct_rows = 0
    for d in range(3):
        for c in range(3):
            if d == c:
                continue
            q_dc = matrices["Q", d, c]
            if any(sum(row, ZERO) != -ONE for row in q_dc):
                raise AssertionError(("S1-row", d, c))
            if any(sum((q_dc[u][v] for u in range(size)), ZERO) != -ONE for v in range(size)):
                raise AssertionError(("S1-column", d, c))
            s1_rows += 2 * size

            left_1 = matrix_product(matrices["A", d, c], matrices["B", c, d])
            left_2 = matrix_product(matrices["B", d, c], matrices["A", c, d])
            right = matrix_product(q_dc, matrices["Q", c, d])
            for u in range(size):
                for v in range(size):
                    if u != v:
                        if left_1[u][v] * left_2[u][v] != 2 * right[u][v]:
                            raise AssertionError(("same-S2", d, c, u, v))
                        same_rows += 1

            e = 3 - d - c
            cross_1 = matrix_product(matrices["A", d, c], matrices["B", c, e])
            cross_2 = matrix_product(matrices["B", d, c], matrices["A", c, e])
            path = matrix_product(q_dc, matrices["Q", c, e])
            q_de = matrices["Q", d, e]
            for u in range(size):
                for v in range(size):
                    if u != v:
                        expected = 2 * path[u][v] - cross_1[u][v] * cross_2[u][v]
                        if q_de[u][v] != expected:
                            raise AssertionError(("distinct-S2", d, c, e, u, v))
                        distinct_rows += 1

    return (
        {
            "components": size,
            "edges": len(edges),
            "ports": len(ports),
            "port_multiplicity": sorted(set(ports.values())),
            "s1_scalar_equalities": s1_rows,
            "same_color_s2_off_diagonal_equalities": same_rows,
            "distinct_color_s2_off_diagonal_equalities": distinct_rows,
        },
        {"state_edges": state_edges},
        edges,
    )


def state_resource_components(
    directed_state_edges: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[set[tuple[int, int]]]:
    adjacency: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for u, v in directed_state_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(adjacency)
    out = []
    while unseen:
        root = next(iter(unseen))
        component = {root}
        queue = deque([root])
        unseen.remove(root)
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    queue.append(v)
        out.append(component)
    return out


def physical_source_for_word(
    word: tuple[int, ...], edges: tuple[tuple[int, int, int, int, Q3, Q3], ...]
) -> tuple[Q3, int]:
    physical_edges: defaultdict[tuple[int, int], Q3] = defaultdict(lambda: ZERO)
    for component, color in enumerate(word):
        matching = ((0, 1), (2, 3)) if color == 0 else (
            ((0, 2), (1, 3)) if color == 1 else ((0, 3), (1, 2))
        )
        for x, y in matching:
            physical_edges[4 * component + x, 4 * component + y] += ONE
    for u, v, a, b, center, leaf in edges:
        if word[u] == a and word[v] == b:
            physical_edges[4 * u, 4 * v] += center
            physical_edges[4 * u + a + 1, 4 * v + b + 1] += leaf

    neighbors: defaultdict[int, list[tuple[int, Q3]]] = defaultdict(list)
    for (u, v), weight in physical_edges.items():
        if weight:
            neighbors[u].append((v, weight))
            neighbors[v].append((u, weight))

    calls = 0

    @lru_cache(maxsize=None)
    def haf(mask: int) -> Q3:
        nonlocal calls
        calls += 1
        if not mask:
            return ONE
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        total = ZERO
        for v, weight in neighbors[u]:
            if rest & (1 << v):
                total += weight * haf(rest ^ (1 << v))
        return total

    return haf((1 << (4 * len(word))) - 1), calls


def check_control_global_failure(state_data: dict, edges: tuple) -> dict:
    resources = state_resource_components(state_data["state_edges"])
    if len(resources) != 7:
        raise AssertionError(len(resources))
    for resource in resources:
        if len(resource) != 6 or Counter(color for _u, color in resource) != Counter({0: 2, 1: 2, 2: 2}):
            raise AssertionError(resource)
        for (u, a), (v, b) in itertools.combinations(resource, 2):
            if a != b and not any(
                {left, right} == {(u, a), (v, b)}
                for left, right in state_data["state_edges"]
            ):
                raise AssertionError((resource, (u, a), (v, b)))

    # First reconstruct the original K2,2,2 P0/P1 route.
    matchings: dict[int, set[tuple[int, int]]] = {0: set(), 1: set()}
    for resource in resources:
        for color in (0, 1):
            pair = tuple(sorted(u for u, c in resource if c == color))
            if len(pair) != 2:
                raise AssertionError(pair)
            matchings[color].add(pair)
    graph: defaultdict[int, set[int]] = defaultdict(set)
    for pairs in matchings.values():
        for u, v in pairs:
            graph[u].add(v)
            graph[v].add(u)
    coloring: dict[int, int] = {}
    for root in range(len(COMPONENTS)):
        if root in coloring:
            continue
        coloring[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                proposed = 1 - coloring[u]
                if v in coloring and coloring[v] != proposed:
                    raise AssertionError("P0 union P1 is not bipartite")
                if v not in coloring:
                    coloring[v] = proposed
                    queue.append(v)
    word = tuple(coloring[u] for u in range(len(COMPONENTS)))
    if len(set(word)) != 2:
        raise AssertionError(word)

    selected = []
    for resource in resources:
        active = sorted((u, color) for u, color in resource if word[u] == color)
        if Counter(color for _u, color in active) != Counter({0: 1, 1: 1}):
            raise AssertionError(active)
        selected.append(active)
    source, recursion_states = physical_source_for_word(word, edges)
    expected = q3(Fraction(1, 128))
    if source != expected:
        raise AssertionError((word, source))

    # Independently reconstruct the stronger complete-resource consumer.  A
    # component is a directed edge from its color-0 resource to its color-1
    # resource.  Find a simple directed cycle and switch exactly its edges.
    resource_of = {}
    for resource_index, resource in enumerate(resources):
        for state in resource:
            resource_of[state] = resource_index
    directed: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for component in range(len(COMPONENTS)):
        start = resource_of[component, 0]
        end = resource_of[component, 1]
        if start == end:
            raise AssertionError(("resource loop", component))
        directed[start].append((end, component))
    if {len(directed[r]) for r in range(len(resources))} != {2}:
        raise AssertionError(directed)

    cycle_components = None
    for start in range(len(resources)):
        queue = deque([(start, (start,), ())])
        while queue and cycle_components is None:
            vertex, path_vertices, path_components = queue.popleft()
            for neighbor, component in directed[vertex]:
                if neighbor == start:
                    cycle_components = path_components + (component,)
                    break
                if neighbor not in path_vertices:
                    queue.append(
                        (
                            neighbor,
                            path_vertices + (neighbor,),
                            path_components + (component,),
                        )
                    )
        if cycle_components is not None:
            break
    if cycle_components is None:
        raise AssertionError("no directed resource cycle")
    cycle_word = tuple(
        1 if component in cycle_components else 0
        for component in range(len(COMPONENTS))
    )
    cycle_source, cycle_recursion_states = physical_source_for_word(cycle_word, edges)
    cycle_expected = q3(Fraction(1, 2 ** len(cycle_components)))
    if cycle_source != cycle_expected:
        raise AssertionError((cycle_components, cycle_word, cycle_source))
    return {
        "resources": len(resources),
        "matching_sizes": {str(color): len(pairs) for color, pairs in matchings.items()},
        "component_word": "".join(map(str, word)),
        "selected_states_per_resource": [len(active) for active in selected],
        "physical_source": source.text(),
        "expected": "1/128",
        "physical_recursion_states": recursion_states,
        "mixed_target": "0",
        "directed_resource_cycle": {
            "length": len(cycle_components),
            "components": list(cycle_components),
            "component_word": "".join(map(str, cycle_word)),
            "physical_source": cycle_source.text(),
            "expected": cycle_expected.text(),
            "physical_recursion_states": cycle_recursion_states,
        },
    }


def check_complete_resource_degree_three_control() -> dict:
    """Literal K3,3,3 resource control for the general consumer."""
    component_list = tuple((part, fiber) for part in range(13) for fiber in range(3))
    index = {component: i for i, component in enumerate(component_list)}
    offsets = (0, 1, 3)
    edge_by_pair = {}
    for resource in range(13):
        for a, b in itertools.combinations(range(3), 2):
            for i in range(3):
                for j in range(3):
                    u = index[(resource + offsets[a]) % 13, i]
                    v = index[(resource + offsets[b]) % 13, j]
                    if u > v:
                        u, v, own_u, own_v = v, u, b, a
                    else:
                        own_u, own_v = a, b
                    pair = (u, v)
                    if pair in edge_by_pair:
                        raise AssertionError(("duplicate component pair", pair))
                    edge_by_pair[pair] = (
                        u,
                        v,
                        own_u,
                        own_v,
                        ONE,
                        q3(Fraction(-1, 3)),
                    )
    edges = tuple(edge_by_pair.values())
    if len(edges) != 13 * 3 * 9:
        raise AssertionError(len(edges))

    ports = Counter()
    for u, v, a, b, _center, _leaf in edges:
        ports[u, a, b] += 1
        ports[v, b, a] += 1
    if len(ports) != len(component_list) * 6 or set(ports.values()) != {3}:
        raise AssertionError((len(ports), Counter(ports.values())))

    # The resource digraph has three parallel edges p -> p-1.  Taking fiber
    # zero on its 13-cycle switches 13 of 39 components.
    word = tuple(fiber == 0 for _part, fiber in component_list)
    word = tuple(int(color) for color in word)
    source, recursion_states = physical_source_for_word(word, edges)
    expected = q3(Fraction(1, 3**13))
    if source != expected:
        raise AssertionError((source, expected))
    return {
        "components": len(component_list),
        "resources": 13,
        "resource_shape": [3, 3, 3],
        "component_edges": len(edges),
        "ordered_port_multiplicity": 3,
        "switched_components": sum(word),
        "literal_physical_source": source.text(),
        "expected": expected.text(),
        "physical_recursion_states": recursion_states,
        "scope": "general-consumer control only; S2 is not asserted",
    }


def lf_sha256(path: Path) -> str:
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()
    return hashlib.sha256(normalized).hexdigest()


def build_result() -> dict:
    shared = check_shared_neighbor_identity()
    local = check_local_support_exhaustion()
    control, state_data, edges = check_control_matrix_identities()
    global_failure = check_control_global_failure(state_data, edges)
    degree_three = check_complete_resource_degree_three_control()
    return {
        "schema": "protected-common-star-two-port-independent-audit-v1",
        "status": "PASS",
        "shared_neighbor_polynomial": shared,
        "local_support_exhaustion": local,
        "repeated_port_control_matrix_route": control,
        "repeated_port_control_global_failure": global_failure,
        "complete_resource_degree_three_control": degree_three,
        "mutation_controls": {
            "omit_minus_2h": "nonzero symbolic residual",
            "omit_global_target": "S1 and S2 pass while the reconstructed mixed word is nonzero",
            "allow_m1_resource": "a resource cycle can switch every component, so mixedness is not forced",
            "allow_zero_factor": "would invalidate the port-factor nonvanishing step",
            "allow_more_than_one_label_per_component_pair": "outside audited support model",
        },
        "scope": (
            "independent companion checks for the analytic at-most-two-port "
            "common-star proof; not a finite proof of the all-order theorem"
        ),
        "global_status_changed": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(json.dumps({"status": "PASS", "output": str(args.output)}))
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
