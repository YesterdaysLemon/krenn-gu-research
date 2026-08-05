"""Verify the endpoint-legal minimum-two certificate hitting theorem."""

from __future__ import annotations

import json
from itertools import combinations, permutations, product

import sympy as sp

from verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction import (
    coefficient,
    symbolic_data,
)

WORDS = tuple(tuple(map(int, word)) for word in ("0000102", "1112101", "1112220", "0101010", "1010220"))
SURVIVOR_CERTIFICATE = tuple(map(int, "0101122"))


def original_data():
    alpha, beta, gamma, x, y, z, a, b, h = symbolic_data()
    a[1][0] = sp.Integer(0)
    return alpha, beta, gamma, x, y, z, a, b, h


def legal_universe(a, b, h):
    universe = []
    for row, u, colour in product(range(5), range(7), range(3)):
        if h[u][row][colour] == 0:
            universe.append((row, u, colour))
    for row, ports in ((5, a), (6, b)):
        for u, colour in product((1, 3, 5), range(3)):
            if ports[u][colour] == 0:
                universe.append((row, u, colour))
    return tuple(universe)


def add_support(base, support):
    alpha, beta, _gamma, _x, _y, _z, a0, b0, h0 = base
    a, b, h = [row[:] for row in a0], [row[:] for row in b0], [[row[:] for row in block] for block in h0]
    variables = sp.symbols(f"t_0:{len(support)}")
    for value, (row, u, colour) in zip(variables, support):
        if row < 5:
            h[u][row][colour] = value
        elif row == 5:
            a[u][colour] = value
        else:
            b[u][colour] = value
    return alpha, beta, variables, a, b, h


def persistent_labels(base, support):
    alpha, beta, variables, a, b, h = add_support(base, support)
    endpoint = {alpha[0]: 1, alpha[3]: 1, beta[0]: 1, beta[3]: -1}
    pure = [sp.expand(coefficient((c,) * 7, a, b, h).subs(endpoint)) for c in range(3)]
    pure_product = sp.expand(sp.prod(pure))
    symbols = sorted(pure_product.free_symbols | set(variables), key=str)
    answer = []
    for label, word in zip(("0000102", "1112101", "1112220", "0101010", "1010220"), WORDS):
        mixed = sp.expand(coefficient(word, a, b, h).subs(endpoint))
        if mixed != 0 and sp.cancel(pure_product / mixed).is_polynomial(*symbols):
            answer.append(label)
    return tuple(answer)


def stabilizer_size():
    edges = {(u, u + 1): 1 if u % 2 == 0 else 0 for u in range(6)}
    ports = {0: {0: {0}, 1: {5, 6}, 2: {3}}, 1: {0: {0, 1}, 1: {6}, 2: {5}}}
    count = 0
    for reverse, colours, swap in product((False, True), permutations(range(3)), (False, True)):
        phi = (lambda u: 6 - u) if reverse else (lambda u: u)
        changed_edges = {tuple(sorted((phi(u), phi(v)))): colours[c] for (u, v), c in edges.items()}
        changed_ports = {0: {c: set() for c in range(3)}, 1: {c: set() for c in range(3)}}
        for port in range(2):
            for colour, vertices in ports[port].items():
                changed_ports[1 - port if swap else port][colours[colour]].update(phi(u) for u in vertices)
        count += changed_edges == edges and changed_ports == ports
    return count


def verify() -> dict[str, object]:
    base = original_data()
    universe = legal_universe(base[6], base[7], base[8])
    assert len(universe) == 104 and stabilizer_size() == 1
    singleton_survivors = [support for support in universe if not persistent_labels(base, (support,))]
    assert singleton_survivors == []
    pair_survivors = [support for support in combinations(universe, 2) if not persistent_labels(base, support)]
    expected = ((3, 6, 0), (4, 5, 0))
    assert pair_survivors == [expected]

    alpha, beta, variables, a, b, h = add_support(base, expected)
    p, q = variables
    c0, c1, c2 = (sp.factor(coefficient((c,) * 7, a, b, h)) for c in range(3))
    x, y, z = base[3], base[4], base[5]
    assert sp.expand(c0 - alpha[0] * beta[1] * x[0] * x[1] * x[2] * (x[3] * x[4] + p * q)) == 0
    mixed = sp.factor(coefficient(SURVIVOR_CERTIFICATE, a, b, h))
    expected_mixed = alpha[0] * beta[2] * x[0] * y[1] * y[3] * y[4] * z[2]
    assert mixed == expected_mixed
    pure_product = sp.expand(c0 * c1 * c2)
    quotient = sp.cancel(pure_product / mixed)
    assert quotient.is_polynomial(*sorted(pure_product.free_symbols, key=str))
    assert sp.expand(pure_product - mixed * quotient) == 0

    return {
        "legal_universe_size": len(universe),
        "singleton_supports_checked": len(universe),
        "singleton_transversals": 0,
        "pair_supports_checked": len(universe) * (len(universe) - 1) // 2,
        "pair_transversals": 1,
        "minimum_relative_hitting_size": 2,
        "unique_pair": [list(edge) for edge in expected],
        "stabilizer_size": 1,
        "orbit_count": 1,
        "full_ideal_certificate": "0101122",
        "full_ideal_saturation_is_unit": True,
    }


def main() -> None:
    print(json.dumps({
        "status": "pass", "field": "exact characteristic zero", "result": verify(),
        "relative_survivors": 1, "full_ideal_survivors": 0,
        "finite_field_proof_used": False, "global_conjecture_resolved": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
