"""Exact replay for the complete common-three-space joint-rank-six exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def e3(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def e9(index: int) -> sp.Matrix:
    return sp.eye(9)[:, index]


def tidx(x: int, y: int, z: int) -> int:
    return 9 * x + 3 * y + z


def pair_blocks(left: sp.Matrix, right: sp.Matrix) -> tuple[sp.Matrix, ...]:
    a = sp.Matrix(
        3,
        3,
        lambda i, j: left[3 + i] * right[6 + j]
        + right[3 + i] * left[6 + j],
    )
    b = sp.Matrix(
        3,
        3,
        lambda i, j: left[i] * right[6 + j]
        + right[i] * left[6 + j],
    )
    c = sp.Matrix(
        3,
        3,
        lambda i, j: left[i] * right[3 + j]
        + right[i] * left[3 + j],
    )
    return a, b, c


def derivative(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    a, b, c = pair_blocks(left, right)
    out = sp.zeros(27, 9)
    for x, y, z in product(range(3), repeat=3):
        row = tidx(x, y, z)
        out[row, x] = a[y, z]
        out[row, 3 + y] = b[x, z]
        out[row, 6 + z] = c[x, y]
    return out


def root_derivative(b23: sp.Matrix, b13: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(27, 9)
    for a, b, c in product(range(3), repeat=3):
        row = tidx(a, b, c)
        out[row, a] = b23[b, c]
        out[row, 3 + b] = b13[a, c]
    return out


def check_coordinate_profiles_and_graph() -> None:
    same = sp.diag(0, 2, 3)
    different = sp.Matrix([[0, 2, 0], [0, 0, 0], [0, 5, 7]])
    for transform, kernel, missing in (
        (same, e3(0), 0),
        (different, e3(0), 1),
    ):
        graph = sp.Matrix.vstack(sp.eye(3), transform)
        relation = sp.Matrix.vstack(-transform.T, sp.eye(3))
        assert graph.rank() == relation.rank() == 3
        assert graph.T * relation == sp.zeros(3, 3)
        assert transform.rank() == 2
        assert transform * kernel == sp.zeros(3, 1)
        assert transform.row(missing) == sp.zeros(1, 3)

    # A transverse root-block control with the required diagonal missing row.
    b23 = sp.Matrix([[2, 1, 3], [0, 11, 0], [5, 7, 13]])
    b13 = sp.Matrix([[17, 19, 23], [29, 31, 37], [41, 43, 47]])
    assert root_derivative(b23, b13).rank() == 6
    assert b23.row(1) == 11 * e3(1).T

    # The exact graph correction has only its selected monomial coefficient.
    a = e3(1)
    ta = different * a
    correction = root_derivative(b23, b13) * sp.Matrix.vstack(a, ta, sp.zeros(3, 1))
    for first, second, third in product(range(3), repeat=3):
        expected = a[first] * b23[second, third] + b13[first, third] * ta[second]
        assert correction[tidx(first, second, third)] == expected
    print("coordinate relation profiles: PASS ((3,2)/(2,2) and graph correction)")


def check_binary_five_product_lemma() -> None:
    # Full-support u: the square kernel is the two scaling-difference plane.
    u = e9(0) + e9(3) + e9(6)
    square_kernel = sp.Matrix.hstack(e9(0) - e9(3), e9(0) - e9(6))
    assert derivative(u, u) * square_kernel == sp.zeros(27, 2)
    assert derivative(u, u).rank() == 7
    generic = sp.Matrix(sp.symbols("v0:9"))
    full_constraints = derivative(u, generic) * square_kernel
    full_solution = sp.linsolve(list(full_constraints), list(generic))
    parameterization = next(iter(full_solution))
    assert all(
        sp.simplify(parameterization[index] - parameterization[0] * u[index]) == 0
        for index in range(9)
    )

    # Two-source u: its square kernel is X+Y; a third component of v leaves
    # only the conjugate scaling line in that kernel.
    two_u = e9(0) + e9(3)
    xy = sp.Matrix.hstack(*[e9(i) for i in range(6)])
    assert derivative(two_u, two_u) * xy == sp.zeros(27, 6)
    two_v = e9(1) + e9(4) + e9(6)
    assert (derivative(two_u, two_v) * xy).rank() == 5

    # Pure u: the unique rank-one square chart forces the two diagonal images
    # to share the other two factors.
    pure_u = e9(0)
    pure_v = e9(3) + e9(6)
    h = e9(3) - e9(6)
    q_plane = sp.Matrix.hstack(e9(1), h)
    assert derivative(pure_u, pure_v) * q_plane == sp.zeros(27, 2)
    square_image = derivative(pure_v, pure_v) * q_plane
    assert square_image.rank() == 1
    r = e9(2) + 3 * e9(3) - 3 * e9(6)
    assert derivative(r, pure_v) * q_plane == sp.zeros(27, 2)
    other_image = derivative(r, pure_u) * q_plane
    assert other_image.rank() == 1
    assert square_image[:, 0] != sp.zeros(27, 1)
    assert other_image[:, 1] != sp.zeros(27, 1)
    # Both nonzero tensors have their only entries on the same Y/Z indices.
    square_support = [i for i, value in enumerate(square_image[:, 0]) if value]
    other_support = [i for i, value in enumerate(other_image[:, 1]) if value]
    assert square_support == [tidx(1, 0, 0)]
    assert other_support == [tidx(0, 0, 0)]
    print("binary five-product obstruction: PASS (full / two-source / pure)")


def check_square_pencil_lemma() -> None:
    # Two-source square chart: Q has a two-plane in X+Y and one Z lift.
    u = e9(0) + e9(3)
    q_plane = sp.Matrix.hstack(e9(0), e9(3), e9(6))
    square = derivative(u, u) * q_plane
    assert square.rank() == 1
    assert [i for i, value in enumerate(square[:, 2]) if value] == [tidx(0, 0, 0)]

    variables = sp.Matrix(sp.symbols("a0:9"))
    zero_system = derivative(u, variables) * q_plane
    zero_solutions = sp.linsolve(list(zero_system), list(variables))
    zero_form = next(iter(zero_solutions))
    free = sorted(set().union(*(entry.free_symbols for entry in zero_form)), key=str)
    assert len(free) == 1
    assert sp.Matrix(zero_form).subs(free[0], 1) == e9(3) - e9(0)

    # No mixed map into the completely disjoint coordinate line X1 Y1 Z1.
    mixed = derivative(u, variables) * q_plane
    forbidden_rows = [index for index in range(27) if index != tidx(1, 1, 1)]
    forbidden_system = mixed[forbidden_rows, :]
    forbidden_solutions = sp.linsolve(list(forbidden_system), list(variables))
    for solution in forbidden_solutions:
        image = mixed.subs(dict(zip(variables, solution, strict=True)))
        assert image[tidx(1, 1, 1), :] == sp.zeros(1, 3)

    # Full-support square chart with a decomposable tangent output.
    full_u = e9(0) + e9(3) + e9(6)
    full_q = sp.Matrix.hstack(e9(0) - e9(3), e9(0) - e9(6), e9(1))
    full_square = derivative(full_u, full_u) * full_q
    assert full_square.rank() == 1
    assert [i for i, value in enumerate(full_square[:, 2]) if value] == [tidx(1, 0, 0)]
    full_zero = derivative(full_u, variables) * full_q
    assert sp.linsolve(list(full_zero), list(variables)) == {tuple([0] * 9)}
    print("square-pencil factor sharing: PASS (zero-divisor <=1 / disjoint line absent)")


def check_two_rank_two_normal_form() -> None:
    # Colours s=0, c=1, j=2.  The two projection kernels and one linked
    # quotient vector give the complete three-plane.
    tau = sp.Rational(5)
    k12 = sp.Matrix.hstack(
        sp.Matrix.vstack(e3(0), sp.zeros(3, 1)),
        sp.Matrix.vstack(sp.zeros(3, 1), e3(1)),
        sp.Matrix.vstack(e3(2), tau * e3(2)),
    )
    relation = sp.Matrix.hstack(
        sp.Matrix.vstack(e3(1), sp.zeros(3, 1)),
        sp.Matrix.vstack(sp.zeros(3, 1), e3(0)),
        sp.Matrix.vstack(-tau * e3(2), e3(2)),
    )
    assert k12.rank() == relation.rank() == 3
    assert k12.T * relation == sp.zeros(3, 3)

    # A coordinate-image atlas block with the required diagonal row is
    # necessarily the matching coordinate monomial.
    z0, z1, z2 = sp.symbols("z0 z1 z2")
    coordinate_image = e3(0) * sp.Matrix([z0, z1, z2]).T
    equations = list(coordinate_image.row(0) - 7 * e3(0).T)
    solution = sp.solve(equations, (z0, z1, z2), dict=True)
    assert solution == [{z0: 7, z1: 0, z2: 0}]

    print("two-rank-two boundary: PASS (normal form / forced diagonal monomial)")


def main() -> None:
    check_coordinate_profiles_and_graph()
    check_binary_five_product_lemma()
    check_square_pencil_lemma()
    check_two_rank_two_normal_form()
    print("balanced m=3 complete common-three-space joint-rank-six exclusion: PASS")


if __name__ == "__main__":
    main()
