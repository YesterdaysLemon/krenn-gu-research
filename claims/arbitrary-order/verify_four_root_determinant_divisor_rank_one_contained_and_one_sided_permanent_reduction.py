"""Focused exact replay for the remaining rank-one determinant branches.

The accompanying theorem owns the arbitrary-point arguments.  This primary
verifier checks, over exact characteristic-zero arithmetic, the labelled
Laplace identities and finite colour-cover reductions used for the
double-contained Branch I and the one-sided Branch II (including its
transpose).  It also checks the balanced augmented-``P_6`` identity, its
one-face defect, and two sharp controls.

The formal companion control below is deliberately *not* asserted to arise
from one common incidence family.  Conversely, the common-incidence anchor
control deliberately fails a mixed target coefficient.  Nothing here proves
``P_5`` nonrestriction, selector attachment, the strategic supply/target
node, or the global Krenn--Gu conjecture.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

COLOURS = tuple(range(3))
Q0, Q1, U0, U1, U2, U3 = tuple(range(6))
PORTS = (U0, U1, U2, U3)
VERTICES = (Q0, Q1) + PORTS
PAIRS = tuple(combinations(VERTICES, 2))
PORT_PAIRS = tuple(combinations(PORTS, 2))
PERMUTATIONS = {degree: tuple(permutations(range(degree))) for degree in (2, 4, 5, 6)}
ZERO = sp.Integer(0)
ONE = sp.Integer(1)

Pair = tuple[int, int]
Word = tuple[int, ...]


def basis(colour: int) -> sp.Matrix:
    """Return a ternary coordinate covector, written as a column."""

    return sp.eye(3)[:, colour]


def exact_matrix(rows: tuple[tuple[int | sp.Rational, ...], ...]) -> sp.Matrix:
    return sp.Matrix(rows)


def edge_key(left: int, right: int) -> Pair:
    return tuple(sorted((left, right)))


def set_edge(
    edges: dict[Pair, sp.Matrix],
    left: int,
    right: int,
    left_form: sp.Matrix,
    right_form: sp.Matrix,
    scalar: sp.Expr | int = ONE,
) -> None:
    """Insert an oriented simple edge into the canonical unoriented table."""

    block = sp.sympify(scalar) * left_form * right_form.T
    key = edge_key(left, right)
    stored = block if left < right else block.T
    edges[key] = edges.get(key, sp.zeros(3)) + stored


def edge_block(edges: dict[Pair, sp.Matrix], left: int, right: int) -> sp.Matrix:
    key = edge_key(left, right)
    block = edges.get(key, sp.zeros(3))
    return block if left < right else block.T


def permanent_columns(columns: tuple[sp.Matrix, ...]) -> sp.Expr:
    """Expand one labelled permanent using every permutation."""

    degree = len(columns)
    assert degree in PERMUTATIONS
    assert all(column.shape == (degree, 1) for column in columns)
    total = ZERO
    for permutation in PERMUTATIONS[degree]:
        term = ONE
        for column, row in zip(columns, permutation, strict=True):
            term *= column[row]
            if term == 0:
                break
        total += term
    return sp.expand(total)


def kernel_embedding(form: sp.Matrix) -> sp.Matrix:
    """Return an exact column basis for the kernel of one covector."""

    assert form.shape == (3, 1)
    nullspace = form.T.nullspace()
    assert nullspace
    embedding = sp.Matrix.hstack(*nullspace)
    assert form.T * embedding == sp.zeros(1, embedding.cols)
    return embedding


def quotient_by_line(form: sp.Matrix) -> sp.Matrix:
    """Return an exact rank-two quotient whose kernel is ``K form``."""

    assert form.shape == (3, 1) and form != sp.zeros(3, 1)
    annihilator = form.T.nullspace()
    assert len(annihilator) == 2
    quotient = sp.Matrix.vstack(*(vector.T for vector in annihilator))
    assert quotient.shape == (2, 3)
    assert quotient.rank() == 2
    assert quotient * form == sp.zeros(2, 1)
    nullspace = quotient.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(form, nullspace[0]).rank() == 1
    return quotient


def companion_value(
    root_maps: dict[int, sp.Matrix],
    omitted_pair: Pair,
    vectors: dict[int, sp.Matrix],
) -> sp.Expr:
    """Evaluate the common-incidence ``P_4`` companion of one pair."""

    complement = tuple(vertex for vertex in VERTICES if vertex not in omitted_pair)
    columns = tuple(root_maps[vertex] * vectors[vertex] for vertex in complement)
    return permanent_columns(columns)


def contracted_target_value(
    root_maps: dict[int, sp.Matrix],
    edges: dict[Pair, sp.Matrix],
    vectors: dict[int, sp.Matrix],
) -> sp.Expr:
    """Evaluate all fifteen edge-times-companion summands."""

    total = ZERO
    for pair in PAIRS:
        left, right = pair
        edge_value = (
            vectors[left].T * edge_block(edges, left, right) * vectors[right]
        )[0]
        total += edge_value * companion_value(root_maps, pair, vectors)
    return sp.expand(total)


def p_value(
    maps: dict[int, sp.Matrix],
    vertex_order: tuple[int, ...],
    local_word: tuple[int, ...],
) -> sp.Expr:
    """Evaluate a direct permanent pullback on one local basis word."""

    columns = tuple(
        maps[vertex][:, local_colour]
        for vertex, local_colour in zip(vertex_order, local_word, strict=True)
    )
    return permanent_columns(columns)


def dense_root_maps() -> dict[int, sp.Matrix]:
    """Return six full-rank exact ``4 x 3`` common-incidence maps."""

    rows = (
        ((1, -1, -1), (1, 0, 1), (-1, 0, -1), (-1, -1, 1)),
        ((-1, -1, -1), (-1, 0, 1), (-1, 1, 1), (0, 1, -1)),
        ((0, 1, -1), (-1, -1, 0), (1, -1, 1), (1, 1, -1)),
        ((-1, 1, 0), (0, 0, 0), (-1, 0, 0), (1, 1, 1)),
        ((0, 0, 0), (1, 1, -1), (-1, 1, -1), (-1, -1, -1)),
        ((0, -1, -1), (1, 0, -1), (-1, 0, 0), (1, -1, -1)),
    )
    maps = {
        vertex: exact_matrix(matrix_rows)
        for vertex, matrix_rows in zip(VERTICES, rows, strict=True)
    }
    assert all(
        matrix.shape == (4, 3) and matrix.rank() == 3 for matrix in maps.values()
    )
    return maps


def branch_i_edges(
    x: sp.Matrix,
    y: sp.Matrix,
    a: dict[int, sp.Matrix],
    c: dict[int, sp.Matrix],
) -> dict[Pair, sp.Matrix]:
    """Build the exact double-contained Wick normal form."""

    edges: dict[Pair, sp.Matrix] = {}
    set_edge(edges, Q0, Q1, x, y)
    for u in PORTS:
        set_edge(edges, Q0, u, x, a[u])
        set_edge(edges, Q1, u, y, c[u])
    for u, v in PORT_PAIRS:
        set_edge(edges, u, v, a[u], c[v], -1)
        set_edge(edges, u, v, c[u], a[v], -1)
    return edges


def dense_branch_i_forms() -> tuple[
    sp.Matrix,
    sp.Matrix,
    dict[int, sp.Matrix],
    dict[int, sp.Matrix],
]:
    x = sp.Matrix([1, 2, -1])
    y = sp.Matrix([2, -1, 3])
    a_rows = ((1, 1, 2), (2, -1, 1), (1, 3, -2), (-2, 1, 1))
    c_rows = ((1, -2, 1), (3, 1, 1), (-1, 2, 3), (2, 1, -3))
    a = {u: sp.Matrix(row) for u, row in zip(PORTS, a_rows, strict=True)}
    c = {u: sp.Matrix(row) for u, row in zip(PORTS, c_rows, strict=True)}
    return x, y, a, c


def restricted_vectors(
    embeddings: dict[int, sp.Matrix],
    local_word: tuple[int, ...],
) -> dict[int, sp.Matrix]:
    return {
        vertex: embeddings[vertex][:, index]
        for vertex, index in zip(VERTICES, local_word, strict=True)
    }


def check_branch_i_kernel_restricted_p5_pullbacks() -> tuple[int, int, int]:
    """Check all eight labelled kernel-restricted ``P_5`` cofactors."""

    root_maps = dense_root_maps()
    x, y, a, c = dense_branch_i_forms()
    edges = branch_i_edges(x, y, a, c)
    coefficient_checks = 0
    p5_permutation_terms = 0

    for t in PORTS:
        for superscript in ("a", "c"):
            embeddings = {vertex: sp.eye(3) for vertex in VERTICES}
            bottom_forms: dict[int, sp.Matrix] = {}
            factor = a[t] if superscript == "a" else c[t]
            if superscript == "a":
                embeddings[Q1] = kernel_embedding(y)
                bottom_forms[Q0] = x
                bottom_forms[Q1] = sp.zeros(3, 1)
                for u in PORTS:
                    if u != t:
                        embeddings[u] = kernel_embedding(a[u])
                        bottom_forms[u] = -c[u]
            else:
                embeddings[Q0] = kernel_embedding(x)
                bottom_forms[Q0] = sp.zeros(3, 1)
                bottom_forms[Q1] = y
                for u in PORTS:
                    if u != t:
                        embeddings[u] = kernel_embedding(c[u])
                        bottom_forms[u] = -a[u]

            p5_vertices = tuple(vertex for vertex in VERTICES if vertex != t)
            p5_maps = {
                vertex: (root_maps[vertex] * embeddings[vertex]).col_join(
                    bottom_forms[vertex].T * embeddings[vertex]
                )
                for vertex in p5_vertices
            }
            dimensions = tuple(embeddings[vertex].cols for vertex in VERTICES)
            for local_word in product(*(range(dimension) for dimension in dimensions)):
                vectors = restricted_vectors(embeddings, local_word)
                lhs = contracted_target_value(root_maps, edges, vectors)
                factor_value = (factor.T * vectors[t])[0]
                p5_word = tuple(
                    local_word[VERTICES.index(vertex)] for vertex in p5_vertices
                )
                rhs = factor_value * p_value(p5_maps, p5_vertices, p5_word)
                assert sp.expand(lhs - rhs) == 0
                coefficient_checks += 1
                p5_permutation_terms += len(PERMUTATIONS[5])

    assert coefficient_checks == 8 * 3 * 3 * 2**4 == 1152
    return 8, coefficient_checks, p5_permutation_terms


def check_branch_i_whole_family_p5_pullbacks() -> tuple[int, int, int]:
    """Check the two whole-family cofactors used when ``x`` and ``y`` differ."""

    root_maps = dense_root_maps()
    x, y, a, c = dense_branch_i_forms()
    edges = branch_i_edges(x, y, a, c)
    checks = 0
    terms = 0

    for factor_vertex, factor, fixed_form, port_forms, bottom_ports in (
        (Q0, x, y, c, a),
        (Q1, y, x, a, c),
    ):
        other_q = Q1 if factor_vertex == Q0 else Q0
        embeddings = {vertex: sp.eye(3) for vertex in VERTICES}
        embeddings[other_q] = kernel_embedding(fixed_form)
        for u in PORTS:
            embeddings[u] = kernel_embedding(port_forms[u])

        p5_vertices = tuple(vertex for vertex in VERTICES if vertex != factor_vertex)
        p5_maps = {}
        for vertex in p5_vertices:
            bottom = bottom_ports[vertex] if vertex in PORTS else sp.zeros(3, 1)
            p5_maps[vertex] = (root_maps[vertex] * embeddings[vertex]).col_join(
                bottom.T * embeddings[vertex]
            )

        dimensions = tuple(embeddings[vertex].cols for vertex in VERTICES)
        for local_word in product(*(range(dimension) for dimension in dimensions)):
            vectors = restricted_vectors(embeddings, local_word)
            lhs = contracted_target_value(root_maps, edges, vectors)
            factor_value = (factor.T * vectors[factor_vertex])[0]
            p5_word = tuple(
                local_word[VERTICES.index(vertex)] for vertex in p5_vertices
            )
            rhs = factor_value * p_value(p5_maps, p5_vertices, p5_word)
            assert sp.expand(lhs - rhs) == 0
            checks += 1
            terms += len(PERMUTATIONS[5])

    assert checks == 2 * 3 * 2**5 == 192
    return 2, checks, terms


NO_BLOCK = 3


def covered_colours(labels: tuple[int, ...]) -> frozenset[int]:
    return frozenset(label for label in labels if label in COLOURS)


def balanced_deletion_solutions() -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Enumerate the exact all-three-covered deletion patterns."""

    solutions = []
    for fixed_label in (*COLOURS, NO_BLOCK):
        for family in product((*COLOURS, NO_BLOCK), repeat=4):
            cover_sizes = tuple(
                len(
                    covered_colours(
                        (fixed_label,)
                        + tuple(family[u] for u in range(4) if u != deleted)
                    )
                )
                for deleted in range(4)
            )
            if cover_sizes == (3, 3, 3, 3):
                solutions.append((fixed_label, family))
    return tuple(solutions)


