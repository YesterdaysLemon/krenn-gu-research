"""Independent exact audit of the tensor binary-resource cover candidate."""

from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import itertools
import json
from pathlib import Path


@dataclass(frozen=True)
class Q3:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = q3(other)
        return Q3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, other):
        return self + -q3(other)

    def __rsub__(self, other):
        return q3(other) - self

    def __mul__(self, other):
        other = q3(other)
        return Q3(self.a * other.a + 3 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - 3 * self.b * self.b
        if not norm:
            raise ZeroDivisionError
        return Q3(self.a / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * q3(other).inverse()

    def __eq__(self, other):
        try:
            other = q3(other)
        except (TypeError, ValueError):
            return NotImplemented
        return self.a == other.a and self.b == other.b

    def __bool__(self):
        return bool(self.a or self.b)

    def text(self):
        if not self.b:
            return str(self.a)
        return f"({self.a})+({self.b})*sqrt(3)"


def q3(value):
    if isinstance(value, Q3):
        return value
    return Q3(Fraction(value))


ZERO, ONE, HALF = Q3(), q3(1), q3(Fraction(1, 2))
T = Q3(Fraction(-1, 2), Fraction(1, 2))
R = Q3(Fraction(2), Fraction(1))


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), ZERO)
             for j in range(len(right[0]))] for i in range(len(left))]


def hadamard(left, right):
    return [[x * y for x, y in zip(row_l, row_r)]
            for row_l, row_r in zip(left, right)]


def scale(value, matrix):
    return [[value * x for x in row] for row in matrix]


