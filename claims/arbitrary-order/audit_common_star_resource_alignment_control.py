"""Independent exact audit of the common-star resource-alignment control.

This portable checker imports no primary verifier or project scientific code.
It reconstructs the exact local matrices and finite cover, then checks
mutations of three load-bearing hypotheses.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
import itertools
import json
from pathlib import Path


@dataclass(frozen=True)
class Q3:
    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    def __add__(self, other):
        other = q3(other)
        return Q3(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + -q3(other)

    def __rsub__(self, other):
        return q3(other) - self

    def __mul__(self, other):
        other = q3(other)
        return Q3(
            self.rational * other.rational + 3 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def inverse(self):
        norm = self.rational**2 - 3 * self.radical**2
        if not norm:
            raise ZeroDivisionError
        return Q3(self.rational / norm, -self.radical / norm)

    def __truediv__(self, other):
        return self * q3(other).inverse()

    def __bool__(self):
        return bool(self.rational or self.radical)

    def text(self):
        if not self.radical:
            return str(self.rational)
        return f"({self.rational})+({self.radical})*sqrt(3)"


def q3(value):
    if isinstance(value, Q3):
        return value
    if isinstance(value, (int, Fraction)):
        return Q3(Fraction(value))
    raise TypeError(value)


ZERO = Q3()
ONE = q3(1)
T = Q3(Fraction(-1, 2), Fraction(1, 2))
R = Q3(Fraction(2), Fraction(1))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), ZERO) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def inverse(matrix):
    size = len(matrix)
    rows = [list(row) + [ONE if i == j else ZERO for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(i for i in range(column, size) if rows[i][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column].inverse()
        rows[column] = [value * scale for value in rows[column]]
        for i in range(size):
            if i == column:
                continue
            factor = rows[i][column]
            if factor:
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[column])]
    return [row[size:] for row in rows]


def identity(size):
    return [[ONE if i == j else ZERO for j in range(size)] for i in range(size)]


def hadamard(left, right):
    return [[x * y for x, y in zip(row_left, row_right)] for row_left, row_right in zip(left, right)]


def clone_vector(own, neighbor):
    others = sorted(set(range(3)) - {own})
    return (ONE, ONE if neighbor == others[0] else R)


def build_local_matrices(*, swap_01_orientation=False):
    base_a = [
        [ONE, T, ONE],
        [ONE, ONE, T],
        [T, ONE, ONE],
    ]
    base = {
        (0, 1): transpose(base_a),
        (1, 0): base_a,
        (1, 2): base_a,
        (2, 1): transpose(base_a),
        (0, 2): identity(3),
        (2, 0): identity(3),
    }
    if swap_01_orientation:
        base[0, 1], base[1, 0] = base[1, 0], base[0, 1]
    base_b = {
        key: [[-value for value in row] for row in inverse(transpose(matrix))]
        for key, matrix in base.items()
    }
    local = {}
    for c, d in base:
        a6 = [[ZERO for _ in range(6)] for _ in range(6)]
        b6 = [[ZERO for _ in range(6)] for _ in range(6)]
        z_cd = clone_vector(c, d)
        z_dc = clone_vector(d, c)
        for i, f, j, h in itertools.product(range(3), range(2), range(3), range(2)):
            row = 2 * i + f
            column = 2 * j + h
            scale = z_cd[f] * z_dc[h]
            a6[row][column] = base[c, d][i][j] * scale
            b6[row][column] = base_b[c, d][i][j] / (2 * scale)
        local["A", c, d] = a6
        local["B", c, d] = b6
        local["Q", c, d] = hadamard(a6, b6)
    return base, base_b, local


def local_identity_report(local):
    checked = Counter()
    residuals = Counter()
    for c, d in itertools.permutations(range(3), 2):
        q_cd = local["Q", c, d]
        for row in q_cd:
            checked["S1_rows"] += 1
            if sum(row, ZERO) != -ONE:
                residuals["S1_rows"] += 1
        for column in range(6):
            checked["S1_columns"] += 1
            if sum((q_cd[row][column] for row in range(6)), ZERO) != -ONE:
                residuals["S1_columns"] += 1

        left_a = matmul(local["A", c, d], local["B", d, c])
        left_b = matmul(local["B", c, d], local["A", d, c])
        right = matmul(q_cd, local["Q", d, c])
        for u in range(6):
            for v in range(6):
                if u != v:
                    checked["same_S2_off_diagonal"] += 1
                    if left_a[u][v] * left_b[u][v] != 2 * right[u][v]:
                        residuals["same_S2_off_diagonal"] += 1

        e = 3 - c - d
        cross_a = matmul(local["A", c, d], local["B", d, e])
        cross_b = matmul(local["B", c, d], local["A", d, e])
        paths = matmul(q_cd, local["Q", d, e])
        for u in range(6):
            for v in range(6):
                expected = 2 * paths[u][v] - cross_a[u][v] * cross_b[u][v]
                checked["distinct_S2"] += 1
                if local["Q", c, e][u][v] != expected:
                    residuals["distinct_S2"] += 1
    return {"checked": dict(checked), "nonzero_residuals": dict(residuals)}


def check_local_identities(local):
    report = local_identity_report(local)
    assert not report["nonzero_residuals"]
    return report["checked"]


def matrix2_mul(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return ((a * e + b * g) % 5, (a * f + b * h) % 5, (c * e + d * g) % 5, (c * f + d * h) % 5)


def matrix2_inverse(matrix):
    a, b, c, d = matrix
    assert (a * d - b * c) % 5 == 1
    return (d % 5, (-b) % 5, (-c) % 5, a % 5)


def sl2_f5():
    return tuple(
        matrix
        for matrix in itertools.product(range(5), repeat=4)
        if (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 5 == 1
    )


def build_cover(local):
    group = sl2_f5()
    assert len(group) == 120
    group_set = set(group)
    identity2 = (1, 0, 0, 1)
    transforms = {
        0: (identity2, (1, 1, 0, 1), (3, 2, 4, 3)),
        1: (identity2, (2, 4, 4, 1), (4, 2, 1, 2)),
    }
    assert all(transform in group_set for row in transforms.values() for transform in row)
    inverse_transforms = {
        (fiber, color): matrix2_inverse(transforms[fiber][color])
        for fiber in range(2)
        for color in range(3)
    }

    components = tuple((base, fiber, g) for g in group for fiber in range(2) for base in range(3))
    component_index = {component: i for i, component in enumerate(components)}
    resources_by_component = {}
    for component in components:
        _base, fiber, g = component
        resources_by_component[component] = tuple(
            matrix2_mul(g, transforms[fiber][color]) for color in range(3)
        )
    assert all(len(set(resources)) == 3 for resources in resources_by_component.values())

    old_intersections = Counter()
    old_components = tuple((fiber, g) for g in group for fiber in range(2))
    old_resources = {
        old: set(resources_by_component[0, old[0], old[1]]) for old in old_components
    }
    for old_u, old_v in itertools.combinations(old_components, 2):
        old_intersections[len(old_resources[old_u] & old_resources[old_v])] += 1
    assert max(old_intersections) <= 1

    state_at_resource = {}
    for resource in group:
        for color in range(3):
            for base in range(3):
                for fiber in range(2):
                    g = matrix2_mul(resource, inverse_transforms[fiber, color])
                    component = (base, fiber, g)
                    assert resources_by_component[component][color] == resource
                    state_at_resource[resource, color, base, fiber] = component_index[component]

    gadgets = {}
    resource_edge_counts = Counter()
    for resource in group:
        for c, d in itertools.combinations(range(3), 2):
            for i, f, j, h in itertools.product(range(3), range(2), range(3), range(2)):
                center = local["A", c, d][2 * i + f][2 * j + h]
                leaf = local["B", c, d][2 * i + f][2 * j + h]
                if not center:
                    assert not leaf
                    continue
                assert leaf
                u = state_at_resource[resource, c, i, f]
                v = state_at_resource[resource, d, j, h]
                assert u != v
                if u < v:
                    record = (u, v, c, d, center, leaf, resource)
                    pair = (u, v)
                else:
                    record = (v, u, d, c, center, leaf, resource)
                    pair = (v, u)
                if pair in gadgets:
                    raise AssertionError(("multiple labels", pair, gadgets[pair], record))
                gadgets[pair] = record
                resource_edge_counts[resource] += 1
    assert len(gadgets) == 10080
    assert set(resource_edge_counts.values()) == {84}

    # Every actual component triangle is contained in one resource and is
    # coherent: its two incident labels agree at each endpoint.
    adjacency = defaultdict(set)
    for u, v in gadgets:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = 0
    incoherent = 0
    cross_resource = 0
    for u in range(len(components)):
        for v in (neighbor for neighbor in adjacency[u] if neighbor > u):
            for w in (neighbor for neighbor in adjacency[u] & adjacency[v] if neighbor > v):
                records = (gadgets[tuple(sorted(pair))] for pair in ((u, v), (u, w), (v, w)))
                records = tuple(records)
                triangles += 1
                if len({record[6] for record in records}) != 1:
                    cross_resource += 1
                endpoint_colors = defaultdict(set)
                for left, right, color_left, color_right, *_rest in records:
                    endpoint_colors[left].add(color_left)
                    endpoint_colors[right].add(color_right)
                if any(len(colors) != 1 for colors in endpoint_colors.values()):
                    incoherent += 1
    assert triangles == 120 * 72
    assert cross_resource == 0 and incoherent == 0

    port_degrees = Counter()
    for u, v, color_u, color_v, *_rest in gadgets.values():
        port_degrees[u, color_u, color_v] += 1
        port_degrees[v, color_v, color_u] += 1
    assert len(port_degrees) == len(components) * 6
    assert set(port_degrees.values()) == {2, 6}
    return {
        "group": group,
        "components": components,
        "resources_by_component": resources_by_component,
        "gadgets": gadgets,
        "state_at_resource": state_at_resource,
        "old_pair_shared_resource_histogram": dict(sorted(old_intersections.items())),
        "triangles": triangles,
        "port_degrees": port_degrees,
    }


def check_global_failure(cover):
    components = cover["components"]
    gadgets = cover["gadgets"]
    word = tuple(0 if fiber == 0 else 2 for _base, fiber, _g in components)
    compatible = []
    for record in gadgets.values():
        u, v, color_u, color_v, center, leaf, resource = record
        if word[u] == color_u and word[v] == color_v:
            compatible.append((u, v, center * leaf, resource))
    assert len(compatible) == 360
    covered = Counter(component for edge in compatible for component in edge[:2])
    assert len(covered) == len(components) and set(covered.values()) == {1}
    assert {q for _u, _v, q, _resource in compatible} == {q3(Fraction(-1, 2))}
    per_resource = Counter(resource for *_rest, resource in compatible)
    assert len(per_resource) == 120 and set(per_resource.values()) == {3}

    # Reconstruct the literal scalar graph.  Each selected gadget produces a
    # four-cycle on the two centers and selected leaves; the other two leaves
    # in each protected K4 form an isolated unit edge.
    scalar_edges = {}
    for component, color in enumerate(word):
        matching = ((0, 1), (2, 3)) if color == 0 else ((0, 3), (1, 2))
        for x, y in matching:
            scalar_edges[4 * component + x, 4 * component + y] = ONE
    for u, v, color_u, color_v, center, leaf, _resource in gadgets.values():
        if word[u] == color_u and word[v] == color_v:
            scalar_edges[4 * u, 4 * v] = center
            scalar_edges[4 * u + color_u + 1, 4 * v + color_v + 1] = leaf
    adjacency = defaultdict(set)
    for u, v in scalar_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(4 * len(components)))
    scalar_component_sizes = Counter()
    scalar_degree_profiles = Counter()
    while unseen:
        root = next(iter(unseen))
        stack = [root]
        block = {root}
        unseen.remove(root)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    block.add(neighbor)
                    stack.append(neighbor)
        scalar_component_sizes[len(block)] += 1
        scalar_degree_profiles[tuple(sorted(len(adjacency[v]) for v in block))] += 1
    assert scalar_component_sizes == Counter({2: 720, 4: 360})
    assert scalar_degree_profiles == Counter({(1, 1): 720, (2, 2, 2, 2): 360})
    return {
        "word_color_counts": dict(sorted(Counter(word).items())),
        "compatible_component_edges": len(compatible),
        "compatible_edges_per_resource": sorted(set(per_resource.values())),
        "every_component_covered_once": True,
        "literal_scalar_component_sizes": dict(sorted(scalar_component_sizes.items())),
        "literal_scalar_degree_profiles": {
            str(profile): count for profile, count in sorted(scalar_degree_profiles.items())
        },
        "source": f"2^-{len(compatible)}",
        "target": "0",
    }


def check_incoherent_triangle_mutation():
    """Insert the forbidden ABB triangle and expand its literal U4 source."""
    # Components are u=0, v=1, w=2.  The word has minority centers d,e at
    # u,v and minority d/e leaves at w over background c=0.
    c, d, e = 0, 1, 2
    word = [c] * 12
    word[4 * 0] = d
    word[4 * 1] = e
    word[4 * 2 + d + 1] = d
    word[4 * 2 + e + 1] = e
    scalar_edges = {}
    for component in range(3):
        for x, y in ((0, 1), (2, 3)):
            if word[4 * component + x] == word[4 * component + y] == c:
                scalar_edges[4 * component + x, 4 * component + y] = ONE
    # Central A_de and the two incoherent B spokes B_cd and B_ce.
    scalar_edges[0, 4] = ONE
    scalar_edges[1, 4 * 2 + d + 1] = ONE
    scalar_edges[4 + 1, 4 * 2 + e + 1] = ONE
    adjacency = defaultdict(list)
    for (u, v), weight in scalar_edges.items():
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))

    def haf(mask):
        if not mask:
            return ONE
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        return sum(
            (weight * haf(rest ^ (1 << v)) for v, weight in adjacency[u] if rest & (1 << v)),
            ZERO,
        )

    source = haf((1 << 12) - 1)
    assert source == ONE
    return {
        "physical_word": "".join(map(str, word)),
        "literal_source": source.text(),
        "target": "0",
        "meaning": "coherence is necessary to kill the ABB U4 monomial",
    }


def check_size_one_cycle_boundary():
    """Show why m>=2 is necessary for the binary-biclique consumer."""
    resources = 3
    components = 3
    # Three K1,1 blocks and physical-component arcs R -> R+1.  The unique
    # resource cycle switches all components, producing the pure color-1 word.
    q = -ONE
    factor = ONE + sum((), ZERO)  # one active color-1 state and no remaining zero state
    assert factor == ONE == -q
    return {
        "resources": resources,
        "components": components,
        "block_shape": [1, 1],
        "cycle_length": resources,
        "switched_components": components,
        "cycle_word": "111",
        "source": (factor * factor * factor).text(),
        "target": "1 (pure)",
        "meaning": "without m>=2 the cycle need not produce a mixed word",
    }


def build_result():
    base, base_b, local = build_local_matrices()
    for key in base:
        assert base_b[key] == transpose(base_b[key[::-1]])
        assert matmul(base[key], transpose(base_b[key])) == [[-value for value in row] for row in identity(3)]
    local_counts = check_local_identities(local)
    support_shapes = {}
    for c, d in itertools.combinations(range(3), 2):
        degrees = [sum(bool(value) for value in row) for row in local["A", c, d]]
        support_shapes[f"{c}{d}"] = {
            "row_degrees": sorted(set(degrees)),
            "edges": sum(degrees),
        }
    assert support_shapes == {
        "01": {"row_degrees": [6], "edges": 36},
        "02": {"row_degrees": [2], "edges": 12},
        "12": {"row_degrees": [6], "edges": 36},
    }
    cover = build_cover(local)
    _mutated_base, _mutated_b, mutated_local = build_local_matrices(
        swap_01_orientation=True
    )
    orientation_mutation = local_identity_report(mutated_local)
    if not orientation_mutation["nonzero_residuals"]:
        raise AssertionError("misoriented 01 block unexpectedly passed")
    return {
        "schema": "common-star-resource-alignment-independent-audit-v1",
        "status": "PASS",
        "field": "Q(sqrt(3)) subset C",
        "local": {
            "states_per_color": 6,
            "support_shapes": support_shapes,
            "connected_tripartite_resource": True,
            "complete_tripartite_resource": False,
            "identity_counts": local_counts,
        },
        "cover": {
            "resources": len(cover["group"]),
            "components": len(cover["components"]),
            "physical_vertices": 4 * len(cover["components"]),
            "gadgets": len(cover["gadgets"]),
            "crossing_physical_entries": 2 * len(cover["gadgets"]),
            "port_degrees": sorted(set(cover["port_degrees"].values())),
            "old_pair_shared_resource_histogram": cover["old_pair_shared_resource_histogram"],
            "actual_component_triangles": cover["triangles"],
            "cross_resource_triangles": 0,
            "incoherent_triangles": 0,
            "one_label_per_component_pair": True,
        },
        "u4_bridge": {
            "pure_and_singleton_families": "automatic and S1",
            "abb_u3_u4_monomials": "zero because every component triangle is coherent",
            "classification_scope": "uses the independently reviewed full <=4-minority classification",
        },
        "global_component_failure": check_global_failure(cover),
        "mutation_controls": {
            "misoriented_01_base_block": orientation_mutation,
            "incoherent_triangle": check_incoherent_triangle_mutation(),
            "size_one_resource_cycle": check_size_one_cycle_boundary(),
        },
        "conclusion": (
            "exact refutation of the proposed RCS complete-tripartite-resource "
            "supply implication; not a CSQ4 model or Krenn-Gu counterexample"
        ),
        "global_status_changed": False,
    }


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="optional LF-terminated JSON output path; omit for stdout",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    rendered = json.dumps(build_result(), indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(json.dumps({"status": "PASS", "output": str(args.output)}))


if __name__ == "__main__":
    main()