def check_branch_i_target_colour_cover() -> tuple[int, int, int, int]:
    """Replay the rank/pure/balanced colour-cover case split exactly."""

    coverage_profiles = 0
    low_rank_profiles = 0
    pure_profiles = 0
    for fixed_label in (*COLOURS, NO_BLOCK):
        for family in product((*COLOURS, NO_BLOCK), repeat=4):
            sizes = tuple(
                len(
                    covered_colours(
                        (fixed_label,)
                        + tuple(family[u] for u in range(4) if u != deleted)
                    )
                )
                for deleted in range(4)
            )
            assert all(0 <= size <= 3 for size in sizes)
            if any(size <= 1 for size in sizes):
                # At least two target colours survive, so the deleted-mode
                # flattening has rank at least two, unlike factor tensor P5.
                low_rank_profiles += 1
            elif any(size == 2 for size in sizes):
                # Exactly one target colour survives.  Equality forces the
                # deleted factor onto that coordinate and the P5 cofactor to
                # the complementary nonzero pure tensor.
                pure_profiles += 1
            coverage_profiles += 1

    balanced = balanced_deletion_solutions()
    assert len(balanced) == 18
    for fixed_label, family in balanced:
        assert fixed_label in COLOURS
        other_colours = set(COLOURS) - {fixed_label}
        assert set(family) == other_colours
        assert all(family.count(colour) == 2 for colour in other_colours)

    # Combine the ``a`` and ``c`` deletion covers.  If their fixed colours
    # differ, the whole-family restriction leaves exactly the ``c``-fixed
    # colour (and symmetrically the ``a``-fixed colour) unblocked.
    combined = 0
    distinct_fixed = 0
    for y_label, a_labels in balanced:
        for x_label, c_labels in balanced:
            combined += 1
            survivors = set(COLOURS) - covered_colours((y_label,) + c_labels)
            if x_label != y_label:
                assert survivors == {x_label}
                distinct_fixed += 1
            else:
                assert not survivors
    assert combined == 18**2 == 324
    assert distinct_fixed == 216
    return coverage_profiles, low_rank_profiles, pure_profiles, combined


