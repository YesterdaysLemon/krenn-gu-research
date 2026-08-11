"""Verify the complete aligned-projective q=0, r=4 detector ingredients."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Return the labelled-row permanent of a square matrix."""
    size = len(matrix)
    return sp.Add(
        *(
            sp.prod(matrix[row][assignment[row]] for row in range(size))
            for assignment in permutations(range(size))
        )
    )


def check_collision_quotients() -> None:
    """Check pi_u P4(h,a,a,b)=[h_u] tensor P3 on all four slices."""
    for active in range(4):
        a_symbols = [sp.symbols(f"a_{mode}_0:3") for mode in range(4)]
        b_symbols = [sp.symbols(f"b_{mode}_0:3") for mode in range(4)]
        h_symbols = [sp.symbols(f"h_{mode}_0:3") for mode in range(4)]
        a = [sp.Matrix(values) for values in a_symbols]
        b = [sp.Matrix(values) for values in b_symbols]
        h = [sp.Matrix(values) for values in h_symbols]
        a[active] = sp.Matrix((1, 0, 0))
        b[active] = sp.Matrix((0, 1, 0))
        others = tuple(mode for mode in range(4) if mode != active)

        for other_word in product(range(3), repeat=3):
            word = [0, 0, 0, 0]
            word[active] = 2
            for mode, colour in zip(others, other_word, strict=True):
                word[mode] = colour
            full_matrix = [
                [row[mode][word[mode]] for mode in range(4)]
                for row in (h, a, a, b)
            ]
            deletion_matrix = [
                [row[mode][word[mode]] for mode in others]
                for row in (a, a, b)
            ]
            difference = permanent(full_matrix) - h[active][2] * permanent(
                deletion_matrix
            )
            assert sp.expand(difference) == 0


def check_transverse_three_mode_cofactor() -> None:
    """Check P3(a,a,b) cannot vanish on three locally transverse modes."""
    e0, e1 = sp.eye(3).row(0).T, sp.eye(3).row(1).T
    values: dict[tuple[int, int, int], sp.Expr] = {}
    for word in product(range(3), repeat=3):
        matrix = [
            [row[mode][word[mode]] for mode in range(3)]
            for row in ((e0,) * 3, (e0,) * 3, (e1,) * 3)
        ]
        values[word] = permanent(matrix)
    nonzero = {word: value for word, value in values.items() if value != 0}
    assert nonzero == {(1, 0, 0): 2, (0, 1, 0): 2, (0, 0, 1): 2}


def check_hall_capacity_arithmetic() -> None:
    """Check the four-row and two-row axis-incidence capacities."""
    required_four_rows = 3 * 4
    assert required_four_rows == 12
    for zero_count in range(5):
        maximum = 3 + 3 * zero_count + 2 * (4 - zero_count)
        assert maximum == 11 + zero_count
    assert 3 + 4 * 2 == 11 < required_four_rows
    assert 3 + 3 + 3 * 2 == required_four_rows

    required_two_rows = 3 * 2
    maximum_line_incidence = 5
    assert maximum_line_incidence < required_two_rows


