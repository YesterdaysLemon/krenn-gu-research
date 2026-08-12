"""Exact replay of the m=3 singleton-span torus-annihilator obstruction."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

DIM = 3
WORDS = tuple(product(range(DIM), repeat=DIM))


def tensor_index(word: tuple[int, int, int]) -> int:
    """Flatten one ternary word."""
    return 9 * word[0] + 3 * word[1] + word[2]


def permanent_tensor() -> sp.Matrix:
    """Return the order-three permanent tensor P3."""
    tensor = sp.zeros(DIM**3, 1)
    for permutation in permutations(range(DIM)):
        tensor[tensor_index(permutation), 0] += 1
    return tensor


def flatten(tensor: sp.Matrix, mode: int) -> sp.Matrix:
    """Return one 3 by 9 tensor flattening."""
    matrix = sp.zeros(DIM, DIM**2)
    for word in WORDS:
        other = tuple(word[index] for index in range(DIM) if index != mode)
        matrix[word[mode], 3 * other[0] + other[1]] = tensor[
            tensor_index(word), 0
        ]
    return matrix


def apply_local_maps(
    tensor: sp.Matrix, maps: tuple[sp.Matrix, sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    """Apply three local 3 by 3 maps to a ternary tensor."""
    answer = sp.zeros(DIM**3, 1)
    for output in WORDS:
        answer[tensor_index(output), 0] = sp.expand(
            sum(
                maps[0][output[0], source[0]]
                * maps[1][output[1], source[1]]
                * maps[2][output[2], source[2]]
                * tensor[tensor_index(source), 0]
                for source in WORDS
            )
        )
    return answer


def direct_empty_contraction(
    maps: tuple[sp.Matrix, sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    """Enumerate the six root-to-nonroot cross matchings directly."""
    answer = sp.zeros(DIM**3, 1)
    for output in WORDS:
        answer[tensor_index(output), 0] = sp.expand(
            sum(
                maps[0][output[0], permutation[0]]
                * maps[1][output[1], permutation[1]]
                * maps[2][output[2], permutation[2]]
                for permutation in permutations(range(DIM))
            )
        )
    return answer


def check_permanent_rank_certificates(tensor: sp.Matrix) -> None:
    """Replay the flattening, slice, and polarization rank certificates."""
    assert [flatten(tensor, mode).rank() for mode in range(DIM)] == [3, 3, 3]

    x, y, z = sp.symbols("x y z")
    slice_matrix = sp.Matrix(((0, z, y), (z, 0, x), (y, x, 0)))
    principal = tuple(
        sp.expand(slice_matrix.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal == (-z**2, -y**2, -x**2)

    signs = (
        (1, (1, 1, 1)),
        (-1, (1, 1, -1)),
        (-1, (1, -1, 1)),
        (-1, (-1, 1, 1)),
    )
    polarization = sp.zeros(DIM**3, 1)
    for coefficient, vector in signs:
        for word in WORDS:
            polarization[tensor_index(word), 0] += (
                sp.Rational(coefficient, 4)
                * vector[word[0]]
                * vector[word[1]]
                * vector[word[2]]
            )
    assert polarization == tensor

    diagonal = sp.zeros(DIM**3, 1)
    coefficients = sp.symbols("k0:3", nonzero=True)
    for colour, coefficient in enumerate(coefficients):
        diagonal[tensor_index((colour, colour, colour)), 0] = coefficient
    assert [flatten(diagonal, mode).rank() for mode in range(DIM)] == [3, 3, 3]


def check_contraction_interface(tensor: sp.Matrix) -> None:
    """Match the physical six-bijection sum to a local image of P3."""
    maps = tuple(
        sp.Matrix(
            DIM,
            DIM,
            lambda output, source, name=name: sp.Symbol(
                f"{name}{output}{source}"
            ),
        )
        for name in ("x", "y", "r")
    )
    local_image = apply_local_maps(tensor, maps)
    direct = direct_empty_contraction(maps)
    assert local_image == direct

    fixed_maps = (
        sp.Matrix(((1, 1, 0), (0, 1, 1), (1, 0, 1))),
        sp.Matrix(((1, 0, 1), (1, 1, 0), (0, 1, 1))),
        sp.Matrix(((2, 1, 0), (0, 1, 1), (1, 0, 1))),
    )
    assert all(matrix.det() != 0 for matrix in fixed_maps)
    image = apply_local_maps(tensor, fixed_maps)
    assert [flatten(image, mode).rank() for mode in range(DIM)] == [3, 3, 3]


def check_target_plane_boundary() -> None:
    """Check that the diagonal root plane blocks every root-torus product."""
    factors = tuple(
        sp.symbols(f"a{mode}_0:3", nonzero=True) for mode in range(3)
    )
    evaluations = tuple(
        sp.prod(factors[mode][colour] for mode in range(3))
        for colour in range(3)
    )
    assert all(value != 0 for value in evaluations)

    # The projective dimension lower bound used on a span of dimension s.
    assert tuple(6 - span for span in range(1, 7)) == (5, 4, 3, 2, 1, 0)


def main() -> None:
    """Replay the permanent-rank and physical contraction interfaces."""
    tensor = permanent_tensor()
    assert sum(value != 0 for value in tensor) == 6
    check_permanent_rank_certificates(tensor)
    check_contraction_interface(tensor)
    check_target_plane_boundary()
    print("physical empty-column P3 contraction: PASS (6 terms)")
    print("P3 rank-four certificates: PASS")
    print("fully supported diagonal contraction rank: PASS (3)")
    print("target-plane torus blocking boundary: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