def balanced_partitions() -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(1 if port in chosen else 2 for port in range(4))
        for chosen in combinations(range(4), 2)
    )


def check_branch_i_seventh_response_split() -> tuple[int, int, sp.Expr]:
    """Check misaligned singleton fibres and the aligned ``e_2`` factor."""

    partitions = balanced_partitions()
    misaligned = 0
    singleton_fibres = 0
    for a_colours in partitions:
        for c_colours in partitions:
            if a_colours == c_colours:
                continue
            fibres: dict[Word, list[tuple[int, int]]] = {}
            for selected in combinations(range(4), 2):
                word = tuple(
                    a_colours[u] if u in selected else c_colours[u] for u in range(4)
                )
                fibres.setdefault(word, []).append(selected)
            singletons = sum(len(routes) == 1 for routes in fibres.values())
            assert singletons >= 2
            singleton_fibres += singletons
            misaligned += 1
    assert misaligned == 30

    gamma = sp.symbols("gamma0:4", nonzero=True)
    ratios = sp.symbols("r0:4")
    alpha = tuple(gamma[u] * ratios[u] for u in range(4))
    coefficient = sum(
        (
            sp.prod(alpha[u] for u in selected)
            * sp.prod(gamma[u] for u in range(4) if u not in selected)
        )
        for selected in combinations(range(4), 2)
    )
    e2 = sum(ratios[u] * ratios[v] for u, v in combinations(range(4), 2))
    assert sp.expand(coefficient - sp.prod(gamma) * e2) == 0
    control_ratios = (
        sp.Rational(1),
        sp.Rational(1),
        sp.Rational(2),
        sp.Rational(-5, 4),
    )
    control_e2 = sum(
        control_ratios[u] * control_ratios[v] for u, v in combinations(range(4), 2)
    )
    assert control_e2 == 0
    return misaligned, singleton_fibres, control_e2


def aligned_branch_i_data() -> tuple[
    dict[Pair, sp.Matrix],
    tuple[sp.Rational, ...],
    tuple[int, ...],
]:
    ratios = (sp.Rational(1), sp.Rational(1), sp.Rational(2), sp.Rational(-5, 4))
    local_colours = (1, 1, 2, 2)
    x = basis(0)
    y = basis(0)
    a = {
        u: ratios[index] * basis(local_colours[index]) for index, u in enumerate(PORTS)
    }
    c = {u: basis(local_colours[index]) for index, u in enumerate(PORTS)}
    return branch_i_edges(x, y, a, c), ratios, local_colours


def formal_companion_value(
    companions: dict[Pair, dict[Word, sp.Expr]],
    pair: Pair,
    outside_word: Word,
) -> sp.Expr:
    complement = tuple(vertex for vertex in VERTICES if vertex not in pair)
    word = tuple(outside_word[VERTICES.index(vertex)] for vertex in complement)
    return companions.get(pair, {}).get(word, ZERO)


def formal_contracted_coefficient(
    edges: dict[Pair, sp.Matrix],
    companions: dict[Pair, dict[Word, sp.Expr]],
    word: Word,
) -> sp.Expr:
    total = ZERO
    for pair in PAIRS:
        left, right = pair
        edge_value = edge_block(edges, left, right)[
            word[VERTICES.index(left)], word[VERTICES.index(right)]
        ]
        total += edge_value * formal_companion_value(companions, pair, word)
    return sp.expand(total)


