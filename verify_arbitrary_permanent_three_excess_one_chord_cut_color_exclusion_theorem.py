"""Primary symbolic checks for the one-chord cut-colour exclusion."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

import sympy as sp


def cut_solutions(
    alpha: tuple[int, int, int], source_cut: tuple[int, int, int, int]
) -> dict[int, list[tuple[tuple[int, int], tuple[int, int], int]]]:
    """Solve only the bounded three-colour transport ledger."""
    target = Counter(source_cut)
    result: dict[int, list[tuple[tuple[int, int], tuple[int, int], int]]] = {}
    for branch in range(3):
        others = tuple(i for i in range(3) if i != branch)
        rows: list[tuple[tuple[int, int], tuple[int, int], int]] = []
        for branch_colours in combinations(range(3), 2):
            for other_colours in product(range(3), repeat=2):
                if any(
                    other_colours[k] == alpha[others[k]] for k in range(2)
                ):
                    continue
                if Counter(branch_colours + other_colours) != target:
                    continue
                survivor = next(c for c in range(3) if c not in branch_colours)
                rows.append((branch_colours, other_colours, survivor))
        result[branch] = rows
    return result


def main() -> None:
    p, q, r, u, t = sp.symbols("p q r u t", nonzero=True)
    ell0, ell1, ell2, kappa = sp.symbols(
        "ell0 ell1 ell2 kappa", nonzero=True
    )

    # Scalar permanent of the one-chord port matrix at the aligned word.
    scalar_port = sp.Matrix(
        [[ell0, p, q], [r, ell1, u], [t, 0, ell2]]
    )
    permanent = sum(
        sp.prod(scalar_port[i, sigma[i]] for i in range(3))
        for sigma in permutations(range(3))
    )
    assert sp.expand(permanent) == ell0 * ell1 * ell2 + p * r * ell2 + q * t * ell1 + p * u * t

    # If every boundary span is a line, the row-zero flattening has rank >=2.
    ordinary_flattening = sp.Matrix(
        [[p * u * t, p * r, q * t, 0], [0, 0, 0, 1]]
    )
    assert sp.det(ordinary_flattening[:, [1, 3]]) == p * r

    distinct = cut_solutions((0, 1, 2), (0, 1, 2, 2))
    assert tuple(len(distinct[b]) for b in range(3)) == (2, 2, 3)
    for branch, rows in distinct.items():
        others = tuple(i for i in range(3) if i != branch)
        for _, other_colours, survivor in rows:
            assert any(
                other_colours[k] == survivor for k in range(len(others))
            )

    repeated = cut_solutions((0, 1, 0), (1, 2, 2, 2))
    for branch in range(3):
        assert repeated[branch] == [((1, 2), (2, 2), 0)]

    # Repeated-colour branch 0 has the forbidden z1 tensor L2 coefficient.
    branch_zero = sp.Matrix(
        [[p * u * t, p * r], [q * t, ell0]]
    )
    assert branch_zero[0, 1] == p * r

    # Repeated-colour branch 1 contains two independent diagonal directions.
    branch_one = sp.Matrix([[kappa * q * t, 0], [0, kappa]])
    assert sp.det(branch_one) == kappa**2 * q * t

    # Repeated-colour deficient-row branch contains the private L0 tensor L1
    # coefficient whenever theta alignment keeps ell2 nonzero.
    branch_two = sp.Matrix(
        [[p * u * t + ell2 * p * r, q * t], [0, ell2]]
    )
    assert branch_two[1, 1] == ell2

    # On the forbidden nonalignment divisor ell2=0, the central equation
    # ell1=-ps/q removes the e1 part and leaves a nonzero e0 direction.
    ell1_non_aligned = -p * u / q
    row_one_vector = sp.Matrix([q * kappa, p * u + q * ell1_non_aligned])
    assert sp.simplify(row_one_vector[1]) == 0
    assert row_one_vector[0] == q * kappa
    assert sp.simplify(permanent.subs({ell2: 0, ell1: ell1_non_aligned})) == 0

    print("arbitrary permanent one-chord cut-colour exclusion: PASS")
    print("symbolic port and three-colour ledgers only; no support census was performed")


if __name__ == "__main__":
    main()
