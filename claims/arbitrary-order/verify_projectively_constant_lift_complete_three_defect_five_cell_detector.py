"""Primary exact checks for the complete three-defect five-cell detector."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import sympy as sp

MODES = tuple(range(5))
WORDS4 = tuple(product(range(3), repeat=4))
WORD4_INDEX = {word: index for index, word in enumerate(WORDS4)}
ZERO = (sp.Integer(0), sp.Integer(0), sp.Integer(0))
E0 = (sp.Integer(1), sp.Integer(0), sp.Integer(0))
E1 = (sp.Integer(0), sp.Integer(1), sp.Integer(0))


def collision_matrix(
    types: tuple[str, ...],
    deleted: int,
    ratios: tuple[sp.Expr, ...],
) -> sp.Matrix:
    """Matrix of h -> P4(h,a,a,b) after one mode deletion."""
    a_rows: list[tuple[sp.Expr, sp.Expr, sp.Expr]] = []
    b_rows: list[tuple[sp.Expr, sp.Expr, sp.Expr]] = []
    for mode, mode_type in enumerate(types):
        if mode_type == "R":
            a_rows.append((ratios[mode], sp.Integer(0), sp.Integer(0)))
            b_rows.append(E0)
        elif mode_type == "B":
            a_rows.append(ZERO)
            b_rows.append(E0)
        elif mode_type == "T":
            a_rows.append(E0)
            b_rows.append(E1)
        else:
            raise ValueError(mode_type)

    retained = tuple(mode for mode in MODES if mode != deleted)
    matrix = sp.zeros(81, 15)
    for h_mode in retained:
        for h_coord in range(3):
            column = 3 * h_mode + h_coord
            for b_mode in retained:
                if b_mode == h_mode:
                    continue
                local_rows = []
                for mode in retained:
                    if mode == h_mode:
                        local_rows.append(
                            tuple(sp.Integer(coord == h_coord) for coord in range(3))
                        )
                    elif mode == b_mode:
                        local_rows.append(b_rows[mode])
                    else:
                        local_rows.append(a_rows[mode])
                for word in WORDS4:
                    coefficient = sp.Integer(2)
                    for local_mode, coord in enumerate(word):
                        coefficient *= local_rows[local_mode][coord]
                    if coefficient:
                        matrix[WORD4_INDEX[word], column] += coefficient
    return matrix


def block_vector(blocks: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]) -> sp.Matrix:
    return sp.Matrix([entry for block in blocks for entry in block])


def coordinate_vector(mode: int, coord: int) -> sp.Matrix:
    vector = sp.zeros(15, 1)
    vector[3 * mode + coord] = 1
    return vector


def candidate_span_matches(matrix: sp.Matrix, candidates: list[sp.Matrix]) -> None:
    candidate_matrix = sp.Matrix.hstack(*candidates)
    assert candidate_matrix.rank() == len(candidates)
    residual = (matrix * candidate_matrix).applyfunc(sp.simplify)
    assert residual == sp.zeros(matrix.rows, len(candidates))
    assert matrix.rank() == 15 - len(candidates)


def assert_kernel_coordinates_zero(
    matrix: sp.Matrix,
    forbidden: tuple[tuple[int, int], ...],
) -> None:
    for vector in matrix.nullspace():
        assert all(vector[3 * mode + coord] == 0 for mode, coord in forbidden)


def assert_zero_b_coordinate_profiles() -> int:
    profiles = 0
    for root_axes in product(range(3), repeat=4):
        if len(set(root_axes)) != 3:
            continue
        profiles += 1
        multiplicities = Counter(root_axes)
        singleton_colours = [colour for colour, count in multiplicities.items() if count == 1]
        assert sorted(multiplicities.values()) == [1, 1, 2]
        assert len(singleton_colours) == 2
        singleton_rows = [root_axes.index(colour) for colour in singleton_colours]
        assert len(set(singleton_rows)) == 2
    assert profiles == 36
    return profiles


def assert_single_deletion_ledger() -> dict[str, int]:
    x, y = sp.symbols("x y", nonzero=True)
    ratios = (x, y, sp.Integer(1), sp.Integer(1), sp.Integer(1))

    rrb = ("R", "R", "B", "T", "T")
    rrtt = collision_matrix(rrb, 2, ratios)
    assert rrtt.rank() == 10
    assert_kernel_coordinates_zero(
        rrtt,
        ((0, 1), (0, 2), (1, 1), (1, 2), (3, 2), (4, 2)),
    )

    rbtt = collision_matrix(rrb, 0, ratios)
    assert rbtt.rank() == 9
    assert_kernel_coordinates_zero(
        rbtt,
        ((1, 1), (1, 2), (2, 1), (2, 2), (3, 2), (4, 2)),
    )

    rbb = ("R", "B", "B", "T", "T")
    bbtt = collision_matrix(rbb, 0, ratios)
    assert bbtt.rank() == 5
    assert_kernel_coordinates_zero(bbtt, ((1, 1), (1, 2), (2, 1), (2, 2)))
    return {"RRTT": 10, "RBTT": 9, "BBTT": 5}


def assert_rrb_kernels() -> tuple[int, int, int]:
    x, y = sp.symbols("x y", nonzero=True)
    ratios = (x, y, sp.Integer(1), sp.Integer(1), sp.Integer(1))
    types = ("R", "R", "B", "T", "T")
    matrices = [collision_matrix(types, deleted, ratios) for deleted in range(3)]

    rr_candidates = [
        block_vector(((-x, 0, 0), (-y, 0, 0), ZERO, E0, ZERO)),
        block_vector(((-x, 0, 0), (-y, 0, 0), ZERO, ZERO, E0)),
        block_vector((E0, E0, (-1, 0, 0), E1, E1)),
    ]
    candidate_span_matches(matrices[0].col_join(matrices[1]), rr_candidates)

    rows_r0_b = (0, 1, 2, 3, 6, 9, 18, 27, 54, 81, 82, 84, 85, 108, 135)
    combined_r0_b = matrices[0].col_join(matrices[2])
    determinant_r0_b = sp.factor(combined_r0_b[list(rows_r0_b), :].det())
    assert determinant_r0_b == -196608 * x**3 * y**7

    rows_r1_b = (0, 1, 2, 3, 6, 9, 18, 27, 54, 81, 82, 84, 85, 90, 99)
    combined_r1_b = matrices[1].col_join(matrices[2])
    determinant_r1_b = sp.factor(combined_r1_b[list(rows_r1_b), :].det())
    assert determinant_r1_b == 196608 * x**7 * y**3
    return 3, 0, 0


def assert_rrr_kernels() -> tuple[int, int, int, int]:
    x, y, z = sp.symbols("x y z", nonzero=True)
    generic_ratios = (x, y, z, sp.Integer(1), sp.Integer(1))
    types = ("R", "R", "R", "T", "T")
    generic = [
        collision_matrix(types, deleted, generic_ratios) for deleted in range(3)
    ]
    rows = (0, 1, 3, 4, 5, 7, 9, 18, 27, 54, 81, 82, 84, 108, 135)
    determinant = sp.factor(generic[0].col_join(generic[1])[list(rows), :].det())
    assert determinant == 196608 * y**3 * z**7 * (x - y) ** 2

    equal_pair_ratios = (x, x, z, sp.Integer(1), sp.Integer(1))
    equal_pair = [
        collision_matrix(types, deleted, equal_pair_ratios) for deleted in range(3)
    ]
    first = block_vector(
        (
            (-x * (2 * x + z), 0, 0),
            (-x * (2 * x + z), 0, 0),
            (z * (x + 2 * z), 0, 0),
            (x - z, 0, 0),
            (x - z, 0, 0),
        )
    )
    second = block_vector(
        (
            (x * (x + z) * (2 * x + z), 0, 0),
            (x * (x + z) * (2 * x + z), 0, 0),
            (-z * (x + z) * (x + 2 * z), 0, 0),
            (-2 * (x + z) * (x - z), -x * z * (x - z), 0),
            (0, x * z * (x - z), 0),
        )
    )
    candidate_span_matches(equal_pair[0].col_join(equal_pair[1]), [first, second])

    all_equal_ratios = (x, x, x, sp.Integer(1), sp.Integer(1))
    all_equal = [
        collision_matrix(types, deleted, all_equal_ratios) for deleted in range(3)
    ]
    line = block_vector(((-1, 0, 0), (-1, 0, 0), E0, ZERO, ZERO))
    transverse = block_vector((ZERO, ZERO, ZERO, (-2, -x, 0), (2, x, 0)))
    candidate_span_matches(all_equal[0].col_join(all_equal[1]), [line, transverse])
    candidate_span_matches(
        all_equal[0].col_join(all_equal[1]).col_join(all_equal[2]),
        [transverse],
    )
    return 0, 2, 2, 1


def assert_rbb_kernels() -> int:
    x = sp.symbols("x", nonzero=True)
    ratios = (x, sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Integer(1))
    types = ("R", "B", "B", "T", "T")
    combined = sp.Matrix.vstack(
        *(collision_matrix(types, deleted, ratios) for deleted in range(3))
    )
    candidates = [
        block_vector(((-x, 0, 0), ZERO, ZERO, E0, ZERO)),
        block_vector(((-x, 0, 0), ZERO, ZERO, ZERO, E0)),
    ]
    candidate_span_matches(combined, candidates)
    return 2


def assert_bbb_kernels() -> tuple[int, int]:
    ratios = (sp.Integer(1),) * 5
    types = ("B", "B", "B", "T", "T")
    matrices = [collision_matrix(types, deleted, ratios) for deleted in range(3)]

    pair_candidates = [
        block_vector(((-1, 0, 0), (-1, 0, 0), E0, ZERO, ZERO)),
        *[coordinate_vector(mode, coord) for mode in (3, 4) for coord in range(3)],
    ]
    candidate_span_matches(matrices[0].col_join(matrices[1]), pair_candidates)

    triple_candidates = [
        coordinate_vector(mode, coord) for mode in (3, 4) for coord in range(3)
    ]
    candidate_span_matches(sp.Matrix.vstack(*matrices), triple_candidates)
    return 7, 6


def assert_inactive_set_census() -> dict[str, int]:
    roots = frozenset(range(4))
    subsets = [
        frozenset(indices)
        for size in range(2, 5)
        for indices in combinations(range(4), size)
    ]
    pairs = [frozenset(indices) for indices in combinations(range(4), 2)]

    rrb = [
        (left, right, b_set)
        for left, right, b_set in product(subsets, repeat=3)
        if not left.intersection(b_set) and not right.intersection(b_set)
    ]
    assert len(rrb) == 6
    assert all(
        len(left) == len(right) == len(b_set) == 2
        and left == right == roots - b_set
        for left, right, b_set in rrb
    )

    rrr_distinct = [
        sets
        for sets in product(pairs, repeat=3)
        if all(not sets[i].intersection(sets[j]) for i, j in combinations(range(3), 2))
    ]
    assert not rrr_distinct

    rrr_two_equal = [
        sets
        for sets in product(pairs, repeat=3)
        if not sets[0].intersection(sets[2])
        and not sets[1].intersection(sets[2])
    ]
    assert len(rrr_two_equal) == 6
    assert all(sets[0] == sets[1] == roots - sets[2] for sets in rrr_two_equal)

    equal_ratio_patterns = []
    for sets in product(pairs, repeat=3):
        if set.intersection(*(set(item) for item in sets)):
            continue
        degrees = tuple(
            sorted((sum(root in item for item in sets) for root in roots), reverse=True)
        )
        equal_ratio_patterns.append(degrees)
    degree_counts = Counter(equal_ratio_patterns)
    assert degree_counts == Counter({(2, 2, 1, 1): 90, (2, 2, 2, 0): 24})

    rbb = []
    for r_set, b_left, b_right in product(subsets, pairs, pairs):
        if b_left.union(b_right) == roots:
            continue
        if b_left != b_right:
            continue
        if not r_set.issubset(b_left):
            continue
        rbb.append((r_set, b_left, b_right))
    assert len(rbb) == 6
    assert all(r_set == b_left == b_right for r_set, b_left, b_right in rbb)

    return {
        "RRB": len(rrb),
        "RRR-two-equal": len(rrr_two_equal),
        "RRR/BBB-equal-ratio": sum(degree_counts.values()),
        "RBB": len(rbb),
    }


def assert_four_b_pair_tensor_boundary() -> int:
    assignments = 0
    for b_mode_count in (4, 5):
        modes = tuple(range(5))
        b_modes = frozenset(range(b_mode_count))
        # The two h rows and the single b row can occupy at most three modes
        # at which either copy of a vanishes.
        for h_left, h_right, b_mode in product(modes, repeat=3):
            if len({h_left, h_right, b_mode}) != 3:
                continue
            assignments += int(b_modes.issubset({h_left, h_right, b_mode}))
    assert assignments == 0
    return 2


def main() -> None:
    profiles = assert_zero_b_coordinate_profiles()
    ranks = assert_single_deletion_ledger()
    rrb = assert_rrb_kernels()
    rrr = assert_rrr_kernels()
    rbb = assert_rbb_kernels()
    bbb = assert_bbb_kernels()
    inactive = assert_inactive_set_census()
    boundary = assert_four_b_pair_tensor_boundary()
    print(f"PASS: {profiles} rank-three zero-b profiles have two singleton colours")
    print(f"PASS: exact retained collision ranks are {ranks}")
    print(f"PASS: RRB common-kernel nullities are {rrb}")
    print(f"PASS: RRR unequal/equal/triple nullities are {rrr}")
    print(f"PASS: RBB triple nullity is {rbb}; BBB pair/triple nullities are {bbb}")
    print(f"PASS: inactive-set ledgers are {inactive}")
    print(f"PASS: {boundary} four-or-five-B pair-tensor boundaries are structural zeros")
    print("SCOPE: every exactly-three-defect R/B five-cell is detected")
    print("SCOPE: four/five R/B defects and global Krenn-Gu remain open")
    print("searches=0")


if __name__ == "__main__":
    main()