def matching_value(edges: dict[Pair, sp.Matrix], word: Word) -> sp.Expr:
    total = ZERO
    for matching in perfect_matchings(VERTICES):
        term = ONE
        for left, right in matching:
            term *= edge_block(edges, left, right)[
                word[VERTICES.index(left)], word[VERTICES.index(right)]
            ]
        total += term
    return sp.expand(total)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def check_formal_balanced_target_control() -> tuple[int, int, int]:
    """Check the independent-companion target and seventh-zero control."""

    edges, _, _ = aligned_branch_i_data()
    mu = (sp.Integer(5), sp.Integer(7), sp.Integer(11))
    companions = {
        edge_key(Q0, Q1): {(0, 0, 0, 0): mu[0]},
        edge_key(U0, U1): {(1, 1, 1, 1): -mu[1] / 2},
        edge_key(U2, U3): {(2, 2, 2, 2): -4 * mu[2] / 3},
    }
    target_coefficients = 0
    seventh_coefficients = 0
    for word in product(COLOURS, repeat=6):
        expected = ZERO
        for colour in COLOURS:
            if word == (colour,) * 6:
                expected = mu[colour]
        assert formal_contracted_coefficient(edges, companions, word) == expected
        assert matching_value(edges, word) == 0
        target_coefficients += 1
        seventh_coefficients += 1
    assert target_coefficients == seventh_coefficients == 729
    return target_coefficients, 15 * target_coefficients, seventh_coefficients


def augmented_maps(
    root_maps: dict[int, sp.Matrix],
    x: sp.Matrix,
    y: sp.Matrix,
    a: dict[int, sp.Matrix],
    c: dict[int, sp.Matrix],
) -> dict[int, sp.Matrix]:
    maps = {
        Q0: root_maps[Q0].col_join(x.T).col_join(sp.zeros(1, 3)),
        Q1: root_maps[Q1].col_join(sp.zeros(1, 3)).col_join(-y.T),
    }
    for u in PORTS:
        maps[u] = root_maps[u].col_join(-c[u].T).col_join(a[u].T)
    assert all(matrix.shape == (6, 3) for matrix in maps.values())
    return maps


def check_bottom_minors() -> int:
    x, y = sp.symbols("x y")
    a = sp.symbols("a0:4")
    c = sp.symbols("c0:4")
    bottom = {
        Q0: sp.Matrix([x, 0]),
        Q1: sp.Matrix([0, -y]),
        **{u: sp.Matrix([-c[index], a[index]]) for index, u in enumerate(PORTS)},
    }

    checks = 0
    assert permanent_columns((bottom[Q0], bottom[Q1])) == -x * y
    checks += 1
    for index, u in enumerate(PORTS):
        assert permanent_columns((bottom[Q0], bottom[u])) == x * a[index]
        assert permanent_columns((bottom[Q1], bottom[u])) == y * c[index]
        checks += 2
    for (u, v), (i, j) in zip(PORT_PAIRS, combinations(range(4), 2), strict=True):
        expected = -(a[i] * c[j] + c[i] * a[j])
        assert permanent_columns((bottom[u], bottom[v])) == expected
        checks += 1
    assert checks == 15
    return checks


def check_augmented_p6_laplace_identity() -> tuple[int, int]:
    """Check all 729 coefficients by direct 720-permutation expansion."""

    root_maps = dense_root_maps()
    x, y, a, c = dense_branch_i_forms()
    edges = branch_i_edges(x, y, a, c)
    maps = augmented_maps(root_maps, x, y, a, c)
    checks = 0
    for word in product(COLOURS, repeat=6):
        vectors = {vertex: basis(word[VERTICES.index(vertex)]) for vertex in VERTICES}
        p6 = p_value(maps, VERTICES, word)
        target = contracted_target_value(root_maps, edges, vectors)
        h = (x.T * vectors[Q0])[0] * (y.T * vectors[Q1])[0]
        pi_q = companion_value(root_maps, edge_key(Q0, Q1), vectors)
        assert sp.expand(p6 - (target - 2 * h * pi_q)) == 0
        checks += 1
    assert checks == 729
    return checks, checks * len(PERMUTATIONS[6])


def quotient_away(colour: int) -> sp.Matrix:
    retained = tuple(value for value in COLOURS if value != colour)
    return sp.Matrix(2, 3, lambda row, column: int(column == retained[row]))


def tensor_flattening(tensor: dict[Word, sp.Expr], mode: int) -> sp.Matrix:
    other_modes = tuple(index for index in range(6) if index != mode)
    other_words = tuple(product(COLOURS, repeat=5))
    return sp.Matrix(
        3,
        len(other_words),
        lambda row, column: tensor.get(
            tuple(
                row if index == mode else other_words[column][other_modes.index(index)]
                for index in range(6)
            ),
            ZERO,
        ),
    )


def check_aligned_one_face_defect() -> tuple[int, int, int]:
    """Replay the quotient-face support and the six flattening ranks."""

    local_colours = (1, 1, 2, 2)
    h = sp.Integer(2)
    mu = (sp.Integer(5), sp.Integer(7), sp.Integer(11))
    psi: dict[Word, sp.Expr] = {}
    for word in product(COLOURS, repeat=4):
        if any(word[index] == local_colours[index] for index in range(4)):
            psi[word] = sp.Integer(
                1 + sum((index + 1) * colour for index, colour in enumerate(word))
            )

    quotient = quotient_away(local_colours[0])
    for colour in local_colours[1:]:
        quotient = sp.kronecker_product(quotient, quotient_away(colour))
    assert quotient.shape == (16, 81)
    assert quotient.rank() == 16
    psi_vector = sp.Matrix([psi.get(word, ZERO) for word in product(COLOURS, repeat=4)])
    assert quotient * psi_vector == sp.zeros(16, 1)
    assert 81 - quotient.rank() == 65

    pi_q = {(0, 0, 0, 0): sp.Rational(mu[0], h)}
    for word, coefficient in psi.items():
        pi_q[word] = pi_q.get(word, ZERO) + coefficient

    tensor: dict[Word, sp.Expr] = {}
    for word in product(COLOURS, repeat=6):
        ghz = next(
            (mu[colour] for colour in COLOURS if word == (colour,) * 6),
            ZERO,
        )
        h_pi = ZERO
        if word[:2] == (0, 0):
            h_pi = h * pi_q.get(word[2:], ZERO)
        tensor[word] = sp.expand(ghz - 2 * h_pi)

        displayed = ZERO
        if word == (0,) * 6:
            displayed -= mu[0]
        if word == (1,) * 6:
            displayed += mu[1]
        if word == (2,) * 6:
            displayed += mu[2]
        if word[:2] == (0, 0):
            displayed -= 2 * h * psi.get(word[2:], ZERO)
        assert tensor[word] == displayed

    ranks = tuple(tensor_flattening(tensor, mode).rank() for mode in range(6))
    assert ranks == (3,) * 6
    return len(psi), quotient.rank(), sum(ranks)


