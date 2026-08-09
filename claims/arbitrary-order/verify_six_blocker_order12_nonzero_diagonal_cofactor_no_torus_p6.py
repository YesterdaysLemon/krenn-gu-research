#!/usr/bin/env python3
"""Verify the nonzero diagonal cofactor core and its no-torus P6 image."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_NONZERO_DIAGONAL_COFACTOR_NO_TORUS_P6.md"


def common_rows():
    output = []
    for mode in range(4):
        matrix = [[0] * 3 for _ in range(4)]
        matrix[mode][0] = 1
        matrix[(mode + 1) % 4][1] = 1
        output.append(matrix)
    output.extend(
        (
            ((0, -4, 4), (2, -3, 2), (2, 5, -6), (2, 1, -2)),
            ((-1, 0, -4), (-2, -4, 0), (0, -2, 4), (0, 1, -2)),
        )
    )
    return tuple(tuple(tuple(row) for row in matrix) for matrix in output)


def blocker_blocks():
    entries = {
        (0, 1): ((1478, 128, 0), (1007, 980, 0), (0, 0, 0)),
        (0, 2): ((-128, 384, 0), (-980, -120, 0), (0, 0, 0)),
        (0, 3): ((-384, 356, 0), (120, 1478, 0), (0, 0, 0)),
        (0, 4): ((640, 784, -784), (234, 1225, -1374), (0, 0, 0)),
        (0, 5): ((100, -384, 1296), (1672, 3772, -1240), (0, 0, 0)),
        (1, 2): ((980, 120, 0), (298, -512, 0), (0, 0, 0)),
        (1, 3): ((-120, -1478, 0), (512, -128, 0), (0, 0, 0)),
        (1, 4): ((-2248, 1796, -640), (-340, -2130, 2428), (0, 0, 0)),
        (1, 5): ((342, 256, 1240), (256, 980, -680), (0, 0, 0)),
        (2, 3): ((-512, 128, 0), (384, -384, 0), (0, 0, 0)),
        (2, 4): ((-256, 640, -640), (-512, 0, 1152), (0, 0, 0)),
        (2, 5): ((-256, -384, -512), (384, -128, 384), (0, 0, 0)),
        (3, 4): ((-256, -384, -384), (-640, 640, -640), (0, 0, 0)),
        (3, 5): ((-384, -256, 384), (256, 384, 128), (0, 0, 0)),
        (4, 5): ((576, 1536, 2304), (-256, 512, -512), (-416, -512, -640)),
    }
    return entries


PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))
PERMUTATIONS_6 = tuple(itertools.permutations(range(6)))


def permanent(matrix) -> int:
    permutations = PERMUTATIONS_4 if len(matrix) == 4 else PERMUTATIONS_6
    return sum(
        prod(matrix[row][permutation[row]] for row in range(len(matrix)))
        for permutation in permutations
    )


def prod(values):
    result = 1
    for value in values:
        result *= value
    return result


def cofactor(common, word, left: int, right: int) -> int:
    modes = [mode for mode in range(6) if mode not in (left, right)]
    return permanent(
        [[common[mode][root][word[mode]] for mode in modes] for root in range(4)]
    )


def coefficient(common, blocks, word) -> int:
    return sum(
        block[word[left]][word[right]] * cofactor(common, word, left, right)
        for (left, right), block in blocks.items()
    )


def coefficient_row(common, edges, indices, word):
    row = {}
    for left, right in edges:
        value = cofactor(common, word, left, right)
        if value:
            row[indices[left, right, word[left], word[right]]] = Fraction(value)
    return row


def add_exact_row(basis, source) -> bool:
    row = dict(source)
    while row:
        pivot = min(row)
        if pivot not in basis:
            inverse = Fraction(1, 1) / row[pivot]
            basis[pivot] = {
                column: value * inverse for column, value in row.items() if value
            }
            return True
        factor = row[pivot]
        for column, value in basis[pivot].items():
            updated = row.get(column, Fraction(0)) - factor * value
            if updated:
                row[column] = updated
            elif column in row:
                del row[column]
    return False


def exact_ranks(common, edges):
    variables = tuple(
        (left, right, row, column)
        for left, right in edges
        for row in range(3)
        for column in range(3)
    )
    indices = {variable: index for index, variable in enumerate(variables)}
    basis = {}
    off_count = 0
    for word in itertools.product(range(3), repeat=6):
        if len(set(word)) == 1:
            continue
        off_count += 1
        add_exact_row(basis, coefficient_row(common, edges, indices, word))
    off_rank = len(basis)
    diagonal_increments = []
    for colour in range(3):
        diagonal_increments.append(
            add_exact_row(
                basis,
                coefficient_row(common, edges, indices, (colour,) * 6),
            )
        )
    assert off_count == 726
    assert len(variables) == 135
    return off_rank, len(basis), diagonal_increments


def matrix_rank(matrix) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = Fraction(1, 1) / rows[rank][column]
        rows[rank] = [value * inverse for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                rows[index][entry] - factor * rows[rank][entry]
                for entry in range(columns)
            ]
        rank += 1
    return rank


def profile(matrix) -> int:
    rank = matrix_rank(matrix)
    mask = 0
    for colour in range(3):
        extended = [*matrix, [int(index == colour) for index in range(3)]]
        if matrix_rank(extended) == rank:
            mask |= 1 << colour
    return mask


def local_realization(common) -> dict[str, int]:
    x = (1, 1, 1)
    z_a = (1, 2, 3)
    z_b = (1, 3, 2)
    h_a = (1, -2, 1)
    h_b = (-1, -1, 2)
    alpha_a = (2, -1, 0)
    zeta_a = (-1, 1, 0)
    alpha_b = (Fraction(3, 2), Fraction(-1, 2), 0)
    zeta_b = (Fraction(-1, 2), Fraction(1, 2), 0)

    def dot(left, right):
        return sum(a * b for a, b in zip(left, right, strict=True))

    def outer(left, right):
        return tuple(tuple(a * b for b in right) for a in left)

    def add(left, right):
        return tuple(
            tuple(left[row][column] + right[row][column] for column in range(3))
            for row in range(3)
        )

    def contract(left, matrix):
        return tuple(
            sum(left[row] * matrix[row][column] for row in range(3))
            for column in range(3)
        )

    def bilinear(left, matrix, right):
        return dot(contract(left, matrix), right)

    assert dot(h_a, x) == dot(h_a, z_a) == 0
    assert dot(h_b, x) == dot(h_b, z_b) == 0
    assert dot(alpha_a, x) == 1 and dot(alpha_a, z_a) == 0
    assert dot(zeta_a, x) == 0 and dot(zeta_a, z_a) == 1
    assert dot(alpha_b, x) == 1 and dot(alpha_b, z_b) == 0
    assert dot(zeta_b, x) == 0 and dot(zeta_b, z_b) == 1

    root_pair = ((1, 0, 0), (0, -1, 0), (0, 0, 0))
    common_to_a = outer((1, 0, 0), h_a)
    common_to_b = outer((1, 0, 0), h_b)
    cross = outer(alpha_a, alpha_b)
    assert bilinear(x, root_pair, x) == 0
    assert bilinear(x, common_to_a, x) == bilinear(x, common_to_a, z_a) == 0
    assert bilinear(x, common_to_b, x) == bilinear(x, common_to_b, z_b) == 0
    assert bilinear(x, cross, x) == 1
    assert bilinear(x, cross, z_b) == bilinear(z_a, cross, x) == 0
    assert bilinear(z_a, cross, z_b) == 0

    appended = ((0, 0, 1),) * 4 + ((1, 0, 0),) * 2
    ranks = []
    profiles = []
    for mode in range(6):
        root_rows = [*common[mode], appended[mode]]
        ranks.append(matrix_rank(root_rows))
        profiles.append(profile(root_rows))
        assert matrix_rank([*root_rows, appended[mode]]) == 3

    pair_blocks = []
    pair_blocks.extend(root_pair for _ in itertools.combinations(range(4), 2))
    pair_blocks.extend(common_to_a for _ in range(4))
    pair_blocks.extend(common_to_b for _ in range(4))
    pair_blocks.append(cross)

    null_section = (1, -1, 0)
    for mode in range(6):
        for root in range(4):
            desired = common[mode][root]
            block = (
                outer((1, 0, 0), desired)
                if any(desired)
                else outer(null_section, (1, 0, 0))
            )
            assert contract(x, block) == desired
            pair_blocks.append(block)

        block_a = add(outer(alpha_a, appended[mode]), outer(zeta_a, appended[mode]))
        block_b = add(outer(alpha_b, appended[mode]), outer(zeta_b, appended[mode]))
        assert contract(x, block_a) == contract(z_a, block_a) == appended[mode]
        assert contract(x, block_b) == contract(z_b, block_b) == appended[mode]
        pair_blocks.extend((block_a, block_b))

    pair_blocks.extend(blocker_blocks().values())
    assert len(pair_blocks) == 66
    assert all(any(entry for row in block for entry in row) for block in pair_blocks)

    pair_blocks_nonzero = len(pair_blocks)

    word = (0, 0, 0, 2, 0, 0)
    endpoint = [
        [
            (common[mode][row] if row < 4 else appended[mode])[word[mode]]
            for mode in range(6)
        ]
        for row in range(6)
    ]
    endpoint_coefficient = permanent(endpoint)
    assert endpoint_coefficient == 4
    return {
        "pair_blocks_nonzero": pair_blocks_nonzero,
        "endpoint_off_diagonal_coefficient": endpoint_coefficient,
        "profile_sum": sum(profiles),
        "rank_sum": sum(ranks),
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero local construction and fixed-core obstruction",
        "rank_Q(Lambda_H^off)=108",
        "span{(-1,1,0)}",
        "all 66 pair blocks",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_CORE_NO_CONCISE_P6.md",
        "SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md",
    ):
        assert (ROOT / dependency).exists()

    common = common_rows()
    blocks = blocker_blocks()
    assert [matrix_rank(matrix) for matrix in common] == [2] * 6
    assert len(blocks) == 15
    assert all(
        any(entry for row in block for entry in row) for block in blocks.values()
    )
    assert (
        sum(entry != 0 for block in blocks.values() for row in block for entry in row)
        == 80
    )

    coefficients = tuple(
        coefficient(common, blocks, word)
        for word in itertools.product(range(3), repeat=6)
    )
    expected = [0] * (3**6)
    expected[0] = -1536
    # Lexicographic constant-one word has base-three index (3^6-1)/2.
    expected[(3**6 - 1) // 2] = 1536
    assert coefficients == tuple(expected)

    off_rank, full_rank, increments = exact_ranks(common, tuple(blocks))
    assert off_rank == 108
    assert full_rank == 109
    assert increments == [True, False, False]
    local = local_realization(common)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "common_row_ranks": [2] * 6,
                "blocker_blocks_nonzero": 15,
                "nonzero_block_entries": 80,
                "cofactor_diagonal": [-1536, 1536, 0],
                "off_diagonal_map_shape": [726, 135],
                "off_diagonal_rank_Q": off_rank,
                "off_diagonal_kernel_dimension_Q": 135 - off_rank,
                "full_map_rank_Q": full_rank,
                "diagonal_kernel_image_dimension_Q": full_rank - off_rank,
                "diagonal_kernel_image_torus_intersection": False,
                "local_realization": local,
                "global_matching_identity_realized": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
