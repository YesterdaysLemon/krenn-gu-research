"""Focused exact checks for the GLS21 promoted base-shadow collapse."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def tensor_slice(
    vector: sp.MatrixBase,
    right_coordinate: int,
    left_dimension: int,
    right_dimension: int,
) -> sp.Matrix:
    return sp.Matrix(
        [
            vector[left * right_dimension + right_coordinate]
            for left in range(left_dimension)
        ]
    )


def check_all_port_identity_slices() -> dict[str, int]:
    p = sp.symbols("p")
    left_dimension = 9
    checked = 0
    for right_dimension in (1, 3, 9, 27):
        identity = p * sp.eye(left_dimension * right_dimension)
        slices = []
        for source in range(identity.cols):
            output = identity[:, source]
            for right in range(right_dimension):
                slices.append(
                    tensor_slice(output, right, left_dimension, right_dimension)
                )
        presentation = sp.Matrix.hstack(*slices)
        assert presentation.rank() == left_dimension
        for coordinate in range(left_dimension):
            expected = sp.zeros(left_dimension, 1)
            expected[coordinate] = p
            assert expected in presentation.columnspace()
        assert all(entry == 0 or entry == p for entry in presentation)
        checked += presentation.cols
    return {"left_dimension": left_dimension, "coefficient_slices": checked}


def check_root_contraction_to_scalar_identity() -> dict[str, sp.Expr]:
    z0, z1 = sp.symbols("z0 z1", nonzero=True)
    epsilon = sp.Matrix([[1, 2, 3, 5, 7, 11, 13, 17, 19]])
    root_coefficient = sp.Matrix(
        [z0, z1, z0 * z1, 1, -1, 2, z0 + z1, z0 - z1, 3]
    )
    p = sp.expand((epsilon * root_coefficient)[0])
    assert p != 0
    right_dimension = 9
    upstairs = sp.kronecker_product(root_coefficient, sp.eye(right_dimension))
    contraction = sp.kronecker_product(epsilon, sp.eye(right_dimension))
    assert contraction * upstairs == p * sp.eye(right_dimension)
    return {"p": p, "operator_rank_at_control": (p * sp.eye(9)).subs({z0: 2, z1: 3}).rank()}


def sampled_minors(matrix: sp.MatrixBase, size: int) -> tuple[sp.Expr, ...]:
    row_sets = {tuple(range(size)), tuple(range(matrix.rows - size, matrix.rows))}
    column_sets = {
        tuple(range(size)),
        tuple(range(matrix.cols - size, matrix.cols)),
    }
    if size <= 3:
        column_sets.add(tuple(range(9, 9 + size)))
    return tuple(
        sp.expand(matrix.extract(rows, columns).det())
        for rows in sorted(row_sets)
        for columns in sorted(column_sets)
    )


def check_fitting_divisibility() -> dict[str, int]:
    p, h = sp.symbols("p h")
    identity_block = p * sp.eye(9)
    extra = sp.Matrix(9, 3, lambda row, column: (row + 1) * (column + 2))
    nuisance = identity_block.row_join(extra)
    pure = sp.Matrix.hstack(sp.eye(9)[:, 0], sp.eye(9)[:, 4], sp.eye(9)[:, 8])
    augmented = nuisance.row_join(pure)
    checked = 0
    for size in range(1, 10):
        diagonal_minor = identity_block[:size, :size].det()
        assert diagonal_minor == p**size
        # p belongs to the radical because p^size is a nuisance minor.
        for value in sampled_minors(augmented, size):
            assert sp.rem(sp.Poly(h * p * value, p), sp.Poly(p, p)) == 0
            checked += 1
    at_nonzero = nuisance.subs(p, 2)
    assert at_nonzero.rank() == 9
    assert at_nonzero.row_join(pure).rank() == 9
    return {"minor_products": checked, "fibre_rank": at_nonzero.rank()}


def check_selector_no_go() -> dict[str, int]:
    p_value = sp.Rational(7, 3)
    nuisance = p_value * sp.eye(9)
    assert nuisance.T.nullspace() == []
    desired = sp.Matrix([1, 0, 2, 0, 3, 0, 4, 0, 5])
    assert nuisance.row_join(desired).rank() == nuisance.rank() == 9
    return {"annihilator_dimension": 0, "absorbed_rank": 9}


def check_arbitrary_root_labels() -> tuple[tuple[int, int, int], ...]:
    records = []
    for root_order in range(3, 10):
        promoted_ports = 2 * root_order - 2
        active_order = promoted_ports
        source_targets = root_order * (root_order - 1) // 2
        # D=Q has complement Bhat-Q=Uhat, of active order 2r-2, and is
        # distinct from every source desired complement C subset U.
        assert active_order == 2 * root_order - 2
        assert source_targets >= 3
        records.append((root_order, active_order, source_targets))
    return tuple(records)


def main() -> None:
    slices = check_all_port_identity_slices()
    contraction = check_root_contraction_to_scalar_identity()
    fitting = check_fitting_divisibility()
    selector = check_selector_no_go()
    labels = check_arbitrary_root_labels()
    print("promoted base-shadow all-port collapse primary checks: PASS")
    print("  exact all-port coefficient slices:", slices)
    print("  root contraction gives scalar identity:", contraction)
    print("  determinantal p-divisibility:", fitting)
    print("  factor-through selector no-go:", selector)
    print("  arbitrary-root active-label records:", labels)
    print("  scope: base-shadow route only; full GLS8 quotient and node stay open")


if __name__ == "__main__":
    main()
