"""Verify the lifted row quotas and minimal-cell two-open detector."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Return a labelled-row permanent."""
    size = len(matrix)
    return sp.Add(
        *(
            sp.prod(matrix[row][assignment[row]] for row in range(size))
            for assignment in permutations(range(size))
        )
    )


def check_hall_quotas() -> None:
    """Check the exact mode counts imported from repeated-row Hall."""
    for r in range(2, 18):
        for q in range(9):
            outside = r + 2 * q
            order = outside + 1
            repeated = q + 1
            assert repeated <= order - 1
            minimum_a_outside = 3 * repeated - 1
            minimum_b_outside = 3 * repeated
            assert minimum_a_outside == 3 * q + 2
            assert minimum_b_outside == 3 * q + 3
            assert minimum_b_outside <= outside if r >= q + 3 else (
                minimum_b_outside > outside
            )
            if r == q + 3:
                assert minimum_b_outside == outside


def p3_collision_tensor(
    a: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    b: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> dict[tuple[int, int, int], sp.Expr]:
    """Evaluate P_3(a,a,b) in the coordinate-word basis."""
    tensor: dict[tuple[int, int, int], sp.Expr] = {}
    for word in product(range(3), repeat=3):
        matrix = [
            [a[mode][word[mode]] for mode in range(3)],
            [a[mode][word[mode]] for mode in range(3)],
            [b[mode][word[mode]] for mode in range(3)],
        ]
        tensor[word] = sp.expand(permanent(matrix))
    return tensor


def check_collision_formula_and_boundary() -> None:
    """Check the labelled formula and a Hall-compatible zero collision."""
    a_symbols = [sp.symbols(f"a{mode}_0:3") for mode in range(3)]
    b_symbols = [sp.symbols(f"b{mode}_0:3") for mode in range(3)]
    a = tuple(sp.Matrix(values) for values in a_symbols)
    b = tuple(sp.Matrix(values) for values in b_symbols)
    tensor = p3_collision_tensor(a, b)

    for word in product(range(3), repeat=3):
        expected = 2 * (
            b[0][word[0]] * a[1][word[1]] * a[2][word[2]]
            + a[0][word[0]] * b[1][word[1]] * a[2][word[2]]
            + a[0][word[0]] * a[1][word[1]] * b[2][word[2]]
        )
        assert sp.expand(tensor[word] - expected) == 0

    axes = tuple(sp.eye(3).row(index).T for index in range(3))
    boundary_b = (axes[0], axes[1], -2 * axes[2])
    boundary = p3_collision_tensor(axes, boundary_b)
    assert all(value == 0 for value in boundary.values())


def check_pure_mixed_recolouring() -> None:
    """Check the P4 coefficient shared by a pure word and its j recolouring."""
    alpha = sp.symbols("alpha_0:3", nonzero=True)
    beta = sp.symbols("beta_0:3", nonzero=True)
    eta = sp.symbols("eta_0:3")
    h_first = {
        (mode, colour): sp.Symbol(f"h_first_{mode}_{colour}")
        for mode in range(3)
        for colour in range(3)
    }
    h_second = {
        (mode, colour): sp.Symbol(f"h_second_{mode}_{colour}")
        for mode in range(3)
        for colour in range(3)
    }
    ell_first = sp.symbols("ell_first_0:3")
    ell_second = sp.symbols("ell_second_0:3")

    def value(
        row: str, column: int, outside_colour: int | None, j_colour: int
    ) -> sp.Expr:
        if column == 3:
            return {
                "h_first": ell_first[j_colour],
                "h_second": ell_second[j_colour],
                "a": eta[j_colour],
                "b": sp.Integer(0),
            }[row]
        assert outside_colour is not None
        if row == "a":
            return alpha[column] if outside_colour == column else sp.Integer(0)
        if row == "b":
            return beta[column] if outside_colour == column else sp.Integer(0)
        table = h_first if row == "h_first" else h_second
        return table[column, outside_colour]

    rows = ("h_first", "h_second", "a", "b")
    for colour in range(3):
        retained = [mode for mode in range(3) if mode != colour]
        cofactor = (
            h_first[retained[0], colour]
            * h_second[retained[1], colour]
            + h_first[retained[1], colour]
            * h_second[retained[0], colour]
        )
        for j_colour in range(3):
            matrix = [
                [
                    value(
                        row,
                        column,
                        colour if column < 3 else None,
                        j_colour,
                    )
                    for column in range(4)
                ]
                for row in rows
            ]
            coefficient = permanent(matrix)
            expected = eta[j_colour] * beta[colour] * cofactor
            assert sp.expand(coefficient - expected) == 0


def check_companion_detection_rank() -> None:
    """Check nonzero detection but failure of fixed-i injectivity."""
    companions = sp.eye(2)
    replacement = sp.Matrix(((7,),))
    fixed_i_map = replacement * companions.row(1)
    other_i_map = replacement * companions.row(0)
    assert fixed_i_map.rank() == 1
    assert other_i_map.rank() == 1
    assert fixed_i_map.col_join(other_i_map).rank() == 2


def main() -> None:
    check_hall_quotas()
    check_collision_formula_and_boundary()
    check_pure_mixed_recolouring()
    check_companion_detection_rank()
    print("PASS: lifted a/b repeated-row Hall quotas and equality arithmetic")
    print("PASS: labelled P3(a,a,b) collision formula")
    print("PASS: Hall-compatible zero collision shows Hall alone is insufficient")
    print("PASS: all nine pure/adjacent-mixed P4 coefficient identities")
    print("PASS: each fixed-i detector is nonzero but not injective")
    print("SCOPE: q=0 r=3 aligned projective cell only for detector conclusion")
    print("SCOPE: r>=4, q>=1, unfactorized, and global cases remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
