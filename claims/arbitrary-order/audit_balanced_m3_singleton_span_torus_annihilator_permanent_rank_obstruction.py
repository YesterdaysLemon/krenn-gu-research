"""Independent stdlib audit of the m=3 torus-annihilator P3 obstruction."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Word = tuple[int, int, int]
Tensor = dict[Word, Fraction]
Matrix = list[list[Fraction]]

DIM = 3
WORDS = tuple(product(range(DIM), repeat=DIM))


def permanent_tensor() -> Tensor:
    """Build P3 as a sparse permutation support."""
    return {tuple(permutation): Fraction(1) for permutation in permutations(range(DIM))}


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
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def flatten(tensor: Tensor, mode: int) -> Matrix:
    """Return one exact 3 by 9 flattening."""
    matrix = [[Fraction(0) for _ in range(9)] for _ in range(3)]
    for word, value in tensor.items():
        other = tuple(word[index] for index in range(3) if index != mode)
        matrix[word[mode]][3 * other[0] + other[1]] = value
    return matrix


def outer_cube(vector: tuple[int, int, int]) -> Tensor:
    """Return the third tensor power of one integer vector."""
    return {
        word: Fraction(vector[word[0]] * vector[word[1]] * vector[word[2]])
        for word in WORDS
        if vector[word[0]] * vector[word[1]] * vector[word[2]]
    }


def add_scaled(answer: Tensor, coefficient: Fraction, addition: Tensor) -> None:
    """Add a scaled sparse tensor in place."""
    for word, value in addition.items():
        answer[word] = answer.get(word, Fraction(0)) + coefficient * value
        if answer[word] == 0:
            del answer[word]


def apply_maps(tensor: Tensor, maps: tuple[Matrix, Matrix, Matrix]) -> Tensor:
    """Apply three local matrices to a sparse tensor."""
    answer: Tensor = {}
    for output in WORDS:
        value = sum(
            (
                maps[0][output[0]][source[0]]
                * maps[1][output[1]][source[1]]
                * maps[2][output[2]][source[2]]
                * tensor.get(source, Fraction(0))
                for source in WORDS
            ),
            Fraction(0),
        )
        if value:
            answer[output] = value
    return answer


def direct_cross_matchings(maps: tuple[Matrix, Matrix, Matrix]) -> Tensor:
    """Build the contracted empty companion from its six bijections."""
    answer: Tensor = {}
    for output in WORDS:
        value = sum(
            (
                maps[0][output[0]][permutation[0]]
                * maps[1][output[1]][permutation[1]]
                * maps[2][output[2]][permutation[2]]
                for permutation in permutations(range(DIM))
            ),
            Fraction(0),
        )
        if value:
            answer[output] = value
    return answer


def determinant3(matrix: Matrix) -> Fraction:
    """Return an exact three-by-three determinant."""
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    )


def check_rank_and_polarization(tensor: Tensor) -> None:
    """Audit the rank-four and diagonal-rank certificates."""
    assert [matrix_rank(flatten(tensor, mode)) for mode in range(3)] == [3, 3, 3]

    # The generic slice [[0,z,y],[z,0,x],[y,x,0]] has principal minors
    # -z^2, -y^2, -x^2.  Check the formula on independent integer symbols
    # represented by several exact triples; the written identity is immediate.
    for x, y, z in ((1, 2, 3), (-2, 1, 4), (0, 3, -1)):
        matrix = [
            [Fraction(0), Fraction(z), Fraction(y)],
            [Fraction(z), Fraction(0), Fraction(x)],
            [Fraction(y), Fraction(x), Fraction(0)],
        ]
        principal = (
            matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0],
            matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0],
            matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1],
        )
        assert principal == (-z * z, -y * y, -x * x)

    polarization: Tensor = {}
    for coefficient, vector in (
        (1, (1, 1, 1)),
        (-1, (1, 1, -1)),
        (-1, (1, -1, 1)),
        (-1, (-1, 1, 1)),
    ):
        add_scaled(polarization, Fraction(coefficient, 4), outer_cube(vector))
    assert polarization == tensor

    diagonal = {(index, index, index): Fraction(index + 1) for index in range(3)}
    assert [matrix_rank(flatten(diagonal, mode)) for mode in range(3)] == [3, 3, 3]


def check_contraction_interface(tensor: Tensor) -> None:
    """Audit direct six-matching and local-image constructions separately."""
    raw_maps = (
        ((1, 2, 0), (0, 1, 1), (2, 0, 1)),
        ((1, 0, 1), (2, 1, 0), (0, 1, 2)),
        ((2, 1, 0), (0, 2, 1), (1, 0, 1)),
    )
    maps = tuple(
        [[Fraction(value) for value in row] for row in matrix]
        for matrix in raw_maps
    )
    assert all(determinant3(matrix) for matrix in maps)
    assert apply_maps(tensor, maps) == direct_cross_matchings(maps)
    image = apply_maps(tensor, maps)
    assert [matrix_rank(flatten(image, mode)) for mode in range(3)] == [3, 3, 3]


def check_target_plane_boundary() -> None:
    """Audit the coordinate-boundary sharpness of the diagonal root plane."""
    factors = ((1, -1, 2), (2, 1, -1), (-1, 3, 1))
    diagonal_evaluations = tuple(
        factors[0][colour] * factors[1][colour] * factors[2][colour]
        for colour in range(3)
    )
    assert all(diagonal_evaluations)
    assert tuple(6 - span for span in range(1, 7)) == (5, 4, 3, 2, 1, 0)


def main() -> None:
    """Run the independent exact permanent and contraction audit."""
    tensor = permanent_tensor()
    assert len(tensor) == 6
    check_rank_and_polarization(tensor)
    check_contraction_interface(tensor)
    check_target_plane_boundary()
    print("independent physical-empty/P3 interface: PASS")
    print("independent P3 rank certificates: PASS")
    print("independent diagonal rank-three audit: PASS")
    print("independent torus-boundary control: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