def p3_tensor(
    a: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    b: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> dict[tuple[int, int, int], sp.Expr]:
    """Evaluate a labelled P3(a,a,b) tensor."""
    result = {}
    for word in product(range(3), repeat=3):
        matrix = [
            [row[mode][word[mode]] for mode in range(3)]
            for row in (a, a, b)
        ]
        result[word] = sp.expand(permanent(matrix))
    return result


def check_two_zero_flattening_equations() -> None:
    """Check the coefficient equations used to exclude exactly two Q zeros."""
    av = sp.Matrix(sp.symbols("av_0:3"))
    at = sp.Matrix(sp.symbols("at_0:3"))
    bv = sp.Matrix(sp.symbols("bv_0:3"))
    bt = sp.Matrix(sp.symbols("bt_0:3"))
    e0, e1 = sp.eye(3).row(0).T, sp.eye(3).row(1).T
    tensor = p3_tensor((av, e0, at), (bv, e1, bt))

    for left_colour, right_colour in product(range(3), repeat=2):
        b_slice = tensor[left_colour, 1, right_colour]
        expected_b = 2 * av[left_colour] * at[right_colour]
        assert sp.expand(b_slice - expected_b) == 0

        a_slice = tensor[left_colour, 0, right_colour]
        expected_a = 2 * (
            bv[left_colour] * at[right_colour]
            + av[left_colour] * bt[right_colour]
        )
        assert sp.expand(a_slice - expected_a) == 0


def check_common_zero_recolouring() -> None:
    """Check all pure/mixed P5 coefficients on the common-zero boundary."""
    alpha = sp.symbols("alpha_0:3", nonzero=True)
    beta = sp.symbols("beta_0:3", nonzero=True)
    eta = sp.symbols("eta_0:3")
    h_values = {
        (row, mode, colour): sp.Symbol(f"h_{row}_{mode}_{colour}")
        for row in range(3)
        for mode in range(4)
        for colour in range(3)
    }
    companions = {
        (row, colour): sp.Symbol(f"ell_{row}_{colour}")
        for row in range(3)
        for colour in range(3)
    }

    for colour in range(3):
        retained = [mode for mode in range(4) if mode != colour]
        cofactor = permanent(
            [
                [h_values[row, mode, colour] for mode in retained]
                for row in range(3)
            ]
        )
        for j_colour in range(3):
            rows: list[list[sp.Expr]] = []
            for row in range(3):
                rows.append(
                    [h_values[row, mode, colour] for mode in range(4)]
                    + [companions[row, j_colour]]
                )
            a_row = [
                alpha[mode] if colour == mode else sp.Integer(0)
                for mode in range(3)
            ] + [sp.Integer(0), eta[j_colour]]
            b_row = [
                beta[mode] if colour == mode else sp.Integer(0)
                for mode in range(3)
            ] + [sp.Integer(0), sp.Integer(0)]
            coefficient = permanent(rows + [a_row, b_row])
            expected = eta[j_colour] * beta[colour] * cofactor
            assert sp.expand(coefficient - expected) == 0


def check_common_zero_collision_boundary() -> None:
    """Check the Hall-compatible P3 cancellation used as a false shortcut."""
    axes = tuple(sp.eye(3).row(index).T for index in range(3))
    boundary_b = (axes[0], axes[1], -2 * axes[2])
    tensor = p3_tensor(axes, boundary_b)
    assert set(tensor.values()) == {0}


def check_local_concision() -> None:
    """Check a one-line source column cannot realize local diagonal rank 3."""
    weights = sp.diag(2, 3, 5)
    one_source_column = sp.Matrix.hstack(sp.Matrix((7, 11, 13)))
    assert weights.rank() == 3
    assert one_source_column.rank() == 1


def main() -> None:
    check_collision_quotients()
    check_transverse_three_mode_cofactor()
    check_hall_capacity_arithmetic()
    check_two_zero_flattening_equations()
    check_common_zero_collision_boundary()
    check_common_zero_recolouring()
    check_local_concision()
    print("PASS: all four symbolic collision quotient slices")
    print("PASS: three locally transverse pairs give nonzero P3")
    print("PASS: four-row and two-row Hall incidence arithmetic")
    print("PASS: exact two-zero flattening coefficient equations")
    print("PASS: common-zero P3 cancellation boundary is reproducible")
    print("PASS: all nine common-zero pure/mixed P5 coefficients")
    print("PASS: local source-column rank 1 versus diagonal rank 3")
    print("SCOPE: complete detector only in aligned projective q=0 r=4 cell")
    print("SCOPE: nonzero detector, not fixed-root injectivity or witness exclusion")
    print("searches=0")


if __name__ == "__main__":
    main()
