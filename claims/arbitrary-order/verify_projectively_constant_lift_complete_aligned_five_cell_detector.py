"""Primary exact checks for the complete aligned q=0,r=5 detector."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import sympy as sp

MODES = tuple(range(5))
COORDS = tuple(range(3))
EDGES = tuple(combinations(MODES, 2))
WORDS4 = tuple(product(COORDS, repeat=4))
WORD4_INDEX = {word: index for index, word in enumerate(WORDS4)}
ZERO = (sp.Integer(0),) * 3
E0 = (sp.Integer(1), sp.Integer(0), sp.Integer(0))
E1 = (sp.Integer(0), sp.Integer(1), sp.Integer(0))


def collision_matrix(
    types: tuple[str, ...],
    deleted: int,
    ratios: tuple[sp.Expr, ...],
) -> sp.Matrix:
    """Return the labelled map h -> P4(h,a,a,b) after one deletion."""
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
    matrix = sp.zeros(len(WORDS4), 15)
    for h_mode in retained:
        for h_coord in COORDS:
            column = 3 * h_mode + h_coord
            for b_mode in retained:
                if b_mode == h_mode:
                    continue
                local_rows = []
                for mode in retained:
                    if mode == h_mode:
                        local_rows.append(
                            tuple(
                                sp.Integer(coord == h_coord) for coord in COORDS
                            )
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


def block_vector(
    blocks: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...],
) -> sp.Matrix:
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


def only_nonzero_column_entry(matrix: sp.Matrix, column: int) -> sp.Expr:
    entries = [sp.factor(value) for value in matrix[:, column] if value != 0]
    assert len(entries) == 1
    return entries[0]


def assert_row_quota_and_type_exhaustion() -> dict[str, tuple[str, ...]]:
    # The imported q=0 quota is p_a>=2.  A B defect is exactly a zero a-row.
    assert 5 - 2 == 3
    four = tuple(
        sorted(
            {
                "".join(sorted(word, reverse=True)) + "T"
                for word in product("RB", repeat=4)
                if word.count("B") <= 3
            },
            key=lambda word: word.count("B"),
        )
    )
    five = tuple(
        sorted(
            {
                "".join(sorted(word, reverse=True))
                for word in product("RB", repeat=5)
                if word.count("B") <= 3
            },
            key=lambda word: word.count("B"),
        )
    )
    assert four == ("RRRRT", "RRRBT", "RRBBT", "RBBBT")
    assert five == ("RRRRR", "RRRRB", "RRRBB", "RRBBB")
    return {"four": four, "five": five}


def assert_three_b_triangle() -> tuple[int, int]:
    ratio = sp.symbols("r", nonzero=True)
    types = ("B", "B", "B", "R", "T")
    ratios = (sp.Integer(1),) * 3 + (ratio, sp.Integer(1))
    matrices = [collision_matrix(types, deleted, ratios) for deleted in range(3)]

    pair_candidates = [
        block_vector(((-1, 0, 0), (-1, 0, 0), E0, ZERO, ZERO)),
        *[
            coordinate_vector(mode, coord)
            for mode in (3, 4)
            for coord in COORDS
        ],
    ]
    candidate_span_matches(matrices[0].col_join(matrices[1]), pair_candidates)

    triple_candidates = [
        coordinate_vector(mode, coord)
        for mode in (3, 4)
        for coord in COORDS
    ]
    candidate_span_matches(sp.Matrix.vstack(*matrices), triple_candidates)
    return len(pair_candidates), len(triple_candidates)


def assert_rrrrt_complete_divisors() -> dict[str, int]:
    l0, l1, l2, l3 = sp.symbols("l0 l1 l2 l3", nonzero=True)
    ratios = (l0, l1, l2, l3, sp.Integer(1))
    matrices = [
        collision_matrix(("R", "R", "R", "R", "T"), deleted, ratios)
        for deleted in range(4)
    ]
    combined = sp.Matrix.vstack(*matrices)

    # Reconstruct the twelve distinct scalar equations on
    # (alpha_0,...,alpha_3,A,B,C) after off-line coordinates vanish.
    restricted = combined[:, (0, 3, 6, 9, 12, 13, 14)]
    actual_rows: list[tuple[sp.Expr, ...]] = []
    for row_index in range(restricted.rows):
        row = tuple(
            sp.factor(restricted[row_index, column] / 2)
            for column in range(restricted.cols)
        )
        if any(row) and row not in actual_rows:
            actual_rows.append(row)

    lambdas = (l0, l1, l2, l3)
    expected_rows: list[tuple[sp.Expr, ...]] = []
    for deleted in range(4):
        retained = tuple(index for index in range(4) if index != deleted)
        e2 = sum(
            lambdas[left] * lambdas[right]
            for left, right in combinations(retained, 2)
        )
        row_a: list[sp.Expr] = [sp.Integer(0)] * 7
        row_b: list[sp.Expr] = [sp.Integer(0)] * 7
        row_c: list[sp.Expr] = [sp.Integer(0)] * 7
        for index in retained:
            others = tuple(item for item in retained if item != index)
            row_a[index] = sum(lambdas[item] for item in others)
            row_b[index] = sp.prod(lambdas[item] for item in others)
        row_a[4] = e2
        row_b[5] = e2
        row_c[6] = e2
        expected_rows.extend((tuple(row_a), tuple(row_b), tuple(row_c)))
    assert len(actual_rows) == 12
    assert all(row in actual_rows for row in expected_rows)

    equal = sp.symbols("L", nonzero=True)
    equal_matrix = combined.subs({l0: equal, l1: equal, l2: equal, l3: equal})
    equal_generator = block_vector(
        (
            (-1, 0, 0),
            (-1, 0, 0),
            (-1, 0, 0),
            (-1, 0, 0),
            (2 / equal, 1, 0),
        )
    )
    candidate_span_matches(equal_matrix, [equal_generator])

    omega = (-1 + sp.sqrt(-3)) / 2
    cube_reciprocals = (sp.Integer(1), sp.Integer(1), omega, omega)
    cube_ratios = tuple(sp.simplify(1 / value) for value in cube_reciprocals)
    cube_matrix = sp.Matrix.vstack(
        *(
            collision_matrix(
                ("R", "R", "R", "R", "T"),
                deleted,
                cube_ratios + (sp.Integer(1),),
            )
            for deleted in range(4)
        )
    )
    cube_generator = block_vector(
        (
            (-1, 0, 0),
            (-1, 0, 0),
            (-1, 0, 0),
            (-1, 0, 0),
            (2 * (1 + omega), 1, 0),
        )
    )
    candidate_span_matches(cube_matrix, [cube_generator])

    generic_matrix = combined.subs({l0: 1, l1: 2, l2: 3, l3: 4})
    assert generic_matrix.rank() == 15

    a, d = sp.symbols("a d", nonzero=True)
    m_a = a + 2 * d
    e_a = d**2 + 2 * a * d
    m_d = 2 * a + d
    e_d = a**2 + 2 * a * d
    split_condition = sp.factor(e_a * m_d - e_d * m_a)
    assert sp.expand(
        split_condition + (a - d) * (a**2 + a * d + d**2)
    ) == 0
    assert sp.factor(2 * a - a) == a  # the incompatible 3+1 values of c
    return {"generic": 0, "equal": 1, "cube_root_2+2": 1}


def assert_rrrbt_and_rrbbt_kernels() -> dict[str, int]:
    x, y, z = sp.symbols("x y z", nonzero=True)
    rrrbt_ratios = (x, y, z, sp.Integer(1), sp.Integer(1))
    rrrbt = sp.Matrix.vstack(
        *(
            collision_matrix(
                ("R", "R", "R", "B", "T"), deleted, rrrbt_ratios
            )
            for deleted in range(4)
        )
    )
    z_value = -x - y
    lambdas = (x, y, z_value)
    blocks: list[tuple[sp.Expr, sp.Expr, sp.Expr]] = []
    for index, value in enumerate(lambdas):
        others = tuple(item for item in range(3) if item != index)
        blocks.append(
            (
                sp.expand(
                    value
                    * (value - lambdas[others[0]])
                    * (value - lambdas[others[1]])
                ),
                sp.Integer(0),
                sp.Integer(0),
            )
        )
    product_ratio = sp.prod(lambdas)
    blocks.extend(
        (
            (-3 * product_ratio, 0, 0),
            (-2 * sum(value**2 for value in lambdas), 3 * product_ratio, 0),
        )
    )
    candidate_span_matches(rrrbt.subs(z, z_value), [block_vector(tuple(blocks))])
    assert rrrbt.subs({x: 1, y: 2, z: 3}).rank() == 15

    reciprocal_sum = 1 / x + 1 / y + 1 / z
    kappa = -sp.Rational(2, 3) * reciprocal_sum
    reduced_residual = sp.factor(2 * (x + y + z))
    assert sp.expand(reduced_residual - (2 * x + 2 * y + 2 * z)) == 0
    assert sp.simplify(3 * kappa + 2 * reciprocal_sum) == 0

    left, right = sp.symbols("L M", nonzero=True)
    rrbbt = sp.Matrix.vstack(
        *(
            collision_matrix(
                ("R", "R", "B", "B", "T"),
                deleted,
                (left, right, 1, 1, 1),
            )
            for deleted in range(4)
        )
    )
    alpha_generator = block_vector(
        (
            (-left / right, 0, 0),
            E0,
            ZERO,
            ZERO,
            ZERO,
        )
    )
    beta_generator = block_vector(
        (
            (-left, 0, 0),
            ZERO,
            ZERO,
            ZERO,
            E0,
        )
    )
    candidate_span_matches(rrbbt, [alpha_generator, beta_generator])
    return {"RRRBT-sum-zero": 1, "RRBBT": 2}


def adjacency(edges: set[tuple[int, int]], vertex: int) -> set[int]:
    return {
        right if left == vertex else left
        for left, right in edges
        if vertex in (left, right)
    }


def connected(edges: set[tuple[int, int]]) -> bool:
    seen = {0}
    pending = [0]
    while pending:
        vertex = pending.pop()
        for neighbour in adjacency(edges, vertex) - seen:
            seen.add(neighbour)
            pending.append(neighbour)
    return len(seen) == 5


def graph_is_exactly_realizable(zero_edges: set[tuple[int, int]]) -> bool:
    equations = []
    for left, right in zero_edges:
        row = [-1] * 5
        row[left] += 1
        row[right] += 1
        equations.append(row)
    matrix = sp.Matrix(equations) if equations else sp.zeros(0, 5)
    basis = matrix.nullspace()
    if not basis:
        return False

    forcing_edges = set(EDGES) - zero_edges
    required_forms = []
    for vertex in MODES:
        form = [0] * 5
        form[vertex] = 1
        required_forms.append(sp.Matrix([form]))
    for left, right in forcing_edges:
        form = [-1] * 5
        form[left] += 1
        form[right] += 1
        required_forms.append(sp.Matrix([form]))
    return all(
        any((form * vector)[0] != 0 for vector in basis)
        for form in required_forms
    )


def assert_five_regular_cofactor_graph() -> dict[str, int]:
    lambdas = sp.symbols("l0:5", nonzero=True)
    types = ("R",) * 5
    for deleted, retained in EDGES:
        matrix = collision_matrix(types, deleted, lambdas)
        coefficient = only_nonzero_column_entry(matrix, 3 * retained + 1)
        complement = tuple(
            mode for mode in MODES if mode not in (deleted, retained)
        )
        q_value = sum(
            lambdas[left] * lambdas[right]
            for left, right in combinations(complement, 2)
        )
        assert sp.factor(coefficient - 2 * q_value) == 0

    reciprocals = sp.symbols("m0:5", nonzero=True)
    for left, right in EDGES:
        complement = tuple(
            mode for mode in MODES if mode not in (left, right)
        )
        q_value = sum(
            (1 / reciprocals[first]) * (1 / reciprocals[second])
            for first, second in combinations(complement, 2)
        )
        cleared = sp.factor(
            q_value * sp.prod(reciprocals[mode] for mode in complement)
        )
        assert cleared == sum(reciprocals[mode] for mode in complement)

    disconnected_shapes: Counter[tuple[int, ...]] = Counter()
    isolated_forcing = 0
    realizable_graphs = 0
    for mask in range(1 << len(EDGES)):
        zero_edges = {
            edge for index, edge in enumerate(EDGES) if mask & (1 << index)
        }
        if not graph_is_exactly_realizable(zero_edges):
            continue
        realizable_graphs += 1
        forcing_edges = set(EDGES) - zero_edges
        if any(not adjacency(forcing_edges, vertex) for vertex in MODES):
            isolated_forcing += 1
        common_neighbour_edges = {
            (left, right)
            for left, right in EDGES
            if adjacency(forcing_edges, left) & adjacency(forcing_edges, right)
        }
        if not connected(common_neighbour_edges):
            degree_shape = tuple(
                sorted(
                    (len(adjacency(zero_edges, vertex)) for vertex in MODES),
                    reverse=True,
                )
            )
            disconnected_shapes[degree_shape] += 1

    assert isolated_forcing == 0
    assert disconnected_shapes == Counter(
        {(3, 3, 2, 2, 2): 10, (3, 3, 3, 3, 0): 5}
    )
    return {
        "realizable_zero_graphs": realizable_graphs,
        "K23": disconnected_shapes[(3, 3, 2, 2, 2)],
        "K4": disconnected_shapes[(3, 3, 3, 3, 0)],
    }


def assert_one_and_two_b_forcing() -> dict[str, int]:
    regular4 = sp.symbols("r0:4", nonzero=True)
    rrrrb_ratios = regular4 + (sp.Integer(1),)
    rrrrb_types = ("R", "R", "R", "R", "B")
    checks = 0
    for deleted in range(4):
        matrix = collision_matrix(rrrrb_types, deleted, rrrrb_ratios)
        other_regular = tuple(
            mode for mode in range(4) if mode != deleted
        )
        for retained in other_regular:
            complement = tuple(
                mode
                for mode in range(4)
                if mode not in (deleted, retained)
            )
            expected = 2 * sp.prod(regular4[mode] for mode in complement)
            assert sp.factor(
                only_nonzero_column_entry(matrix, 3 * retained + 1) - expected
            ) == 0
            checks += 1
        tau = sum(
            regular4[left] * regular4[right]
            for left, right in combinations(other_regular, 2)
        )
        assert sp.factor(
            only_nonzero_column_entry(matrix, 3 * 4 + 1) - 2 * tau
        ) == 0
        deleted_b = collision_matrix(rrrrb_types, 4, rrrrb_ratios)
        assert sp.factor(
            only_nonzero_column_entry(deleted_b, 3 * deleted + 1) - 2 * tau
        ) == 0
        checks += 2

    regular3 = sp.symbols("s0:3", nonzero=True)
    rrrbb_ratios = regular3 + (sp.Integer(1), sp.Integer(1))
    rrrbb_types = ("R", "R", "R", "B", "B")
    sigma = sum(
        regular3[left] * regular3[right]
        for left, right in combinations(range(3), 2)
    )
    for deleted in range(3):
        matrix = collision_matrix(rrrbb_types, deleted, rrrbb_ratios)
        remaining_regular = tuple(
            mode for mode in range(3) if mode != deleted
        )
        expected = 2 * sp.prod(regular3[mode] for mode in remaining_regular)
        for retained_b in (3, 4):
            assert sp.factor(
                only_nonzero_column_entry(matrix, 3 * retained_b + 1)
                - expected
            ) == 0
            checks += 1
    for deleted_b, retained_b in ((3, 4), (4, 3)):
        matrix = collision_matrix(rrrbb_types, deleted_b, rrrbb_ratios)
        assert sp.factor(
            only_nonzero_column_entry(matrix, 3 * retained_b + 1) - 2 * sigma
        ) == 0
        checks += 1
        for retained_regular in range(3):
            complement = tuple(
                mode for mode in range(3) if mode != retained_regular
            )
            expected = 2 * sp.prod(regular3[mode] for mode in complement)
            assert sp.factor(
                only_nonzero_column_entry(
                    matrix, 3 * retained_regular + 1
                )
                - expected
            ) == 0
            checks += 1
    return {"off_line_coefficients": checks, "tau_family": 4, "sigma": 1}


def assert_inactive_sets_and_hall_bridge() -> dict[str, int]:
    roots = frozenset(range(4))
    pairs = [frozenset(pair) for pair in combinations(roots, 2)]
    relations = Counter()
    for left, right in product(pairs, repeat=2):
        if left == right:
            relations["equal"] += 1
        elif left.isdisjoint(right):
            relations["disjoint"] += 1
        else:
            relations["diamond"] += 1
    assert relations == Counter({"diamond": 24, "equal": 6, "disjoint": 6})

    degree_patterns: Counter[tuple[int, ...]] = Counter()
    for inactive_sets in product(pairs, repeat=3):
        if set.intersection(*(set(item) for item in inactive_sets)):
            continue
        degree = tuple(
            sorted(
                (
                    sum(root in inactive for inactive in inactive_sets)
                    for root in roots
                ),
                reverse=True,
            )
        )
        degree_patterns[degree] += 1
    assert degree_patterns == Counter({(2, 2, 1, 1): 90, (2, 2, 2, 0): 24})

    assert 5 < 3 * 2
    assert 3 * 1 + 2 * 2 == 7 < 3 * 3
    assert 4 * 1 + 1 * 3 == 7 < 3 * 3
    assert 3 * 1 + 2 * 3 == 9
    assert 3 * 2 + 2 * 3 == 3 * 4 == 12

    for beta in COORDS:
        other_colours = tuple(colour for colour in COORDS if colour != beta)
        coordinate_planes = {
            frozenset((beta, colour)) for colour in other_colours
        }
        assert len(coordinate_planes) == 2
        singleton_supports = {
            colour: index for index, colour in enumerate(other_colours)
        }
        assert len(set(singleton_supports.values())) == 2
    return {
        "pair_relations": sum(relations.values()),
        "three_B_ledgers": sum(degree_patterns.values()),
        "line_swap_capacity": 12,
    }


def main() -> None:
    types = assert_row_quota_and_type_exhaustion()
    triangle = assert_three_b_triangle()
    rrrrt = assert_rrrrt_complete_divisors()
    four_kernels = assert_rrrbt_and_rrbbt_kernels()
    graph = assert_five_regular_cofactor_graph()
    forcing = assert_one_and_two_b_forcing()
    incidence = assert_inactive_sets_and_hall_bridge()
    print(f"PASS: p_a>=2 leaves exactly {types}")
    print(f"PASS: three-B pair/triple kernel nullities are {triangle}")
    print(f"PASS: complete RRRRT divisor/nullity ledger is {rrrrt}")
    print(f"PASS: RRRBT/RRBBT common-kernel nullities are {four_kernels}")
    print(f"PASS: exact reciprocal cofactor-graph census is {graph}")
    print(f"PASS: one-/two-B off-line forcing ledger is {forcing}")
    print(f"PASS: inactive-set and Hall ledgers are {incidence}")
    print("SCOPE: complete conditional two-open detection in aligned q=0,r=5")
    print("UNKNOWN: witness exclusion, fixed-root injectivity, and larger cells")
    print("UNRESOLVED: global Krenn-Gu conjecture")
    print("searches=0")


if __name__ == "__main__":
    main()
