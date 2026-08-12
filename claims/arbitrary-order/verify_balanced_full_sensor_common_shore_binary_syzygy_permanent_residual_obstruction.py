"""Exact replay of the S2P binary syzygy--permanent obstruction."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def tensor2(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    """Return a two-factor tensor in lexicographic coordinates."""
    return sp.Matrix([x[i] * y[j] for i, j in product(range(2), repeat=2)])


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    """Return a three-factor tensor in lexicographic coordinates."""
    return sp.Matrix(
        [x[i] * y[j] * z[k] for i, j, k in product(range(2), repeat=3)]
    )


def alternating(
    first: list[sp.Matrix], second: list[sp.Matrix], third: list[sp.Matrix]
) -> sp.Matrix:
    """Mixed alternating tensor of three triples."""
    return (
        tensor3(first[0], second[1], third[2])
        + tensor3(second[0], third[1], first[2])
        + tensor3(third[0], first[1], second[2])
        - tensor3(first[0], third[1], second[2])
        - tensor3(second[0], first[1], third[2])
        - tensor3(third[0], second[1], first[2])
    )


def alternating_map(forms: list[sp.Matrix]) -> tuple[sp.Matrix, sp.Matrix]:
    """Build -Alt(F(e0),F(e1),.) and the diagonal F(U) inclusion."""
    first = [form[:, 0] for form in forms]
    second = [form[:, 1] for form in forms]
    columns: list[sp.Matrix] = []
    for slot in range(3):
        for coordinate in range(2):
            triple = [sp.zeros(2, 1) for _ in range(3)]
            triple[slot][coordinate] = 1
            columns.append(-alternating(first, second, triple))
    diagonal = sp.Matrix.vstack(*forms)
    return sp.Matrix.hstack(*columns), diagonal


def pair_alternant(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Compute (F_left tensor F_right)(e0 wedge e1)."""
    return tensor2(left[:, 0], right[:, 1]) - tensor2(
        left[:, 1], right[:, 0]
    )


def polarized_permanent(triples: list[list[sp.Matrix]]) -> sp.Matrix:
    """Compute the sign-free six-term permanent of three triples."""
    total = sp.zeros(8, 1)
    for sigma in permutations(range(3)):
        total += tensor3(
            triples[sigma[0]][0],
            triples[sigma[1]][1],
            triples[sigma[2]][2],
        )
    return sp.expand(total)


def generic_kernel_triples(forms: list[sp.Matrix]) -> list[list[sp.Matrix]]:
    """Return three symbolic triples in the diagonal kernel F(U)."""
    triples: list[list[sp.Matrix]] = []
    for label in ("x", "y", "r"):
        u0, u1 = sp.symbols(f"{label}0 {label}1")
        parameter = sp.Matrix([u0, u1])
        triples.append([form * parameter for form in forms])
    return triples


def quotient_rows(indices: list[tuple[int, int, int]]) -> sp.Matrix:
    """Select tensor coordinates implementing a displayed quotient."""
    rows = []
    for index in indices:
        row = sp.zeros(1, 8)
        row[0, 4 * index[0] + 2 * index[1] + index[2]] = 1
        rows.append(row)
    return sp.Matrix.vstack(*rows)


def block_map(
    c12: sp.Matrix, c13: sp.Matrix, c23: sp.Matrix
) -> sp.Matrix:
    """Build the singleton map directly from three flattened two-blocks."""
    columns: list[sp.Matrix] = []
    for slot in range(3):
        for coordinate in range(2):
            basis = sp.zeros(2, 1)
            basis[coordinate] = 1
            column = sp.zeros(8, 1)
            if slot == 0:
                for i, j, k in product(range(2), repeat=3):
                    column[4 * i + 2 * j + k] = basis[i] * c23[2 * j + k]
            elif slot == 1:
                for i, j, k in product(range(2), repeat=3):
                    column[4 * i + 2 * j + k] = c13[2 * i + k] * basis[j]
            else:
                for i, j, k in product(range(2), repeat=3):
                    column[4 * i + 2 * j + k] = c12[2 * i + j] * basis[k]
            columns.append(column)
    return sp.Matrix.hstack(*columns)


def assert_kernel(map_matrix: sp.Matrix, expected: sp.Matrix) -> None:
    """Check that the displayed two- or three-plane is the full kernel."""
    assert map_matrix * expected == sp.zeros(8, expected.cols)
    assert expected.rank() == expected.cols
    assert map_matrix.rank() + expected.cols == 6