def anchor_root_maps() -> dict[int, sp.Matrix]:
    maps = dense_root_maps()
    maps[U0] = maps[U0].copy()
    maps[U0][:, 2] /= 2
    assert all(matrix.rank() == 3 for matrix in maps.values())
    return maps


def common_incidence_coefficient(
    root_maps: dict[int, sp.Matrix],
    edges: dict[Pair, sp.Matrix],
    word: Word,
) -> sp.Expr:
    vectors = {vertex: basis(word[VERTICES.index(vertex)]) for vertex in VERTICES}
    return contracted_target_value(root_maps, edges, vectors)


def check_common_incidence_anchor_control() -> tuple[int, int, int]:
    """Check pure anchors plus an exposed mixed coefficient on one real deck."""

    root_maps = anchor_root_maps()
    edges, _, _ = aligned_branch_i_data()
    pi_q_0000 = permanent_columns(tuple(root_maps[u][:, 0] for u in PORTS))
    pi_q_2200 = permanent_columns(
        (
            root_maps[U0][:, 2],
            root_maps[U1][:, 2],
            root_maps[U2][:, 0],
            root_maps[U3][:, 0],
        )
    )
    pi_01_1111 = permanent_columns(
        (
            root_maps[Q0][:, 1],
            root_maps[Q1][:, 1],
            root_maps[U2][:, 1],
            root_maps[U3][:, 1],
        )
    )
    pi_23_2222 = permanent_columns(
        (
            root_maps[Q0][:, 2],
            root_maps[Q1][:, 2],
            root_maps[U0][:, 2],
            root_maps[U1][:, 2],
        )
    )
    assert (pi_q_0000, pi_01_1111, pi_23_2222, pi_q_2200) == (2, 2, -1, 1)

    pure = tuple(
        common_incidence_coefficient(root_maps, edges, (colour,) * 6)
        for colour in COLOURS
    )
    assert pure == (2, -4, sp.Rational(3, 4))
    exposed_word = (0, 0, 2, 2, 0, 0)
    exposed = common_incidence_coefficient(root_maps, edges, exposed_word)
    assert exposed == 1

    nonzero_mixed = 0
    for word in product(COLOURS, repeat=6):
        coefficient = common_incidence_coefficient(root_maps, edges, word)
        if coefficient != 0 and len(set(word)) > 1:
            nonzero_mixed += 1
    assert nonzero_mixed > 0
    return 3, nonzero_mixed, exposed


def branch_ii_edges(
    contained_q: int,
    escaping_q: int,
    x: sp.Matrix,
    y: sp.Matrix,
    d: sp.Matrix,
    active_ports: tuple[int, ...],
    a: dict[int, sp.Matrix],
    c: dict[int, sp.Matrix],
) -> dict[Pair, sp.Matrix]:
    """Build a singleton or signed two-port Branch-II normal form."""

    assert {contained_q, escaping_q} == {Q0, Q1}
    assert 1 <= len(active_ports) <= 2
    edges: dict[Pair, sp.Matrix] = {}
    set_edge(edges, contained_q, escaping_q, x, y)
    signs = {active_ports[0]: ONE}
    if len(active_ports) == 2:
        signs[active_ports[1]] = -ONE
    for u in PORTS:
        if u in active_ports:
            set_edge(edges, contained_q, u, x, a[u])
            set_edge(edges, escaping_q, u, d, a[u], signs[u])
        set_edge(edges, escaping_q, u, y, c[u])
    for u, v in PORT_PAIRS:
        if u in active_ports:
            set_edge(edges, u, v, a[u], c[v], -1)
        if v in active_ports:
            set_edge(edges, u, v, c[u], a[v], -1)
    return edges


def branch_ii_singleton_edges(
    contained_q: int,
    escaping_q: int,
    x: sp.Matrix,
    y: sp.Matrix,
    active_port: int,
    a_s: sp.Matrix,
    escaping_block: sp.Matrix,
    c: dict[int, sp.Matrix],
) -> dict[Pair, sp.Matrix]:
    """Build the full singleton form, with no rank-one assumption on ``C_s``."""

    assert {contained_q, escaping_q} == {Q0, Q1}
    assert escaping_block.shape == (3, 3)
    edges: dict[Pair, sp.Matrix] = {}
    set_edge(edges, contained_q, escaping_q, x, y)
    set_edge(edges, contained_q, active_port, x, a_s)
    key = edge_key(escaping_q, active_port)
    edges[key] = escaping_block if escaping_q < active_port else escaping_block.T
    for u in PORTS:
        if u == active_port:
            continue
        set_edge(edges, escaping_q, u, y, c[u])
        set_edge(edges, active_port, u, a_s, c[u], -1)
    return edges


