"""Exact repeated-port controls for the protected common-star Q4 parent.

The construction uses 14 protected K4 components indexed by Z/7 x {0,1}.
All arithmetic is performed in Q(sqrt(3)).  Component-constant amplitudes are
computed both by a scalar hafnian on all 56 physical vertices and by an
independent component-level double-hafnian expansion.

This is a sharp control, not a Q4 witness: it passes every constant,
singleton, and double-component target row, but has an explicit nonzero U4
source and an explicit nonconstant component-word source.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import itertools
import json
from pathlib import Path


@dataclass(frozen=True)
class Q3:
    """An exact element ``rational + radical * sqrt(3)``."""

    rational: Fraction = Fraction(0)
    radical: Fraction = Fraction(0)

    def __add__(self, other):
        other = q3(other)
        return Q3(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + (-q3(other))

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
        norm = self.rational * self.rational - 3 * self.radical * self.radical
        if not norm:
            raise ZeroDivisionError
        return Q3(self.rational / norm, -self.radical / norm)

    def __truediv__(self, other):
        return self * q3(other).inverse()

    def __eq__(self, other):
        try:
            other = q3(other)
        except TypeError:
            return NotImplemented
        return (self.rational, self.radical) == (other.rational, other.radical)

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
ONE = Q3(Fraction(1))
R = Q3(Fraction(2), Fraction(1))
MINUS_HALF = Q3(Fraction(-1, 2))
COLOR_POSITIONS = (0, 1, 3)
STEP_TO_LABEL = {
    (COLOR_POSITIONS[b] - COLOR_POSITIONS[a]) % 7: (a, b)
    for a in range(3)
    for b in range(3)
    if a != b
}
assert len(STEP_TO_LABEL) == 6


def port_vector(own, neighbor):
    others = sorted(set(range(3)) - {own})
    return (ONE, ONE if neighbor == others[0] else R)


COMPONENTS = tuple((part, fiber) for part in range(7) for fiber in range(2))
BLOCK_STATES = tuple((color, fiber) for color in range(3) for fiber in range(2))


def construction_edges():
    edges = []
    for u, (part_u, fiber_u) in enumerate(COMPONENTS):
        for v in range(u + 1, len(COMPONENTS)):
            part_v, fiber_v = COMPONENTS[v]
            if part_u == part_v:
                continue
            a, b = STEP_TO_LABEL[(part_v - part_u) % 7]
            center = port_vector(a, b)[fiber_u] * port_vector(b, a)[fiber_v]
            leaf = MINUS_HALF / center
            edges.append((u, v, a, b, center, leaf))
    return tuple(edges)


EDGES = construction_edges()


def matching_layers(edge_weights):
    """Enumerate matchings, keyed by their covered component set."""
    items = tuple(edge_weights.items())
    layers = defaultdict(lambda: ZERO)

    def recurse(index, used, product):
        if index == len(items):
            layers[used] = layers[used] + product
            return
        recurse(index + 1, used, product)
        (u, v), weight = items[index]
        bits = (1 << u) | (1 << v)
        if not used & bits:
            recurse(index + 1, used | bits, product * weight)

    recurse(0, 0, ONE)
    return layers


def component_source(component_word, edges=EDGES):
    """Independent double-hafnian expansion for a component-color word."""
    center = {}
    leaf = {}
    for u, v, a, b, A, B in edges:
        if component_word[u] == a and component_word[v] == b:
            center[u, v] = center.get((u, v), ZERO) + A
            leaf[u, v] = leaf.get((u, v), ZERO) + B
    center_layers = matching_layers(center)
    leaf_layers = matching_layers(leaf)
    return sum(
        (value * leaf_layers[mask] for mask, value in center_layers.items()), ZERO
    )


def physical_source_stats(physical_word, edges=EDGES):
    """Return the scalar hafnian and number of nonzero perfect-match terms."""
    assert len(physical_word) == 4 * len(COMPONENTS)
    entries = {}
    for component in range(len(COMPONENTS)):
        for x in range(4):
            for y in range(x + 1, 4):
                color = (x ^ y) - 1
                u, v = 4 * component + x, 4 * component + y
                if physical_word[u] == physical_word[v] == color:
                    entries[u, v] = ONE
    for u, v, a, b, A, B in edges:
        center_u, center_v = 4 * u, 4 * v
        if physical_word[center_u] == a and physical_word[center_v] == b:
            entries[center_u, center_v] = A
        leaf_u, leaf_v = 4 * u + a + 1, 4 * v + b + 1
        if physical_word[leaf_u] == a and physical_word[leaf_v] == b:
            entries[leaf_u, leaf_v] = B

    neighbors = [[] for _ in physical_word]
    for (u, v), value in entries.items():
        neighbors[u].append((v, value))
        neighbors[v].append((u, value))

    @lru_cache(maxsize=None)
    def recurse(mask):
        if not mask:
            return ONE, 1
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        total = ZERO
        term_count = 0
        for v, value in neighbors[u]:
            if rest & (1 << v):
                subtotal, subcount = recurse(rest ^ (1 << v))
                total += value * subtotal
                term_count += subcount
        return total, term_count

    return recurse((1 << len(physical_word)) - 1)


def physical_source(physical_word, edges=EDGES):
    """Recursively expand the scalar hafnian on the actual physical graph."""
    return physical_source_stats(physical_word, edges)[0]


def expanded_component_word(component_word):
    return tuple(color for color in component_word for _ in range(4))


def physical_component_source(component_word, edges=EDGES):
    return physical_source(expanded_component_word(component_word), edges)


def label_at(edge, endpoint):
    u, v, a, b, _A, _B = edge
    if endpoint == u:
        return a, b
    if endpoint == v:
        return b, a
    raise ValueError(endpoint)


def target_rows():
    """Yield every constant, singleton, and double-component target row."""
    for c in range(3):
        yield "constant", (c,) * len(COMPONENTS), ONE
        alternatives = tuple(color for color in range(3) if color != c)
        for u in range(len(COMPONENTS)):
            for a in alternatives:
                word = [c] * len(COMPONENTS)
                word[u] = a
                yield "singleton", tuple(word), ZERO
        for u, v in itertools.combinations(range(len(COMPONENTS)), 2):
            for a, b in itertools.product(alternatives, repeat=2):
                word = [c] * len(COMPONENTS)
                word[u], word[v] = a, b
                yield "double", tuple(word), ZERO


def check_target_layers(edges=EDGES, stop_after=None):
    counts = Counter()
    mismatches = []
    for layer, word, target in target_rows():
        component = component_source(word, edges)
        physical = physical_component_source(word, edges)
        counts[layer] += 1
        if component != target or physical != target or component != physical:
            mismatches.append(
                {
                    "layer": layer,
                    "word": "".join(map(str, word)),
                    "target": target.text(),
                    "component_source": component.text(),
                    "physical_source": physical.text(),
                }
            )
            if stop_after is not None and len(mismatches) >= stop_after:
                break
    return {"counts": dict(counts), "mismatches": mismatches}


def local_k222_source(mask):
    """Double-hafnian source for one coherent six-state K2,2,2 resource."""
    center = {}
    leaf = {}
    for u, (a, fiber_u) in enumerate(BLOCK_STATES):
        if not mask & (1 << u):
            continue
        for v in range(u + 1, len(BLOCK_STATES)):
            if not mask & (1 << v):
                continue
            b, fiber_v = BLOCK_STATES[v]
            if a == b:
                continue
            A = port_vector(a, b)[fiber_u] * port_vector(b, a)[fiber_v]
            B = MINUS_HALF / A
            center[u, v] = A
            leaf[u, v] = B
    center_layers = matching_layers(center)
    leaf_layers = matching_layers(leaf)
    return sum(
        (value * leaf_layers[state] for state, value in center_layers.items()), ZERO
    )


LOCAL_VALUES_BY_COUNTS = {
    (0, 0, 0): ONE,
    (1, 0, 0): ONE,
    (2, 0, 0): ONE,
    (1, 1, 0): Q3(Fraction(1, 2)),
    (2, 1, 0): ZERO,
    (2, 2, 0): ZERO,
    (1, 1, 1): MINUS_HALF,
    (2, 1, 1): ZERO,
    (2, 2, 1): q3(4),
    (2, 2, 2): q3(-11),
}


def local_k222_table():
    table = []
    histogram = Counter()
    for mask in range(1 << len(BLOCK_STATES)):
        counts = tuple(
            sum(bool(mask & (1 << (2 * color + fiber))) for fiber in range(2))
            for color in range(3)
        )
        canonical_counts = tuple(sorted(counts, reverse=True))
        value = local_k222_source(mask)
        if value != LOCAL_VALUES_BY_COUNTS[canonical_counts]:
            raise AssertionError((mask, counts, value))
        histogram[value.text()] += 1
        table.append(
            {
                "mask": mask,
                "selected_states": [
                    f"{color}{fiber}"
                    for index, (color, fiber) in enumerate(BLOCK_STATES)
                    if mask & (1 << index)
                ],
                "color_counts": counts,
                "source": value.text(),
            }
        )
    expected_histogram = Counter(
        {"0": 27, "1/2": 12, "1": 10, "-1/2": 8, "4": 6, "-11": 1}
    )
    if histogram != expected_histogram:
        raise AssertionError(histogram)
    return table, histogram


def binary_fiber_failure(edges=EDGES):
    word = tuple(fiber for _part in range(7) for fiber in range(2))
    component = component_source(word, edges)
    physical = physical_component_source(word, edges)
    expected = Q3(Fraction(1, 128))
    if component != expected or physical != expected:
        raise AssertionError((component, physical))
    return {
        "component_word": "".join(map(str, word)),
        "component_source": component.text(),
        "physical_source": physical.text(),
        "target": "0",
    }


def find_u4_failure(edges=EDGES):
    c, d, e = 0, 1, 2
    w = 0
    u = 8
    v = 12
    physical_word = [c] * (4 * len(COMPONENTS))
    physical_word[4 * w + d + 1] = d
    physical_word[4 * w + e + 1] = e
    physical_word[4 * u] = d
    physical_word[4 * v] = e
    source, matching_terms = physical_source_stats(tuple(physical_word), edges)

    by_pair = {(edge[0], edge[1]): edge for edge in edges}
    central = by_pair[tuple(sorted((u, v)))]
    wu = by_pair[tuple(sorted((w, u)))]
    wv = by_pair[tuple(sorted((w, v)))]
    if label_at(central, u) != (d, e):
        raise AssertionError("unexpected central label")
    if label_at(wu, w) != (e, c) or label_at(wv, w) != (d, c):
        raise AssertionError("unexpected spoke label")
    expected = central[4] * wu[5] * wv[5]
    if source != expected or source != Q3(Fraction(1, 4)) or matching_terms != 1:
        raise AssertionError((source, expected, matching_terms))
    return {
        "base_color": c,
        "changed_leaf_component": w,
        "changed_center_components": [u, v],
        "physical_word": "".join(map(str, physical_word)),
        "source": source.text(),
        "target": "0",
        "nonzero_perfect_matching_terms": matching_terms,
        "unique_matching_product": expected.text(),
    }


def scan_abb_u3_family(edges=EDGES):
    checked = 0
    nonzero = 0
    first = None
    for c in range(3):
        alternatives = tuple(color for color in range(3) if color != c)
        d, e = alternatives
        for w in range(len(COMPONENTS)):
            for v in range(len(COMPONENTS)):
                if v == w:
                    continue
                for center_color in alternatives:
                    word = [c] * (4 * len(COMPONENTS))
                    word[4 * w + d + 1] = d
                    word[4 * w + e + 1] = e
                    word[4 * v] = center_color
                    value = physical_source(tuple(word), edges)
                    checked += 1
                    if value:
                        nonzero += 1
                        if first is None:
                            first = {
                                "base_color": c,
                                "two_leaf_component": w,
                                "center_component": v,
                                "center_color": center_color,
                                "physical_word": "".join(map(str, word)),
                                "source": value.text(),
                            }
    return {"checked": checked, "nonzero": nonzero, "first_nonzero": first}


def validate_construction():
    if len(EDGES) != 84:
        raise AssertionError(len(EDGES))
    degree = Counter()
    ports = Counter()
    for edge in EDGES:
        u, v, _a, _b, A, B = edge
        if not A or not B or A * B != MINUS_HALF:
            raise AssertionError(edge)
        degree.update((u, v))
        own, neighbor = label_at(edge, u)
        ports[u, own, neighbor] += 1
        own, neighbor = label_at(edge, v)
        ports[v, own, neighbor] += 1
    if set(degree.values()) != {12}:
        raise AssertionError(degree)
    if len(ports) != 14 * 6 or set(ports.values()) != {2}:
        raise AssertionError(ports)


def build_result():
    validate_construction()
    target_layers = check_target_layers()
    if target_layers["mismatches"]:
        raise AssertionError(target_layers["mismatches"][0])
    local_table, local_histogram = local_k222_table()
    abb_u3 = scan_abb_u3_family()
    if abb_u3["nonzero"]:
        raise AssertionError(abb_u3["first_nonzero"])
    return {
        "schema": "protected-common-star-repeated-port-control-v1",
        "field": "Q(sqrt(3)) subset C",
        "components": 14,
        "physical_vertices": 56,
        "component_graph": "complete seven-partite graph with parts of size two",
        "component_edges": len(EDGES),
        "degree": 12,
        "ordered_port_multiplicity": 2,
        "edge_product": "-1/2",
        "component_target_layers": {
            "counts": target_layers["counts"],
            "mismatches": 0,
            "physical_and_double_haf_routes_both_checked": True,
        },
        "abb_three_minority_family": abb_u3,
        "binary_fiber_full_component_failure": binary_fiber_failure(),
        "explicit_u4_failure": find_u4_failure(),
        "coherent_k222_local_partition": {
            "state_order": [f"{color}{fiber}" for color, fiber in BLOCK_STATES],
            "table": local_table,
            "value_histogram": dict(sorted(local_histogram.items())),
            "zero_masks": local_histogram["0"],
            "nonzero_masks": 64 - local_histogram["0"],
            "value_by_sorted_color_counts": {
                "000": "1",
                "100": "1",
                "200": "1",
                "110": "1/2",
                "210": "0",
                "220": "0",
                "111": "-1/2",
                "211": "0",
                "221": "4",
                "222": "-11",
            },
        },
        "scope": (
            "exact control against sufficiency of constant, singleton, and "
            "double-component targets; not a Q4 or full-target witness"
        ),
        "global_status_changed": False,
    }


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="optional JSON output path; omit to write the result to stdout",
    )
    return parser.parse_args()


def cli():
    args = parse_args()
    rendered = json.dumps(build_result(), indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
        print(json.dumps({"status": "PASS", "output": str(args.output)}))


if __name__ == "__main__":
    cli()
