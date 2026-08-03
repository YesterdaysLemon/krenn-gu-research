"""Exact checks for the top two-port synchronization observability boundary.

No support, colour-word, alignment, or graph-family enumeration is used.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def zeon_add(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result = dict(left)
    for mask, value in right.items():
        result[mask] = sp.expand(result.get(mask, 0) + value)
    return {mask: value for mask, value in result.items() if value != 0}


def zeon_scale(poly: dict[int, sp.Expr], scalar: sp.Expr) -> dict[int, sp.Expr]:
    return {
        mask: sp.expand(scalar * value)
        for mask, value in poly.items()
        if scalar * value != 0
    }


def zeon_mul(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(
                result.get(mask, 0) + left_value * right_value
            )
    return {mask: value for mask, value in result.items() if value != 0}


def zeon_inverse(poly: dict[int, sp.Expr], port_count: int) -> dict[int, sp.Expr]:
    assert poly.get(0) == 1
    nilpotent = zeon_add(poly, {0: -1})
    result = {0: sp.Integer(1)}
    power = {0: sp.Integer(1)}
    for degree in range(1, port_count + 1):
        power = zeon_mul(power, nilpotent)
        result = zeon_add(result, zeon_scale(power, sp.Integer((-1) ** degree)))
    return result


def hafnian(matrix: sp.Matrix) -> sp.Expr:
    size = matrix.rows
    assert matrix.cols == size and size % 2 == 0
    memo: dict[int, sp.Expr] = {0: sp.Integer(1)}

    def evaluate(mask: int) -> sp.Expr:
        if mask in memo:
            return memo[mask]
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        total = sp.Integer(0)
        candidates = rest
        while candidates:
            second_bit = candidates & -candidates
            second = second_bit.bit_length() - 1
            total += matrix[first, second] * evaluate(rest ^ second_bit)
            candidates ^= second_bit
        memo[mask] = sp.expand(total)
        return memo[mask]

    return evaluate((1 << size) - 1)


def permanent(matrix: sp.Matrix) -> sp.Expr:
    size = matrix.rows
    assert matrix.cols == size
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in range(size):
        next_states: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + value * matrix[row, column]
                )
        states = next_states
    return states[(1 << size) - 1]


def main() -> None:
    # The direct sector is coordinatewise surjective when h is nonzero.
    target_entries = sp.symbols("t00:03 t10:13 t20:23")
    target = sp.Matrix(3, 3, target_entries)
    h_value = sp.Integer(2)
    direct_block = target / h_value
    zero = sp.zeros(3, 1)
    recovered = h_value * direct_block + outer(zero, zero) + outer(zero, zero)
    assert recovered == target

    # A synchronized pair has rank at most two.  Its generic 3x3 determinant
    # vanishes identically, while the direct physical block I_3 has rank 3.
    a0 = sp.Matrix(sp.symbols("a00:03"))
    b0 = sp.Matrix(sp.symbols("b00:03"))
    a1 = sp.Matrix(sp.symbols("a10:13"))
    b1 = sp.Matrix(sp.symbols("b10:13"))
    synchronized = outer(a0, b1) + outer(b0, a1)
    assert sp.expand(synchronized.det()) == 0
    assert sp.eye(3).det() == 1
    assert sp.eye(3).rank() == 3

    # Two-residual dual-Wick recovery on four scalar ports.
    port_count = 4
    pair_masks: dict[tuple[int, int], int] = {
        pair: (1 << pair[0]) | (1 << pair[1])
        for pair in combinations(range(port_count), 2)
    }
    b_edge = {pair: sp.Symbol(f"B{pair[0]}{pair[1]}") for pair in pair_masks}
    a = sp.symbols("a0:4")
    b = sp.symbols("b0:4")
    k_edge = {
        pair: a[pair[0]] * b[pair[1]] + b[pair[0]] * a[pair[1]]
        for pair in pair_masks
    }
    q_b = {pair_masks[pair]: value for pair, value in b_edge.items()}
    q_k = {pair_masks[pair]: value for pair, value in k_edge.items()}
    # exp(Q_B) truncates after two factors on four square-zero ports.
    m_family = zeon_add(
        {0: sp.Integer(1)},
        zeon_add(q_b, zeon_scale(zeon_mul(q_b, q_b), sp.Rational(1, 2))),
    )
    h = sp.Symbol("h")
    z_family = zeon_mul(m_family, zeon_add({0: h}, q_k))
    for pair, mask in pair_masks.items():
        assert sp.expand(z_family[mask] - h * b_edge[pair] - k_edge[pair]) == 0

    n_family = zeon_add(z_family, zeon_scale(m_family, -h))
    relative = zeon_mul(n_family, zeon_inverse(m_family, port_count))
    assert set(relative) == set(q_k)
    for mask, value in q_k.items():
        assert sp.expand(relative[mask] - value) == 0

    full_mask = (1 << port_count) - 1
    tangent_four = sp.Integer(0)
    for pair, pair_mask in pair_masks.items():
        complement = full_mask ^ pair_mask
        complement_pair = tuple(i for i in range(port_count) if complement & (1 << i))
        tangent_four += k_edge[pair] * b_edge[complement_pair]
    assert sp.expand(n_family[full_mask] - tangent_four) == 0

    # Four-residual models with the same top permanent and different lower
    # hafnian/cofactor layers.
    a_zero = sp.zeros(4)
    a_split = sp.zeros(4)
    a_split[0, 1] = a_split[1, 0] = 1
    a_split[2, 3] = a_split[3, 2] = 1
    incidence = sp.eye(4)
    assert permanent(incidence) == 1
    assert hafnian(a_zero) == 0
    assert hafnian(a_split) == 1

    def quadratic_layer(residual: sp.Matrix, pair: tuple[int, int]) -> sp.Expr:
        complement = [i for i in range(4) if i not in pair]
        residual_minor = residual.extract(complement, complement)
        incidence_minor = incidence.extract(list(pair), list(pair))
        return sp.expand(hafnian(residual_minor) * permanent(incidence_minor))

    zero_quadratic = {
        pair: quadratic_layer(a_zero, pair) for pair in combinations(range(4), 2)
    }
    split_quadratic = {
        pair: quadratic_layer(a_split, pair) for pair in combinations(range(4), 2)
    }
    assert all(value == 0 for value in zero_quadratic.values())
    assert split_quadratic[(0, 1)] == 1
    assert split_quadratic[(2, 3)] == 1
    assert all(
        value == 0
        for pair, value in split_quadratic.items()
        if pair not in ((0, 1), (2, 3))
    )

    # Strict-support substitutions.
    strict_support = lambda order: 3 * order + 3
    assert strict_support(5) == 18
    assert strict_support(6) == 21
    assert strict_support(7) == 24
    assert 3 * 5 + 6 == 21  # r=5 one-port extraction
    assert 3 * 5 + 9 == 24  # r=5 synchronized two-port extraction

    print("top two-port direct sector: surjective")
    print("generic synchronized 3x3 determinant: identically zero")
    print("rank-three physical top block I3: not synchronized")
    print("paired-depth q=2 correction: synchronized exactly")
    print("q=4 equal-top/different-lower witness: exact")
    print("strict extracted supports P5/P6/P7: 18/21/24")
    print("unconditional top-only P7 transfer: NOT AVAILABLE")


if __name__ == "__main__":
    main()