def check_branch_ii_singleton_p4_quotients() -> tuple[int, int, int]:
    """Check every singleton and transpose two-line quotient exactly."""

    root_maps = dense_root_maps()
    x = sp.Matrix([1, 2, -1])
    y = sp.Matrix([2, -1, 3])
    a = {
        u: sp.Matrix(row)
        for u, row in zip(
            PORTS, ((1, 1, 2), (2, -1, 1), (1, 3, -2), (-2, 1, 1)), strict=True
        )
    }
    c = {
        u: sp.Matrix(row)
        for u, row in zip(
            PORTS, ((1, -2, 1), (3, 1, 1), (-1, 2, 3), (2, 1, -3)), strict=True
        )
    }
    escaping_block = sp.Matrix(((1, 2, -1), (3, -2, 4), (2, 1, 5)))
    identities = 0
    coefficients = 0
    for contained_q, escaping_q in ((Q0, Q1), (Q1, Q0)):
        for s in PORTS:
            edges = branch_ii_singleton_edges(
                contained_q,
                escaping_q,
                x,
                y,
                s,
                a[s],
                escaping_block,
                c,
            )
            pi_y = quotient_by_line(y)
            pi_a = quotient_by_line(a[s])
            d_s = pi_y * escaping_block * pi_a.T
            assert d_s != sp.zeros(2)
            embeddings = {vertex: sp.eye(3) for vertex in VERTICES}
            embeddings[escaping_q] = pi_y.T
            embeddings[s] = pi_a.T
            p4_vertices = tuple(
                vertex for vertex in VERTICES if vertex not in (escaping_q, s)
            )
            p4_maps = {
                vertex: root_maps[vertex] * embeddings[vertex] for vertex in p4_vertices
            }
            dimensions = tuple(embeddings[vertex].cols for vertex in VERTICES)
            for local_word in product(*(range(dimension) for dimension in dimensions)):
                vectors = restricted_vectors(embeddings, local_word)
                lhs = contracted_target_value(root_maps, edges, vectors)
                p4_word = tuple(
                    local_word[VERTICES.index(vertex)] for vertex in p4_vertices
                )
                q1_index = local_word[VERTICES.index(escaping_q)]
                s_index = local_word[VERTICES.index(s)]
                rhs = d_s[q1_index, s_index] * p_value(p4_maps, p4_vertices, p4_word)
                assert sp.expand(lhs - rhs) == 0
                coefficients += 1
            identities += 1
    assert identities == 8
    assert coefficients == 8 * 2**2 * 3**4 == 2592
    return identities, coefficients, coefficients * len(PERMUTATIONS[4])


def check_branch_ii_singleton_colour_and_rank_gate() -> tuple[int, int, int]:
    """Replay the target-colour quotient and conditional P4 rank gate."""

    rank_two_obstructions = 0
    pure_p4_routes = 0
    for x_label, y_label in product(COLOURS, repeat=2):
        survivors = set(COLOURS) - {x_label, y_label}
        if x_label == y_label:
            assert len(survivors) == 2
            rank_two_obstructions += 1
        else:
            assert len(survivors) == 1
            pure_p4_routes += 1
    assert (rank_two_obstructions, pure_p4_routes) == (3, 6)

    # The imported decomposable-P4 theorem is used only conditionally: if
    # every restricted map has rank at least two, a nonzero pure P4 forces
    # at least two ranks equal to two.  Rank <=1 is kept as its own branch.
    low_rank_profiles = 0
    imported_exclusions = 0
    for ranks in product(range(4), repeat=4):
        if any(rank <= 1 for rank in ranks):
            low_rank_profiles += 1
            continue
        theorem_conclusion = sum(rank == 2 for rank in ranks) >= 2
        if not theorem_conclusion:
            # Such profiles are precisely the ones excluded by the cited
            # P4 rank-drop theorem, not by a hidden local-rank assumption.
            assert sum(rank == 3 for rank in ranks) >= 3
            imported_exclusions += 1
    assert (low_rank_profiles, imported_exclusions) == (240, 5)
    return rank_two_obstructions, pure_p4_routes, low_rank_profiles


def check_branch_ii_two_port_p5_pullbacks() -> tuple[int, int, int]:
    """Check both directed P5 cofactors for all pairs and the transpose."""

    root_maps = dense_root_maps()
    x = sp.Matrix([1, 2, -1])
    y = sp.Matrix([2, -1, 3])
    d = sp.Matrix([1, 1, 1])
    a = {
        u: sp.Matrix(row)
        for u, row in zip(
            PORTS, ((1, 1, 2), (2, -1, 1), (1, 3, -2), (-2, 1, 1)), strict=True
        )
    }
    c = {
        u: sp.Matrix(row)
        for u, row in zip(
            PORTS, ((1, -2, 1), (3, 1, 1), (-1, 2, 3), (2, 1, -3)), strict=True
        )
    }
    identities = 0
    coefficients = 0

    for contained_q, escaping_q in ((Q0, Q1), (Q1, Q0)):
        for s, t in PORT_PAIRS:
            edges = branch_ii_edges(contained_q, escaping_q, x, y, d, (s, t), a, c)
            signs = {s: ONE, t: -ONE}
            for killed, factored in ((s, t), (t, s)):
                embeddings = {vertex: sp.eye(3) for vertex in VERTICES}
                embeddings[contained_q] = kernel_embedding(x)
                embeddings[escaping_q] = kernel_embedding(y)
                embeddings[killed] = kernel_embedding(a[killed])
                p5_vertices = tuple(vertex for vertex in VERTICES if vertex != factored)
                bottom_forms = {vertex: sp.zeros(3, 1) for vertex in p5_vertices}
                bottom_forms[escaping_q] = signs[factored] * d
                for u in PORTS:
                    if u != factored:
                        bottom_forms[u] = -c[u]
                p5_maps = {
                    vertex: (root_maps[vertex] * embeddings[vertex]).col_join(
                        bottom_forms[vertex].T * embeddings[vertex]
                    )
                    for vertex in p5_vertices
                }
                dimensions = tuple(embeddings[vertex].cols for vertex in VERTICES)
                for local_word in product(
                    *(range(dimension) for dimension in dimensions)
                ):
                    vectors = restricted_vectors(embeddings, local_word)
                    lhs = contracted_target_value(root_maps, edges, vectors)
                    factor_value = (a[factored].T * vectors[factored])[0]
                    p5_word = tuple(
                        local_word[VERTICES.index(vertex)] for vertex in p5_vertices
                    )
                    rhs = factor_value * p_value(p5_maps, p5_vertices, p5_word)
                    assert sp.expand(lhs - rhs) == 0
                    coefficients += 1
                identities += 1
    assert identities == 2 * 6 * 2 == 24
    assert coefficients == identities * 2**3 * 3**3 == 5184
    return identities, coefficients, coefficients * len(PERMUTATIONS[5])


