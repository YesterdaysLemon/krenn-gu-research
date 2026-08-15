"""Independent no-SymPy audit of the fixed-pair A-line-split exclusion."""

from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import json


P = 3
EDGES = tuple(combinations(range(4), 2))
EDGE_COORDINATE_PERMUTATIONS = tuple(
    tuple(permutations((4, 5, i, j))) for i, j in EDGES
)
COMPLEMENT_PERMUTATIONS = tuple(
    tuple(permutations(tuple(k for k in range(6) if k not in (i, j))))
    for i, j in EDGES
)

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)
QUADRICS = (M1, M2, D0, D1, D2)

PHI1 = (
    (0, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1),
    (-1, 0, -1, 1, 0, 0),
)
PHI2 = (
    (1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1),
    (0, -1, -1, 1, 0, 0),
)
APROJ = ((0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 1))

FIXTURE_JSON = """[[[[1,0,1,0,1,2],[0,1,1,0,0,0],[0,0,0,1,1,2]],[[1,0,0,1,0,0],[0,1,0,0,2,1],[0,0,1,1,0,0]],[[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,0,1,1]],[[2,1,0,0,0,0],[2,0,1,0,0,0],[1,0,0,1,0,0]]],[[[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,0,1,1]],[[1,0,0,2,2,1],[0,1,0,0,1,2],[0,0,1,0,1,2]],[[1,0,0,0,2,1],[0,1,1,0,1,2],[0,0,0,1,2,1]],[[2,1,0,0,0,0],[2,0,1,0,0,0],[1,0,0,1,0,0]]],[[[1,0,0,2,2,2],[0,1,0,0,1,1],[0,0,1,2,2,2]],[[1,0,0,1,0,0],[0,1,0,1,0,0],[0,0,1,1,0,0]],[[1,0,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,2,2]],[[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,0,2,1]]],[[[1,0,0,1,0,0],[0,1,0,2,0,0],[0,0,1,1,0,0]],[[1,0,0,0,0,0],[0,1,0,0,2,1],[0,0,1,2,0,0]],[[1,0,1,0,0,0],[0,1,1,0,0,0],[0,0,0,1,1,2]],[[0,2,1,0,0,0],[0,1,0,1,0,0],[0,0,0,0,1,1]]],[[[1,0,0,0,1,1],[0,1,1,0,2,2],[0,0,0,1,2,2]],[[1,0,0,1,0,0],[0,1,0,1,0,0],[0,0,1,1,0,0]],[[1,0,0,1,0,0],[0,1,0,0,0,0],[0,0,1,2,2,2]],[[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,0,2,1]]],[[[1,1,0,0,0,0],[0,0,1,0,2,2],[0,0,0,1,1,1]],[[1,0,0,2,0,0],[0,1,0,0,2,2],[0,0,1,0,0,0]],[[1,0,0,1,0,0],[0,1,0,1,0,0],[0,0,1,1,0,0]],[[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,0,2,1]]],[[[1,0,1,0,0,0],[0,1,2,0,1,1],[0,0,0,1,0,0]],[[0,1,0,1,0,0],[0,0,1,1,0,0],[0,0,0,0,1,2]],[[1,0,0,1,1,1],[0,1,0,2,1,1],[0,0,1,2,0,0]],[[1,1,0,0,0,0],[2,0,1,0,0,0],[1,0,0,1,0,0]]],[[[1,0,0,1,0,0],[0,1,0,2,0,0],[0,0,1,1,0,0]],[[1,0,1,0,0,0],[0,1,0,0,2,1],[0,0,0,1,1,2]],[[1,0,1,0,0,0],[0,1,2,2,0,0],[0,0,0,0,1,2]],[[0,2,1,0,0,0],[0,1,0,1,0,0],[0,0,0,0,1,1]]],[[[0,1,0,1,0,0],[0,0,1,1,0,0],[0,0,0,0,1,2]],[[1,0,2,2,0,0],[0,1,1,2,0,0],[0,0,0,0,1,1]],[[1,0,0,0,1,1],[0,1,0,1,0,0],[0,0,1,0,2,2]],[[1,1,0,0,0,0],[2,0,1,0,0,0],[1,0,0,1,0,0]]]]"""
FIXTURE_SHA256 = "b24836d1b7f47f7de00f045d15015b3568cf6a63958402c3d3c4d2b2765e19ad"

