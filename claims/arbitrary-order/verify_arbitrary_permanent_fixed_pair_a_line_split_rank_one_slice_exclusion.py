"""Exact checks for the fixed-pair A-line-split rank-one-slice exclusion."""

from collections import Counter
import hashlib
from itertools import combinations, permutations, product
import json

import sympy as sp


EDGES = tuple(combinations(range(4), 2))
FULL6 = (1 << 6) - 1

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


HITS_F3 = (
    (
        ((1, 0, 1, 0, 1, 2), (0, 1, 1, 0, 0, 0), (0, 0, 0, 1, 1, 2)),
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 0, 2, 1), (0, 0, 1, 1, 0, 0)),
        ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 1)),
        ((2, 1, 0, 0, 0, 0), (2, 0, 1, 0, 0, 0), (1, 0, 0, 1, 0, 0)),
    ),
    (
        ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 1)),
        ((1, 0, 0, 2, 2, 1), (0, 1, 0, 0, 1, 2), (0, 0, 1, 0, 1, 2)),
        ((1, 0, 0, 0, 2, 1), (0, 1, 1, 0, 1, 2), (0, 0, 0, 1, 2, 1)),
        ((2, 1, 0, 0, 0, 0), (2, 0, 1, 0, 0, 0), (1, 0, 0, 1, 0, 0)),
    ),
    (
        ((1, 0, 0, 2, 2, 2), (0, 1, 0, 0, 1, 1), (0, 0, 1, 2, 2, 2)),
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0)),
        ((1, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 1, 2, 2)),
        ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 2, 1)),
    ),
    (
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 2, 0, 0), (0, 0, 1, 1, 0, 0)),
        ((1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 2, 1), (0, 0, 1, 2, 0, 0)),
        ((1, 0, 1, 0, 0, 0), (0, 1, 1, 0, 0, 0), (0, 0, 0, 1, 1, 2)),
        ((0, 2, 1, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1)),
    ),
    (
        ((1, 0, 0, 0, 1, 1), (0, 1, 1, 0, 2, 2), (0, 0, 0, 1, 2, 2)),
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0)),
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 0, 0, 0), (0, 0, 1, 2, 2, 2)),
        ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 2, 1)),
    ),
    (
        ((1, 1, 0, 0, 0, 0), (0, 0, 1, 0, 2, 2), (0, 0, 0, 1, 1, 1)),
        ((1, 0, 0, 2, 0, 0), (0, 1, 0, 0, 2, 2), (0, 0, 1, 0, 0, 0)),
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0)),
        ((1, 1, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 2, 1)),
    ),
    (
        ((1, 0, 1, 0, 0, 0), (0, 1, 2, 0, 1, 1), (0, 0, 0, 1, 0, 0)),
        ((0, 1, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 2)),
        ((1, 0, 0, 1, 1, 1), (0, 1, 0, 2, 1, 1), (0, 0, 1, 2, 0, 0)),
        ((1, 1, 0, 0, 0, 0), (2, 0, 1, 0, 0, 0), (1, 0, 0, 1, 0, 0)),
    ),
    (
        ((1, 0, 0, 1, 0, 0), (0, 1, 0, 2, 0, 0), (0, 0, 1, 1, 0, 0)),
        ((1, 0, 1, 0, 0, 0), (0, 1, 0, 0, 2, 1), (0, 0, 0, 1, 1, 2)),
        ((1, 0, 1, 0, 0, 0), (0, 1, 2, 2, 0, 0), (0, 0, 0, 0, 1, 2)),
        ((0, 2, 1, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1)),
    ),
    (
        ((0, 1, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 2)),
        ((1, 0, 2, 2, 0, 0), (0, 1, 1, 2, 0, 0), (0, 0, 0, 0, 1, 1)),
        ((1, 0, 0, 0, 1, 1), (0, 1, 0, 1, 0, 0), (0, 0, 1, 0, 2, 2)),
        ((1, 1, 0, 0, 0, 0), (2, 0, 1, 0, 0, 0), (1, 0, 0, 1, 0, 0)),
    ),
)

