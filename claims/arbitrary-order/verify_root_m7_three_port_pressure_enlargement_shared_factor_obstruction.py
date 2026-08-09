"""Verify the shared-factor obstruction for the three-port enlargement."""

from __future__ import annotations

import json
from itertools import combinations, product

import sympy as sp

from verify_root_m7_hall_satisfying_two_port_pure_p7_construction import (
    path_principal_signatures,
)
from verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction import (
    ROWS,
    coefficient,
    matching_count,
    support_edges,
    symbolic_data,
)

W = (0, 0, 0, 0, 1, 0, 2)


def data():
    alpha, beta, gamma, x, y, z, a, b, h = symbolic_data()
    delta, epsilon = sp.symbols("delta epsilon")
    b[5][1] = delta
    a[5][2] = epsilon
    return alpha, beta, gamma, delta, epsilon, x, y, z, a, b, h


def verify() -> dict[str, object]:
    alpha, beta, gamma, delta, epsilon, x, y, z, a, b, h = data()
    c0, c1, c2 = (coefficient((colour,) * 7, a, b, h) for colour in range(3))
    cw = coefficient(W, a, b, h)
    p0 = alpha[0] * beta[1] + beta[0] * gamma
    p1 = alpha[2] * beta[3] + alpha[3] * delta
    assert sp.expand(c0 - p0 * sp.prod(x)) == 0
    assert sp.expand(c1 - p1 * sp.prod(y)) == 0
    assert sp.expand(c2 - alpha[1] * beta[2] * sp.prod(z)) == 0
    assert epsilon not in c2.free_symbols
    root_mixed = x[0] * x[1] * x[3] * y[4] * z[2]
    assert sp.expand(cw - p0 * root_mixed) == 0

    pure_product = sp.expand(c0 * c1 * c2)
    quotient = x[2] * x[4] * p1 * sp.prod(y[:4])
    quotient *= alpha[1] * beta[2] * z[0] * z[1] * z[3] * z[4]
    assert sp.expand(pure_product - cw * quotient) == 0

    edges = support_edges(W, a, b, h)
    assert matching_count(edges) == 2
    base_alpha, base_beta, base_gamma, base_x, base_y, base_z, base_a, base_b, base_h = symbolic_data()
    del base_alpha, base_beta, base_gamma, base_x, base_y, base_z
    base_edges = support_edges(W, base_a, base_b, base_h)
    missing = sorted(set(product(ROWS, range(7))) - base_edges)
    previous_pairs = [pair for pair in combinations(missing, 2) if matching_count(base_edges | set(pair)) > 2]
    assert len(previous_pairs) == 30
    triple_new = {(6, 5, 1), (5, 5, 2)}
    contained = 0
    for pair in previous_pairs:
        global_pair = {(row, column, W[column]) for row, column in pair}
        contained += global_pair <= triple_new
    assert contained == 0

    principals = path_principal_signatures()
    assert not principals[1] and not principals[5]

    # Exact endpoint-compatible, pure-nonzero, full-rank specialization.
    specialization = {
        alpha[0]: 1, alpha[1]: 1, alpha[2]: 1, alpha[3]: 1,
        beta[0]: 1, beta[1]: 1, beta[2]: 1, beta[3]: -1,
        gamma: 1, delta: 2, epsilon: 3,
        **{variable: 1 for variable in x + y + z},
    }
    assert [sp.expand(value.subs(specialization)) for value in (c0, c1, c2)] == [2, 1, 1]
    a_num = [sp.Matrix([entry.subs(specialization) for entry in row]) for row in a]
    b_num = [sp.Matrix([entry.subs(specialization) for entry in row]) for row in b]
    assert sp.Matrix.hstack(*a_num).rank() == sp.Matrix.hstack(*b_num).rank() == 3
    local_ranks = []
    root_spans = []
    for root in range(5):
        root_spans.append(sp.Matrix([[h[u][root][c].subs(specialization) for c in range(3)] for u in range(7)]).rank())
    for u in range(7):
        rows = [[h[u][root][c].subs(specialization) for c in range(3)] for root in range(5)]
        rows += [[entry.subs(specialization) for entry in a[u]], [entry.subs(specialization) for entry in b[u]]]
        local_ranks.append(sp.Matrix(rows).rank())
    assert root_spans == [3] * 5 and local_ranks == [3] * 7

    return {
        "principal_saturation_is_unit_ideal": True,
        "mixed_word": "0000102",
        "pure_and_mixed_matching_counts_colour_zero": [2, 2],
        "previous_pair_shell_supports_contained": contained,
        "endpoint_cofactor_compatible": True,
        "full_rank_hall_specialization": True,
        "pure_coefficients_at_specialization": [2, 1, 1],
    }


def main() -> None:
    print(json.dumps({
        "status": "pass",
        "field": "exact characteristic zero",
        "result": verify(),
        "three_port_support_full_p7_exists": False,
        "finite_field_proof_used": False,
        "global_conjecture_resolved": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