EXPECTED_SUMMARIES = (
    ((1, 1, 2, 3), ((3, 1, 2, 1), (3, 2, 2, 1)), (5, 5, 3, 3)),
    ((2, 1, 1, 3), ((2, 3, 3, 1), (2, 2, 3, 1)), (3, 5, 5, 3)),
    ((1, 3, 1, 2), ((2, 1, 2, 2), (3, 1, 3, 2)), (5, 3, 5, 3)),
    ((3, 1, 1, 2), ((1, 2, 3, 2), (2, 3, 3, 1)), (3, 5, 5, 3)),
    ((1, 3, 1, 2), ((2, 1, 2, 2), (3, 1, 3, 2)), (5, 3, 5, 3)),
    ((1, 1, 3, 2), ((2, 2, 1, 2), (2, 3, 1, 2)), (5, 5, 3, 3)),
    ((1, 2, 1, 3), ((2, 2, 3, 1), (3, 1, 3, 2)), (5, 3, 5, 3)),
    ((3, 1, 1, 2), ((1, 3, 3, 2), (2, 2, 3, 1)), (3, 5, 5, 3)),
    ((2, 1, 1, 3), ((2, 3, 3, 1), (1, 3, 2, 2)), (3, 5, 5, 3)),
)


def rank_mod(rows, modulus=P):
    matrix = [[value % modulus for value in row] for row in rows]
    rank = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], modulus - 2, modulus)
        matrix[rank] = [(inverse * value) % modulus for value in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [
                    (x - scale * y) % modulus
                    for x, y in zip(matrix[i], matrix[rank], strict=True)
                ]
        rank += 1
    return rank


def rank_q(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [
                    x - scale * y
                    for x, y in zip(matrix[i], matrix[rank], strict=True)
                ]
        rank += 1
    return rank


def permanent_on_coordinates(vectors, coordinate_permutations, modulus=None):
    value = 0
    for assignment in coordinate_permutations:
        term = 1
        for mode, coordinate in enumerate(assignment):
            term *= vectors[mode][coordinate]
        value += term
    return value % modulus if modulus is not None else value


def coefficient(q, vectors, modulus=None):
    value = sum(
        q[edge] * permanent_on_coordinates(vectors, COMPLEMENT_PERMUTATIONS[edge])
        for edge in range(6)
    )
    return value % modulus if modulus is not None else value


def check_basis_tensor_factorization():
    projective_lines = ((1, 0), (1, 1), (1, 2), (0, 1))
    r_basis = tuple(tuple(int(i == j) for i in range(6)) for j in range(4))
    checked = 0
    for lines in product(projective_lines, repeat=3):
        line_bases = tuple(
            (*r_basis, (0, 0, 0, 0, line[0], line[1])) for line in lines
        )
        bases = (*line_bases, r_basis)
        for edge, (i, j) in enumerate(EDGES):
            for labels in product(range(5), range(5), range(5), range(4)):
                vectors = tuple(bases[mode][labels[mode]] for mode in range(4))
                direct = permanent_on_coordinates(
                    vectors, EDGE_COORDINATE_PERMUTATIONS[edge], P
                )
                alpha = tuple(int(labels[mode] == 4) for mode in range(3))

                def j_pair(left, right):
                    return (left[0] * right[1] + left[1] * right[0]) % P

                def g_pair(left, right):
                    return (left[i] * right[j] + left[j] * right[i]) % P

                rhs = (
                    j_pair(lines[0], lines[1])
                    * alpha[0]
                    * alpha[1]
                    * g_pair(vectors[2], vectors[3])
                    + j_pair(lines[0], lines[2])
                    * alpha[0]
                    * alpha[2]
                    * g_pair(vectors[1], vectors[3])
                    + j_pair(lines[1], lines[2])
                    * alpha[1]
                    * alpha[2]
                    * g_pair(vectors[0], vectors[3])
                ) % P
                assert direct == rhs
                checked += 1
    assert checked == 4**3 * 6 * 5**3 * 4
    return checked


def check_exception_patterns():
    checked = 0
    for exceptions in product((-1, 0, 1, 2), repeat=3):
        counts = tuple(exceptions.count(mode) for mode in range(3))
        assert sum(count <= 1 for count in counts) >= 2
        checked += 1
    assert checked == 64
    return checked


def signed_lift(hit):
    return tuple(
        tuple(tuple(-1 if value == 2 else value for value in row) for row in plane)
        for plane in hit
    )


def ledger(planes, modulus=None):
    return {
        word: tuple(
            coefficient(
                q,
                tuple(planes[mode][word[mode]] for mode in range(4)),
                modulus,
            )
            for q in QUADRICS
        )
        for word in product(range(3), repeat=4)
    }


def matrix_rank(rows, modulus=None):
    return rank_mod(rows, modulus) if modulus is not None else rank_q(rows)


def input_ranks(data, modulus=None):
    answer = []
    for mode in range(4):
        rows = []
        for label in range(3):
            row = []
            for output in range(3):
                for other in product(range(3), repeat=3):
                    word = []
                    cursor = 0
                    for current_mode in range(4):
                        if current_mode == mode:
                            word.append(label)
                        else:
                            word.append(other[cursor])
                            cursor += 1
                    row.append(data[tuple(word)][output + 2])
            rows.append(row)
        answer.append(matrix_rank(rows, modulus))
    return tuple(answer)


def slice_ranks(data, output, modulus=None):
    answer = []
    for mode in range(4):
        rows = []
        for label in range(3):
            row = []
            for other in product(range(3), repeat=3):
                word = []
                cursor = 0
                for current_mode in range(4):
                    if current_mode == mode:
                        word.append(label)
                    else:
                        word.append(other[cursor])
                        cursor += 1
                row.append(data[tuple(word)][output + 2])
            rows.append(row)
        answer.append(matrix_rank(rows, modulus))
    return tuple(answer)


def projection_profile(planes, functionals, modulus=None):
    answer = []
    for plane in planes:
        rows = [
            [
                sum(a * b for a, b in zip(functional, vector, strict=True))
                for functional in functionals
            ]
            for vector in plane
        ]
        answer.append(matrix_rank(rows, modulus))
    return tuple(answer)


def mixed_radical_dimensions(planes, modulus=None):
    answer = []
    standard = tuple(tuple(int(i == j) for i in range(6)) for j in range(6))
    for mode in range(4):
        rows = []
        for q in (M1, M2):
            for labels in product(range(3), repeat=3):
                row = []
                for basis_vector in standard:
                    vectors = []
                    cursor = 0
                    for current_mode in range(4):
                        if current_mode == mode:
                            vectors.append(basis_vector)
                        else:
                            vectors.append(planes[current_mode][labels[cursor]])
                            cursor += 1
                    row.append(coefficient(q, tuple(vectors), modulus))
                rows.append(row)
        answer.append(6 - matrix_rank(rows, modulus))
    return tuple(answer)


def check_fixtures():
    assert hashlib.sha256(FIXTURE_JSON.encode()).hexdigest() == FIXTURE_SHA256
    hits_f3 = json.loads(FIXTURE_JSON)
    assert len(hits_f3) == 9
    observed = []
    for hit_f3 in hits_f3:
        planes = signed_lift(hit_f3)
        assert all(rank_q(plane) == 3 for plane in planes)
        data = ledger(planes)
        assert all(row[0] == row[1] == 0 for row in data.values())
        assert rank_q([row[2:] for row in data.values()]) == 3
        assert tuple(slice_ranks(data, output) for output in range(3)) == (
            (1, 1, 1, 1),
        ) * 3
        ranks = input_ranks(data)
        assert tuple(sorted(ranks)) == (1, 1, 2, 3)
        assert tuple(sorted(projection_profile(planes, APROJ))) == (0, 1, 1, 1)
        phi = (
            projection_profile(planes, PHI1),
            projection_profile(planes, PHI2),
        )
        radicals = mixed_radical_dimensions(planes)
        assert tuple(sorted(radicals)) == (3, 3, 5, 5)
        assert all(
            radicals[mode] == 5 for mode in range(4) if ranks[mode] == 1
        )

        data_f3 = ledger(hit_f3, P)
        assert all(row[0] == row[1] == 0 for row in data_f3.values())
        assert rank_mod([row[2:] for row in data_f3.values()]) == 3
        assert tuple(slice_ranks(data_f3, output, P) for output in range(3)) == (
            (1, 1, 1, 1),
        ) * 3
        observed.append((ranks, phi, radicals))
    assert tuple(observed) == EXPECTED_SUMMARIES
    return tuple(observed)


def main():
    basis_checks = check_basis_tensor_factorization()
    exception_checks = check_exception_patterns()
    fixture_summaries = check_fixtures()
    print("F3 ambient basis-tensor line-split checks: PASS", basis_checks)
    print("independent exception-pattern exhaustion: PASS", exception_checks)
    print("independent nine-fixture signed-Q replay: PASS")
    for index, summary in enumerate(fixture_summaries, start=1):
        print(index, summary)
    print("independent A-line-split exclusion audit: PASS")


if __name__ == "__main__":
    main()
