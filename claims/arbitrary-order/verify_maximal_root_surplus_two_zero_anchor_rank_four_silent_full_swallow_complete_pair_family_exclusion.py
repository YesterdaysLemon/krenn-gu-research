"""Focused exact checks for the GLS47 rank-four pair-family exclusion."""

from __future__ import annotations

import sympy as sp


def synchronization_replay() -> None:
    """Check that the three edge coefficients have a nonzero product."""

    v0 = sp.symbols("v0_0:2")
    v1 = sp.symbols("v1_0:2")
    v2 = sp.symbols("v2_0:2")
    c01 = sp.symbols("c01_0:4")
    c02 = sp.symbols("c02_0:4")
    c12 = sp.symbols("c12_0:4")

    def bilinear(
        left: tuple[sp.Symbol, ...],
        right: tuple[sp.Symbol, ...],
        coefficients: tuple[sp.Symbol, ...],
    ) -> sp.Expr:
        return sp.expand(
            sum(
                coefficients[2 * row + column] * left[row] * right[column]
                for row in range(2)
                for column in range(2)
            )
        )

    beta01 = bilinear(v0, v1, c01)
    beta02 = bilinear(v0, v2, c02)
    beta12 = bilinear(v1, v2, c12)
    product_polynomial = sp.Poly(
        sp.expand(beta01 * beta02 * beta12),
        *v0,
        *v1,
        *v2,
        *c01,
        *c02,
        *c12,
    )
    assert not product_polynomial.is_zero
    assert product_polynomial.total_degree() == 9


def matrix_units() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(3, 3, lambda row, column: int({row, column} == {i, j}))
        for i, j in ((0, 1), (0, 2), (1, 2))
    )


def left_right_normalization_replay() -> None:
    """Replay the exact normalization of a synchronized triangle."""

    left = sp.Matrix(((1, 1, 0), (0, 1, 1), (1, 0, 1)))
    right = sp.Matrix(((1, 0, 1), (1, 1, 0), (0, 1, 2)))
    assert left.det() != 0
    assert right.det() != 0
    for symmetric_unit in matrix_units():
        physical = left * symmetric_unit * right.T
        transformed = left.inv() * physical * right.inv().T
        assert sp.simplify(transformed - symmetric_unit) == sp.zeros(3)

    # A one-coordinate left kernel cannot kill a graph over Delta because f
    # has zero diagonal: the kth coordinate survives unchanged.
    h, ell = sp.symbols("h ell", nonzero=True)
    offdiag = sp.Matrix(
        (
            (0, *sp.symbols("f01 f02")),
            (sp.symbols("f10"), 0, sp.symbols("f12")),
            (*sp.symbols("f20 f21"), 0),
        )
    )
    for color in range(3):
        row = sp.zeros(1, 3)
        row[0, color] = h
        diagonal_unit = sp.zeros(3)
        diagonal_unit[color, color] = 1
        graph_row = row * (diagonal_unit + ell * offdiag)
        assert sp.expand(graph_row[color] - h) == 0


def rank_one_complement_replay() -> None:
    """Replay the Sym_0 rank-one and common-skew identities."""

    a, b, c = sp.symbols("a b c")
    symmetric_zero = sp.Matrix(((0, a, b), (a, 0, c), (b, c, 0)))
    principal_minors = tuple(
        sp.expand(symmetric_zero.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal_minors == (-a**2, -b**2, -c**2)

    u = sp.Matrix(sp.symbols("u0:3"))
    v = sp.Matrix(sp.symbols("v0:3"))
    factors = sp.Matrix.hstack(u, v)
    symplectic = sp.Matrix(((0, 1), (-1, 0)))
    skew = u * v.T - v * u.T
    assert sp.simplify(skew - factors * symplectic * factors.T) == sp.zeros(3)

    scale = sp.symbols("scale", nonzero=True)
    symmetric_rank_one = scale * u * u.T
    assert tuple(symmetric_rank_one[index, index] for index in range(3)) == tuple(
        scale * entry**2 for entry in u
    )


def membership_system(
    mates: tuple[int, ...],
    diagonal: tuple[int, int, int],
) -> tuple[sp.Matrix, tuple[sp.Symbol, ...]]:
    """Build N_i in Sym_0+K*diag(d) for selected coordinate mates."""

    a_symbols = sp.symbols("a0:3")
    b_symbols = sp.symbols("b0:3")
    lambda_symbols = sp.symbols(f"lambda0:{len(mates)}")
    a = sp.Matrix(a_symbols)
    b = sp.Matrix(b_symbols)
    equations = []
    for mate, scalar in zip(mates, lambda_symbols, strict=True):
        unit = sp.eye(3)[:, mate]
        matrix = a * unit.T + unit * b.T
        for row in range(3):
            for column in range(row + 1, 3):
                equations.append(matrix[row, column] - matrix[column, row])
        for row in range(3):
            equations.append(matrix[row, row] - scalar * diagonal[row])
    variables = (*a_symbols, *b_symbols, *lambda_symbols)
    coefficient_matrix, target = sp.linear_eq_to_matrix(equations, variables)
    assert target == sp.zeros(len(equations), 1)
    return coefficient_matrix, variables


def label_locking_replay() -> None:
    """Check external deletion and every triangle-block multiplicity."""

    diagonal = (2, 3, 5)
    external, _ = membership_system((0, 1, 2), diagonal)
    assert external.shape == (18, 9)
    assert external.rank() == 9

    for color in range(3):
        mates = tuple(index for index in range(3) if index != color)
        block, _ = membership_system(mates, diagonal)
        assert block.shape == (12, 8)
        assert block.rank() == 7
        nullspace = block.nullspace()
        assert len(nullspace) == 1
        expected = sp.Matrix(
            [
                *(1 if index == color else 0 for index in range(3)),
                *(1 if index == color else 0 for index in range(3)),
                0,
                0,
            ]
        )
        assert sp.Matrix.hstack(nullspace[0], expected).rank() == 1

    assert sp.Matrix.hstack(*[unit.reshape(9, 1) for unit in matrix_units()]).rank() == 3


def main() -> None:
    synchronization_replay()
    left_right_normalization_replay()
    rank_one_complement_replay()
    label_locking_replay()
    print("GLS47 rank-four complete-pair exclusion primary checks: PASS")
    print("  synchronized edge product: nonzero formal polynomial")
    print("  left-right triangle normalization: exact")
    print("  Sym_0 rank-one/skew identities: exact")
    print("  external system rank 9; triangle-block systems rank 7")
    print("  complete normalized image rank <=3; rank-four fibre EMPTY")
    print("  ranks >=5 and global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