def check_branch_ii_two_port_colour_cover() -> tuple[int, int]:
    """Exhaust the both-zero cover and expose the final pure-word defect."""

    both_zero_patterns = []
    for x_label, y_label, a_s, a_t in product(COLOURS, repeat=4):
        first = covered_colours((x_label, y_label, a_s))
        second = covered_colours((x_label, y_label, a_t))
        if first == second == frozenset(COLOURS):
            both_zero_patterns.append((x_label, y_label, a_s, a_t))
    assert len(both_zero_patterns) == 6
    for x_label, y_label, a_s, a_t in both_zero_patterns:
        assert x_label != y_label
        third = next(colour for colour in COLOURS if colour not in (x_label, y_label))
        assert a_s == a_t == third

        # At the all-x word every Branch-II edge has a forced wrong-colour
        # factor: H has y at the escaping shore, A has third at its port,
        # C has y or third, and every B term has a third-colour active factor.
        x_form = basis(x_label)
        y_form = basis(y_label)
        d_form = sp.Matrix([1, 1, 1])
        a = {u: sp.zeros(3, 1) for u in PORTS}
        c = {u: sp.Matrix([1, 2, 3]) for u in PORTS}
        a[U0] = basis(third)
        a[U1] = basis(third)
        edges = branch_ii_edges(Q0, Q1, x_form, y_form, d_form, (U0, U1), a, c)
        pure_word = (x_label,) * 6
        assert all(
            edge_block(edges, left, right)[x_label, x_label] == 0
            for left, right in PAIRS
        )
        assert pure_word == (x_label,) * 6
    return len(both_zero_patterns), 2


def check_quartic_kernel_contraction() -> tuple[int, int, int]:
    """Check the sign-twisted P6 contraction and six Wick routes."""

    root_maps = dense_root_maps()
    x = sp.Matrix([1, 1, 1])
    y = sp.Matrix([1, 2, 3])
    z0 = sp.Matrix([1, 1, -2])
    z1 = sp.Matrix([1, 1, -1])
    assert (x.T * z0)[0] == (y.T * z1)[0] == 0
    assert all(entry != 0 for entry in (*z0, *z1))
    _, _, a, c = dense_branch_i_forms()
    edges = branch_i_edges(x, y, a, c)
    maps = augmented_maps(root_maps, x, y, a, c)
    p0 = root_maps[Q0] * z0
    p1 = root_maps[Q1] * z1
    q_form = sp.zeros(6)
    for row, column in product(range(4), repeat=2):
        q_form[row, column] = permanent_columns(
            (p0, p1, sp.eye(4)[:, row], sp.eye(4)[:, column])
        )
    assert q_form == q_form.T
    port_maps = {index: maps[u] for index, u in enumerate(PORTS)}

    coefficient_checks = 0
    wick_routes = 0
    fixed = {Q0: z0, Q1: z1}
    for port_word in product(COLOURS, repeat=4):
        vectors = dict(fixed)
        vectors.update({u: basis(port_word[index]) for index, u in enumerate(PORTS)})
        p6_columns = tuple(maps[vertex] * vectors[vertex] for vertex in VERTICES)
        direct = permanent_columns(p6_columns)
        target = contracted_target_value(root_maps, edges, vectors)
        h = (x.T * z0)[0] * (y.T * z1)[0]
        assert h == 0
        assert sp.expand(direct - target) == 0
        sym_value = sym_abq_pullback_coefficient(q_form, port_maps, port_word)
        assert sp.expand(direct - sym_value) == 0

        wick = ZERO
        for u, v in PORT_PAIRS:
            edge_value = (vectors[u].T * edge_block(edges, u, v) * vectors[v])[0]
            q_value = companion_value(root_maps, (u, v), vectors)
            wick += edge_value * q_value
            wick_routes += 1
        assert sp.expand(direct - wick) == 0
        coefficient_checks += 1
    assert coefficient_checks == 81
    assert wick_routes == 81 * 6
    return coefficient_checks, wick_routes, coefficient_checks * len(PERMUTATIONS[6])


def sym_abq_pullback_coefficient(
    q_form: sp.Matrix,
    phi: dict[int, sp.Matrix],
    word: Word,
) -> sp.Expr:
    """Evaluate the labelled ``Sym(a b q)`` pullback of Lemma 1."""

    assert len(word) == 4
    ambient_dimension = q_form.rows
    ambient_a = sp.eye(ambient_dimension)[:, ambient_dimension - 2]
    ambient_b = sp.eye(ambient_dimension)[:, ambient_dimension - 1]
    alpha = {mode: ambient_a.T * phi[mode] for mode in range(4)}
    beta = {mode: ambient_b.T * phi[mode] for mode in range(4)}
    total = ZERO
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            k, ell = tuple(mode for mode in range(4) if mode not in (i, j))
            total += (
                alpha[i][word[i]]
                * beta[j][word[j]]
                * (phi[k][:, word[k]].T * q_form * phi[ell][:, word[ell]])[0]
            )
    return sp.expand(total)


