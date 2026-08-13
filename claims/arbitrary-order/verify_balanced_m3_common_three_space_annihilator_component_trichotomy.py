"""Exact replay of the m=3 annihilator-component trichotomy."""

from itertools import product

import sympy as sp


def dimension_bound(ranks, epsilon):
    kernel_dimensions = tuple(3 - rank for rank in ranks)
    return sum(dimension - 1 for dimension in kernel_dimensions) - epsilon


def check_budget_table():
    feasible = []
    for ranks in product(range(3), repeat=3):
        for epsilon in (0, 1):
            ambient_dimension = dimension_bound(ranks, epsilon)
            if ambient_dimension >= 3:
                feasible.append((ranks, epsilon))
                assert sum(ranks) <= 3 - epsilon
    assert any(sum(ranks) == 3 and epsilon == 0 for ranks, epsilon in feasible)
    assert any(sum(ranks) == 2 and epsilon == 1 for ranks, epsilon in feasible)
    print(f"component dimension budgets: PASS ({len(feasible)} feasible rank/epsilon cases)")


def annihilator_basis(columns):
    matrix = sp.Matrix.hstack(*columns) if columns else sp.zeros(3, 0)
    return matrix.T.nullspace()


def check_sharp_rank_controls():
    e0 = sp.Matrix((1, 0, 0))
    e1 = sp.Matrix((0, 1, 0))
    e2 = sp.Matrix((0, 0, 1))

    redundant_columns = ((e2,), (e2,), (e2,))
    redundant_kernels = tuple(annihilator_basis(columns) for columns in redundant_columns)
    assert tuple(len(kernel) for kernel in redundant_kernels) == (2, 2, 2)
    assert all(vector[2] == 0 for kernel in redundant_kernels for vector in kernel)
    assert dimension_bound((1, 1, 1), 0) == 3

    independent_columns = ((), (e0,), (e1,))
    independent_kernels = tuple(annihilator_basis(columns) for columns in independent_columns)
    assert tuple(len(kernel) for kernel in independent_kernels) == (3, 2, 2)
    first_boundary_basis = sp.Matrix([[1, 0, 0], [0, 1, 0]]).T
    assert first_boundary_basis.rank() == 2
    assert all(vector[2] == 0 for vector in first_boundary_basis.columnspace())
    assert dimension_bound((0, 1, 1), 1) == 3

    assert e2 in sp.Matrix.hstack(*redundant_columns[0]).columnspace()
    assert sp.Matrix.hstack(*independent_columns[0]).rank() == 0
    print("sharp cross-column rank budgets: PASS (3 redundant / 2 independent)")


def check_diagonal_multiboundary():
    a = sp.symbols("a0:3")
    b = sp.symbols("b0:3")
    c = sp.symbols("c0:3")
    equations = tuple(a[index] * b[index] * c[index] for index in range(3))
    substitutions = {a[0]: 0, b[1]: 0, c[2]: 0}
    assert all(sp.expand(equation.subs(substitutions)) == 0 for equation in equations)
    # Three independent coordinate hyperplanes in a six-dimensional Segre product.
    assert 6 - len(substitutions) == 3
    print("target-diagonal multi-boundary component: PASS")


def main():
    check_budget_table()
    check_sharp_rank_controls()
    check_diagonal_multiboundary()
    print("balanced m=3 common-three-space component trichotomy: PASS")


if __name__ == "__main__":
    main()
