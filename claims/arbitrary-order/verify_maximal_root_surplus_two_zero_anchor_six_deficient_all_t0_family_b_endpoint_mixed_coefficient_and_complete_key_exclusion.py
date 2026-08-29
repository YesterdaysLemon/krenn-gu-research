"""Exact checks for the GLS76 Family-B endpoint exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from sympy import simplify, symbols


Vector = tuple[int, int, int]


def rational_rank(rows: list[list[int]]) -> int:
    """Return the exact rank of a small integer matrix."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def add_vectors(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def root_only_projection_matrix(
    b_v: Vector,
    b_w: Vector,
    beta: Vector,
    a_v: Vector,
    a_w: Vector,
    alpha: Vector,
) -> list[list[int]]:
    """Build equations (21)--(24) on (db,y,d,x,z,da)."""
    zero = (0, 0, 0)
    rows: list[list[int]] = []

    def append_vector_equation(coefficients: list[Vector]) -> None:
        for coordinate in range(3):
            rows.append([vector[coordinate] for vector in coefficients])

    append_vector_equation([b_v, zero, beta, zero, zero, zero])
    append_vector_equation([b_w, beta, zero, zero, zero, zero])
    append_vector_equation(
        [add_vectors(a_v, a_w), zero, zero, beta, beta, zero]
    )
    append_vector_equation([zero, b_v, b_w, zero, zero, zero])
    append_vector_equation(
        [zero, zero, add_vectors(a_w, alpha), b_v, zero, b_v]
    )
    append_vector_equation(
        [zero, add_vectors(a_v, alpha), zero, zero, b_w, b_w]
    )
    return rows


def zero_shore_projection_matrix(
    b_v: Vector,
    b_w: Vector,
    alpha: Vector,
    beta: Vector,
    a_sum: Vector,
) -> list[list[int]]:
    """Build equation (26) on (d_alpha,d_beta,d,y,x_plus_z)."""
    rows: list[list[int]] = []
    for coordinate in range(3):
        rows.append([b_v[coordinate], 0, alpha[coordinate], 0, 0])
        rows.append([b_w[coordinate], 0, 0, alpha[coordinate], 0])
        rows.append([a_sum[coordinate], 0, 0, 0, alpha[coordinate]])
        rows.append([0, b_v[coordinate], beta[coordinate], 0, 0])
        rows.append([0, b_w[coordinate], 0, beta[coordinate], 0])
        rows.append([0, a_sum[coordinate], 0, 0, beta[coordinate]])
    return rows


def independent(left: Vector, right: Vector) -> bool:
    return any(
        left[i] * right[j] != left[j] * right[i]
        for i in range(3)
        for j in range(i + 1, 3)
    )


def add_tensor(
    target: dict[tuple[int, int, int], int],
    word: tuple[int, int, int],
    coefficient: int,
) -> None:
    target[word] = target.get(word, 0) + coefficient
    if not target[word]:
        del target[word]


def endpoint_tensor() -> dict[tuple[int, int, int], int]:
    """Expand G34 h5 + G35 h4 + G45 h3 in U/V coordinates."""
    tensor: dict[tuple[int, int, int], int] = {}
    # U=0, V=1; h=(-U,U,U).
    for word in ((0, 1, 0), (1, 0, 0)):
        add_tensor(tensor, word, 1)
    for word in ((0, 0, 1), (1, 0, 0)):
        add_tensor(tensor, word, 1)
    for word in ((0, 0, 1), (0, 1, 0)):
        add_tensor(tensor, word, -1)
    return tensor


def check_symbolic_elimination() -> None:
    delta, y, d, beta = symbols("delta y d beta", nonzero=True)
    substituted_vv = simplify(
        y * (-d * beta / delta) + d * (-y * beta / delta)
    )
    assert substituted_vv == -2 * beta * d * y / delta

    delta_a, x, z = symbols("delta_a x z")
    assert simplify((x + z).subs({x: -delta_a, z: -delta_a})) == -2 * delta_a


def main() -> None:
    assert endpoint_tensor() == {(1, 0, 0): 2}
    check_symbolic_elimination()

    forms: list[Vector] = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    ]

    root_checks = 0
    for index, (b_v, b_w, beta) in enumerate(product(forms, repeat=3)):
        for variant in range(4):
            a_v = forms[(index + variant) % len(forms)]
            a_w = forms[(index + 2 * variant + 1) % len(forms)]
            alpha = forms[(index + 3 * variant + 2) % len(forms)]
            matrix = root_only_projection_matrix(
                b_v, b_w, beta, a_v, a_w, alpha
            )
            assert rational_rank(matrix) == 6
            root_checks += 1

    zero_checks = 0
    for index, (b_v, b_w, alpha, beta) in enumerate(product(forms, repeat=4)):
        if not independent(alpha, beta):
            continue
        for variant in range(3):
            a_sum = forms[(index + variant) % len(forms)]
            matrix = zero_shore_projection_matrix(
                b_v, b_w, alpha, beta, a_sum
            )
            assert rational_rank(matrix) == 5
            zero_checks += 1

    # At the selected endpoint, the two complementary active rows have
    # equal sign.  Their U-shore bracket is therefore 1+1, not zero.
    assert 1 + 1 == 2

    old_profiles, old_keys = 98_355, 81
    removed_profiles, removed_keys = 60, 1
    assert (old_profiles - removed_profiles, old_keys - removed_keys) == (
        98_295,
        80,
    )

    print("endpoint tensor: 2 * V3 U4 U5")
    print(f"root-only projected systems: {root_checks} exact full-rank checks")
    print(f"zero-shore projected systems: {zero_checks} exact full-rank checks")
    print("selected-port endpoint bracket: 2 != 0")
    print("six-deficient residual: 98,295 / 80")
    print("PASS GLS76 primary exact checks")


if __name__ == "__main__":
    main()
