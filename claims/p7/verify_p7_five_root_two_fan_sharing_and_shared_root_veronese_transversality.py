"""Verify five-root two-fan sharing and shared-root transversality."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

PAIRS = tuple(combinations(range(4), 2))


def fan_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Return the flattened mixed permanental compound."""
    return sp.Matrix.hstack(
        *(
            sp.kronecker_product(left[:, first], right[:, second])
            + sp.kronecker_product(left[:, second], right[:, first])
            for first, second in PAIRS
        )
    )


def hollow(face: sp.Matrix) -> sp.Matrix:
    """Make the hollow symmetric matrix with the given pair coordinates."""
    result = sp.zeros(4)
    for index, (first, second) in enumerate(PAIRS):
        result[first, second] = result[second, first] = face[index]
    return result


def veronese_matrix(kernel_basis: sp.Matrix) -> sp.Matrix:
    """Evaluate binary quadrics on the rows of a 4-by-2 kernel basis."""
    return sp.Matrix(
        [
            (row[0] ** 2, 2 * row[0] * row[1], row[1] ** 2)
            for row in kernel_basis.tolist()
        ]
    )


def bilinear(left: sp.Matrix, block: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Evaluate a bilinear edge block."""
    return sp.expand((left.T * block * right)[0])


def recovered_incidence(incidence: sp.Matrix) -> sp.Matrix:
    """Recover tangent-to-port columns from the physical 3-by-3 blocks."""
    frozen_port = sp.Matrix((1, 1, 1))
    beta = sp.Matrix(((1, 0, 0),))
    tangent = sp.Matrix.hstack(sp.eye(3)[:, 1], sp.eye(3)[:, 2])
    columns = []
    for port in range(4):
        first, second = incidence[:, port]
        covector = sp.Matrix((-(first + second), first, second))
        block = covector * beta
        columns.append(tangent.T * block * frozen_port)
    return sp.Matrix.hstack(*columns)


def main() -> None:
    face = sp.Matrix(sp.symbols("x0:6"))

    common = sp.Matrix(((-1, -1, 1, 0), (-1, -2, 0, 1)))
    other_one = sp.Matrix(((1, 0, 0, 0), (0, 1, 0, 0)))
    other_two = sp.Matrix(((0, 0, 1, 0), (0, 0, 0, 1)))
    combined_other = other_one.col_join(other_two)
    kernel_basis = sp.Matrix(((1, 0), (0, 1), (1, 1), (1, 2)))

    assert combined_other == sp.eye(4)
    assert common.rank() == 2
    assert common * kernel_basis == sp.zeros(2, 2)
    assert kernel_basis.rank() == 2

    fan_one = fan_matrix(common, other_one)
    fan_two = fan_matrix(common, other_two)
    sandwich_one = common * hollow(face) * other_one.T
    sandwich_two = common * hollow(face) * other_two.T
    assert fan_one * face == sp.Matrix(list(sandwich_one))
    assert fan_two * face == sp.Matrix(list(sandwich_two))
    assert fan_one.rank() == fan_two.rank() == 4
    assert fan_one.col_join(fan_two).rank() == 6
    assert fan_one.col_join(fan_two).nullspace() == []

    veronese = veronese_matrix(kernel_basis)
    assert veronese.rank() == 3
    symmetric_coordinates = sp.Matrix(sp.symbols("s0:3"))
    symmetric = sp.Matrix(
        (
            (symmetric_coordinates[0], symmetric_coordinates[1]),
            (symmetric_coordinates[1], symmetric_coordinates[2]),
        )
    )
    lifted = kernel_basis * symmetric * kernel_basis.T
    assert sp.Matrix([lifted[index, index] for index in range(4)]) == (
        veronese * symmetric_coordinates
    )

    boundary_common = sp.Matrix(((1, -1, 0, 0), (0, 0, 1, -1)))
    boundary_kernel = sp.Matrix(((1, 0), (1, 0), (0, 1), (0, 1)))
    boundary_one = sp.Matrix(((1, 0, 1, 1), (0, 1, 1, 2)))
    boundary_two = sp.Matrix(((1, 0, 1, 2), (0, 1, 2, 1)))
    boundary_combined = boundary_one.col_join(boundary_two)
    boundary_fan_one = fan_matrix(boundary_common, boundary_one)
    boundary_fan_two = fan_matrix(boundary_common, boundary_two)
    boundary_stack = boundary_fan_one.col_join(boundary_fan_two)
    common_face = sp.Matrix((0, 1, 1, 1, 1, 0))

    assert boundary_common * boundary_kernel == sp.zeros(2, 2)
    assert boundary_combined.det() == -1
    assert veronese_matrix(boundary_kernel).rank() == 2
    assert boundary_fan_one.rank() == boundary_fan_two.rank() == 4
    assert boundary_stack.rank() == 5
    assert boundary_stack * common_face == sp.zeros(8, 1)
    assert len(boundary_stack.nullspace()) == 1

    disjoint_left_one = sp.Matrix(((1, 0, 1, 0), (0, 1, 0, 1)))
    disjoint_right_one = sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0)))
    disjoint_left_two = boundary_one
    disjoint_right_two = boundary_two
    disjoint_fan_one = fan_matrix(disjoint_left_one, disjoint_right_one)
    disjoint_fan_two = fan_matrix(disjoint_left_two, disjoint_right_two)
    assert disjoint_fan_one.rank() == disjoint_fan_two.rank() == 4
    assert disjoint_fan_one.col_join(disjoint_fan_two).rank() == 6

    change_left = sp.Matrix(((1, 1), (0, 1)))
    change_right = sp.Matrix(((2, 0), (1, 1)))
    repolarized = fan_matrix(
        change_left * disjoint_left_one,
        change_right * disjoint_right_one,
    )
    assert repolarized == (
        sp.kronecker_product(change_left, change_right) * disjoint_fan_one
    )
    assert repolarized.nullspace() == disjoint_fan_one.nullspace()

    roots = set(range(5))
    equal_pair = {0, 1}
    shared_pair = {0, 2}
    disjoint_pair = {2, 3}
    assert len((roots - equal_pair) & (roots - equal_pair)) == 3
    assert len((roots - equal_pair) & (roots - shared_pair)) == 2
    assert len((roots - equal_pair) & (roots - disjoint_pair)) == 1
    assert equal_pair <= roots - disjoint_pair
    assert disjoint_pair <= roots - equal_pair

    shore_matrix = sp.ones(3)
    assert shore_matrix.per() == 6

    frozen = sp.Matrix((1, 1, 1))
    alpha = sp.Matrix(((1, 0, 0),))
    beta = sp.Matrix(((1, 0, 0),))
    projection = sp.eye(3) - frozen * alpha
    tangent_one = sp.eye(3)[:, 1]
    tangent_two = sp.eye(3)[:, 2]
    blocker = alpha.T * beta
    assert projection * frozen == sp.zeros(3, 1)
    assert projection * tangent_one == tangent_one
    assert projection * tangent_two == tangent_two
    assert bilinear(frozen, blocker, frozen) == 1
    assert bilinear(tangent_one, blocker, frozen) == 0
    assert bilinear(tangent_two, blocker, frozen) == 0

    for incidence in (
        common,
        other_one,
        other_two,
        disjoint_left_one,
        disjoint_right_one,
        disjoint_left_two,
        disjoint_right_two,
    ):
        assert recovered_incidence(incidence) == incidence

    print("PASS: exhaustive equal/shared/disjoint five-root shore geometry")
    print("PASS: exact shared-root Veronese kernel dichotomy")
    print("PASS: shared-root rank-six and sharp rank-five controls")
    print("PASS: disjoint rank-six control with a common fifth shore root")
    print("PASS: common torus P7 edge blocks and unit pure shore rows")
    print("SCOPE: target GHZ and forced legal occurrence remain UNKNOWN")
    print("searches=0 graph_enumerations=0 support_enumerations=0")


if __name__ == "__main__":
    main()
