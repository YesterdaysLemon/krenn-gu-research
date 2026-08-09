"""Primary symbolic checks for the B3 phase-holonomy no-go."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


Permutation = tuple[int, int, int]


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right."""
    return tuple(left[right[index]] for index in range(3))  # type: ignore[return-value]


def parity(perm: Permutation) -> int:
    inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
    return inversions % 2


def main() -> None:
    group = tuple(permutations(range(3)))
    identity: Permutation = (0, 1, 2)
    t12: Permutation = (1, 0, 2)
    t13: Permutation = (2, 1, 0)
    t23: Permutation = (0, 2, 1)
    r123: Permutation = (1, 2, 0)
    r132: Permutation = (2, 0, 1)
    order = (identity, t12, t13, t23, r123, r132)
    assert set(group) == set(order)

    symbols = sp.symbols("w_e w_12 w_13 w_23 w_123 w_132", nonzero=True)
    weights = dict(zip(order, symbols, strict=True))
    even = tuple(perm for perm in group if parity(perm) == 0)
    odd = tuple(perm for perm in group if parity(perm) == 1)
    phase_sum = sum(weights.values())
    toric = sp.prod(weights[perm] for perm in even) - sp.prod(
        weights[perm] for perm in odd
    )

    for tau in group:
        rebased = {
            rho: sp.cancel(weights[compose(tau, rho)] / weights[tau]) for rho in group
        }
        assert sp.cancel(sum(rebased.values()) - phase_sum / weights[tau]) == 0
        rebased_toric = sp.prod(rebased[perm] for perm in even) - sp.prod(
            rebased[perm] for perm in odd
        )
        expected_sign = 1 if parity(tau) == 0 else -1
        assert sp.cancel(rebased_toric - expected_sign * toric / weights[tau] ** 3) == 0

    _, a, b, c, u, v = symbols
    normalized = {identity: 1, t12: a, t13: b, t23: c, r123: u, r132: v}

    def normalized_rebase(tau: Permutation) -> tuple[sp.Expr, ...]:
        return tuple(
            sp.cancel(normalized[compose(tau, rho)] / normalized[tau])
            for rho in order[1:]
        )

    assert normalized_rebase(t12) == (1 / a, v / a, u / a, c / a, b / a)
    assert normalized_rebase(r123) == (b / u, c / u, a / u, v / u, 1 / u)

    centralizer_t12 = {perm for perm in group if compose(perm, t12) == compose(t12, perm)}
    centralizer_r123 = {
        perm for perm in group if compose(perm, r123) == compose(r123, perm)
    }
    assert centralizer_t12 == {identity, t12}
    assert centralizer_r123 == {identity, r123, r132}

    theta = -2 + sp.sqrt(3)
    matrix = sp.Matrix([[1, 1, 1 / theta], [1, 1, 1], [theta, 1, 1]])
    physical_weights = {
        perm: sp.prod(matrix[row, perm[row]] for row in range(3)) for perm in group
    }
    expected_weights = (1, 1, 1, 1, theta, 1 / theta)
    assert all(
        sp.simplify(physical_weights[perm] - expected) == 0
        for perm, expected in zip(order, expected_weights, strict=True)
    )
    assert sp.simplify(matrix.per()) == 0
    assert sp.simplify(theta + 1 / theta + 4) == 0

    c2_ratios = (
        physical_weights[t12] / physical_weights[identity],
        physical_weights[identity] / physical_weights[t12],
    )
    assert all(sp.simplify(ratio - 1) == 0 for ratio in c2_ratios)

    c3_ratios = (
        physical_weights[r123] / physical_weights[identity],
        physical_weights[r132] / physical_weights[r123],
        physical_weights[identity] / physical_weights[r132],
    )
    expected_c3_ratios = (theta, theta**-2, theta)
    assert all(
        sp.simplify(ratio - expected) == 0
        for ratio, expected in zip(c3_ratios, expected_c3_ratios, strict=True)
    )
    assert all(sp.simplify(ratio + 1) != 0 for ratio in c3_ratios)

    variable = sp.Symbol("T")
    polynomial = variable**2 + (1 + a + b + c) * variable + a * b * c
    difference = sp.expand((variable - u) * (variable - v) - polynomial)
    expected_difference = -(1 + a + b + c + u + v) * variable + (u * v - a * b * c)
    assert sp.expand(difference - expected_difference) == 0

    print("arbitrary permanent B3 phase-holonomy no-go: PASS")
    print("six-term symbolic group audit only; no graph or matching census was performed")


if __name__ == "__main__":
    main()