def inverse(matrix):
    n = len(matrix)
    rows = [row[:] + unit[:] for row, unit in zip(matrix, eye(n))]
    for column in range(n):
        pivot = next(row for row in range(column, n) if rows[row][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        factor = rows[column][column].inverse()
        rows[column] = [factor * x for x in rows[column]]
        for row in range(n):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [x - factor * y for x, y in
                         zip(rows[row], rows[column])]
    return [row[n:] for row in rows]


def kron(left, right):
    return [[x * y for x in row_l for y in row_r]
            for row_l in left for row_r in right]


def matrix_equal(left, right):
    return all(x == y for row_l, row_r in zip(left, right)
               for x, y in zip(row_l, row_r))


def construct_tensor_data():
    small = [[ONE, T, ONE], [ONE, ONE, T], [T, ONE, ONE]]
    left, right = eye(5), eye(5)
    for i, j in itertools.product(range(3), repeat=2):
        left[i][j] = small[i][j]
        right[i + 2][j + 2] = small[i][j]
    m = matmul(left, right)
    n = scale(-ONE, transpose(inverse(m)))
    support = {(i, j) for i, j in itertools.product(range(5), repeat=2)
               if m[i][j]}
    assert support == {(i, j) for i, j in itertools.product(range(5), repeat=2)
                       if n[i][j]}
    assert len(support) == 21

    f = {(0, 1): transpose(m), (0, 2): eye(5), (1, 2): m}
    for a, b in list(f):
        f[b, a] = transpose(f[a, b])
    swap = {0: 1, 1: 0, 2: 2}
    g = {(a, b): f[swap[a], swap[b]]
         for a, b in itertools.permutations(range(3), 2)}

    tensor_a, tensor_b, tensor_q = {}, {}, {}
    for a, b in itertools.permutations(range(3), 2):
        tensor_a[a, b] = kron(f[a, b], g[a, b])
        # Compute the 25-dimensional dual directly rather than importing or
        # trusting the author's tensor inverse formula.
        tensor_b[a, b] = scale(-ONE, transpose(inverse(tensor_a[a, b])))
        tensor_q[a, b] = hadamard(tensor_a[a, b], tensor_b[a, b])
        assert matrix_equal(matmul(tensor_a[a, b], transpose(tensor_b[a, b])),
                            scale(-ONE, eye(25)))
        assert all(sum(row, ZERO) == -ONE for row in tensor_q[a, b])

    support_counts = {
        f"{a}{b}": sum(bool(x) for row in tensor_a[a, b] for x in row)
        for a, b in ((0, 1), (0, 2), (1, 2))
    }
    assert support_counts == {"01": 441, "02": 105, "12": 105}

    strict_checks = 0
    for c, d, e in itertools.permutations(range(3), 3):
        h = matmul(tensor_q[d, c], tensor_q[c, e])
        xy = hadamard(matmul(tensor_a[d, c], tensor_b[c, e]),
                      matmul(tensor_b[d, c], tensor_a[c, e]))
        assert matrix_equal(h, scale(-ONE, tensor_q[d, e]))
        assert matrix_equal(xy, h)
        strict_checks += 2 * 25 * 25
    return m, n, tensor_a, tensor_b, tensor_q, support_counts, strict_checks


def port_vector(own, neighbor):
    others = sorted(set(range(3)) - {own})
    return (ONE, ONE if neighbor == others[0] else R)


def local_edges(tensor_a, tensor_b):
    states = tuple(itertools.product(range(3), range(25), range(2)))
    edges = {}
    by_pair = Counter()
    for u, (a, p, clone_u) in enumerate(states):
        for v in range(u + 1, len(states)):
            b, q, clone_v = states[v]
            if a == b or not tensor_a[a, b][p][q]:
                continue
            factor = port_vector(a, b)[clone_u] * port_vector(b, a)[clone_v]
            A = tensor_a[a, b][p][q] * factor
            B = tensor_b[a, b][p][q] / (2 * factor)
            assert A and B
            edges[u, v] = (A, B)
            by_pair[a, b] += 1
    assert by_pair == Counter({(0, 1): 1764, (0, 2): 420, (1, 2): 420})
    assert len(edges) == 2604
    return states, edges, by_pair


MODULUS = 5
GROUP = tuple((a, b, c, d) for a, b, c, d in
              itertools.product(range(MODULUS), repeat=4)
              if (a * d - b * c) % MODULUS == 1)
TRANSITIONS = {
    0: ((1, 0, 0, 1), (1, 1, 0, 1), (3, 2, 4, 3)),
    1: ((1, 0, 0, 1), (2, 4, 4, 1), (4, 2, 1, 2)),
}


def group_mul(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return ((a * e + b * g) % MODULUS, (a * f + b * h) % MODULUS,
            (c * e + d * g) % MODULUS, (c * f + d * h) % MODULUS)


def group_inverse(matrix):
    a, b, c, d = matrix
    return d % MODULUS, -b % MODULUS, -c % MODULUS, a % MODULUS


def incidence_data():
    assert len(GROUP) == 120
    group_index = {matrix: index for index, matrix in enumerate(GROUP)}
    resources = [[] for _ in GROUP]
    membership = {}
    for clone in range(2):
        for g_index, g in enumerate(GROUP):
            old = clone * len(GROUP) + g_index
            for color in range(3):
                resource = group_index[group_mul(g, TRANSITIONS[clone][color])]
                resources[resource].append((old, color, clone))
                membership[old, color] = resource
    assert all(len(resource) == 6 for resource in resources)
    assert len(membership) == 720

    adjacency = {}
    for old in range(240):
        adjacency["c", old] = {("r", membership[old, color]) for color in range(3)}
    for resource, items in enumerate(resources):
        adjacency["r", resource] = {("c", old) for old, _color, _clone in items}
    girth = None
    for start in adjacency:
        distance, parent = {start: 0}, {start: None}
        queue = deque((start,))
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in distance:
                    distance[neighbor] = distance[node] + 1
                    parent[neighbor] = node
                    queue.append(neighbor)
                elif parent[node] != neighbor:
                    cycle = distance[node] + distance[neighbor] + 1
                    girth = cycle if girth is None else min(girth, cycle)
    assert girth == 8
    return group_index, resources, membership, girth


def instantiate_cover(states, local, resources, group_index):
    transition_inverses = {
        (clone, color): group_inverse(TRANSITIONS[clone][color])
        for clone in range(2) for color in range(3)
    }

    def component_id(base, clone, resource, color):
        g = group_mul(GROUP[resource], transition_inverses[clone, color])
        return (clone * 120 + group_index[g]) * 25 + base

    gadgets = {}
    resource_counts = Counter()
    component_adjacency = [set() for _ in range(6000)]
    for resource in range(120):
        actual = [component_id(base, clone, resource, color)
                  for color, base, clone in states]
        assert len(set(actual)) == 150
        for (u, v), (A, B) in local.items():
            actual_u, actual_v = actual[u], actual[v]
            color_u, color_v = states[u][0], states[v][0]
            if actual_u > actual_v:
                actual_u, actual_v = actual_v, actual_u
                color_u, color_v = color_v, color_u
            pair = actual_u, actual_v
            assert pair not in gadgets
            gadgets[pair] = (resource, color_u, color_v, A, B)
            resource_counts[resource] += 1
            component_adjacency[actual_u].add(actual_v)
            component_adjacency[actual_v].add(actual_u)
    assert len(gadgets) == 312480
    assert set(resource_counts.values()) == {2604}

    triangle_count = 0
    for u, neighbors_u in enumerate(component_adjacency):
        for v in neighbors_u:
            if v <= u:
                continue
            for w in neighbors_u & component_adjacency[v]:
                if w <= v:
                    continue
                triangle_count += 1
                data = (gadgets[u, v], gadgets[u, w], gadgets[v, w])
                assert len({item[0] for item in data}) == 1
                labels = {
                    u: (data[0][1], data[1][1]),
                    v: (data[0][2], data[2][1]),
                    w: (data[1][2], data[2][2]),
                }
                assert all(left == right for left, right in labels.values())
    assert triangle_count == 423360
    return gadgets, component_adjacency, triangle_count


def binary_state_components(gadgets):
    summaries = {}
    for colors in ((0, 1), (0, 2), (1, 2)):
        adjacency = {(component, color): set()
                     for component in range(6000) for color in colors}
        for (u, v), (_resource, color_u, color_v, _A, _B) in gadgets.items():
            if {color_u, color_v} != set(colors):
                continue
            left, right = (u, color_u), (v, color_v)
            adjacency[left].add(right)
            adjacency[right].add(left)
        pending = set(adjacency)
        shapes = Counter()
        all_noncomplete = True
        while pending:
            part = {next(iter(pending))}
            queue = deque(part)
            while queue:
                for neighbor in adjacency[queue.popleft()]:
                    if neighbor not in part:
                        part.add(neighbor)
                        queue.append(neighbor)
            pending.difference_update(part)
            left_count = sum(color == colors[0] for _component, color in part)
            right_count = len(part) - left_count
            edge_count = sum(len(adjacency[state]) for state in part) // 2
            shapes[left_count, right_count, edge_count] += 1
            all_noncomplete &= edge_count < left_count * right_count
        assert all_noncomplete
        summaries[f"{colors[0]}{colors[1]}"] = {
            "components": sum(shapes.values()),
            "shapes": {f"{a}+{b}:{edges}": count
                       for (a, b, edges), count in sorted(shapes.items())},
            "all_noncomplete": True,
        }
    assert summaries == {
        "01": {"components": 120, "shapes": {"50+50:1764": 120},
               "all_noncomplete": True},
        "02": {"components": 600, "shapes": {"10+10:84": 600},
               "all_noncomplete": True},
        "12": {"components": 600, "shapes": {"10+10:84": 600},
               "all_noncomplete": True},
    }
    return summaries


def hafnian(vertices, adjacency):
    local_index = {vertex: index for index, vertex in enumerate(vertices)}
    neighbors = [[] for _ in vertices]
    for vertex in vertices:
        u = local_index[vertex]
        for other, weight in adjacency[vertex]:
            if other in local_index:
                neighbors[u].append((local_index[other], weight))

    @lru_cache(maxsize=None)
    def recurse(mask):
        if not mask:
            return ONE, 1
        choices = [u for u in range(len(vertices)) if mask & (1 << u)]
        u = min(choices, key=lambda item: sum(mask & (1 << v)
                                              for v, _weight in neighbors[item]))
        rest = mask ^ (1 << u)
        total, ways = ZERO, 0
        for v, weight in neighbors[u]:
            if rest & (1 << v):
                tail, count = recurse(rest ^ (1 << v))
                total += weight * tail
                ways += count
        return total, ways

    value, ways = recurse((1 << len(vertices)) - 1)
    return value, ways, recurse.cache_info().currsize


def bad_word_scalar_factorization(gadgets):
    colors = [0 if component // 3000 == 0 else 2 for component in range(6000)]
    adjacency = [[] for _ in range(24000)]

    def add(u, v, weight):
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))

    for component, color in enumerate(colors):
        for x, y in itertools.combinations(range(4), 2):
            if x ^ y == color + 1:
                add(4 * component + x, 4 * component + y, ONE)
    active_gadgets = 0
    for (u, v), (_resource, color_u, color_v, A, B) in gadgets.items():
        if colors[u] != color_u or colors[v] != color_v:
            continue
        add(4 * u, 4 * v, A)
        add(4 * u + color_u + 1, 4 * v + color_v + 1, B)
        active_gadgets += 1
    assert active_gadgets == 12600

    pending = set(range(24000))
    size_histogram = Counter()
    value_histogram = Counter()
    way_histogram = Counter()
    cache_histogram = Counter()
    full_value, full_ways = ONE, 1
    while pending:
        part = {next(iter(pending))}
        queue = deque(part)
        while queue:
            for neighbor, _weight in adjacency[queue.popleft()]:
                if neighbor not in part:
                    part.add(neighbor)
                    queue.append(neighbor)
        pending.difference_update(part)
        size_histogram[len(part)] += 1
        value, ways, cache_states = hafnian(tuple(sorted(part)), adjacency)
        value_histogram[value.text()] += 1
        way_histogram[str(ways)] += 1
        cache_histogram[cache_states] += 1
        full_value *= value
        full_ways *= ways

    block = Q3(Fraction(-463, 2592))
    assert size_histogram == Counter({2: 6000, 20: 600})
    assert value_histogram == Counter({"1": 6000, block.text(): 600})
    assert way_histogram == Counter({"1": 6000, "6130": 600})
    expected = ONE
    for _ in range(600):
        expected *= block
    assert full_value == expected
    assert full_ways == 6130 ** 600
    return {
        "assignment": "clone 0 -> color 0; clone 1 -> color 2",
        "active_gadgets": active_gadgets,
        "scalar_component_sizes": dict(size_histogram),
        "scalar_component_values": dict(value_histogram),
        "scalar_component_matching_counts": dict(way_histogram),
        "twenty_vertex_haf_cache_states": {
            str(key): count for key, count in cache_histogram.items() if key != 2
        },
        "block_source": block.text(),
        "global_source": "(-463/2592)^600",
        "global_source_nonzero": bool(full_value),
        "global_matching_count": str(full_ways),
        "target": "0",
    }


def build_result():
    m, n, tensor_a, tensor_b, _tensor_q, support_counts, strict_checks = (
        construct_tensor_data()
    )
    states, local, local_pair_counts = local_edges(tensor_a, tensor_b)
    group_index, resources, _membership, girth = incidence_data()
    gadgets, _adjacency, triangle_count = instantiate_cover(
        states, local, resources, group_index
    )
    binary_components = binary_state_components(gadgets)
    failure = bad_word_scalar_factorization(gadgets)
    result = {
        "schema": "binary-resource-tensor-cover-independent-audit-v1",
        "field": "Q(sqrt(3)) subset C",
        "base_M_support": sum(bool(x) for row in m for x in row),
        "base_N_same_support": all(bool(x) == bool(y) for row_m, row_n in zip(m, n)
                                    for x, y in zip(row_m, row_n)),
        "tensor_support_counts": support_counts,
        "strict_triple_scalar_entries_checked": strict_checks,
        "local_states": len(states),
        "local_edges": len(local),
        "local_edges_by_color_pair": {f"{a}{b}": count
                                      for (a, b), count in local_pair_counts.items()},
        "cover": {
            "resources": 120,
            "components": 6000,
            "physical_vertices": 24000,
            "old_incidence_girth": girth,
            "gadgets": len(gadgets),
            "component_triangles_checked": triangle_count,
            "all_component_triangles_coherent": True,
            "simple_one_label_component_graph": True,
        },
        "binary_state_components": binary_components,
        "explicit_full_component_failure": failure,
        "scope": "exact candidate countercontrol to BS; not a CSQ4 or global witness",
        "global_status_changed": False,
    }
    result["status"] = "PASS"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        print(json.dumps({"status": "PASS", "output": args.output.as_posix()}))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
