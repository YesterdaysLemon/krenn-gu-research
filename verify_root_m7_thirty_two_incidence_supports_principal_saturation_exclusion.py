"""Verify exact principal saturation exclusions for all thirty pair supports."""

from __future__ import annotations

import json
from itertools import combinations, permutations, product

import sympy as sp

from verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction import (
    ROWS,
    coefficient,
    matching_count,
    support_edges,
    symbolic_data,
)

W = (0, 0, 0, 0, 1, 0, 2)
PRESSURE = (1, 1, 1, 2, 1, 0, 1)
PRESSURE_LAST = (1, 1, 1, 2, 2, 2, 0)


def enlarged_data(pair, index):
    alpha, beta, gamma, x, y, z, a, b, h = symbolic_data()
    new = sp.symbols(f"u_{index} v_{index}")
    for value, (row, column) in zip(new, pair):
        colour = W[column]
        if row < 5:
            h[column][row][colour] = value
        elif row == 5:
            a[column][colour] = value
        else:
            b[column][colour] = value
    return alpha, beta, gamma, x, y, z, a, b, h


def stabilizer_size() -> int:
    path = {(u, u + 1): 1 if u % 2 == 0 else 0 for u in range(6)}
    ports = {
        0: {0: {0, 1}, 1: {5, 6}, 2: {3}},
        1: {0: {0, 1}, 1: {6}, 2: {5}},
    }
    count = 0
    for reverse in (False, True):
        vertex = (lambda u: 6 - u) if reverse else (lambda u: u)
        for colours in permutations(range(3)):
            transformed_path = {}
            for (u, v), colour in path.items():
                edge = tuple(sorted((vertex(u), vertex(v))))
                transformed_path[edge] = colours[colour]
            if transformed_path != path:
                continue
            for swap in (False, True):
                transformed = {0: {c: set() for c in range(3)}, 1: {c: set() for c in range(3)}}
                for port in range(2):
                    for colour, vertices in ports[port].items():
                        target_port = 1 - port if swap else port
                        transformed[target_port][colours[colour]].update(vertex(u) for u in vertices)
                if transformed == ports:
                    count += 1
    return count


def verify() -> dict[str, object]:
    *_, base_a, base_b, base_h = symbolic_data()
    base_edges = support_edges(W, base_a, base_b, base_h)
    missing = sorted(set(product(ROWS, range(7))) - base_edges)
    pairs = [pair for pair in combinations(missing, 2) if matching_count(base_edges | set(pair)) > 2]
    assert len(pairs) == 30
    assert stabilizer_size() == 1

    classes = {"mixed_0000102": [], "mixed_1112101": [], "mixed_1112220": []}
    endpoint_legal = []
    records = []
    for index, pair in enumerate(pairs):
        *_, a, b, h = enlarged_data(pair, index)
        c0, c1, c2 = (coefficient((colour,) * 7, a, b, h) for colour in range(3))
        pure_product = sp.expand(c0 * c1 * c2)
        candidates = (
            ("mixed_0000102", coefficient(W, a, b, h)),
            ("mixed_1112101", coefficient(PRESSURE, a, b, h)),
            ("mixed_1112220", coefficient(PRESSURE_LAST, a, b, h)),
        )
        chosen = None
        for label, mixed in candidates:
            if mixed == 0:
                continue
            quotient = sp.cancel(pure_product / mixed)
            symbols = sorted(pure_product.free_symbols | mixed.free_symbols, key=str)
            if (
                sp.denom(quotient) == 1
                and quotient.is_polynomial(*symbols)
                and sp.expand(pure_product - mixed * quotient) == 0
            ):
                chosen = label
                break
        assert chosen is not None
        classes[chosen].append(index)

        legal = not any(row in (5, 6) and column in (2, 4, 6) for row, column in pair)
        endpoint_legal.append(legal)
        records.append({"index": index, "pair": [list(edge) for edge in pair], "certificate": chosen, "endpoint_legal": legal})

    assert [len(classes[key]) for key in classes] == [15, 14, 1]
    assert sum(endpoint_legal) == 18
    assert classes["mixed_1112220"] == [25]
    return {
        "stabilizer_size": 1,
        "orbit_count": 30,
        "support_count": 30,
        "certificate_counts": {key: len(value) for key, value in classes.items()},
        "endpoint_legal": sum(endpoint_legal),
        "endpoint_illegal": len(endpoint_legal) - sum(endpoint_legal),
        "all_saturations_unit_ideal": True,
        "records": records,
    }


def main() -> None:
    print(json.dumps({
        "status": "pass",
        "field": "exact characteristic zero",
        "result": verify(),
        "survivor_supports": 0,
        "larger_support_shells_resolved": False,
        "finite_field_proof_used": False,
        "global_conjecture_resolved": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
