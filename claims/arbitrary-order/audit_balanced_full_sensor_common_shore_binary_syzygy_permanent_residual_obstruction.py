"""Independent stdlib audit of the S2P binary residual obstruction.

This audit imports neither SymPy, the primary verifier, nor repository code.
It reconstructs the shore blocks first, builds the singleton map directly,
and uses exact ``Fraction`` row reduction and sparse support checks.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Scalar = Fraction
Vector = tuple[Scalar, Scalar]
Triple = tuple[Vector, Vector, Vector]
Matrix = list[list[Scalar]]

ZERO: Vector = (Fraction(0), Fraction(0))
E0: Vector = (Fraction(1), Fraction(0))
E1: Vector = (Fraction(0), Fraction(1))


def tensor2(left: Vector, right: Vector) -> list[Scalar]:
    """Flatten a two-factor tensor lexicographically."""
    return [left[i] * right[j] for i, j in product(range(2), repeat=2)]


def tensor3(first: Vector, second: Vector, third: Vector) -> list[Scalar]:
    """Flatten a three-factor tensor lexicographically."""
    return [
        first[i] * second[j] * third[k]
        for i, j, k in product(range(2), repeat=3)
    ]


def subtract(left: list[Scalar], right: list[Scalar]) -> list[Scalar]:
    """Subtract equal-length exact vectors."""
    return [x - y for x, y in zip(left, right, strict=True)]


def scale(value: Scalar, vector: list[Scalar]) -> list[Scalar]:
    """Scale an exact vector."""
    return [value * entry for entry in vector]


def pair_alternant(left: tuple[Vector, Vector], right: tuple[Vector, Vector]) -> list[Scalar]:
    """Apply two maps to the standard exterior generator."""
    return subtract(tensor2(left[0], right[1]), tensor2(left[1], right[0]))


def column_index(i: int, j: int, k: int) -> int:
    """Return the flattened coordinate of one binary root word."""
    return 4 * i + 2 * j + k


def direct_map(c12: list[Scalar], c13: list[Scalar], c23: list[Scalar]) -> Matrix:
    """Build D_C directly from its three shore blocks."""
    columns: Matrix = []
    for slot, coordinate in product(range(3), range(2)):
        basis = E0 if coordinate == 0 else E1
        column = [Fraction(0) for _ in range(8)]
        for i, j, k in product(range(2), repeat=3):
            if slot == 0:
                column[column_index(i, j, k)] = basis[i] * c23[2 * j + k]
            elif slot == 1:
                column[column_index(i, j, k)] = c13[2 * i + k] * basis[j]
            else:
                column[column_index(i, j, k)] = c12[2 * i + j] * basis[k]
        columns.append(column)
    return [[columns[column][row] for column in range(6)] for row in range(8)]


def map_from_forms(forms: tuple[tuple[Vector, Vector], ...]) -> Matrix:
    """Derive the three blocks from a kernel plane, then build D_C."""
    c12 = scale(Fraction(-1), pair_alternant(forms[0], forms[1]))
    c13 = pair_alternant(forms[0], forms[2])
    c23 = scale(Fraction(-1), pair_alternant(forms[1], forms[2]))
    return direct_map(c12, c13, c23)


def matrix_rank(matrix: Matrix) -> int:
    """Compute exact rank by independently written Gauss--Jordan reduction."""
    work = [row[:] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def multiply(matrix: Matrix, vector: list[Scalar]) -> list[Scalar]:
    """Multiply an exact matrix by a column vector."""
    return [
        sum((entry * value for entry, value in zip(row, vector, strict=True)), Fraction(0))
        for row in matrix
    ]


def diagonal_basis(forms: tuple[tuple[Vector, Vector], ...]) -> list[list[Scalar]]:
    """Return the two columns spanning the displayed kernel plane."""
    return [
        [entry for form in forms for entry in form[parameter]]
        for parameter in range(2)
    ]


def assert_exact_kernel(matrix: Matrix, basis: list[list[Scalar]]) -> None:
    """Check containment, independence, and the rank--nullity equality."""
    assert all(multiply(matrix, vector) == [Fraction(0)] * 8 for vector in basis)
    basis_matrix = [[vector[row] for vector in basis] for row in range(6)]
    assert matrix_rank(basis_matrix) == len(basis)
    assert matrix_rank(matrix) + len(basis) == 6


def select_rows(matrix: Matrix, words: list[tuple[int, int, int]]) -> Matrix:
    """Apply a coordinate quotient by selecting surviving tensor words."""
    return [matrix[column_index(*word)][:] for word in words]


def split_triple(vector: list[Scalar]) -> Triple:
    """Split a six-vector into its three binary components."""
    return (
        (vector[0], vector[1]),
        (vector[2], vector[3]),
        (vector[4], vector[5]),
    )


def permanent(first: Triple, second: Triple, third: Triple) -> list[Scalar]:
    """Evaluate the polarized sign-free six-term permanent."""
    triples = (first, second, third)
    answer = [Fraction(0) for _ in range(8)]
    for sigma in permutations(range(3)):
        term = tensor3(
            triples[sigma[0]][0],
            triples[sigma[1]][1],
            triples[sigma[2]][2],
        )
        answer = [
            value + addition for value, addition in zip(answer, term, strict=True)
        ]
    return answer


def all_basis_permanents(basis: list[list[Scalar]]) -> list[list[Scalar]]:
    """Use trilinearity to span all permanents of one kernel basis."""
    triples = [split_triple(vector) for vector in basis]
    return [permanent(triples[i], triples[j], triples[k]) for i, j, k in product(range(len(basis)), repeat=3)]


def in_column_span(matrix: Matrix, vector: list[Scalar]) -> bool:
    """Test exact column-span membership by rank augmentation."""
    augmented = [row + [value] for row, value in zip(matrix, vector, strict=True)]
    return matrix_rank(matrix) == matrix_rank(augmented)


def main() -> None:
    """Replay the four rank types and every zero-block boundary."""
    identity = (E0, E1)
    rank_u0 = (E0, ZERO)
    rank_u1 = (ZERO, E0)
    rank_sum = (E0, E0)
    patterns = {
        "222": (identity, identity, identity),
        "122": (rank_u0, identity, identity),
        "211": (identity, rank_u0, rank_u1),
        "111": (rank_u0, rank_u1, rank_sum),
    }

    maps: dict[str, Matrix] = {}
    bases: dict[str, list[list[Scalar]]] = {}
    for name, forms in patterns.items():
        matrix = map_from_forms(forms)
        basis = diagonal_basis(forms)
        maps[name] = matrix
        bases[name] = basis
        assert_exact_kernel(matrix, basis)
        assert all(
            any(pair_alternant(forms[i], forms[j]))
            for i, j in ((0, 1), (0, 2), (1, 2))
        )

    # Type 222 lies in the kernel of commutative multiplication by total
    # binary weight.  A nonzero pure tensor cannot lie in that kernel.
    for column in range(6):
        weight_sums = [Fraction(0) for _ in range(4)]
        for i, j, k in product(range(2), repeat=3):
            weight_sums[i + j + k] += maps["222"][column_index(i, j, k)][column]
        assert weight_sums == [Fraction(0)] * 4

    # Type 122 has, modulo its fixed first line, a one-dimensional quotient
    # generated by a rank-two two-factor tensor.
    reduced_122 = select_rows(
        maps["122"], [(1, j, k) for j, k in product(range(2), repeat=2)]
    )
    assert matrix_rank(reduced_122) == 1
    quotient_column = next(
        [reduced_122[row][column] for row in range(4)]
        for column in range(6)
        if any(reduced_122[row][column] for row in range(4))
    )
    assert quotient_column[0] * quotient_column[3] - quotient_column[1] * quotient_column[2]

    # The double/triple quotients vanish in types 211 and 111.
    assert not any(
        entry
        for row in select_rows(maps["211"], [(i, 1, 1) for i in range(2)])
        for entry in row
    )
    assert not any(entry for row in select_rows(maps["111"], [(1, 1, 1)]) for entry in row)

    # Trilinearity reduces the permanent factor-line assertions to kernel
    # basis triples.
    for value in all_basis_permanents(bases["122"]):
        assert all(value[column_index(1, j, k)] == 0 for j, k in product(range(2), repeat=2))
    for value in all_basis_permanents(bases["211"]):
        assert all(
            value[column_index(i, j, k)] == 0
            for i, j, k in product(range(2), repeat=3)
            if j == 1 or k == 1
        )
    for value in all_basis_permanents(bases["111"]):
        assert value[1:] == [Fraction(0)] * 7

    # Exactly one zero block: C12=e0e0, C13=-e0e0, C23=0.
    c12 = tensor2(E0, E0)
    c13 = scale(Fraction(-1), tensor2(E0, E0))
    c23 = [Fraction(0)] * 4
    zero_map = direct_map(c12, c13, c23)
    zero_basis = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
    ]
    assert_exact_kernel(zero_map, zero_basis)
    assert not any(
        entry
        for row in select_rows(zero_map, [(i, 1, 1) for i in range(2)])
        for entry in row
    )
    for value in all_basis_permanents(zero_basis):
        assert all(
            value[column_index(i, j, k)] == 0
            for i, j, k in product(range(2), repeat=3)
            if j == 1 or k == 1
        )

    # Exactly two zero blocks: the missing root component on the full kernel
    # makes every polarized permanent zero.
    one_block_map = direct_map(c12, [Fraction(0)] * 4, [Fraction(0)] * 4)
    one_block_kernel = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
    ]
    assert_exact_kernel(one_block_map, one_block_kernel)
    assert all(not any(value) for value in all_basis_permanents(one_block_kernel))

    # Three zero blocks have zero image.
    assert matrix_rank(direct_map([Fraction(0)] * 4, [Fraction(0)] * 4, [Fraction(0)] * 4)) == 0

    # Sharp type-122 control: Q=e000 and P=e011 share exactly the first line.
    kernel = split_triple(bases["122"][0])
    scaled_kernel = tuple(
        tuple(entry / 6 for entry in component) for component in kernel
    )
    sharp_q = permanent(scaled_kernel, kernel, kernel)
    sharp_p = tensor3(E0, E1, E1)
    assert sharp_q == tensor3(E0, E0, E0)
    assert in_column_span(maps["122"], sharp_p)

    print("independent S2P normal-form audit: PASS (4/4)")
    print("independent S2P zero-block audit: PASS (3/3)")
    print("independent S2P transverse residual: EMPTY")
    print("independent S2P sharp shared-factor control: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
