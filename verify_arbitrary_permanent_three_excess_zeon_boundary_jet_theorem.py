"""Primary symbolic proof guards for the zeon boundary jet theorem."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def permanent(matrix: sp.Matrix) -> sp.Expr:
    assert matrix.rows == matrix.cols
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            sp.prod(matrix[row, permutation[row]] for row in range(matrix.rows))
            for permutation in permutations(range(matrix.rows))
        )
    )


def zeon_coefficients(
    expression: sp.Expr,
    generators: tuple[sp.Symbol, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    """Reduce a polynomial modulo the squares of all generators."""
    answer: dict[tuple[int, ...], sp.Expr] = {}
    polynomial = sp.Poly(sp.expand(expression), *generators)
    for exponent, coefficient in polynomial.terms():
        if any(value > 1 for value in exponent):
            continue
        answer[exponent] = sp.expand(answer.get(exponent, 0) + coefficient)
    return answer


def main() -> None:
    x = sp.Matrix(2, 2, sp.symbols("x00 x01 x10 x11"))
    y = sp.Matrix(2, 2, sp.symbols("y00 y01 y10 y11"))
    z = sp.Matrix(2, 2, sp.symbols("z00 z01 z10 z11"))
    w = sp.Matrix(2, 2, sp.symbols("w00 w01 w10 w11"))
    u0, u1, v0, v1 = sp.symbols("u0 u1 v0 v1")
    generators = (u0, u1, v0, v1)

    zv = z * sp.Matrix([v0, v1])
    uy = sp.Matrix([[u0, u1]]) * y
    jet = permanent(w + zv * uy)
    coefficients = zeon_coefficients(jet, generators)

    assert coefficients[(0, 0, 0, 0)] == permanent(w)

    c_per = sp.Matrix(
        2,
        2,
        lambda q, r: permanent(w.minor_submatrix(r, q)),
    )
    elementary = (y * c_per * z).applyfunc(sp.expand)
    for i in range(2):
        for j in range(2):
            exponent = tuple(
                int(position == i) if position < 2 else int(position - 2 == j)
                for position in range(4)
            )
            assert coefficients[exponent] == elementary[i, j]

    top_exponent = (1, 1, 1, 1)
    assert sp.expand(coefficients[top_exponent] - 2 * permanent(y) * permanent(z)) == 0

    full = x.row_join(y).col_join(z.row_join(w))
    reconstructed = permanent(x) * coefficients[(0, 0, 0, 0)]
    for i in range(2):
        for j in range(2):
            exponent = tuple(
                int(position == i) if position < 2 else int(position - 2 == j)
                for position in range(4)
            )
            reconstructed += x.minor_submatrix(i, j)[0, 0] * coefficients[exponent]
    reconstructed += coefficients[top_exponent] / 2
    assert sp.expand(permanent(full) - reconstructed) == 0

    # Saturated three-port top layer: per(v u^T)=3! u0u1u2v0v1v2.
    u = sp.symbols("U0:3")
    v = sp.symbols("V0:3")
    rank_one = sp.Matrix(v) * sp.Matrix([u])
    top_three = zeon_coefficients(permanent(rank_one), tuple(u + v))
    assert top_three[(1, 1, 1, 1, 1, 1)] == 6

    print("zeon boundary jet all-layer identity: PASS")
    print("fixed symbolic 2+2 block and degree-three factorial; no family census")


if __name__ == "__main__":
    main()