EXPECTED_Q_PHI = (
    ((3, 1, 2, 1), (3, 2, 2, 1)),
    ((2, 3, 3, 1), (2, 2, 3, 1)),
    ((2, 1, 2, 2), (3, 1, 3, 2)),
    ((1, 2, 3, 2), (2, 3, 3, 1)),
    ((2, 1, 2, 2), (3, 1, 3, 2)),
    ((2, 2, 1, 2), (2, 3, 1, 2)),
    ((2, 2, 3, 1), (3, 1, 3, 2)),
    ((1, 3, 3, 2), (2, 2, 3, 1)),
    ((2, 3, 3, 1), (1, 3, 2, 2)),
)
FIXTURE_SHA256 = "b24836d1b7f47f7de00f045d15015b3568cf6a63958402c3d3c4d2b2765e19ad"


def multiply(left, right, modulus=None):
    out = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            value = out.get(left_mask | right_mask, 0) + left_value * right_value
            if modulus is not None:
                value %= modulus
            out[left_mask | right_mask] = value
    return {mask: value for mask, value in out.items() if value != 0}


def coefficient(q, vectors, modulus=None):
    polynomial = {
        (1 << i) | (1 << j): value
        for value, (i, j) in zip(q, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {1 << i: value for i, value in enumerate(vector) if value}
        polynomial = multiply(polynomial, linear, modulus)
    value = polynomial.get(FULL6, 0)
    return value % modulus if modulus is not None else value


def rank_mod(rows, modulus):
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
        for i, row in enumerate(matrix):
            if i != rank and row[column]:
                scale = row[column]
                matrix[i] = [
                    (x - scale * y) % modulus
                    for x, y in zip(row, matrix[rank], strict=True)
                ]
        rank += 1
    return rank


def signed_lift(hit):
    return tuple(
        tuple(tuple(-1 if value == 2 else value for value in row) for row in plane)
        for plane in hit
    )


def tensor_ledger(planes, modulus=None):
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


def tensor_input_ranks(ledger, modulus=None):
    ranks = []
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
                    row.append(ledger[tuple(word)][output + 2])
            rows.append(row)
        ranks.append(rank_mod(rows, modulus) if modulus else sp.Matrix(rows).rank())
    return tuple(ranks)


def slice_multilinear_ranks(ledger, output, modulus=None):
    ranks = []
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
                row.append(ledger[tuple(word)][output + 2])
            rows.append(row)
        ranks.append(rank_mod(rows, modulus) if modulus else sp.Matrix(rows).rank())
    return tuple(ranks)


def projection_profile(planes, rows, modulus=None):
    profile = []
    for plane in planes:
        matrix = [
            [sum(a * b for a, b in zip(functional, vector, strict=True)) for functional in rows]
            for vector in plane
        ]
        profile.append(rank_mod(matrix, modulus) if modulus else sp.Matrix(matrix).rank())
    return tuple(profile)


def mixed_contraction_rows(planes, mode, modulus=None):
    rows = []
    for q in (M1, M2):
        for other_labels in product(range(3), repeat=3):
            row = []
            for coordinate in range(6):
                vectors = []
                cursor = 0
                for current_mode in range(4):
                    if current_mode == mode:
                        vectors.append(tuple(int(i == coordinate) for i in range(6)))
                    else:
                        vectors.append(planes[current_mode][other_labels[cursor]])
                        cursor += 1
                row.append(coefficient(q, tuple(vectors), modulus))
            rows.append(row)
    return rows


def check_symbolic_factorization():
    g_symbols = sp.symbols("g01 g02 g03 g12 g13 g23")
    alphas = sp.symbols("alpha2 alpha3 alpha4")
    u = tuple(tuple(sp.symbols(f"u{mode}4 u{mode}5")) for mode in (2, 3, 4))
    r = tuple(
        tuple(sp.symbols(f"r{mode}0 r{mode}1 r{mode}2 r{mode}3"))
        for mode in (2, 3, 4, 5)
    )
    vectors = tuple(
        (*r[index], alphas[index] * u[index][0], alphas[index] * u[index][1])
        for index in range(3)
    ) + ((*r[3], 0, 0),)

    direct_value = 0
    for coefficient_value, (i, j) in zip(g_symbols, EDGES, strict=True):
        coordinates = (4, 5, i, j)
        for assignment in permutations(coordinates):
            direct_value += coefficient_value * sp.prod(
                vectors[mode][coordinate] for mode, coordinate in enumerate(assignment)
            )

    def j(left, right):
        return left[0] * right[1] + left[1] * right[0]

    def g_pair(left, right):
        return sum(
            value * (left[i] * right[j] + left[j] * right[i])
            for value, (i, j) in zip(g_symbols, EDGES, strict=True)
        )

    rhs = (
        j(u[0], u[1]) * alphas[0] * alphas[1] * g_pair(r[2], r[3])
        + j(u[0], u[2]) * alphas[0] * alphas[2] * g_pair(r[1], r[3])
        + j(u[1], u[2]) * alphas[1] * alphas[2] * g_pair(r[0], r[3])
    )
    assert sp.expand(direct_value - rhs) == 0
    return len(sp.Add.make_args(sp.expand(direct_value)))


def check_exception_count():
    histogram = Counter()
    for exceptions in product((-1, 0, 1, 2), repeat=3):
        counts = tuple(exceptions.count(mode) for mode in range(3))
        assert sum(counts) <= 3
        assert sum(count <= 1 for count in counts) >= 2
        histogram[tuple(sorted(counts))] += 1
    assert sum(histogram.values()) == 64
    return dict(sorted(histogram.items()))


def check_fixtures():
    payload = json.dumps(HITS_F3, separators=(",", ":")).encode()
    assert hashlib.sha256(payload).hexdigest() == FIXTURE_SHA256
    summaries = []
    for index, hit_f3 in enumerate(HITS_F3):
        planes = signed_lift(hit_f3)
        assert all(sp.Matrix(plane).rank() == 3 for plane in planes)
        ledger = tensor_ledger(planes)
        assert all(row[0] == row[1] == 0 for row in ledger.values())
        assert sp.Matrix([row[2:] for row in ledger.values()]).rank() == 3
        slice_ranks = tuple(slice_multilinear_ranks(ledger, output) for output in range(3))
        assert slice_ranks == ((1, 1, 1, 1),) * 3
        input_ranks = tensor_input_ranks(ledger)
        assert tuple(sorted(input_ranks)) == (1, 1, 2, 3)
        a_profile = projection_profile(planes, APROJ)
        assert tuple(sorted(a_profile)) == (0, 1, 1, 1)
        phi_profiles = (
            projection_profile(planes, PHI1),
            projection_profile(planes, PHI2),
        )
        assert phi_profiles == EXPECTED_Q_PHI[index]

        radical_dimensions = []
        for mode in range(4):
            rows = mixed_contraction_rows(planes, mode)
            rank = sp.Matrix(rows).rank()
            radical_dimensions.append(6 - rank)
            if input_ranks[mode] == 1:
                assert rank == 1
                generator = sp.Matrix(rows).rowspace()[0]
                assert all(generator[coordinate] == 0 for coordinate in range(4))
                assert generator[4] != 0 and generator[5] != 0
                assert sp.simplify((generator[4] / generator[5]) ** 2) == 1
        assert tuple(sorted(radical_dimensions)) == (3, 3, 5, 5)
        assert all(
            radical_dimensions[mode] == 5
            for mode in range(4)
            if input_ranks[mode] == 1
        )

        ledger_f3 = tensor_ledger(hit_f3, 3)
        assert all(row[0] == row[1] == 0 for row in ledger_f3.values())
        assert rank_mod([row[2:] for row in ledger_f3.values()], 3) == 3
        assert tuple(
            slice_multilinear_ranks(ledger_f3, output, 3) for output in range(3)
        ) == ((1, 1, 1, 1),) * 3
        summaries.append((input_ranks, phi_profiles, tuple(radical_dimensions)))
    return tuple(summaries)


def main():
    symbolic_terms = check_symbolic_factorization()
    exception_histogram = check_exception_count()
    fixture_summaries = check_fixtures()
    print("symbolic line-split factorization: PASS", symbolic_terms)
    print("exception-pattern exhaustion: PASS", exception_histogram)
    print("nine signed-Q fixture replays: PASS")
    for index, summary in enumerate(fixture_summaries, start=1):
        print(index, summary)
    print("A-line-split rank-one-slice exclusion verification: PASS")


if __name__ == "__main__":
    main()
