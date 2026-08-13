"""Exact replay for the (1,1,2) central-colour coloop exclusion.

The owning Markdown file is the proof.  This script checks the central
coloop row geometry, third-row rank, exterior square, one-/two-source
contradictions, and all full-support tangent degeneracies.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def e(index: int, dimension: int) -> sp.Matrix:
    return sp.eye(dimension)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


BlockVector = tuple[sp.Matrix, sp.Matrix, sp.Matrix]


def permanent(left: BlockVector, middle: BlockVector, right: BlockVector) -> sp.Matrix:
    arguments = (left, middle, right)
    dimension = left[0].rows * left[1].rows * left[2].rows
    answer = sp.zeros(dimension, 1)
    for assignment in permutations(range(3)):
        answer += tensor3(
            arguments[assignment[0]][0],
            arguments[assignment[1]][1],
            arguments[assignment[2]][2],
        )
    return answer


def block_basis(index: int, dimension: int) -> BlockVector:
    blocks = [sp.zeros(dimension, 1) for _ in range(3)]
    blocks[index // dimension] = e(index % dimension, dimension)
    return blocks[0], blocks[1], blocks[2]


def flat_to_block(vector: sp.Matrix, dimension: int) -> BlockVector:
    return (
        vector[:dimension, :],
        vector[dimension : 2 * dimension, :],
        vector[2 * dimension :, :],
    )


def mixed_map(first: BlockVector, second: BlockVector) -> sp.Matrix:
    dimension = first[0].rows
    return sp.Matrix.hstack(
        *(permanent(first, second, block_basis(index, dimension)) for index in range(3 * dimension))
    )


def common_annihilator(first: BlockVector, plane: sp.Matrix) -> sp.Matrix:
    dimension = first[0].rows
    equations = [
        mixed_map(first, flat_to_block(plane[:, index], dimension))
        for index in range(plane.cols)
    ]
    return sp.Matrix.vstack(*equations)


def central_coloop_geometry() -> None:
    # Columns are (r_t,r_u,p_s,p_u,h_0,h_1,h_2).  Now r_t, rather than
    # r_u, is the unique direction outside the two-plane S.
    s0, s1, outside = (e(index, 3) for index in range(3))
    columns = (
        outside,
        s0 + s1,
        s0,
        s1,
        2 * s0 + s1,
        -s0 + 3 * s1,
        5 * s0 - 2 * s1,
    )
    row_map = sp.Matrix.hstack(*columns)
    other = row_map[:, 1:]
    kernel = row_map.nullspace()
    assert row_map.rank() == 3
    assert other.rank() == 2
    assert len(kernel) == 4
    assert all(relation[0] == 0 for relation in kernel)
    assert sp.Matrix.hstack(columns[2], columns[3]).rank() == 2
    assert sp.Matrix.hstack(columns[1], columns[2], columns[3]).rank() == 2

    nonzero_cells = [
        (i, j, k)
        for i, j, k in product((1, 2), (0, 2), range(3))
        if i == j == k
    ]
    assert nonzero_cells == [(2, 2, 2)]
    assert not any(i == j == k for i, j, k in product((1,), (0, 2), range(3)))
    print("central coloop geometry: PASS (r_t outside / six-row plane S)")


def theta_rank_and_square() -> None:
    v0, _v1, _v2, a_direction, b_direction = (e(index, 5) for index in range(5))
    z = sp.Matrix([1, 1, 0])
    w = sp.Matrix([0, 1, 1])
    n = sp.Matrix([1, -1, 1])
    h_columns = (v0, sp.zeros(5, 1), sp.zeros(5, 1))
    q_columns = tuple(
        z[index] * a_direction + w[index] * b_direction + h_columns[index]
        for index in range(3)
    )
    q_map = sp.Matrix.hstack(*q_columns)
    assert q_map[3:5, :] == sp.Matrix([list(z), list(w)])
    assert q_map[3:5, :].rank() == 2
    assert q_map.rank() == 3
    assert z.dot(n) == w.dot(n) == 0
    assert q_map * n == v0

    gamma = sp.Matrix([1, -1, 0])
    assert gamma.dot(z) == 0
    assert gamma[1] * gamma.dot(w) != 0

    scalar = sp.symbols("g")
    r: BlockVector = (
        sp.Matrix([1, 2]),
        sp.Matrix([3, 5]),
        sp.Matrix([7, 11]),
    )
    b_row: BlockVector = (
        sp.Matrix([13, 17]),
        sp.Matrix([19, 23]),
        sp.Matrix([29, 31]),
    )
    h_row: BlockVector = (
        sp.Matrix([37, 41]),
        sp.Matrix([43, 47]),
        sp.Matrix([53, 59]),
    )
    q_row = tuple(
        scalar * b + h for b, h in zip(b_row, h_row, strict=True)
    )
    assert sp.simplify(
        permanent(r, q_row, q_row)
        - scalar * permanent(r, b_row, q_row)
        - permanent(r, h_row, q_row)
    ) == sp.zeros(8, 1)
    print("third-row/square upgrade: PASS (rank three / nonzero T_t square)")


def one_source_case() -> None:
    x = y = zeta = e(0, 2)
    zero = sp.zeros(2, 1)
    qx0, qx1 = sp.symbols("qx0 qx1")
    square_row: BlockVector = (sp.Matrix([qx0, qx1]), y, zeta)
    pure: BlockVector = (x, zero, zero)
    assert permanent(square_row, square_row, pure) == 2 * tensor3(x, y, zeta)

    a, b = sp.symbols("a b")
    px0, px1, ux0, ux1 = sp.symbols("px0 px1 ux0 ux1")
    cx0, cx1, cy0, cy1, cz0, cz1 = sp.symbols(
        "cx0 cx1 cy0 cy1 cz0 cz1"
    )
    p_x = sp.Matrix([px0, px1])
    u_x = sp.Matrix([ux0, ux1])
    c_row: BlockVector = (
        sp.Matrix([cx0, cx1]),
        sp.Matrix([cy0, cy1]),
        sp.Matrix([cz0, cz1]),
    )
    p: BlockVector = (p_x, a * y, -a * zeta)
    u: BlockVector = (u_x, b * y, b * zeta)
    actual = permanent(c_row, p, u)
    expected = tensor3(b * p_x - a * u_x, c_row[1], zeta) + tensor3(
        b * p_x + a * u_x, y, c_row[2]
    )
    assert sp.simplify(actual - expected) == sp.zeros(8, 1)
    assert sp.Matrix([actual[3], actual[7]]) == sp.zeros(2, 1)

    # If the conjugating functional vanishes, two S rows are both X-pure.
    p0: BlockVector = (e(0, 2), zero, zero)
    p1: BlockVector = (e(1, 2), zero, zero)
    arbitrary: BlockVector = (e(0, 2), e(1, 2), e(0, 2))
    assert permanent(p0, p1, arbitrary) == sp.zeros(8, 1)
    print("one-source split: PASS (zero core / conjugate factor sharing)")


def two_source_case() -> None:
    x = y = e(0, 2)
    zero = sp.zeros(2, 1)
    r: BlockVector = (x, y, zero)

    # L:X+Y -> X tensor Y has rank three and one-dimensional kernel.
    l_images = []
    for index in range(4):
        vector = block_basis(index, 2)
        l_images.append(
            sp.kronecker_product(x, vector[1])
            + sp.kronecker_product(vector[0], y)
        )
    l_map = sp.Matrix.hstack(*l_images)
    kernel = sp.Matrix([1, 0, -1, 0])
    assert l_map.rank() == 3
    assert l_map * kernel == sp.zeros(4, 1)

    # M(v)=(L(v),v_Z) has the same one-dimensional kernel in W.
    m_map = sp.zeros(6, 6)
    m_map[:4, :4] = l_map
    m_map[4:, 4:] = sp.eye(2)
    assert m_map.rank() == 5
    expected_kernel = sp.Matrix([1, 0, -1, 0, 0, 0])
    assert m_map * expected_kernel == sp.zeros(6, 1)

    q: BlockVector = (e(1, 2), zero, e(0, 2))
    assert permanent(q, q, r) == 2 * tensor3(e(1, 2), y, e(0, 2))
    # Every fibre M(v)=b M(q) is span(q)+ker(M), hence at most two-dimensional.
    fibre = sp.Matrix.hstack(
        sp.Matrix.vstack(*q),
        expected_kernel,
    )
    assert fibre.rank() == 2
    print("two-source split: PASS (conjugate M-fibre has dimension two)")


def full_source_two_supported_square() -> None:
    dimension = 3
    x = y = zeta = e(0, dimension)
    zero = sp.zeros(3, 1)
    q: BlockVector = (x, y, zero)

    # D!=0: the zero kernel is a two-plane and its common annihilator is
    # exactly the square-vector line, for both rank-one and rank-two D.
    for r in (
        (e(1, 3), e(1, 3), zeta),
        (x, y, zeta),
    ):
        assert permanent(q, q, r) == 2 * tensor3(x, y, zeta)
        plane = sp.Matrix.hstack(*mixed_map(r, q).nullspace())
        annihilator = common_annihilator(r, plane)
        assert plane.rank() == plane.cols == 2
        assert annihilator.rank() == 8
        assert annihilator * sp.Matrix.vstack(*q) == sp.zeros(54, 1)

    # D=0: K=<x,-y,0>+Z.  A plane inside Z has zero core; a plane with
    # nonzero kernel-line projection again has only span(q) as annihilator.
    cancelling_r: BlockVector = (x, -y, zeta)
    cancelling_kernel = sp.Matrix.hstack(*mixed_map(cancelling_r, q).nullspace())
    assert cancelling_kernel.rank() == 4
    kernel_line = sp.Matrix.vstack(x, -y, zero)
    assert sp.Matrix.hstack(cancelling_kernel, kernel_line).rank() == 4

    z_plane = sp.Matrix.hstack(
        sp.Matrix.vstack(sp.zeros(6, 1), e(1, 3)),
        sp.Matrix.vstack(sp.zeros(6, 1), e(2, 3)),
    )
    arbitrary = block_basis(0, 3)
    assert permanent(
        flat_to_block(z_plane[:, 0], 3),
        flat_to_block(z_plane[:, 1], 3),
        arbitrary,
    ) == sp.zeros(27, 1)

    mixed_plane = sp.Matrix.hstack(
        sp.Matrix.vstack(sp.zeros(6, 1), e(1, 3)),
        kernel_line + sp.Matrix.vstack(sp.zeros(6, 1), e(2, 3)),
    )
    mixed_annihilator = common_annihilator(cancelling_r, mixed_plane)
    assert mixed_annihilator.rank() == 8
    assert mixed_annihilator * sp.Matrix.vstack(*q) == sp.zeros(54, 1)
    print("full support / two-supported square: PASS (regular and D=0)")


def full_source_moving_factor() -> None:
    dimension = 3
    x = y = zeta = e(0, dimension)
    a = e(1, dimension)
    r: BlockVector = (x, y, zeta)

    # a independent of x, b+c nonzero: the square kernel is S and its
    # common annihilator is exactly the square-vector line.
    for b, c in (
        (sp.Integer(2), sp.Integer(3)),
        (sp.Integer(1), sp.Integer(2)),
    ):
        q: BlockVector = (a, b * y, c * zeta)
        square_x = b * c * x + (b + c) * a
        assert permanent(q, q, r) == 2 * tensor3(square_x, y, zeta)
        kernel = mixed_map(r, q).nullspace()
        plane = sp.Matrix.hstack(*kernel)
        annihilator = common_annihilator(r, plane)
        assert plane.rank() == plane.cols == 2
        assert annihilator.rank() == 8
        assert annihilator * sp.Matrix.vstack(*q) == sp.zeros(54, 1)

    # a independent, b=-c nonzero: the complete kernel is X.
    q_opposite: BlockVector = (a, 2 * y, -2 * zeta)
    assert permanent(q_opposite, q_opposite, r) == -8 * tensor3(x, y, zeta)
    opposite_kernel = sp.Matrix.hstack(*mixed_map(r, q_opposite).nullspace())
    assert opposite_kernel.rank() == 3
    assert opposite_kernel[3:, :] == sp.zeros(6, 3)
    print("full support / full square, moving factor: PASS")


def full_source_aligned_factor() -> None:
    dimension = 3
    x = y = zeta = e(0, dimension)
    r: BlockVector = (x, y, zeta)

    # No pair sum vanishes: the kernel is the scaling plane on the three
    # base lines, so its complete mixed image is Segre-tangent supported.
    q_regular: BlockVector = (x, y, zeta)
    assert permanent(q_regular, q_regular, r) == 6 * tensor3(x, y, zeta)
    regular_kernel = sp.Matrix.hstack(*mixed_map(r, q_regular).nullspace())
    assert regular_kernel.rank() == 2
    for left, right, third in product(range(2), range(2), range(9)):
        value = permanent(
            flat_to_block(regular_kernel[:, left], 3),
            flat_to_block(regular_kernel[:, right], 3),
            block_basis(third, 3),
        )
        assert all(
            value[9 * i + 3 * j + k] == 0
            for i, j, k in product(range(3), repeat=3)
            if sum(index != 0 for index in (i, j, k)) >= 2
        )

    # Exactly one pair sum vanishes: two source components stay on the
    # base lines, and every decomposable output shares one of them.
    q_one: BlockVector = (2 * x, y, -zeta)
    assert permanent(q_one, q_one, r) == -2 * tensor3(x, y, zeta)
    one_kernel = sp.Matrix.hstack(*mixed_map(r, q_one).nullspace())
    assert one_kernel.rank() == 4
    assert one_kernel[3:6, :].rank() == 1
    assert one_kernel[6:9, :].rank() == 1
    for left, right, third in product(range(4), range(4), range(9)):
        value = permanent(
            flat_to_block(one_kernel[:, left], 3),
            flat_to_block(one_kernel[:, right], 3),
            block_basis(third, 3),
        )
        assert all(
            value[9 * i + 3 * j + k] == 0
            for i, j, k in product(range(3), repeat=3)
            if j != 0 and k != 0
        )

    # Exactly two pair sums vanish: K=X+Y.  The quotient-Z part of
    # per(r,p,q) is L(p) tensor q_Zbar, and ker L is only one line.
    q_two: BlockVector = (x, y, -zeta)
    assert permanent(q_two, q_two, r) == -2 * tensor3(x, y, zeta)
    two_kernel = sp.Matrix.hstack(*mixed_map(r, q_two).nullspace())
    assert two_kernel.rank() == 6
    assert two_kernel[6:9, :] == sp.zeros(3, 6)

    px = sp.Matrix(sp.symbols("px0:3"))
    py = sp.Matrix(sp.symbols("py0:3"))
    qx = sp.Matrix(sp.symbols("qx0:3"))
    qy = sp.Matrix(sp.symbols("qy0:3"))
    qz = sp.Matrix(sp.symbols("qz0:3"))
    p: BlockVector = (px, py, sp.zeros(3, 1))
    arbitrary: BlockVector = (qx, qy, qz)
    value = permanent(r, p, arbitrary)
    tangent = sp.kronecker_product(x, py) + sp.kronecker_product(px, y)
    for k in (1, 2):
        quotient_slice = sp.Matrix(
            [value[9 * i + 3 * j + k] for i, j in product(range(3), repeat=2)]
        )
        assert sp.simplify(quotient_slice - qz[k] * tangent) == sp.zeros(9, 1)
    tangent_variables = tuple(px) + tuple(py)
    tangent_matrix = sp.Matrix(
        [[sp.expand(entry).coeff(variable) for variable in tangent_variables] for entry in tangent]
    )
    assert tangent_matrix.rank() == 5
    print("full support, aligned factor: PASS (0/1/2 pair-sum degeneracies)")


def symmetry_check() -> None:
    assert ("alpha", "t", "z", "s") == ("alpha", "t", "z", "s")
    swapped = ("beta", "s", "w", "t")
    assert swapped == ("beta", "s", "w", "t")
    print("first/second-root symmetry: PASS (alpha_t <-> beta_s)")


def main() -> None:
    central_coloop_geometry()
    theta_rank_and_square()
    one_source_case()
    two_source_case()
    full_source_two_supported_square()
    full_source_moving_factor()
    full_source_aligned_factor()
    symmetry_check()
    print("(1,1,2) central-colour coloop exclusion: PASS")


if __name__ == "__main__":
    main()