def check_arbitrary_rank_quartic_radical_gate() -> tuple[int, int, int]:
    """Replay the contraction identity and every rank/radical alternative."""

    ambient_dimension = 6
    x_dimension = 4
    ambient_a = basis_vector = sp.eye(ambient_dimension)[:, x_dimension]
    ambient_b = sp.eye(ambient_dimension)[:, x_dimension + 1]
    z = basis(0)
    other_maps = {
        1: sp.Matrix.hstack(
            sp.eye(ambient_dimension)[:, 0] + ambient_a,
            sp.eye(ambient_dimension)[:, 1] + ambient_b,
            sp.eye(ambient_dimension)[:, 2] + ambient_a + ambient_b,
        ),
        2: sp.Matrix.hstack(
            sp.eye(ambient_dimension)[:, 1] + ambient_a,
            sp.eye(ambient_dimension)[:, 2] + ambient_b,
            sp.eye(ambient_dimension)[:, 3] + ambient_a - ambient_b,
        ),
        3: sp.Matrix.hstack(
            sp.eye(ambient_dimension)[:, 2] - ambient_a,
            sp.eye(ambient_dimension)[:, 3] + ambient_b,
            sp.eye(ambient_dimension)[:, 0] + ambient_a + 2 * ambient_b,
        ),
    }
    assert basis_vector == ambient_a
    assert all(matrix.rank() == 3 for matrix in other_maps.values())

    rank_cases = 0
    radical_cases = 0
    contraction_coefficients = 0
    fixtures: list[tuple[int, bool]] = []
    fixtures.extend((rank, True) for rank in range(4))
    fixtures.extend((rank, False) for rank in range(1, 5))
    for q_rank, use_radical in fixtures:
        q_form = sp.zeros(ambient_dimension)
        for index in range(q_rank):
            q_form[index, index] = index + 1
        assert q_form.rank() == q_rank
        top_vector = sp.eye(ambient_dimension)[:, q_rank if use_radical else 0]
        phi0 = sp.Matrix.hstack(top_vector, ambient_a, ambient_b)
        phi = {0: phi0, **other_maps}
        assert all(matrix.rank() == 3 for matrix in phi.values())

        alpha0 = ambient_a.T * phi0
        beta0 = ambient_b.T * phi0
        assert alpha0 == sp.Matrix([[0, 1, 0]])
        assert beta0 == sp.Matrix([[0, 0, 1]])
        assert alpha0 * z == beta0 * z == sp.zeros(1, 1)
        contracted_vector = phi0 * z
        ambient_ell = contracted_vector.T * q_form

        if use_radical:
            assert ambient_ell == sp.zeros(1, ambient_dimension)
            radical_cases += 1
        else:
            assert ambient_ell != sp.zeros(1, ambient_dimension)
            independent = sp.Matrix.vstack(ambient_a.T, ambient_b.T, ambient_ell)
            assert independent.rank() == 3

        for remaining_word in product(COLOURS, repeat=3):
            direct = sum(
                z[source_colour]
                * sym_abq_pullback_coefficient(
                    q_form,
                    phi,
                    (source_colour,) + remaining_word,
                )
                for source_colour in COLOURS
            )

            expected = ZERO
            remaining_modes = (1, 2, 3)
            alpha = {mode: ambient_a.T * phi[mode] for mode in remaining_modes}
            beta = {mode: ambient_b.T * phi[mode] for mode in remaining_modes}
            for i in remaining_modes:
                for j in remaining_modes:
                    if i == j:
                        continue
                    (k,) = tuple(mode for mode in remaining_modes if mode not in (i, j))
                    expected += (
                        alpha[i][remaining_word[i - 1]]
                        * beta[j][remaining_word[j - 1]]
                        * (ambient_ell * phi[k][:, remaining_word[k - 1]])[0]
                    )
            assert sp.expand(direct - expected) == 0
            if use_radical:
                assert direct == 0
            contraction_coefficients += 1

        if use_radical:
            # A hypothetical weighted diagonal pullback contracts to a
            # nonzero tensor for every nonzero z.  Here z=e_0, so its sole
            # surviving coefficient is the declared nonzero weight nu_0.
            weights = (sp.Integer(2), sp.Integer(3), sp.Integer(5))
            target_contraction = tuple(
                weights[colour] * z[colour] for colour in COLOURS
            )
            assert target_contraction == (2, 0, 0)
        rank_cases += 1

    assert (rank_cases, radical_cases, contraction_coefficients) == (8, 4, 216)
    return rank_cases, radical_cases, contraction_coefficients


def main() -> None:
    branch_i = check_branch_i_kernel_restricted_p5_pullbacks()
    whole = check_branch_i_whole_family_p5_pullbacks()
    cover = check_branch_i_target_colour_cover()
    seventh = check_branch_i_seventh_response_split()
    formal = check_formal_balanced_target_control()
    minors = check_bottom_minors()
    p6 = check_augmented_p6_laplace_identity()
    face = check_aligned_one_face_defect()
    anchor = check_common_incidence_anchor_control()
    singleton = check_branch_ii_singleton_p4_quotients()
    singleton_gate = check_branch_ii_singleton_colour_and_rank_gate()
    two_port = check_branch_ii_two_port_p5_pullbacks()
    two_port_cover = check_branch_ii_two_port_colour_cover()
    quartic = check_quartic_kernel_contraction()
    radical = check_arbitrary_rank_quartic_radical_gate()

    print("FOUR-ROOT RANK-ONE CONTAINED/ONE-SIDED PRIMARY PASS")
    print(
        f"  Branch I: {branch_i[0]} restricted P5 cofactors, "
        f"{branch_i[1]} coefficients / {branch_i[2]} permutation terms"
    )
    print(
        f"  whole-family: {whole[0]} cofactors, {whole[1]} coefficients / "
        f"{whole[2]} permutation terms"
    )
    print(
        f"  colour cover: {cover[0]} profiles; low-rank={cover[1]}, "
        f"pure={cover[2]}, balanced pairs={cover[3]}"
    )
    print(
        f"  seventh: {seventh[0]} misaligned pairs / {seventh[1]} singleton "
        f"fibres; control e2={seventh[2]}"
    )
    print(
        f"  formal control: {formal[0]} target coefficients / {formal[1]} "
        f"terms; {formal[2]} seventh coefficients"
    )
    print(
        f"  augmented P6: {minors} bottom minors; {p6[0]} coefficients / "
        f"{p6[1]} permutation terms"
    )
    print(
        f"  face defect: {face[0]} supported entries, quotient rank {face[1]}, "
        f"flattening-rank sum {face[2]}"
    )
    print(
        f"  common-incidence anchor: {anchor[0]} pure anchors, "
        f"{anchor[1]} mixed defects, exposed={anchor[2]}"
    )
    print(
        f"  Branch II singleton: {singleton[0]} quotient identities, "
        f"{singleton[1]} coefficients / {singleton[2]} permutation terms; "
        f"gate={singleton_gate}"
    )
    print(
        f"  Branch II two-port: {two_port[0]} directed/transpose cofactors, "
        f"{two_port[1]} coefficients / {two_port[2]} permutation terms; "
        f"both-zero patterns={two_port_cover[0]}"
    )
    print(
        f"  quartic contraction: {quartic[0]} coefficients, "
        f"{quartic[1]} Wick routes / {quartic[2]} permutation terms"
    )
    print(
        f"  arbitrary-rank gate: {radical[0]} rank/radical fixtures, "
        f"{radical[1]} radical contradictions / {radical[2]} contractions"
    )
    print("  exact arithmetic only; strategic node and global conjecture remain open")


if __name__ == "__main__":
    main()
