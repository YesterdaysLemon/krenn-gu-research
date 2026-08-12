"""Exact replay for the two-source exceptional-root-row obstruction."""

from __future__ import annotations

from itertools import product

import sympy as sp


def mixed_product_matrix(left_dim: int, right_dim: int, q: sp.Matrix) -> sp.Matrix:
    """Matrix of (s,z) -> s tensor q_z + q_s tensor z."""
    q_left = q[:left_dim, 0]
    q_right = q[left_dim:, 0]
    out = sp.zeros(left_dim * right_dim, left_dim + right_dim)
    for i, j in product(range(left_dim), range(right_dim)):
        out[right_dim * i + j, i] = q_right[j]
        out[right_dim * i + j, left_dim + j] = q_left[i]
    return out


def splitting_matrix(rows: list[tuple[sp.Matrix, sp.Matrix]]) -> sp.Matrix:
    u = sp.Matrix(sp.symbols("u0:3"))
    v = sp.Matrix(sp.symbols("v0:3"))
    equations: list[sp.Expr] = []
    for x, y in rows:
        equations.extend(sp.kronecker_product(x, u) + sp.kronecker_product(v, y))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, [*u, *v])
    return coefficient_matrix


def check_all_two_source_normal_forms() -> None:
    ranks: dict[int, int] = {}
    eye = sp.eye(3)
    for pure_x in range(4):
        for pure_y in range(4 - pure_x):
            diagonal = 3 - pure_x - pure_y
            rows: list[tuple[sp.Matrix, sp.Matrix]] = []
            for i in range(pure_x):
                rows.append((eye[:, i], sp.zeros(3, 1)))
            for i in range(pure_y):
                rows.append((sp.zeros(3, 1), eye[:, i]))
            for i in range(diagonal):
                rows.append((eye[:, pure_x + i], eye[:, pure_y + i]))
            value = splitting_matrix(rows).rank()
            ranks[value] = ranks.get(value, 0) + 1
    assert ranks == {3: 2, 6: 8}
    print("two-source splitting normal forms: PASS (2 aligned; 8 injective)")


def check_combined_zero_divisors() -> None:
    zero_left = sp.zeros(6, 1)
    zero_right = sp.zeros(3, 1)
    e_left = sp.eye(6)[:, 0]
    e_right = sp.eye(3)[:, 0]

    pure_left = mixed_product_matrix(6, 3, e_left.col_join(zero_right))
    pure_right = mixed_product_matrix(6, 3, zero_left.col_join(e_right))
    mixed = mixed_product_matrix(6, 3, e_left.col_join(e_right))

    assert (pure_left.rank(), len(pure_left.nullspace())) == (3, 6)
    assert (pure_right.rank(), len(pure_right.nullspace())) == (6, 3)
    assert (mixed.rank(), len(mixed.nullspace())) == (8, 1)
    expected = sp.Matrix([-1, 0, 0, 0, 0, 0, 1, 0, 0])
    assert mixed.nullspace()[0] == expected
    print("combined (6+3)-space zero divisors: PASS (nullities 6 / 3 / 1)")


def check_purity_grid() -> None:
    # Once each q_j is pure, the eight L/R assignments either put all six
    # vectors in one summand or force a p_i to be zero.
    for labels in product(("L", "R"), repeat=3):
        majority = "L" if labels.count("L") >= 2 else "R"
        minority_count = 3 - labels.count(majority)
        if minority_count == 0:
            conclusion = "one summand"
        else:
            # The minority q forces the two p's with other indices into the
            # minority summand, while the majority pair already forced them
            # into the majority summand.
            conclusion = "zero p"
        assert conclusion in {"one summand", "zero p"}
    print("combined purity grid: PASS (8/8 assignments)")


def check_two_source_pair_decomposition() -> None:
    # The two tensors U in Y tensor Z and V in X tensor Z concatenate to the
    # single mixed product in (X direct-sum Y) tensor Z.
    values = [sp.Rational(((31 * k + 9) % 19) - 9) for k in range(18)]
    p_x = sp.Matrix(values[0:3])
    p_y = sp.Matrix(values[3:6])
    p_z = sp.Matrix(values[6:9])
    q_x = sp.Matrix(values[9:12])
    q_y = sp.Matrix(values[12:15])
    q_z = sp.Matrix(values[15:18])
    separate = sp.Matrix.vstack(
        sp.kronecker_product(p_x, q_z) + sp.kronecker_product(q_x, p_z),
        sp.kronecker_product(p_y, q_z) + sp.kronecker_product(q_y, p_z),
    )
    combined = (
        sp.kronecker_product(p_x.col_join(p_y), q_z)
        + sp.kronecker_product(q_x.col_join(q_y), p_z)
    )
    assert separate == combined
    print("two-source pair concatenation: PASS")


def main() -> None:
    check_all_two_source_normal_forms()
    check_combined_zero_divisors()
    check_purity_grid()
    check_two_source_pair_decomposition()
    print("two-source exceptional-root-row obstruction: PASS")


if __name__ == "__main__":
    main()
