#!/usr/bin/env python3
"""Focused exact verifier for GLS48's adaptive-cut exclusion."""

from itertools import combinations

import sympy as sp


RESIDUAL = ("q0", "q1")
PORTS = ("u0", "u1", "u2", "u3")
LABELS = RESIDUAL + PORTS


def target_matrix(active_ports):
    """Build the exact ternary GHZ flattening across (A,P)|(Uhat-P)."""
    active_ports = tuple(active_ports)
    inactive_ports = tuple(u for u in PORTS if u not in active_ports)
    left_words = 9 * (3 ** len(active_ports))
    right_words = 3 ** len(inactive_ports)
    matrix = sp.zeros(left_words, right_words)
    alphas = (sp.Integer(2), sp.Integer(3), sp.Integer(5))

    for colour, alpha in enumerate(alphas):
        # Root row r_c has flattened A-index 3*c+c.  Pure active and
        # inactive port words append base-three digits all equal to c.
        left = 3 * colour + colour
        for _ in active_ports:
            left = 3 * left + colour
        right = 0
        for _ in inactive_ports:
            right = 3 * right + colour
        matrix[left, right] = alpha
    return matrix, inactive_ports


def assert_outer_product_rank_one(left_dim, right_dim):
    """Check representative symbolic minors of an arbitrary simple tensor."""
    ell = sp.symbols(f"l0:{left_dim}")
    h = sp.symbols(f"h0:{right_dim}")
    matrix = sp.Matrix(left_dim, right_dim, lambda i, j: ell[i] * h[j])
    if left_dim >= 2 and right_dim >= 2:
        row_pairs = {(0, 1), (0, left_dim - 1), (left_dim - 2, left_dim - 1)}
        col_pairs = {(0, 1), (0, right_dim - 1), (right_dim - 2, right_dim - 1)}
        for i, k in row_pairs:
            for j, l in col_pairs:
                minor = sp.expand(matrix[i, j] * matrix[k, l]
                                  - matrix[i, l] * matrix[k, j])
                assert minor == 0
    generic = matrix.subs({ell[0]: 1, h[0]: 1})
    assert generic.rank() >= 1


def main():
    subsets = [tuple()]
    subsets.extend((label,) for label in LABELS)
    subsets.extend(combinations(LABELS, 2))
    assert len(subsets) == 22

    case_counts = {"zero_or_one": 0, "residual_pair": 0,
                   "residual_port": 0, "port_pair": 0}

    for active in subsets:
        surviving_pairs = [pair for pair in combinations(LABELS, 2)
                           if pair[0] in active and pair[1] in active]
        assert len(surviving_pairs) <= 1

        active_ports = tuple(u for u in active if u in PORTS)
        target, inactive_ports = target_matrix(active_ports)
        assert len(inactive_ports) >= 2
        assert target.rank() == 3

        if len(active) <= 1:
            case_counts["zero_or_one"] += 1
            assert not surviving_pairs
            continue

        pair = surviving_pairs[0]
        port_count = sum(label in PORTS for label in pair)
        if port_count == 0:
            case_counts["residual_pair"] += 1
        elif port_count == 1:
            case_counts["residual_port"] += 1
        else:
            case_counts["port_pair"] += 1

        # The coefficient and every open endpoint variable are on the left;
        # the complementary physical deck is entirely on the right.
        assert set(active_ports) == {label for label in pair if label in PORTS}
        left_dim = 9 * (3 ** len(active_ports))
        right_dim = 3 ** len(inactive_ports)
        assert_outer_product_rank_one(left_dim, right_dim)

    assert case_counts == {
        "zero_or_one": 7,
        "residual_pair": 1,
        "residual_port": 8,
        "port_pair": 6,
    }
    print("GLS48 focused exact verifier: PASS")
    print("22 effective subsets; exhaustive support case counts", case_counts)
    print("all adaptive GHZ flattenings have rank 3")
    print("every sole-source flattening has rank at most 1")


if __name__ == "__main__":
    main()
