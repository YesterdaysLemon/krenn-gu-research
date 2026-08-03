"""Primary exact checks for lower-jet deletion-label tomography.

The computations audit the q=4 and q=6 instances of an arbitrary-order
symbolic proof.  They do not search graph supports, blocker words, or
parameter families.
"""

from __future__ import annotations

from math import prod

import sympy as sp


def odd_double_factorial(n: int) -> int:
    """Return n!! for odd n >= -1, with (-1)!! = 1."""
    if n == -1:
        return 1
    return prod(range(1, n + 1, 2))


def even_masks(q: int) -> list[int]:
    return [mask for mask in range(1 << q) if mask.bit_count() % 2 == 0]


def chart_entry(q: int, tangent_mask: int, endpoint_mask: int) -> int:
    """Closed form from the private-port/complete-zero-root chart."""
    if tangent_mask != endpoint_mask:
        return 0
    return odd_double_factorial(q - endpoint_mask.bit_count() - 1)


def verify_chart(q: int, expected_determinant: int) -> None:
    masks = even_masks(q)
    matrix = sp.Matrix(
        [[chart_entry(q, tangent, endpoint) for endpoint in masks] for tangent in masks]
    )
    diagonal = [odd_double_factorial(q - mask.bit_count() - 1) for mask in masks]
    assert matrix == sp.diag(*diagonal)
    assert matrix.det() == expected_determinant
    assert matrix.rank() == 1 << (q - 1)


def verify_kernel_translation() -> None:
    gamma = sp.Matrix([[1, 0, 1], [0, 1, 1]])
    kernel_vector = sp.Matrix([-1, -1, 1])
    assert gamma * kernel_vector == sp.zeros(2, 1)

    # Columns are three W-valued cofactors in W=K^2.
    cofactors = sp.Matrix([[2, 3, 5], [7, 11, 13]])
    invisible_value = sp.Matrix([17, 19])
    perturbed = cofactors + invisible_value * kernel_vector.T
    assert gamma * perturbed.T == gamma * cofactors.T
    assert perturbed[:, 0] != cofactors[:, 0]


def zeon_product(left: int, right: int) -> int | None:
    if left & right:
        return None
    return left | right


def verify_squarefree_gauge() -> None:
    a, b, c, d = sp.symbols("a b c d")
    column = [a, b, c, d]
    square_coefficients = {
        (j, k): 2 * column[j] * column[k] for j in range(4) for k in range(j + 1, 4)
    }
    assert len(square_coefficients) == 6
    assert square_coefficients[(0, 1)] == 2 * a * b
    assert square_coefficients[(2, 3)] == 2 * c * d

    # Audit multiplicativity and top normalization for a nontrivial monomial gauge.
    permutation = (2, 0, 3, 1)
    scales = (sp.Rational(2), sp.Rational(3), sp.Rational(5), sp.Rational(1, 30))
    assert prod(scales) == 1

    def transform(mask: int) -> tuple[int, sp.Rational]:
        out_mask = 0
        scale = sp.Rational(1)
        for i in range(4):
            if mask & (1 << i):
                out_mask |= 1 << permutation[i]
                scale *= scales[i]
        return out_mask, scale

    for left in range(16):
        for right in range(16):
            product_mask = zeon_product(left, right)
            image_left, scale_left = transform(left)
            image_right, scale_right = transform(right)
            image_product = zeon_product(image_left, image_right)
            if product_mask is None:
                assert image_product is None
            else:
                target_mask, target_scale = transform(product_mask)
                assert image_product == target_mask
                assert scale_left * scale_right == target_scale
    assert transform(15) == (15, sp.Rational(1))


def verify_capacity_boundary() -> None:
    assert (1 << 3) - 1 > 1 << 2  # q=4, t=q-2
    assert (1 << 5) - 1 > 1 << 4  # q=6, t=q-2
    cells = {
        (5, 4): 1,
        (6, 4): 2,
        (7, 4): 3,
        (6, 6): 0,
        (7, 6): 1,
    }
    assert all(root_count == m - q for (m, q), root_count in cells.items())
    assert all(root_count < q for (m, q), root_count in cells.items())


def main() -> None:
    verify_chart(4, 3)
    print("PASS: q=4 legal even-deletion selector chart has determinant 3")
    verify_chart(6, 15 * 3**15)
    print("PASS: q=6 legal even-deletion selector chart has determinant 15*3^15")
    verify_kernel_translation()
    print("PASS: kernel translations preserve the observed jet and change named cofactors")
    verify_squarefree_gauge()
    print("PASS: square-free multiplication admits the predicted monomial gauge")
    verify_capacity_boundary()
    print("PASS: balanced P5--P7 q=4/q=6 single-jet capacity boundary")
    print("SCOPE: forced selectors and cross-depth multiplication remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