def main() -> None:
    """Replay all normal forms, quotient certificates, and sharpness."""
    identity = sp.eye(2)
    rank_u0 = sp.Matrix([[1, 0], [0, 0]])
    rank_u1 = sp.Matrix([[0, 1], [0, 0]])
    rank_sum = sp.Matrix([[1, 1], [0, 0]])
    patterns = {
        "222": [identity, identity, identity],
        "122": [rank_u0, identity, identity],
        "211": [identity, rank_u0, rank_u1],
        "111": [rank_u0, rank_u1, rank_sum],
    }

    maps: dict[str, sp.Matrix] = {}
    for name, forms in patterns.items():
        map_matrix, diagonal = alternating_map(forms)
        maps[name] = map_matrix
        assert_kernel(map_matrix, diagonal)
        assert all(
            pair_alternant(forms[i], forms[j]) != sp.zeros(4, 1)
            for i, j in ((0, 1), (0, 2), (1, 2))
        )

    # In type 222, commutative multiplication records only Hamming weight.
    # Every alternating column maps to zero in Sym^3(K^2).
    multiplication = sp.zeros(4, 8)
    for i, j, k in product(range(2), repeat=3):
        multiplication[i + j + k, 4 * i + 2 * j + k] = 1
    assert multiplication * maps["222"] == sp.zeros(4, 6)

    # Type 122: quotient the first factor by its fixed line.  The remaining
    # column space is the one-dimensional span of a rank-two alternant.
    quotient_first = quotient_rows([(1, j, k) for j, k in product(range(2), repeat=2)])
    reduced_122 = quotient_first * maps["122"]
    assert reduced_122.rank() == 1
    nonzero_122 = next(
        reduced_122[:, column]
        for column in range(reduced_122.cols)
        if reduced_122[:, column] != sp.zeros(4, 1)
    )
    assert sp.Matrix(2, 2, list(nonzero_122)).rank() == 2

    # Types 211 and 111: the simultaneous quotient at all rank-one positions
    # kills the alternating image.
    quotient_23 = quotient_rows([(i, 1, 1) for i in range(2)])
    assert quotient_23 * maps["211"] == sp.zeros(2, 6)
    quotient_123 = quotient_rows([(1, 1, 1)])
    assert quotient_123 * maps["111"] == sp.zeros(1, 6)

    # A permanent of diagonal-kernel triples has the fixed factor at every
    # rank-one position.
    permanent_122 = polarized_permanent(generic_kernel_triples(patterns["122"]))
    assert all(permanent_122[4 + offset] == 0 for offset in range(4))
    permanent_211 = polarized_permanent(generic_kernel_triples(patterns["211"]))
    assert all(
        permanent_211[4 * i + 2 * j + k] == 0
        for i, j, k in product(range(2), repeat=3)
        if j == 1 or k == 1
    )
    permanent_111 = polarized_permanent(generic_kernel_triples(patterns["111"]))
    assert all(permanent_111[index] == 0 for index in range(1, 8))

    # One-zero-block form: C12=e0e0, C13=-e0e0, C23=0.
    e0 = sp.Matrix([1, 0])
    e1 = sp.Matrix([0, 1])
    c12 = tensor2(e0, e0)
    c13 = -tensor2(e0, e0)
    c23 = sp.zeros(4, 1)
    zero_block_map = block_map(c12, c13, c23)
    zero_block_kernel = sp.Matrix.hstack(
        sp.Matrix([1, 0, 0, 0, 0, 0]),
        sp.Matrix([0, 1, 0, 0, 0, 0]),
        sp.Matrix([0, 0, 1, 0, 1, 0]),
    )
    assert_kernel(zero_block_map, zero_block_kernel)
    assert quotient_first * zero_block_map == sp.zeros(4, 6)
    assert quotient_23 * zero_block_map == sp.zeros(2, 6)

    zx0, zx1, zy0, zy1, zr0, zr1 = sp.symbols("zx0 zx1 zy0 zy1 zr0 zr1")
    zero_kernel_triples = [
        [sp.Matrix([zx0, zx1]), e0, e0],
        [sp.Matrix([zy0, zy1]), e0, e0],
        [sp.Matrix([zr0, zr1]), e0, e0],
    ]
    zero_permanent = polarized_permanent(zero_kernel_triples)
    assert all(
        zero_permanent[4 * i + 2 * j + k] == 0
        for i, j, k in product(range(2), repeat=3)
        if j == 1 or k == 1
    )

    # Sharp type-122 example.  Three proportional kernel vectors have pure
    # permanent e000 after rescaling one by 1/6, while the image contains e011.
    kernel_vector = [e0, e0, e0]
    sharp_permanent = polarized_permanent(
        [
            [component / 6 for component in kernel_vector],
            kernel_vector,
            kernel_vector,
        ]
    )
    expected_q = tensor3(e0, e0, e0)
    assert sharp_permanent == expected_q
    sharp_parameter = sp.Matrix([0, 0, 0, 0, 0, -1])
    expected_p = tensor3(e0, e1, e1)
    assert maps["122"] * sharp_parameter == expected_p

    print("S2P canonical kernel classification: PASS (4/4)")
    print("S2P one-zero-block degeneration: PASS")
    print("S2P transverse pure residual: EMPTY")
    print("S2P shared-factor sharpness: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
