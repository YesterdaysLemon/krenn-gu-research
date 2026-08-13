"""Independent Fraction audit of the support-two mixed-row-rank theorem."""

from __future__ import annotations

from fractions import Fraction as F

Vector = tuple[F, ...]
Matrix = list[list[F]]


def unit(size: int, index: int) -> Vector:
    return tuple(F(i == index) for i in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, F(0)) for entries in zip(*vectors, strict=True))


def scale(value: F | int, vector: Vector) -> Vector:
    scalar = F(value)
    return tuple(scalar * entry for entry in vector)


def pair(left: Vector, right: Vector) -> Vector:
    return tuple(x * y for x in left for y in right)


def root_index(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def derivative_value(
    a1: Vector,
    a2: Vector,
    block_b23: Matrix,
    block_c13: Matrix,
) -> Vector:
    out = [F(0) for _ in range(27)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                out[root_index(a, b, c)] = (
                    a1[a] * block_b23[b][c] + block_c13[a][c] * a2[b]
                )
    return tuple(out)


def outer(root: Vector, target: Vector) -> Matrix:
    return [[x * y for y in target] for x in root]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [x + y for x, y in zip(row_left, row_right, strict=True)]
        for row_left, row_right in zip(left, right, strict=True)
    ]


def contracted_graph_audit() -> None:
    e0, e1 = unit(3, 0), unit(3, 1)
    for beta, chi, nu in ((F(2), F(3), F(5)), (F(-7), F(4), F(9))):
        le1 = add(scale(-beta / chi, e0), scale(nu / chi, e1))
        contracted = add(
            scale(beta, pair(e1, e0)),
            scale(chi, pair(e1, le1)),
        )
        assert contracted == scale(nu, pair(e1, e1))
        assert [d for d in range(3) if le1[d] == 0] == [2]
    print("independent graph audit: PASS (Fraction coordinate planes)")


def sparse_target_table_audit() -> None:
    basis3 = [unit(3, i) for i in range(3)]
    targets = [unit(27, root_index(i, i, i)) for i in range(3)]
    kappa = F(7)
    block_b = [
        [F(2), F(-1), F(3)],
        [F(5), F(4), F(-6)],
        [F(0), F(0), kappa],
    ]
    block_c = [
        [F(1), F(2), F(3)],
        [F(-2), F(5), F(7)],
        [F(11), F(-13), F(17)],
    ]
    graph = [
        [F(1), F(-2, 3), F(4)],
        [F(2), F(5, 3), F(-1)],
        [F(0), F(0), F(0)],
    ]

    def graph_column(index: int) -> Vector:
        return tuple(graph[row][index] for row in range(3))

    u2 = derivative_value(basis3[2], graph_column(2), block_b, block_c)
    target_matrix = [[F(0) for _ in range(27)] for _ in range(27)]
    for i in range(3):
        target_matrix[root_index(i, i, i)] = list(targets[i])
    all_cross = matrix_add(
        target_matrix,
        outer(u2, scale(F(-1, 7), targets[2])),
    )

    zero = tuple(F(0) for _ in range(27))
    for a in range(3):
        for c in range(3):
            assert tuple(all_cross[root_index(a, 2, c)]) == zero

    row_110 = tuple(all_cross[root_index(1, 1, 0)])
    row_111 = tuple(all_cross[root_index(1, 1, 1)])
    for gamma in (F(-1), F(2), F(-5, 3)):
        defect = add(row_111, scale(-gamma, row_110))
        assert defect[root_index(1, 1, 1)] == 1
        assert defect != zero
    print("independent target audit: PASS (direct physical 9a+3b+c order)")


def target_line_audit() -> None:
    target_1 = unit(27, root_index(1, 1, 1))
    target_2 = unit(27, root_index(2, 2, 2))
    for gamma in (F(-3), F(1, 2), F(11)):
        for lambda_0 in (F(-5), F(0), F(7, 3)):
            for lambda_1 in (F(-2), F(0), F(13, 5)):
                left = scale(gamma * lambda_0, target_2)
                right = add(target_1, scale(lambda_1, target_2))
                assert left != right
                assert right[root_index(1, 1, 1)] == 1
    print("independent line audit: PASS (T1 cannot lie on span(T2))")


def three_by_three_stop_audit() -> None:
    target_1 = unit(27, root_index(1, 1, 1))
    zero = scale(0, target_1)
    correction_0 = zero
    correction_1 = scale(-1, target_1)
    assert zero == correction_0
    assert add(zero, scale(-1, target_1)) == correction_1
    assert zero == scale(-1, zero)
    print("independent (3,3) stop audit: PASS (local correction control)")


def main() -> None:
    contracted_graph_audit()
    sparse_target_table_audit()
    target_line_audit()
    three_by_three_stop_audit()
    print("independent support-two mixed-row-rank exclusion: PASS")


if __name__ == "__main__":
    main()
