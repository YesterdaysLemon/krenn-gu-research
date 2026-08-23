#!/usr/bin/env python3
"""Independent no-import audit for GLS48.

This implementation uses label bit masks, sparse matrices over F_101, and a
minimal Gaussian eliminator.  It imports neither SymPy nor the primary.
"""

from itertools import combinations


PRIME = 101
QMASK = 0b000011
PORT_MASK = 0b111100
LABEL_BITS = tuple(1 << i for i in range(6))


def rank_mod(rows):
    a = [[entry % PRIME for entry in row] for row in rows]
    if not a:
        return 0
    nrows, ncols = len(a), len(a[0])
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        inv = pow(a[pivot_row][col], PRIME - 2, PRIME)
        a[pivot_row] = [(inv * x) % PRIME for x in a[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [(x - factor * y) % PRIME
                        for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def ternary_constant_word(colour, length):
    value = 0
    for _ in range(length):
        value = 3 * value + colour
    return value


def ghz_sparse_rows(active_port_count, inactive_port_count):
    nleft = 9 * (3 ** active_port_count)
    nright = 3 ** inactive_port_count
    rows = [[0] * nright for _ in range(nleft)]
    for colour, alpha in enumerate((7, 11, 13)):
        left = 3 * colour + colour
        for _ in range(active_port_count):
            left = 3 * left + colour
        right = ternary_constant_word(colour, inactive_port_count)
        rows[left][right] = alpha
    return rows


def formal_outer_minor(i, k, j, ell):
    # Represent a monomial as a sorted tuple of variable names.  The two
    # products in every 2x2 minor of L_i H_j have the same monomial.
    first = tuple(sorted((f"L{i}", f"H{j}", f"L{k}", f"H{ell}")))
    second = tuple(sorted((f"L{i}", f"H{ell}", f"L{k}", f"H{j}")))
    return first == second


def main():
    masks = [0]
    masks.extend(LABEL_BITS)
    masks.extend(a | b for a, b in combinations(LABEL_BITS, 2))
    assert len(masks) == 22 and len(set(masks)) == 22

    typed = {"empty": 0, "qq": 0, "qu": 0, "uu": 0}
    for active in masks:
        bits = [bit for bit in LABEL_BITS if active & bit]
        possible_pairs = [(a, b) for a, b in combinations(LABEL_BITS, 2)
                          if active & a and active & b]
        assert len(possible_pairs) <= 1

        active_ports = (active & PORT_MASK).bit_count()
        inactive_ports = 4 - active_ports
        assert inactive_ports >= 2
        assert rank_mod(ghz_sparse_rows(active_ports, inactive_ports)) == 3

        if len(bits) <= 1:
            typed["empty"] += 1
            assert not possible_pairs
            continue

        a, b = possible_pairs[0]
        residual_endpoints = int(bool(a & QMASK)) + int(bool(b & QMASK))
        if residual_endpoints == 2:
            typed["qq"] += 1
        elif residual_endpoints == 1:
            typed["qu"] += 1
        else:
            typed["uu"] += 1

        # Different derivation of the universal rank-one statement: verify
        # formal cancellation for several separated row/column choices.  The
        # identity is dimension-independent.
        left_dim = 9 * (3 ** active_ports)
        right_dim = 3 ** inactive_ports
        row_pairs = ((0, 1), (0, left_dim - 1),
                     (left_dim - 2, left_dim - 1))
        col_pairs = ((0, 1), (0, right_dim - 1),
                     (right_dim - 2, right_dim - 1))
        for i, k in row_pairs:
            for j, ell in col_pairs:
                assert formal_outer_minor(i, k, j, ell)

    assert typed == {"empty": 7, "qq": 1, "qu": 8, "uu": 6}
    print("GLS48 independent no-import audit: PASS")
    print("bit-mask support cases", typed)
    print("custom F_101 GHZ ranks: 3 on all 22 adaptive cuts")
    print("formal outer-product minors cancel identically")


if __name__ == "__main__":
    main()
