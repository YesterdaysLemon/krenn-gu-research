"""Independent exact controls for the protected common-star obstruction.

This portable audit imports no project scientific implementation.  Its first
route constructs all 4k physical vertices and recursively expands their scalar
hafnian.  Its second route enumerates the component-level double hafnian.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import itertools
import json
from pathlib import Path


def add_entry(entries, u, v, a, b, weight):
    if u > v:
        u, v, a, b = v, u, b, a
    entries[u, v, a, b] = entries.get((u, v, a, b), 0) + weight


def physical_entries(component_count, gadgets):
    entries = {}
    for component in range(component_count):
        for x in range(4):
            for y in range(x + 1, 4):
                difference = x ^ y
                if difference:
                    color = difference - 1
                    add_entry(
                        entries,
                        4 * component + x,
                        4 * component + y,
                        color,
                        color,
                        1,
                    )
    for u, v, a, b, A, B in gadgets:
        assert u < v and a != b and A and B
        add_entry(entries, 4 * u, 4 * v, a, b, A)
        add_entry(entries, 4 * u + a + 1, 4 * v + b + 1, a, b, B)
    return entries


def physical_coefficient(component_colors, gadgets):
    n = 4 * len(component_colors)
    word = tuple(c for c in component_colors for _ in range(4))
    entries = physical_entries(len(component_colors), gadgets)

    @lru_cache(maxsize=None)
    def recurse(mask):
        if not mask:
            return 1
        first_bit = mask & -mask
        u = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        result = 0
        choices = rest
        while choices:
            bit = choices & -choices
            choices ^= bit
            v = bit.bit_length() - 1
            weight = entries.get((u, v, word[u], word[v]), 0)
            if weight:
                result += weight * recurse(rest ^ bit)
        return result

    return recurse((1 << n) - 1)


def hafnian(vertices, edge_weights):
    vertices = tuple(vertices)

    @lru_cache(maxsize=None)
    def recurse(state):
        if not state:
            return 1
        u = state[0]
        total = 0
        for index in range(1, len(state)):
            v = state[index]
            weight = edge_weights.get(tuple(sorted((u, v))), 0)
            if weight:
                total += weight * recurse(state[1:index] + state[index + 1 :])
        return total

    return recurse(vertices)


def subset_formula(component_colors, gadgets):
    count = len(component_colors)
    A_edges = {}
    B_edges = {}
    for u, v, a, b, A, B in gadgets:
        if component_colors[u] == a and component_colors[v] == b:
            pair = (u, v)
            A_edges[pair] = A_edges.get(pair, 0) + A
            B_edges[pair] = B_edges.get(pair, 0) + B
    total = 0
    for size in range(0, count + 1, 2):
        for subset in itertools.combinations(range(count), size):
            total += hafnian(subset, A_edges) * hafnian(subset, B_edges)
    return total


def matching_polynomial(component_colors, gadgets):
    active = [g for g in gadgets if component_colors[g[0]] == g[2]
              and component_colors[g[1]] == g[3]]

    def recurse(index, used):
        if index == len(active):
            return 1
        u, v, _a, _b, A, B = active[index]
        total = recurse(index + 1, used)
        if u not in used and v not in used:
            total += A * B * recurse(index + 1, used | {u, v})
        return total

    return recurse(0, set())


def endpoint_ports(gadgets):
    ports = []
    for u, v, a, b, _A, _B in gadgets:
        ports.extend(((u, a, b), (v, b, a)))
    return ports


def main():
    # Forest control: all three path edges are active on the alternating word.
    forest = [
        (0, 1, 0, 1, 2, 3),
        (1, 2, 1, 0, 5, 7),
        (2, 3, 0, 1, 11, 13),
    ]
    forest_word = (0, 1, 0, 1)
    forest_values = {
        "physical": physical_coefficient(forest_word, forest),
        "subset_formula": subset_formula(forest_word, forest),
        "ordinary_matching_polynomial": matching_polynomial(forest_word, forest),
    }
    assert len(set(forest_values.values())) == 1

    # Even-cycle control: center and leaf perfect matchings can differ.
    cycle = [
        (0, 1, 0, 1, 1, 1),
        (1, 2, 1, 0, 1, 1),
        (2, 3, 0, 1, 1, 1),
        (0, 3, 0, 1, 1, 1),
    ]
    cycle_word = (0, 1, 0, 1)
    cycle_values = {
        "physical": physical_coefficient(cycle_word, cycle),
        "subset_formula": subset_formula(cycle_word, cycle),
        "ordinary_matching_polynomial": matching_polynomial(cycle_word, cycle),
    }
    assert cycle_values["physical"] == cycle_values["subset_formula"]
    assert cycle_values["physical"] != cycle_values["ordinary_matching_polynomial"]

    # Exhaust every component-constant word in both controls.  The physical
    # route recursively expands the scalar graph on all 4k physical vertices;
    # it shares no recurrence with the component-level subset formula.
    forest_all_words = []
    cycle_all_words = []
    for word in itertools.product(range(3), repeat=4):
        physical = physical_coefficient(word, forest)
        subset = subset_formula(word, forest)
        ordinary = matching_polynomial(word, forest)
        assert physical == subset == ordinary
        forest_all_words.append(word)

        physical = physical_coefficient(word, cycle)
        subset = subset_formula(word, cycle)
        ordinary = matching_polynomial(word, cycle)
        assert physical == subset
        cycle_all_words.append((word, physical != ordinary))

    # Dropping triangle-freeness: one common neighbour removes the product
    # q_uw*q_vw counted by the disjoint-star factorization.
    triangle = [
        (0, 1, 0, 1, 1, 1),
        (0, 2, 0, 2, 1, -1),
        (1, 2, 1, 2, 1, -1),
    ]
    triangle_words = {
        "u_singleton": (0, 2, 2),
        "v_singleton": (2, 1, 2),
        "both_changed": (0, 1, 2),
    }
    triangle_values = {
        name: physical_coefficient(word, triangle)
        for name, word in triangle_words.items()
    }
    assert triangle_values == {
        "u_singleton": 0,
        "v_singleton": 0,
        "both_changed": 0,
    }
    triangle_claimed_disjoint_star_residual = 1
    triangle_all_words = []
    for word in itertools.product(range(3), repeat=3):
        physical = physical_coefficient(word, triangle)
        subset = subset_formula(word, triangle)
        assert physical == subset
        triangle_all_words.append(word)

    # Dropping one-label-per-component-edge: all six unequal labels on the
    # unique k=2 component pair, each with A*B=-1, satisfy every one of the
    # nine component-constant GHZ targets exactly.
    multilabel = [
        (0, 1, a, b, 1, -1)
        for a in range(3)
        for b in range(3)
        if a != b
    ]
    multilabel_values = {
        "".join(map(str, word)): physical_coefficient(word, multilabel)
        for word in itertools.product(range(3), repeat=2)
    }
    multilabel_targets = {
        "".join(map(str, word)): int(word[0] == word[1])
        for word in itertools.product(range(3), repeat=2)
    }
    assert multilabel_values == multilabel_targets

    # Saturated-port local control.  These are the exact three compatible
    # edges forced around a selected uv row once the three relevant ports are
    # unique.  The displayed configurations are local controls rather than
    # claims that the omitted ports satisfy every component target.
    port_path = [
        (0, 1, 0, 1, 1, -1),
        (0, 2, 0, 2, 1, -1),
        (1, 3, 1, 2, 1, -1),
    ]
    port_path_words = {
        "selected_edge_singleton": (0, 1, 1, 1),
        "u_spoke_singleton": (0, 2, 2, 2),
        "v_spoke_singleton": (2, 1, 2, 2),
        "both_changed": (0, 1, 2, 2),
    }
    assert len(endpoint_ports(port_path)) == len(set(endpoint_ports(port_path)))
    port_path_values = {
        name: physical_coefficient(word, port_path)
        for name, word in port_path_words.items()
    }
    assert port_path_values == {
        "selected_edge_singleton": 0,
        "u_spoke_singleton": 0,
        "v_spoke_singleton": 0,
        "both_changed": -1,
    }
    assert all(
        physical_coefficient(word, port_path) == subset_formula(word, port_path)
        for word in port_path_words.values()
    )

    port_triangle = [
        (0, 1, 0, 1, 1, -1),
        (0, 2, 0, 2, 1, -1),
        (1, 2, 1, 2, 1, -1),
    ]
    port_triangle_words = {
        "selected_edge_singleton": (0, 1, 1),
        "u_spoke_singleton": (0, 2, 2),
        "v_spoke_singleton": (2, 1, 2),
        "both_changed": (0, 1, 2),
    }
    assert len(endpoint_ports(port_triangle)) == len(
        set(endpoint_ports(port_triangle))
    )
    port_triangle_values = {
        name: physical_coefficient(word, port_triangle)
        for name, word in port_triangle_words.items()
    }
    assert port_triangle_values == {
        "selected_edge_singleton": 0,
        "u_spoke_singleton": 0,
        "v_spoke_singleton": 0,
        "both_changed": -2,
    }
    assert all(
        physical_coefficient(word, port_triangle)
        == subset_formula(word, port_triangle)
        for word in port_triangle_words.values()
    )

    result = {
        "schema": "protected-common-star-independent-controls-v1",
        "arithmetic": "exact integers",
        "forest_control": {
            "component_colors": forest_word,
            "values": forest_values,
            "all_equal": True,
            "all_component_words_checked": len(forest_all_words),
            "all_physical_subset_and_ordinary_equal": True,
        },
        "even_cycle_control": {
            "component_colors": cycle_word,
            "values": cycle_values,
            "physical_equals_subset_formula": True,
            "physical_differs_from_ordinary_matching_polynomial": True,
            "all_component_words_checked": len(cycle_all_words),
            "physical_subset_mismatches": 0,
            "ordinary_matching_polynomial_mismatches": sum(
                differs for _word, differs in cycle_all_words
            ),
        },
        "triangle_hypothesis_control": {
            "component_colors": triangle_words,
            "actual_sources": triangle_values,
            "claimed_disjoint_star_residual_if_triangle_freeness_were_omitted":
                triangle_claimed_disjoint_star_residual,
            "all_three_relevant_mixed_targets_hold": True,
            "all_component_constant_targets_claimed": False,
            "all_component_words_checked": len(triangle_all_words),
            "physical_subset_mismatches": 0,
        },
        "one_label_hypothesis_control": {
            "components": 2,
            "labels_on_the_single_component_pair": 6,
            "actual_sources": multilabel_values,
            "targets": multilabel_targets,
            "all_nine_component_constant_targets_hold": True,
        },
        "unique_endpoint_port_extension_control": {
            "definition": "port=(component,own_color,neighbor_color)",
            "distinct_spoke_endpoints": {
                "component_colors": port_path_words,
                "actual_sources": port_path_values,
                "endpoint_ports_unique": True,
                "both_changed_expected_failure": -1,
            },
            "shared_spoke_endpoint": {
                "component_colors": port_triangle_words,
                "actual_sources": port_triangle_values,
                "endpoint_ports_unique": True,
                "both_changed_expected_failure": -2,
            },
            "physical_subset_mismatches": 0,
            "scope": "local three-port controls; not full target models",
        },
        "global_status_changed": False,
    }
    return result


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
    result = main()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
        print(json.dumps({"status": "PASS", "output": str(args.output)}))


if __name__ == "__main__":
    cli()
